#!/usr/bin/env python3
"""
AUDITORÍA COMPLETA DEL SISTEMA ANALYSER MÉTODO v3.1
Verifica la efectividad real de la detección y análisis cognitivo
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "colaborative" / "bases_rag" / "cognitiva" / "metadatos.db"

def auditoria_completa_sistema():
    print("🔍 AUDITORÍA COMPLETA - ANALYSER MÉTODO v3.1")
    print("=" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🗃️ Base de datos: {DB_PATH}")
    print("=" * 70)
    
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0)
        cursor = conn.cursor()
        
        # 1. ANÁLISIS GENERAL
        print("\n📊 1. ANÁLISIS GENERAL DE DATOS")
        print("-" * 40)
        
        cursor.execute("SELECT COUNT(*) FROM perfiles_cognitivos")
        total_registros = cursor.fetchone()[0]
        print(f"📁 Total registros: {total_registros}")
        
        if total_registros == 0:
            print("❌ ERROR CRÍTICO: No hay registros en la base de datos")
            print("💡 Solución: Ejecutar python colaborative/scripts/ingesta_cognitiva.py")
            return
        
        # 2. ANÁLISIS DE AUTORÍA
        print("\n👤 2. ANÁLISIS DE AUTORÍA (LAYOUT + SEMÁNTICA)")
        print("-" * 50)
        
        cursor.execute("""
            SELECT archivo, autor, autor_confianza, fuente 
            FROM perfiles_cognitivos 
            ORDER BY autor_confianza DESC
        """)
        autores_data = cursor.fetchall()
        
        autores_validos = 0
        autores_fallback = 0
        confianzas = []
        
        for archivo, autor, confianza, fuente in autores_data:
            if confianza and confianza > 0:
                confianzas.append(confianza)
                if confianza > 0.7:
                    autores_validos += 1
                    status = "✅ ALTA"
                elif confianza > 0.4:
                    status = "⚠️ MEDIA"
                else:
                    status = "❌ BAJA"
            else:
                autores_fallback += 1
                status = "❌ SIN DATOS"
                confianza = 0.0
            
            print(f"  📄 {archivo[:30]:<30} | 👤 {autor[:20]:<20} | 🎯 {confianza:.2f} | {status}")
        
        avg_confianza = sum(confianzas) / len(confianzas) if confianzas else 0
        print(f"\n📈 Promedio confianza autoría: {avg_confianza:.2f}")
        print(f"✅ Autores alta confianza (>0.7): {autores_validos}/{total_registros}")
        print(f"⚠️ Detección fallback: {autores_fallback}/{total_registros}")
        
        # 3. ANÁLISIS ARISTOTÉLICO
        print("\n🏛️ 3. ANÁLISIS ARISTOTÉLICO (ETHOS, PATHOS, LOGOS)")
        print("-" * 55)
        
        cursor.execute("""
            SELECT archivo, autor, ethos, pathos, logos, modalidad_epistemica
            FROM perfiles_cognitivos
        """)
        aristotelico_data = cursor.fetchall()
        
        ethos_validos = pathos_validos = logos_validos = modalidad_validas = 0
        
        for archivo, autor, ethos, pathos, logos, modalidad in aristotelico_data:
            # Verificar valores aristotélicos
            e_status = "✅" if ethos and ethos > 0 else "❌"
            p_status = "✅" if pathos and pathos > 0 else "❌"
            l_status = "✅" if logos and logos > 0 else "❌"
            m_status = "✅" if modalidad and modalidad != "No detectada" else "❌"
            
            if ethos and ethos > 0: ethos_validos += 1
            if pathos and pathos > 0: pathos_validos += 1
            if logos and logos > 0: logos_validos += 1
            if modalidad and modalidad != "No detectada": modalidad_validas += 1
            
            print(f"  📄 {archivo[:25]:<25} | E:{ethos or 0:.2f}{e_status} P:{pathos or 0:.2f}{p_status} L:{logos or 0:.2f}{l_status} | {modalidad or 'N/A':<12}{m_status}")
        
        print(f"\n📊 Efectividad análisis aristotélico:")
        print(f"  🎭 Ethos detectado: {ethos_validos}/{total_registros} ({ethos_validos/total_registros*100:.1f}%)")
        print(f"  ❤️ Pathos detectado: {pathos_validos}/{total_registros} ({pathos_validos/total_registros*100:.1f}%)")
        print(f"  🧠 Logos detectado: {logos_validos}/{total_registros} ({logos_validos/total_registros*100:.1f}%)")
        print(f"  🏛️ Modalidad epistémica: {modalidad_validas}/{total_registros} ({modalidad_validas/total_registros*100:.1f}%)")
        
        # 4. ANÁLISIS DE RAZONAMIENTO
        print("\n🧭 4. ANÁLISIS DE RAZONAMIENTO JURÍDICO")
        print("-" * 45)
        
        cursor.execute("""
            SELECT archivo, autor, razonamiento_top3, estructura_silogistica
            FROM perfiles_cognitivos
        """)
        razonamiento_data = cursor.fetchall()
        
        razonamiento_validos = silogismo_validos = 0
        
        for archivo, autor, razonamiento_json, silogismo_json in razonamiento_data:
            # Analizar razonamiento
            try:
                if razonamiento_json:
                    razonamiento = json.loads(razonamiento_json)
                    if isinstance(razonamiento, list) and len(razonamiento) > 0:
                        primer_razon = razonamiento[0]
                        if isinstance(primer_razon, dict) and primer_razon.get("clase"):
                            razonamiento_validos += 1
                            r_status = "✅"
                            razon_texto = primer_razon.get("clase", "N/A")
                        else:
                            r_status = "❌"
                            razon_texto = "Sin datos"
                    else:
                        r_status = "❌"
                        razon_texto = "Lista vacía"
                else:
                    r_status = "❌"
                    razon_texto = "Null"
            except:
                r_status = "❌"
                razon_texto = "Error JSON"
            
            # Analizar silogismo
            try:
                if silogismo_json:
                    silogismo = json.loads(silogismo_json)
                    if isinstance(silogismo, dict) and silogismo.get("nombre"):
                        silogismo_validos += 1
                        s_status = "✅"
                        silog_texto = silogismo.get("nombre", "N/A")
                    else:
                        s_status = "❌"
                        silog_texto = "Sin nombre"
                else:
                    s_status = "❌"
                    silog_texto = "Null"
            except:
                s_status = "❌"
                silog_texto = "Error JSON"
            
            print(f"  📄 {archivo[:25]:<25} | 🧭 {razon_texto[:15]:<15}{r_status} | 📐 {silog_texto[:15]:<15}{s_status}")
        
        print(f"\n📊 Efectividad análisis de razonamiento:")
        print(f"  🧭 Razonamiento detectado: {razonamiento_validos}/{total_registros} ({razonamiento_validos/total_registros*100:.1f}%)")
        print(f"  📐 Silogismo detectado: {silogismo_validos}/{total_registros} ({silogismo_validos/total_registros*100:.1f}%)")
        
        # 5. ANÁLISIS TELEOLÓGICO
        print("\n🎯 5. ANÁLISIS TELEOLÓGICO Y PÁRRAFOS")
        print("-" * 40)
        
        cursor.execute("""
            SELECT archivo, indice_teleologico, roles_parrafos
            FROM perfiles_cognitivos
        """)
        teleologico_data = cursor.fetchall()
        
        teleologico_validos = parrafos_validos = 0
        
        for archivo, indice_json, roles_json in teleologico_data:
            # Verificar índice teleológico
            try:
                if indice_json:
                    indice = json.loads(indice_json)
                    if isinstance(indice, dict) and indice.get("nodos_detectados"):
                        teleologico_validos += 1
                        t_status = "✅"
                        nodos_count = len(indice.get("nodos_detectados", []))
                    else:
                        t_status = "❌"
                        nodos_count = 0
                else:
                    t_status = "❌"
                    nodos_count = 0
            except:
                t_status = "❌"
                nodos_count = 0
            
            # Verificar roles de párrafos
            try:
                if roles_json:
                    roles = json.loads(roles_json)
                    if isinstance(roles, list) and len(roles) > 0:
                        parrafos_validos += 1
                        p_status = "✅"
                        parrafos_count = len(roles)
                    else:
                        p_status = "❌"
                        parrafos_count = 0
                else:
                    p_status = "❌"
                    parrafos_count = 0
            except:
                p_status = "❌"
                parrafos_count = 0
            
            print(f"  📄 {archivo[:30]:<30} | 🎯 {nodos_count:2d} nodos{t_status} | 📝 {parrafos_count:2d} párrafos{p_status}")
        
        print(f"\n📊 Efectividad análisis estructural:")
        print(f"  🎯 Índice teleológico: {teleologico_validos}/{total_registros} ({teleologico_validos/total_registros*100:.1f}%)")
        print(f"  📝 Clasificación párrafos: {parrafos_validos}/{total_registros} ({parrafos_validos/total_registros*100:.1f}%)")
        
        # 6. RESUMEN EJECUTIVO
        print("\n" + "=" * 70)
        print("📋 RESUMEN EJECUTIVO - EFECTIVIDAD DEL SISTEMA")
        print("=" * 70)
        
        # Calcular score general
        scores = {
            "autoría": (autores_validos / total_registros) * 100,
            "aristotélico": ((ethos_validos + pathos_validos + logos_validos + modalidad_validas) / (total_registros * 4)) * 100,
            "razonamiento": ((razonamiento_validos + silogismo_validos) / (total_registros * 2)) * 100,
            "teleológico": ((teleologico_validos + parrafos_validos) / (total_registros * 2)) * 100
        }
        
        score_general = sum(scores.values()) / len(scores)
        
        print(f"🎯 SCORE GENERAL: {score_general:.1f}%")
        print()
        print("📊 DESGLOSE POR MÓDULO:")
        for modulo, score in scores.items():
            if score >= 80:
                status = "✅ EXCELENTE"
            elif score >= 60:
                status = "⚠️ BUENO"
            elif score >= 40:
                status = "❌ REGULAR"
            else:
                status = "❌ DEFICIENTE"
            print(f"  {modulo.capitalize():<15}: {score:5.1f}% {status}")
        
        # 7. DIAGNÓSTICO Y RECOMENDACIONES
        print(f"\n🔧 DIAGNÓSTICO Y RECOMENDACIONES:")
        print("-" * 40)
        
        if score_general >= 80:
            print("✅ Sistema funcionando ÓPTIMAMENTE")
            print("💡 El motor RAG cuenta con análisis cognitivo de alta calidad")
        elif score_general >= 60:
            print("⚠️ Sistema funcionando BIEN con margen de mejora")
            print("💡 Considerar reprocesamiento de documentos con baja confianza")
        elif score_general >= 40:
            print("❌ Sistema con PROBLEMAS de efectividad")
            print("💡 Revisar algoritmos de detección y parámetros")
        else:
            print("❌ Sistema CRÍTICO - Requiere intervención inmediata")
            print("💡 Posible problema en detector_razonamiento_aristotelico.py")
        
        # Recomendaciones específicas
        if scores["autoría"] < 70:
            print("🔍 Mejorar detección de autoría: revisar patrones de layout")
        if scores["aristotélico"] < 70:
            print("🏛️ Mejorar análisis aristotélico: verificar patrones retóricos")
        if scores["razonamiento"] < 70:
            print("🧭 Mejorar detección de razonamiento: revisar conectores lógicos")
        if scores["teleológico"] < 70:
            print("🎯 Mejorar análisis teleológico: revisar patrones estructurales")
        
        conn.close()
        
        print("=" * 70)
        
        return {
            "score_general": score_general,
            "scores_modulos": scores,
            "total_registros": total_registros,
            "estado": "excelente" if score_general >= 80 else "bueno" if score_general >= 60 else "regular" if score_general >= 40 else "critico"
        }
        
    except Exception as e:
        print(f"❌ ERROR en auditoría: {str(e)}")
        return None

if __name__ == "__main__":
    resultado = auditoria_completa_sistema()
    if resultado and resultado["estado"] in ["regular", "critico"]:
        print(f"\n⚠️ ACCIÓN REQUERIDA: Score {resultado['score_general']:.1f}% indica problemas")
        print("🔧 Ejecutar diagnóstico del detector aristotélico")
    else:
        print(f"\n🎉 Sistema operativo con score {resultado['score_general']:.1f}%")