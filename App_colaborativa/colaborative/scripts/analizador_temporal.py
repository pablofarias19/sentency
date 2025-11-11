"""
📅 ANALIZADOR TEMPORAL DE EVOLUCIÓN DOCTRINAL
==============================================
Detecta evolución de pensamiento y conceptos a lo largo del tiempo.
"""

import re
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Tuple
from pathlib import Path
from collections import defaultdict
import json

class AnalizadorTemporal:
    """
    Analiza evolución temporal de conceptos, autores y doctrinas.
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.periodos = {
            'clasico': (1900, 1950),
            'moderno': (1951, 1990),
            'contemporaneo': (1991, 2010),
            'actual': (2011, 2030)
        }
    
    def extraer_fecha_publicacion(self, texto_pdf: str, metadata: Dict) -> Tuple[int, str]:
        """
        Extrae fecha de publicación del PDF.
        
        Returns:
            (año, fuente_deteccion)
        """
        # 1. Intentar desde metadatos
        if metadata and 'CreationDate' in metadata:
            try:
                # Formato típico: D:20150325120000
                fecha_str = metadata['CreationDate']
                match = re.search(r'(\d{4})', fecha_str)
                if match:
                    año = int(match.group(1))
                    if 1900 <= año <= 2030:
                        return año, 'metadata_pdf'
            except:
                pass
        
        # 2. Buscar en texto (portada typical patterns)
        patrones_fecha = [
            r'(?:publicado|editado|copyright|©)\s*(?:en)?\s*(\d{4})',
            r'(?:edición|ed\.)\s*(\d{4})',
            r'\((\d{4})\)',  # Año entre paréntesis
            r'(\d{4})\s*[-–]\s*\d{4}',  # Rango de años
            r'(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+(?:de\s+)?(\d{4})'
        ]
        
        # Buscar solo en primeras 3 páginas (portada)
        texto_portada = texto_pdf[:5000]
        
        for patron in patrones_fecha:
            matches = re.findall(patron, texto_portada, re.IGNORECASE)
            if matches:
                # Tomar el primer año válido
                for año_str in matches:
                    try:
                        año = int(año_str)
                        if 1900 <= año <= 2030:
                            return año, 'texto_portada'
                    except:
                        continue
        
        # 3. Buscar en referencias bibliográficas (últimas páginas)
        texto_final = texto_pdf[-5000:]
        for patron in patrones_fecha:
            matches = re.findall(patron, texto_final, re.IGNORECASE)
            if matches:
                años = []
                for año_str in matches:
                    try:
                        año = int(año_str)
                        if 1900 <= año <= 2030:
                            años.append(año)
                    except:
                        continue
                
                if años:
                    # Usar el año más reciente de las referencias como aproximación
                    return max(años), 'bibliografia'
        
        # 4. Fallback: fecha actual
        return datetime.now().year, 'fallback_actual'
    
    def clasificar_periodo(self, año: int) -> str:
        """Clasifica el año en un periodo doctrinal."""
        for periodo, (inicio, fin) in self.periodos.items():
            if inicio <= año <= fin:
                return periodo
        return 'indeterminado'
    
    def analizar_evolucion_autor(self, autor: str, ventana_años: int = 5) -> Dict[str, Any]:
        """
        Analiza evolución del pensamiento de un autor a lo largo del tiempo.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Obtener todos los documentos del autor con fecha
        cursor.execute("""
            SELECT archivo, fecha_publicacion, periodo_doctrinal,
                   formalismo, creatividad, dogmatismo, empirismo,
                   interdisciplinariedad, nivel_abstraccion,
                   complejidad_sintactica, uso_jurisprudencia,
                   razonamiento_dominante
            FROM perfiles_cognitivos
            WHERE autor = ? AND fecha_publicacion IS NOT NULL
            ORDER BY fecha_publicacion
        """, (autor,))
        
        docs = cursor.fetchall()
        conn.close()
        
        if not docs:
            return {'estado': 'sin_datos', 'autor': autor}
        
        # Agrupar por ventanas temporales
        ventanas = self._crear_ventanas_temporales(docs, ventana_años)
        
        # Calcular cambios significativos
        cambios = self._detectar_cambios_significativos(ventanas)
        
        # Detectar tendencias
        tendencias = self._calcular_tendencias(ventanas)
        
        return {
            'autor': autor,
            'total_documentos': len(docs),
            'rango_temporal': (docs[0][1], docs[-1][1]) if docs else None,
            'ventanas_temporales': ventanas,
            'cambios_significativos': cambios,
            'tendencias': tendencias,
            'evolucion_conceptual': self._analizar_evolucion_conceptual(docs)
        }
    
    def _crear_ventanas_temporales(self, docs: List, ventana_años: int) -> List[Dict]:
        """Agrupa documentos en ventanas temporales."""
        if not docs:
            return []
        
        año_min = min(doc[1] for doc in docs if doc[1])
        año_max = max(doc[1] for doc in docs if doc[1])
        
        ventanas = []
        for año_inicio in range(año_min, año_max + 1, ventana_años):
            año_fin = año_inicio + ventana_años - 1
            
            docs_ventana = [doc for doc in docs if doc[1] and año_inicio <= doc[1] <= año_fin]
            
            if docs_ventana:
                # Calcular promedios de rasgos
                rasgos_promedio = {
                    'formalismo': sum(d[3] or 0 for d in docs_ventana) / len(docs_ventana),
                    'creatividad': sum(d[4] or 0 for d in docs_ventana) / len(docs_ventana),
                    'dogmatismo': sum(d[5] or 0 for d in docs_ventana) / len(docs_ventana),
                    'empirismo': sum(d[6] or 0 for d in docs_ventana) / len(docs_ventana),
                    'interdisciplinariedad': sum(d[7] or 0 for d in docs_ventana) / len(docs_ventana),
                    'nivel_abstraccion': sum(d[8] or 0 for d in docs_ventana) / len(docs_ventana),
                    'complejidad_sintactica': sum(d[9] or 0 for d in docs_ventana) / len(docs_ventana),
                    'uso_jurisprudencia': sum(d[10] or 0 for d in docs_ventana) / len(docs_ventana)
                }
                
                ventanas.append({
                    'periodo': f"{año_inicio}-{año_fin}",
                    'año_inicio': año_inicio,
                    'año_fin': año_fin,
                    'cantidad_docs': len(docs_ventana),
                    'rasgos_promedio': rasgos_promedio,
                    'razonamiento_dominante': self._moda([d[11] for d in docs_ventana if d[11]])
                })
        
        return ventanas
    
    def _detectar_cambios_significativos(self, ventanas: List[Dict]) -> List[Dict]:
        """Detecta cambios significativos entre ventanas temporales."""
        cambios = []
        umbral_significativo = 0.15  # 15% de cambio
        
        for i in range(1, len(ventanas)):
            ventana_anterior = ventanas[i-1]
            ventana_actual = ventanas[i]
            
            rasgos_ant = ventana_anterior['rasgos_promedio']
            rasgos_act = ventana_actual['rasgos_promedio']
            
            for rasgo in rasgos_ant.keys():
                diferencia = rasgos_act[rasgo] - rasgos_ant[rasgo]
                
                if abs(diferencia) >= umbral_significativo:
                    cambios.append({
                        'periodo_origen': ventana_anterior['periodo'],
                        'periodo_destino': ventana_actual['periodo'],
                        'rasgo': rasgo,
                        'cambio': diferencia,
                        'porcentaje_cambio': (diferencia / rasgos_ant[rasgo] * 100) if rasgos_ant[rasgo] > 0 else 0,
                        'direccion': 'aumento' if diferencia > 0 else 'disminución',
                        'significancia': 'alta' if abs(diferencia) > 0.25 else 'media'
                    })
        
        # Ordenar por magnitud del cambio
        cambios.sort(key=lambda x: abs(x['cambio']), reverse=True)
        
        return cambios
    
    def _calcular_tendencias(self, ventanas: List[Dict]) -> Dict[str, str]:
        """Calcula tendencias generales por rasgo."""
        if len(ventanas) < 2:
            return {}
        
        tendencias = {}
        
        primera_ventana = ventanas[0]['rasgos_promedio']
        ultima_ventana = ventanas[-1]['rasgos_promedio']
        
        for rasgo in primera_ventana.keys():
            valor_inicial = primera_ventana[rasgo]
            valor_final = ultima_ventana[rasgo]
            diferencia = valor_final - valor_inicial
            
            if abs(diferencia) < 0.05:
                tendencia = 'estable'
            elif diferencia > 0:
                tendencia = 'creciente' if diferencia > 0.15 else 'creciente_leve'
            else:
                tendencia = 'decreciente' if diferencia < -0.15 else 'decreciente_leve'
            
            tendencias[rasgo] = tendencia
        
        return tendencias
    
    def _analizar_evolucion_conceptual(self, docs: List) -> List[Dict]:
        """Analiza evolución de conceptos clave."""
        # Simplificado - en producción extraer keywords de cada documento
        evoluciones = []
        
        # Detectar cambios en razonamiento dominante
        razonamientos = [doc[11] for doc in docs if doc[11]]
        if len(razonamientos) >= 2:
            if razonamientos[0] != razonamientos[-1]:
                evoluciones.append({
                    'tipo': 'cambio_metodologico',
                    'descripcion': f'Transición de {razonamientos[0]} a {razonamientos[-1]}',
                    'periodo': f"{docs[0][1]} → {docs[-1][1]}"
                })
        
        return evoluciones
    
    def analizar_evolucion_concepto(self, concepto: str) -> Dict[str, Any]:
        """
        Analiza cómo evoluciona un concepto específico en el corpus a lo largo del tiempo.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar documentos que mencionen el concepto
        # Nota: esto requeriría búsqueda full-text, simplificamos por ahora
        cursor.execute("""
            SELECT autor, fecha_publicacion, archivo,
                   formalismo, creatividad, nivel_abstraccion
            FROM perfiles_cognitivos
            WHERE fecha_publicacion IS NOT NULL
            ORDER BY fecha_publicacion
        """)
        
        docs = cursor.fetchall()
        conn.close()
        
        # Agrupar por década
        por_decada = defaultdict(list)
        for doc in docs:
            if doc[1]:
                decada = (doc[1] // 10) * 10
                por_decada[decada].append(doc)
        
        evolucion = []
        for decada in sorted(por_decada.keys()):
            docs_decada = por_decada[decada]
            evolucion.append({
                'decada': f"{decada}s",
                'cantidad_autores': len(set(d[0] for d in docs_decada)),
                'cantidad_documentos': len(docs_decada),
                'formalismo_promedio': sum(d[3] or 0 for d in docs_decada) / len(docs_decada),
                'creatividad_promedio': sum(d[4] or 0 for d in docs_decada) / len(docs_decada),
                'abstraccion_promedio': sum(d[5] or 0 for d in docs_decada) / len(docs_decada)
            })
        
        return {
            'concepto': concepto,
            'evolucion_por_decada': evolucion,
            'tendencia_general': self._detectar_tendencia_concepto(evolucion)
        }
    
    def _detectar_tendencia_concepto(self, evolucion: List[Dict]) -> str:
        """Detecta tendencia general del concepto."""
        if len(evolucion) < 2:
            return 'insuficientes_datos'
        
        primera_decada = evolucion[0]
        ultima_decada = evolucion[-1]
        
        aumento_documentos = ultima_decada['cantidad_documentos'] > primera_decada['cantidad_documentos']
        
        if aumento_documentos:
            return 'creciente_relevancia'
        else:
            return 'estable_o_decreciente'
    
    def _moda(self, lista: List) -> Any:
        """Retorna el valor más frecuente."""
        if not lista:
            return None
        return max(set(lista), key=lista.count)
    
    def generar_timeline(self, autor: str = None) -> List[Dict]:
        """
        Genera timeline completo del corpus o de un autor.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if autor:
            cursor.execute("""
                SELECT fecha_publicacion, archivo, razonamiento_dominante,
                       formalismo, creatividad
                FROM perfiles_cognitivos
                WHERE autor = ? AND fecha_publicacion IS NOT NULL
                ORDER BY fecha_publicacion
            """, (autor,))
        else:
            cursor.execute("""
                SELECT fecha_publicacion, autor, archivo, razonamiento_dominante
                FROM perfiles_cognitivos
                WHERE fecha_publicacion IS NOT NULL
                ORDER BY fecha_publicacion
            """)
        
        eventos = []
        for row in cursor.fetchall():
            eventos.append({
                'año': row[0],
                'autor': row[1] if not autor else autor,
                'documento': row[2] if not autor else row[1],
                'metodologia': row[3] if not autor else row[2],
                'periodo': self.clasificar_periodo(row[0])
            })
        
        conn.close()
        return eventos


# ==========================================================
# EJEMPLO DE USO
# ==========================================================
if __name__ == "__main__":
    # Simulación (requiere BD real para funcionar)
    print("📅 ANALIZADOR TEMPORAL - Módulo de Evolución Doctrinal")
    print("=" * 70)
    print("✅ Funcionalidades implementadas:")
    print("   • Extracción automática de fechas de publicación")
    print("   • Clasificación en periodos doctrinales")
    print("   • Análisis de evolución de autores")
    print("   • Detección de cambios significativos")
    print("   • Timeline de evolución conceptual")
    print("   • Tendencias temporales por rasgo cognitivo")
    print("\n💡 Uso: analizador = AnalizadorTemporal(db_path)")
    print("        evolucion = analizador.analizar_evolucion_autor('Autor X')")
