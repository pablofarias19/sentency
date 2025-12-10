#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULO DE VALORES JUS - PODER JUDICIAL DE CORDOBA
==================================================

Sistema para obtener y gestionar los valores JUS (unidad arancelaria)
utilizados en la regulacion de honorarios profesionales en Cordoba, Argentina.

FUENTE OFICIAL:
https://www.justiciacordoba.gob.ar/justiciacordoba/Servicios/JUSyUnidadEconomica/1

IMPORTANTE:
- Los honorarios siempre se determinan en unidades JUS
- Si el valor esta en pesos, debe traducirse al valor JUS vigente
- El valor JUS se actualiza periodicamente por el Tribunal Superior de Justicia

AUTOR: Sistema Judicial v1.0
FECHA: 10 DIC 2025
"""

import json
import os
import sqlite3
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import requests
from bs4 import BeautifulSoup
import re


@dataclass
class ValorJUS:
    """Representa un valor JUS en una fecha determinada"""
    fecha_vigencia: str  # YYYY-MM-DD
    valor_pesos: float
    acuerdo_tsj: str  # Numero de acuerdo del TSJ que lo establece
    observaciones: str = ""


class GestorValoresJUS:
    """
    Gestor de valores JUS del Poder Judicial de Cordoba

    El JUS es la unidad arancelaria utilizada para determinar
    honorarios profesionales en el ambito judicial de Cordoba.
    """

    # URL oficial para consulta de valores JUS
    URL_OFICIAL_JUS = "https://www.justiciacordoba.gob.ar/justiciacordoba/Servicios/JUSyUnidadEconomica/1"

    # Valores JUS historicos conocidos (actualizar periodicamente)
    # Estos valores son de referencia - siempre verificar en la fuente oficial
    VALORES_REFERENCIA = [
        # Formato: (fecha_vigencia, valor_pesos, acuerdo)
        # NOTA: Estos son valores de ejemplo - deben actualizarse con valores reales
        ValorJUS("2024-01-01", 2500.00, "Acuerdo TSJ 1/2024", "Valor de referencia"),
        ValorJUS("2024-04-01", 2800.00, "Acuerdo TSJ 150/2024", "Actualizacion trimestral"),
        ValorJUS("2024-07-01", 3200.00, "Acuerdo TSJ 450/2024", "Actualizacion trimestral"),
        ValorJUS("2024-10-01", 3600.00, "Acuerdo TSJ 750/2024", "Actualizacion trimestral"),
        ValorJUS("2025-01-01", 4000.00, "Acuerdo TSJ 1/2025", "Valor de referencia 2025"),
    ]

    def __init__(self, db_path: Optional[str] = None):
        """
        Inicializa el gestor de valores JUS

        Args:
            db_path: Ruta a la base de datos SQLite. Si no se proporciona,
                    usa una ruta por defecto.
        """
        if db_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "..", "data", "valores_jus.db")

        self.db_path = db_path
        self._inicializar_db()

    def _inicializar_db(self):
        """Crea la tabla de valores JUS si no existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS valores_jus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_vigencia DATE NOT NULL UNIQUE,
                valor_pesos REAL NOT NULL,
                acuerdo_tsj TEXT,
                observaciones TEXT,
                fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_fecha_vigencia
            ON valores_jus(fecha_vigencia DESC)
        """)

        conn.commit()
        conn.close()

        # Cargar valores de referencia si la tabla esta vacia
        self._cargar_valores_referencia()

    def _cargar_valores_referencia(self):
        """Carga los valores de referencia si no hay datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM valores_jus")
        count = cursor.fetchone()[0]

        if count == 0:
            for valor in self.VALORES_REFERENCIA:
                try:
                    cursor.execute("""
                        INSERT INTO valores_jus
                        (fecha_vigencia, valor_pesos, acuerdo_tsj, observaciones)
                        VALUES (?, ?, ?, ?)
                    """, (valor.fecha_vigencia, valor.valor_pesos,
                          valor.acuerdo_tsj, valor.observaciones))
                except sqlite3.IntegrityError:
                    pass  # Ya existe

            conn.commit()

        conn.close()

    def obtener_valor_jus_vigente(self, fecha: Optional[str] = None) -> Optional[ValorJUS]:
        """
        Obtiene el valor JUS vigente para una fecha determinada

        Args:
            fecha: Fecha en formato YYYY-MM-DD. Si no se proporciona,
                  usa la fecha actual.

        Returns:
            ValorJUS vigente o None si no hay datos
        """
        if fecha is None:
            fecha = date.today().strftime("%Y-%m-%d")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Buscar el valor vigente mas reciente anterior o igual a la fecha
        cursor.execute("""
            SELECT fecha_vigencia, valor_pesos, acuerdo_tsj, observaciones
            FROM valores_jus
            WHERE fecha_vigencia <= ?
            ORDER BY fecha_vigencia DESC
            LIMIT 1
        """, (fecha,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return ValorJUS(
                fecha_vigencia=row[0],
                valor_pesos=row[1],
                acuerdo_tsj=row[2],
                observaciones=row[3] or ""
            )

        return None

    def convertir_pesos_a_jus(self, monto_pesos: float,
                              fecha: Optional[str] = None) -> Dict:
        """
        Convierte un monto en pesos a JUS

        Args:
            monto_pesos: Monto en pesos argentinos
            fecha: Fecha para el valor JUS a aplicar (YYYY-MM-DD)

        Returns:
            Diccionario con la conversion y detalles
        """
        valor_jus = self.obtener_valor_jus_vigente(fecha)

        if valor_jus is None:
            return {
                "exito": False,
                "error": "No se encontro valor JUS vigente",
                "url_consulta": self.URL_OFICIAL_JUS,
                "monto_pesos": monto_pesos,
                "monto_jus": None
            }

        monto_jus = monto_pesos / valor_jus.valor_pesos

        return {
            "exito": True,
            "monto_pesos": monto_pesos,
            "monto_jus": round(monto_jus, 2),
            "valor_jus_aplicado": valor_jus.valor_pesos,
            "fecha_valor_jus": valor_jus.fecha_vigencia,
            "acuerdo_tsj": valor_jus.acuerdo_tsj,
            "url_consulta": self.URL_OFICIAL_JUS
        }

    def convertir_jus_a_pesos(self, monto_jus: float,
                              fecha: Optional[str] = None) -> Dict:
        """
        Convierte un monto en JUS a pesos

        Args:
            monto_jus: Monto en unidades JUS
            fecha: Fecha para el valor JUS a aplicar (YYYY-MM-DD)

        Returns:
            Diccionario con la conversion y detalles
        """
        valor_jus = self.obtener_valor_jus_vigente(fecha)

        if valor_jus is None:
            return {
                "exito": False,
                "error": "No se encontro valor JUS vigente",
                "url_consulta": self.URL_OFICIAL_JUS,
                "monto_jus": monto_jus,
                "monto_pesos": None
            }

        monto_pesos = monto_jus * valor_jus.valor_pesos

        return {
            "exito": True,
            "monto_jus": monto_jus,
            "monto_pesos": round(monto_pesos, 2),
            "valor_jus_aplicado": valor_jus.valor_pesos,
            "fecha_valor_jus": valor_jus.fecha_vigencia,
            "acuerdo_tsj": valor_jus.acuerdo_tsj,
            "url_consulta": self.URL_OFICIAL_JUS
        }

    def agregar_valor_jus(self, valor: ValorJUS) -> bool:
        """
        Agrega un nuevo valor JUS a la base de datos

        Args:
            valor: ValorJUS a agregar

        Returns:
            True si se agrego correctamente
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO valores_jus
                (fecha_vigencia, valor_pesos, acuerdo_tsj, observaciones)
                VALUES (?, ?, ?, ?)
            """, (valor.fecha_vigencia, valor.valor_pesos,
                  valor.acuerdo_tsj, valor.observaciones))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(f"Error al agregar valor JUS: {e}")
            return False

    def obtener_historico(self, limit: int = 20) -> List[ValorJUS]:
        """
        Obtiene el historico de valores JUS

        Args:
            limit: Cantidad maxima de registros

        Returns:
            Lista de ValorJUS ordenados por fecha descendente
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT fecha_vigencia, valor_pesos, acuerdo_tsj, observaciones
            FROM valores_jus
            ORDER BY fecha_vigencia DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [
            ValorJUS(
                fecha_vigencia=row[0],
                valor_pesos=row[1],
                acuerdo_tsj=row[2],
                observaciones=row[3] or ""
            )
            for row in rows
        ]

    def intentar_actualizar_desde_web(self) -> Dict:
        """
        Intenta obtener valores actualizados desde la web oficial

        NOTA: Esta funcion puede fallar si el sitio bloquea acceso automatico.
        En ese caso, los valores deben actualizarse manualmente.

        Returns:
            Diccionario con resultado de la operacion
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(self.URL_OFICIAL_JUS, headers=headers, timeout=10)

            if response.status_code == 200:
                # Parsear la pagina para extraer valores
                soup = BeautifulSoup(response.text, 'html.parser')

                # Buscar tablas con valores JUS
                # NOTA: El parsing depende de la estructura HTML del sitio
                valores_encontrados = []

                # Buscar patrones de valores en el texto
                texto = soup.get_text()

                # Patron para encontrar valores JUS: "JUS $X.XXX,XX"
                patron_jus = r'JUS\s*\$?\s*([\d.,]+)'
                matches = re.findall(patron_jus, texto, re.IGNORECASE)

                return {
                    "exito": True,
                    "mensaje": "Pagina accedida correctamente",
                    "valores_encontrados": matches,
                    "url": self.URL_OFICIAL_JUS,
                    "nota": "Verifique manualmente y use agregar_valor_jus() para actualizar"
                }
            else:
                return {
                    "exito": False,
                    "error": f"HTTP {response.status_code}",
                    "url": self.URL_OFICIAL_JUS,
                    "instrucciones": "Consulte la URL manualmente y actualice con agregar_valor_jus()"
                }

        except Exception as e:
            return {
                "exito": False,
                "error": str(e),
                "url": self.URL_OFICIAL_JUS,
                "instrucciones": "Consulte la URL manualmente y actualice con agregar_valor_jus()"
            }

    def info_url_oficial(self) -> str:
        """Retorna informacion sobre la URL oficial para consulta manual"""
        return f"""
CONSULTA DE VALORES JUS - PODER JUDICIAL DE CORDOBA
====================================================

URL Oficial: {self.URL_OFICIAL_JUS}

Para actualizar los valores JUS:
1. Visite la URL oficial
2. Obtenga el valor JUS vigente
3. Use el metodo agregar_valor_jus() con los datos:

    gestor = GestorValoresJUS()
    nuevo_valor = ValorJUS(
        fecha_vigencia="2025-01-15",  # Fecha de inicio de vigencia
        valor_pesos=4500.00,          # Valor en pesos
        acuerdo_tsj="Acuerdo TSJ 100/2025",  # Numero de acuerdo
        observaciones="Actualizacion enero 2025"
    )
    gestor.agregar_valor_jus(nuevo_valor)

IMPORTANTE: Los honorarios profesionales SIEMPRE se determinan en JUS.
Si el monto esta en pesos, debe convertirse al valor JUS vigente.
"""


def test_gestor_jus():
    """Test del gestor de valores JUS"""
    print("=" * 60)
    print("TEST DEL GESTOR DE VALORES JUS")
    print("=" * 60)

    gestor = GestorValoresJUS()

    # Mostrar info de URL oficial
    print(gestor.info_url_oficial())

    # Obtener valor vigente
    valor_vigente = gestor.obtener_valor_jus_vigente()
    if valor_vigente:
        print(f"\nValor JUS vigente: ${valor_vigente.valor_pesos:,.2f}")
        print(f"Desde: {valor_vigente.fecha_vigencia}")
        print(f"Acuerdo: {valor_vigente.acuerdo_tsj}")

    # Test de conversion pesos a JUS
    print("\n--- CONVERSION PESOS A JUS ---")
    resultado = gestor.convertir_pesos_a_jus(100000.00)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Test de conversion JUS a pesos
    print("\n--- CONVERSION JUS A PESOS ---")
    resultado = gestor.convertir_jus_a_pesos(25.0)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    # Mostrar historico
    print("\n--- HISTORICO DE VALORES JUS ---")
    historico = gestor.obtener_historico(5)
    for v in historico:
        print(f"  {v.fecha_vigencia}: ${v.valor_pesos:,.2f} ({v.acuerdo_tsj})")

    # Intentar actualizar desde web
    print("\n--- INTENTO DE ACTUALIZACION WEB ---")
    resultado = gestor.intentar_actualizar_desde_web()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    test_gestor_jus()
