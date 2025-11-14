#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔮 MOTOR PREDICTIVO JUDICIAL v1.0
==================================

Predice decisiones judiciales usando Machine Learning.

Funcionalidades:
- Extrae factores relevantes de casos
- Entrena modelos por juez
- Predice resultados (hace_lugar/rechaza/parcial)
- Identifica factores más importantes
- Calcula pesos de factores
- Guarda en tabla factores_predictivos

Modelos:
- Random Forest Classifier
- Logistic Regression
- Feature importance analysis

AUTOR: Sistema de Análisis Judicial Argentina
FECHA: 12 NOV 2025
"""

import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import Counter
import pickle

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import accuracy_score, classification_report
    import numpy as np
    SKLEARN_DISPONIBLE = True
except ImportError:
    SKLEARN_DISPONIBLE = False
    print("⚠️ scikit-learn no disponible. Instalar con: pip install scikit-learn")

# Configuración
# Importar configuración centralizada
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DATABASE_PATH as DB_FILE, BASES_RAG_DIR

SCRIPT_DIR = Path(__file__).parent
MODELS_DIR = BASES_RAG_DIR / "modelos_predictivos"

# Colores
class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")


class ExtractorFactores:
    """
    Extrae factores relevantes de casos para análisis predictivo
    """

    def __init__(self):
        """Inicializa el extractor"""
        pass

    def extraer_factores(self, sentencia: Dict) -> Dict[str, any]:
        """
        Extrae factores relevantes de una sentencia

        Args:
            sentencia: Diccionario con datos de la sentencia

        Returns:
            Diccionario con factores extraídos
        """
        factores = {}

        # Factor: Materia
        factores['materia'] = sentencia.get('materia', 'desconocida')

        # Factor: Tipo de actor (empresa, persona, estado)
        actor = sentencia.get('actor', '')
        if actor:
            if any(term in actor.lower() for term in ['s.a.', 's.r.l.', 'empresa', 'sociedad']):
                factores['tipo_actor'] = 'empresa'
            elif 'estado' in actor.lower() or 'provincia' in actor.lower() or 'nacion' in actor.lower():
                factores['tipo_actor'] = 'estado'
            else:
                factores['tipo_actor'] = 'persona'
        else:
            factores['tipo_actor'] = 'desconocido'

        # Factor: Tipo de demandado
        demandado = sentencia.get('demandado', '')
        if demandado:
            if any(term in demandado.lower() for term in ['s.a.', 's.r.l.', 'empresa', 'sociedad']):
                factores['tipo_demandado'] = 'empresa'
            elif 'estado' in demandado.lower() or 'provincia' in demandado.lower() or 'nacion' in demandado.lower():
                factores['tipo_demandado'] = 'estado'
            else:
                factores['tipo_demandado'] = 'persona'
        else:
            factores['tipo_demandado'] = 'desconocido'

        # Factor: Análisis judicial (si existe)
        perfil = sentencia.get('perfil', {})
        if isinstance(perfil, str):
            try:
                perfil = json.loads(perfil)
            except:
                perfil = {}

        judicial = perfil.get('analisis_judicial', {})

        # Tests aplicados
        tests = judicial.get('tests_aplicados', {})
        factores['test_proporcionalidad'] = 1 if tests.get('test_proporcionalidad', 0) > 0.3 else 0
        factores['test_razonabilidad'] = 1 if tests.get('test_razonabilidad', 0) > 0.3 else 0

        # In dubio pro
        indubio = judicial.get('in_dubio_pro_aplicado', {})
        factores['in_dubio_pro_operario'] = 1 if indubio.get('pro_operario', 0) > 0.3 else 0
        factores['in_dubio_pro_consumidor'] = 1 if indubio.get('pro_consumidor', 0) > 0.3 else 0

        # Derechos protegidos
        derechos = judicial.get('derechos_protegidos', {})
        factores['proteccion_trabajo'] = derechos.get('trabajo', 0)
        factores['proteccion_igualdad'] = derechos.get('igualdad', 0)

        # Estándar probatorio
        factores['estandar_prueba'] = judicial.get('estandar_prueba', 'sana_critica')

        # Interpretación
        factores['interpretacion'] = judicial.get('interpretacion_normativa', 'mixta')

        # Factor: Longitud del texto (proxy de complejidad)
        texto = sentencia.get('texto_completo', '')
        factores['longitud_texto'] = len(texto.split()) if texto else 0

        # Factor: ¿Hay monto mencionado? (laboral, daños)
        if texto:
            tiene_monto = bool(re.search(r'\$\s*[\d,.]+|pesos\s+[\d,.]+', texto, re.IGNORECASE))
            factores['menciona_monto'] = 1 if tiene_monto else 0
        else:
            factores['menciona_monto'] = 0

        return factores

    def factores_a_vector(self, factores: Dict, feature_names: List[str] = None) -> Tuple[List, List[str]]:
        """
        Convierte factores a vector numérico para ML

        Returns:
            Tupla (vector, nombres_features)
        """
        if feature_names is None:
            # Inferir features desde los factores
            feature_names = []
            vector = []

            for key, value in sorted(factores.items()):
                if isinstance(value, (int, float)):
                    feature_names.append(key)
                    vector.append(value)
                elif isinstance(value, str):
                    # One-hot encoding simple
                    feature_names.append(f"{key}_{value}")
                    vector.append(1)

            return vector, feature_names

        # Usar feature_names dados
        vector = []
        for fname in feature_names:
            if '_' in fname:
                # Es un one-hot encoding
                key, valor = fname.rsplit('_', 1)
                if factores.get(key) == valor:
                    vector.append(1)
                else:
                    vector.append(0)
            else:
                # Es un valor numérico
                vector.append(factores.get(fname, 0))

        return vector, feature_names


class MotorPredictivoJudicial:
    """
    Motor de predicción de decisiones judiciales
    """

    def __init__(self, db_path: Path = DB_FILE):
        """Inicializa el motor"""
        if not SKLEARN_DISPONIBLE:
            raise ImportError("scikit-learn no está disponible")

        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.extractor = ExtractorFactores()
        self.models_dir = MODELS_DIR
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.conectar_bd()

    def conectar_bd(self):
        """Conecta a la BD"""
        if not self.db_path.exists():
            raise FileNotFoundError(f"BD no encontrada: {self.db_path}")

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def cerrar_bd(self):
        """Cierra la conexión"""
        if self.conn:
            self.conn.close()

    def obtener_sentencias_juez(self, juez: str) -> List[Dict]:
        """Obtiene sentencias de un juez con resultado conocido"""
        self.cursor.execute("""
        SELECT
            sentencia_id,
            materia,
            resultado,
            actor,
            demandado,
            perfil_cognitivo,
            texto_completo
        FROM sentencias_por_juez_arg
        WHERE juez = ?
          AND resultado IS NOT NULL
          AND resultado != ''
        """, (juez,))

        sentencias = []
        for row in self.cursor.fetchall():
            sent_id, materia, resultado, actor, demandado, perfil_json, texto = row

            perfil = {}
            if perfil_json:
                try:
                    perfil = json.loads(perfil_json)
                except:
                    pass

            sentencias.append({
                'sentencia_id': sent_id,
                'materia': materia,
                'resultado': resultado,
                'actor': actor,
                'demandado': demandado,
                'perfil': perfil,
                'texto_completo': texto
            })

        return sentencias

    def entrenar_modelo(self, juez: str, min_sentencias: int = 5) -> Optional[Dict]:
        """
        Entrena un modelo predictivo para un juez

        Returns:
            Diccionario con modelo y metadatos o None
        """
        print(f"\n{Colors.BOLD}Entrenando modelo para: {juez}{Colors.ENDC}")

        # Obtener sentencias
        sentencias = self.obtener_sentencias_juez(juez)

        if len(sentencias) < min_sentencias:
            print_warning(f"  Insuficientes sentencias ({len(sentencias)} < {min_sentencias})")
            return None

        print_success(f"  Sentencias disponibles: {len(sentencias)}")

        # Extraer factores
        X = []  # Features
        y = []  # Labels (resultados)
        feature_names_list = []

        for sent in sentencias:
            factores = self.extractor.extraer_factores(sent)
            vector, fnames = self.extractor.factores_a_vector(factores)

            if not feature_names_list:
                feature_names_list = fnames

            X.append(vector)
            y.append(sent['resultado'])

        if not X:
            print_error("  No se pudieron extraer factores")
            return None

        # Convertir a numpy
        X = np.array(X)
        y = np.array(y)

        # Verificar variabilidad
        if len(set(y)) < 2:
            print_warning(f"  Solo hay una clase ({set(y)}), no se puede entrenar")
            return None

        print_info(f"  Features: {len(feature_names_list)}, Clases: {set(y)}")

        # Dividir train/test
        if len(sentencias) >= 10:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y if len(set(y)) > 1 else None
            )
        else:
            # Muy pocas sentencias, usar todas para entrenar
            X_train, X_test, y_train, y_test = X, X, y, y

        # Entrenar Random Forest
        try:
            modelo = RandomForestClassifier(
                n_estimators=50,
                max_depth=5,
                min_samples_split=2,
                random_state=42
            )
            modelo.fit(X_train, y_train)

            # Evaluar
            y_pred = modelo.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)

            print_success(f"  Accuracy: {accuracy:.2%}")

            # Feature importance
            importances = modelo.feature_importances_
            feature_importance = list(zip(feature_names_list, importances))
            feature_importance.sort(key=lambda x: x[1], reverse=True)

            print_info("  Top 5 factores importantes:")
            for fname, importance in feature_importance[:5]:
                print(f"    - {fname}: {importance:.3f}")

            # Guardar modelo
            modelo_data = {
                'modelo': modelo,
                'feature_names': feature_names_list,
                'accuracy': accuracy,
                'n_sentencias': len(sentencias),
                'clases': list(set(y)),
                'feature_importance': feature_importance,
                'fecha_entrenamiento': datetime.now().isoformat()
            }

            # Guardar en disco
            modelo_path = self.models_dir / f"modelo_{juez.replace(' ', '_')}.pkl"
            with open(modelo_path, 'wb') as f:
                pickle.dump(modelo_data, f)

            print_success(f"  Modelo guardado: {modelo_path.name}")

            # Guardar factores en BD
            self.guardar_factores_bd(juez, feature_importance)

            return modelo_data

        except Exception as e:
            print_error(f"  Error al entrenar: {e}")
            return None

    def guardar_factores_bd(self, juez: str, feature_importance: List[Tuple[str, float]]):
        """Guarda factores predictivos en la BD"""
        # Limpiar factores antiguos
        self.cursor.execute("DELETE FROM factores_predictivos WHERE juez = ?", (juez,))

        # Guardar nuevos
        for factor, peso in feature_importance:
            try:
                self.cursor.execute("""
                INSERT INTO factores_predictivos (
                    juez,
                    factor,
                    peso,
                    confianza,
                    ejemplos,
                    fecha_calculo
                ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    juez,
                    factor,
                    float(peso),
                    min(1.0, peso * 2),  # Confianza basada en importancia
                    0,  # Por ahora
                    datetime.now().isoformat()
                ))
            except sqlite3.Error:
                pass

        self.conn.commit()

    def predecir(self, juez: str, factores_caso: Dict) -> Optional[Dict]:
        """
        Predice el resultado para un caso

        Args:
            juez: Nombre del juez
            factores_caso: Diccionario con factores del caso

        Returns:
            Diccionario con predicción o None
        """
        # Cargar modelo
        modelo_path = self.models_dir / f"modelo_{juez.replace(' ', '_')}.pkl"

        if not modelo_path.exists():
            print_error(f"Modelo no encontrado para {juez}")
            print_info("Ejecutar primero el entrenamiento")
            return None

        with open(modelo_path, 'rb') as f:
            modelo_data = pickle.load(f)

        # Convertir factores a vector
        vector, _ = self.extractor.factores_a_vector(
            factores_caso,
            feature_names=modelo_data['feature_names']
        )

        # Predecir
        modelo = modelo_data['modelo']
        prediccion = modelo.predict([vector])[0]
        probabilidades = modelo.predict_proba([vector])[0]

        # Obtener probabilidad de la clase predicha
        clases = modelo.classes_
        prob_prediccion = probabilidades[list(clases).index(prediccion)]

        resultado = {
            'prediccion': prediccion,
            'confianza': float(prob_prediccion),
            'probabilidades': {clase: float(prob) for clase, prob in zip(clases, probabilidades)},
            'factores_importantes': modelo_data['feature_importance'][:5],
            'accuracy_modelo': modelo_data['accuracy']
        }

        return resultado

    def entrenar_todos_los_jueces(self, min_sentencias: int = 5) -> Dict:
        """Entrena modelos para todos los jueces"""
        print(f"\n{Colors.BOLD}{'='*70}")
        print("ENTRENAMIENTO DE MODELOS PREDICTIVOS - TODOS LOS JUECES")
        print(f"{'='*70}{Colors.ENDC}\n")

        # Obtener jueces
        self.cursor.execute("""
        SELECT DISTINCT juez
        FROM sentencias_por_juez_arg
        WHERE resultado IS NOT NULL AND resultado != ''
        """)

        jueces = [row[0] for row in self.cursor.fetchall()]

        if not jueces:
            print_error("No hay jueces con sentencias y resultados")
            return {'total': 0, 'entrenados': 0}

        print_info(f"Jueces candidatos: {len(jueces)}")

        # Entrenar cada juez
        entrenados = 0
        for juez in jueces:
            try:
                modelo = self.entrenar_modelo(juez, min_sentencias)
                if modelo:
                    entrenados += 1
            except Exception as e:
                print_error(f"Error con {juez}: {e}")

        # Resumen
        print(f"\n{Colors.BOLD}{'='*70}")
        print("RESUMEN")
        print(f"{'='*70}{Colors.ENDC}")
        print(f"Jueces candidatos: {len(jueces)}")
        print(f"{Colors.OKGREEN}Modelos entrenados: {entrenados}{Colors.ENDC}\n")

        return {
            'total': len(jueces),
            'entrenados': entrenados
        }


