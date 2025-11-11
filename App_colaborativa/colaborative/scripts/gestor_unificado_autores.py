#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 GESTOR UNIFICADO DE BASES DE AUTORES
========================================

Sistema centralizado que:
- Consulta TODAS las bases de datos automáticamente
- Combina información de múltiples fuentes
- Cachea informes generados para evitar regeneración
- Sincroniza datos entre bases
- Proporciona API unificada para acceso a autores

FECHA: 11 NOV 2025
AUTOR: Sistema Cognitivo Jurídico
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import hashlib

class GestorUnificadoAutores:
    """
    Gestor centralizado que consulta todas las bases de datos
    y proporciona acceso unificado a información de autores
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        
        # Definir todas las bases de datos disponibles
        self.bases_datos = {
            'pensamiento_v2': self.base_path / 'colaborative/data/pensamiento_integrado_v2.db',
            'metadatos': self.base_path / 'colaborative/bases_rag/cognitiva/metadatos.db',
            'autor_centrico': self.base_path / 'colaborative/bases_rag/cognitiva/autor_centrico.db',
            'perfiles_autorales': self.base_path / 'colaborative/bases_rag/cognitiva/perfiles_autorales.db',
            'multicapa': self.base_path / 'colaborative/bases_rag/cognitiva/multicapa_pensamiento.db',
        }
        
        # Cache de informes generados
        self.cache_dir = self.base_path / 'colaborative/data/cache_informes'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Mapeo de tablas por base
        self.tablas_por_base = {
            'pensamiento_v2': ['perfiles_integrados_v2'],
            'metadatos': ['perfiles_cognitivos'],
            'autor_centrico': ['perfiles_autorales_expandidos'],
            'perfiles_autorales': ['perfiles_autorales'],
            'multicapa': ['capas_pensamiento']
        }
        
        # Mapeo de columnas de autor
        self.columnas_autor = {
            'pensamiento_v2': 'autor',
            'metadatos': 'autor',
            'autor_centrico': 'autor',
            'perfiles_autorales': 'autor',
            'multicapa': 'autor'
        }
    
    def buscar_autor_todas_bases(self, nombre_autor: str) -> Dict[str, Any]:
        """
        Busca un autor en TODAS las bases de datos disponibles
        y combina los resultados
        """
        print(f"\n🔍 Buscando '{nombre_autor}' en todas las bases...")
        print("="*70)
        
        resultados_combinados = {
            'autor': nombre_autor,
            'encontrado_en': [],
            'datos_combinados': {},
            'timestamp_busqueda': datetime.now().isoformat()
        }
        
        for nombre_base, ruta_db in self.bases_datos.items():
            if not ruta_db.exists():
                print(f"  ⚠️ {nombre_base}: Base no encontrada")
                continue
            
            try:
                conn = sqlite3.connect(ruta_db)
                cur = conn.cursor()
                
                # Buscar en cada tabla de esta base
                for tabla in self.tablas_por_base.get(nombre_base, []):
                    columna_autor = self.columnas_autor.get(nombre_base, 'autor')
                    
                    try:
                        # Verificar si la tabla existe
                        cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tabla,))
                        if not cur.fetchone():
                            continue
                        
                        # Buscar autor
                        cur.execute(f"SELECT * FROM {tabla} WHERE {columna_autor} = ?", (nombre_autor,))
                        resultado = cur.fetchone()
                        
                        if resultado:
                            # Obtener nombres de columnas
                            cur.execute(f"PRAGMA table_info({tabla})")
                            columnas = [col[1] for col in cur.fetchall()]
                            
                            # Crear diccionario con los datos
                            datos_tabla = dict(zip(columnas, resultado))
                            
                            resultados_combinados['encontrado_en'].append({
                                'base': nombre_base,
                                'tabla': tabla,
                                'num_campos': len(datos_tabla)
                            })
                            
                            # Combinar datos (sin sobrescribir)
                            for key, value in datos_tabla.items():
                                clave_completa = f"{nombre_base}_{tabla}_{key}"
                                if clave_completa not in resultados_combinados['datos_combinados']:
                                    resultados_combinados['datos_combinados'][clave_completa] = value
                            
                            print(f"  ✅ {nombre_base}.{tabla}: {len(datos_tabla)} campos")
                    
                    except sqlite3.Error as e:
                        print(f"  ⚠️ {nombre_base}.{tabla}: Error - {e}")
                        continue
                
                conn.close()
                
            except Exception as e:
                print(f"  ❌ {nombre_base}: Error general - {e}")
        
        # Resumen
        total_bases = len(resultados_combinados['encontrado_en'])
        print(f"\n📊 Encontrado en {total_bases} base(s)")
        
        if total_bases == 0:
            return None
        
        return resultados_combinados
    
    def listar_todos_autores(self) -> List[str]:
        """
        Lista TODOS los autores únicos en todas las bases
        """
        autores = set()
        
        for nombre_base, ruta_db in self.bases_datos.items():
            if not ruta_db.exists():
                continue
            
            try:
                conn = sqlite3.connect(ruta_db)
                cur = conn.cursor()
                
                for tabla in self.tablas_por_base.get(nombre_base, []):
                    columna_autor = self.columnas_autor.get(nombre_base, 'autor')
                    
                    try:
                        cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tabla,))
                        if not cur.fetchone():
                            continue
                        
                        cur.execute(f"SELECT DISTINCT {columna_autor} FROM {tabla}")
                        for row in cur.fetchall():
                            if row[0]:
                                autores.add(row[0])
                    except:
                        continue
                
                conn.close()
            except:
                continue
        
        return sorted(list(autores))
    
    def obtener_informe_cacheado(self, nombre_autor: str) -> Optional[Dict]:
        """
        Busca informe cacheado previamente generado
        """
        # Generar hash del nombre para nombre de archivo
        autor_hash = hashlib.md5(nombre_autor.encode()).hexdigest()
        cache_file = self.cache_dir / f"informe_{autor_hash}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                # Verificar si el cache no es muy antiguo (7 días)
                timestamp = datetime.fromisoformat(cached_data.get('timestamp', '2000-01-01'))
                dias_antiguedad = (datetime.now() - timestamp).days
                
                if dias_antiguedad < 7:
                    print(f"✅ Informe encontrado en caché (generado hace {dias_antiguedad} días)")
                    return cached_data
                else:
                    print(f"⚠️ Informe en caché muy antiguo ({dias_antiguedad} días), regenerando...")
            except:
                pass
        
        return None
    
    def guardar_informe_cache(self, nombre_autor: str, informe_data: Dict):
        """
        Guarda informe en caché para evitar regeneración
        """
        try:
            autor_hash = hashlib.md5(nombre_autor.encode()).hexdigest()
            cache_file = self.cache_dir / f"informe_{autor_hash}.json"
            
            # Agregar timestamp
            informe_data['timestamp'] = datetime.now().isoformat()
            informe_data['autor'] = nombre_autor
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(informe_data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Informe guardado en caché: {cache_file.name}")
            return True
        except Exception as e:
            print(f"⚠️ Error guardando caché: {e}")
            return False
    
    def limpiar_cache_antiguo(self, dias: int = 30):
        """
        Elimina informes cacheados más antiguos que X días
        """
        eliminados = 0
        
        for cache_file in self.cache_dir.glob("informe_*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                timestamp = datetime.fromisoformat(data.get('timestamp', '2000-01-01'))
                dias_antiguedad = (datetime.now() - timestamp).days
                
                if dias_antiguedad > dias:
                    cache_file.unlink()
                    eliminados += 1
            except:
                continue
        
        print(f"🗑️ Eliminados {eliminados} informes antiguos del caché")
        return eliminados
    
    def sincronizar_autor_entre_bases(self, nombre_autor: str, datos_maestros: Dict):
        """
        Sincroniza información de un autor entre todas las bases
        (solo actualiza campos faltantes, no sobrescribe)
        """
        print(f"\n🔄 Sincronizando '{nombre_autor}' entre bases...")
        
        # Esta función requeriría lógica más compleja según la estructura
        # de cada base. Por ahora, es un placeholder.
        
        print("⚠️ Sincronización manual requerida")
        return False
    
    def generar_reporte_estado_bases(self) -> Dict:
        """
        Genera reporte del estado de todas las bases
        """
        reporte = {
            'timestamp': datetime.now().isoformat(),
            'bases': {}
        }
        
        for nombre_base, ruta_db in self.bases_datos.items():
            info_base = {
                'existe': ruta_db.exists(),
                'ruta': str(ruta_db),
                'tablas': {},
                'total_autores': 0
            }
            
            if ruta_db.exists():
                try:
                    conn = sqlite3.connect(ruta_db)
                    cur = conn.cursor()
                    
                    for tabla in self.tablas_por_base.get(nombre_base, []):
                        try:
                            cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tabla,))
                            if cur.fetchone():
                                columna_autor = self.columnas_autor.get(nombre_base, 'autor')
                                cur.execute(f"SELECT COUNT(DISTINCT {columna_autor}) FROM {tabla}")
                                num_autores = cur.fetchone()[0]
                                
                                cur.execute(f"SELECT COUNT(*) FROM {tabla}")
                                num_registros = cur.fetchone()[0]
                                
                                info_base['tablas'][tabla] = {
                                    'autores_unicos': num_autores,
                                    'registros_totales': num_registros
                                }
                                info_base['total_autores'] += num_autores
                        except:
                            info_base['tablas'][tabla] = {'error': True}
                    
                    conn.close()
                except Exception as e:
                    info_base['error'] = str(e)
            
            reporte['bases'][nombre_base] = info_base
        
        return reporte


# ══════════════════════════════════════════════════════════════════════════
# INSTANCIA GLOBAL SINGLETON
# ══════════════════════════════════════════════════════════════════════════

gestor_autores = GestorUnificadoAutores()


# ══════════════════════════════════════════════════════════════════════════
# FUNCIONES DE UTILIDAD PARA IMPORTAR
# ══════════════════════════════════════════════════════════════════════════

def buscar_autor(nombre: str) -> Optional[Dict]:
    """Busca autor en todas las bases"""
    return gestor_autores.buscar_autor_todas_bases(nombre)

def listar_autores() -> List[str]:
    """Lista todos los autores disponibles"""
    return gestor_autores.listar_todos_autores()

def obtener_informe_cache(nombre: str) -> Optional[Dict]:
    """Obtiene informe desde caché si existe"""
    return gestor_autores.obtener_informe_cacheado(nombre)

def guardar_informe(nombre: str, informe: Dict) -> bool:
    """Guarda informe en caché"""
    return gestor_autores.guardar_informe_cache(nombre, informe)


# ══════════════════════════════════════════════════════════════════════════
# TEST Y DEMOSTRACIÓN
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔗 GESTOR UNIFICADO DE BASES DE AUTORES")
    print("="*70)
    
    # Test 1: Buscar autor específico
    print("\n📋 TEST 1: Buscar 'Luciana B. Scotti'")
    resultado = buscar_autor('Luciana B. Scotti')
    if resultado:
        print(f"\n✅ Encontrado en {len(resultado['encontrado_en'])} base(s):")
        for base in resultado['encontrado_en']:
            print(f"  • {base['base']}.{base['tabla']} ({base['num_campos']} campos)")
        print(f"\n📊 Total campos combinados: {len(resultado['datos_combinados'])}")
    else:
        print("❌ No encontrado")
    
    # Test 2: Listar todos los autores
    print("\n📋 TEST 2: Listar primeros 10 autores disponibles")
    autores = listar_autores()
    print(f"\n✅ Total autores únicos: {len(autores)}")
    print("Primeros 10:")
    for i, autor in enumerate(autores[:10], 1):
        print(f"  {i}. {autor}")
    
    # Test 3: Reporte de estado
    print("\n📋 TEST 3: Reporte de estado de bases")
    reporte = gestor_autores.generar_reporte_estado_bases()
    print(f"\nEstado de bases:")
    for nombre, info in reporte['bases'].items():
        status = "✅" if info['existe'] else "❌"
        autores_count = info.get('total_autores', 0)
        print(f"  {status} {nombre}: {autores_count} autores")
        for tabla, datos in info.get('tablas', {}).items():
            if 'error' not in datos:
                print(f"      → {tabla}: {datos['autores_unicos']} autores, {datos['registros_totales']} registros")
    
    # Test 4: Caché de informes
    print("\n📋 TEST 4: Sistema de caché")
    cache_count = len(list(gestor_autores.cache_dir.glob("informe_*.json")))
    print(f"  Informes en caché: {cache_count}")
    print(f"  Directorio caché: {gestor_autores.cache_dir}")
    
    print("\n" + "="*70)
    print("✅ Tests completados")
    print("="*70 + "\n")