def main():
    """Función principal"""
    import argparse
    import sys

    if not SKLEARN_DISPONIBLE:
        print_error("scikit-learn no está disponible")
        print_info("Instalar con: pip install scikit-learn numpy")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description='Motor predictivo judicial con Machine Learning'
    )
    parser.add_argument(
        'juez',
        nargs='?',
        help='Nombre del juez para entrenar'
    )
    parser.add_argument(
        '--todos',
        action='store_true',
        help='Entrenar modelos para todos los jueces'
    )
    parser.add_argument(
        '--predecir',
        action='store_true',
        help='Modo predicción (requiere --juez y factores)'
    )
    parser.add_argument(
        '--min-sentencias',
        type=int,
        default=5,
        help='Mínimo de sentencias para entrenar (default: 5)'
    )

    args = parser.parse_args()

    # Crear motor
    try:
        motor = MotorPredictivoJudicial()
    except Exception as e:
        print_error(str(e))
        sys.exit(1)

    try:
        if args.todos:
            stats = motor.entrenar_todos_los_jueces(args.min_sentencias)
            sys.exit(0)

        elif args.juez and not args.predecir:
            modelo = motor.entrenar_modelo(args.juez, args.min_sentencias)
            sys.exit(0 if modelo else 1)

        elif args.predecir and args.juez:
            # Modo predicción interactivo
            print(f"\nPredicción para: {args.juez}")
            print("Ingrese factores del caso (ejemplo: materia=despido, tipo_actor=persona)")
            print("(presione Enter vacío para terminar)")

            factores = {}
            while True:
                entrada = input("Factor: ").strip()
                if not entrada:
                    break
                if '=' in entrada:
                    key, value = entrada.split('=', 1)
                    # Intentar convertir a número
                    try:
                        value = float(value)
                    except:
                        pass
                    factores[key.strip()] = value

            if factores:
                resultado = motor.predecir(args.juez, factores)
                if resultado:
                    print(f"\n{Colors.BOLD}PREDICCIÓN:{Colors.ENDC}")
                    print(f"  Resultado: {resultado['prediccion']}")
                    print(f"  Confianza: {resultado['confianza']:.2%}")
                    print(f"\n  Probabilidades:")
                    for clase, prob in resultado['probabilidades'].items():
                        print(f"    {clase}: {prob:.2%}")

            sys.exit(0)

        else:
            parser.print_help()
            sys.exit(1)

    finally:
        motor.cerrar_bd()


if __name__ == "__main__":
    main()
