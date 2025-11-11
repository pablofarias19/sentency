# -*- coding: utf-8 -*-
"""
Reprocesar el PDF de Eduardo Barreira Delfino con análisis cognitivo completo
"""
import os
import sys
import sqlite3
import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime

# Agregar ruta de scripts
sys.path.insert(0, str(Path(__file__).parent / "colaborative" / "scripts"))

# Importar vectorizador cognitivo
from vectorizador_cognitivo import extraer_rasgos_cognitivos

# Configuración
BASE_PATH = Path(__file__).parent / "colaborative"
DB_PATH = BASE_PATH / "bases_rag" / "cognitiva" / "metadatos.db"
PDF_PATH = BASE_PATH / "data" / "pdfs" / "general" / "CONTRATOS DE LEASING - Eduardo Barreira Delfino.pdf"

def extraer_texto_pdf(ruta_pdf):
    """Extrae texto completo del PDF"""
    try:
        doc = fitz.open(ruta_pdf)
        texto_completo = ""
        
        for pagina in doc:
            texto_completo += pagina.get_text()
        
        doc.close()
        return texto_completo
    except Exception as e:
        print(f"❌ Error extrayendo texto: {e}")
        return ""

def actualizar_perfil_cognitivo():
    """Actualiza el perfil de Eduardo Barreira Delfino con análisis cognitivo completo"""
    
    print(f"\n{'='*60}")
    print("🔄 REPROCESANDO PERFIL DE EDUARDO BARREIRA DELFINO")
    print(f"{'='*60}\n")
    
    # 1. Extraer texto del PDF
    print(f"📄 Extrayendo texto de: {PDF_PATH.name}")
    if not PDF_PATH.exists():
        print(f"❌ ERROR: No se encuentra el archivo {PDF_PATH}")
        return False
    
    texto = extraer_texto_pdf(str(PDF_PATH))
    
    if not texto:
        print("❌ ERROR: No se pudo extraer texto del PDF")
        return False
    
    total_palabras = len(texto.split())
    print(f"✅ Texto extraído: {total_palabras} palabras\n")
    
    # 2. Calcular rasgos cognitivos
    print("🧠 Calculando rasgos cognitivos...")
    rasgos = extraer_rasgos_cognitivos(texto)
    
    print("\n📊 RASGOS CALCULADOS:")
    print(f"  • Formalismo:              {rasgos['formalismo']:.3f}")
    print(f"  • Creatividad:             {rasgos['creatividad']:.3f}")
    print(f"  • Dogmatismo:              {rasgos['dogmatismo']:.3f}")
    print(f"  • Empirismo:               {rasgos['empirismo']:.3f}")
    print(f"  • Interdisciplinariedad:   {rasgos['interdisciplinariedad']:.3f}")
    print(f"  • Nivel de Abstracción:    {rasgos['nivel_abstraccion']:.3f}")
    print(f"  • Complejidad Sintáctica:  {rasgos['complejidad_sintactica']:.3f}")
    print(f"  • Uso de Jurisprudencia:   {rasgos['uso_jurisprudencia']:.3f}")
    
    # 3. Actualizar base de datos
    print(f"\n💾 Actualizando base de datos...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        # Actualizar registro existente
        cur.execute("""
            UPDATE perfiles_cognitivos
            SET formalismo = ?,
                creatividad = ?,
                dogmatismo = ?,
                empirismo = ?,
                interdisciplinariedad = ?,
                nivel_abstraccion = ?,
                complejidad_sintactica = ?,
                uso_jurisprudencia = ?,
                total_palabras = ?,
                fecha_analisis = ?
            WHERE autor = 'Eduardo Barreira Delfino'
        """, (
            rasgos['formalismo'],
            rasgos['creatividad'],
            rasgos['dogmatismo'],
            rasgos['empirismo'],
            rasgos['interdisciplinariedad'],
            rasgos['nivel_abstraccion'],
            rasgos['complejidad_sintactica'],
            rasgos['uso_jurisprudencia'],
            total_palabras,
            datetime.now().isoformat()
        ))
        
        filas_actualizadas = cur.rowcount
        conn.commit()
        
        # Verificar actualización
        cur.execute("""
            SELECT formalismo, creatividad, dogmatismo, empirismo, 
                   interdisciplinariedad, nivel_abstraccion, 
                   complejidad_sintactica, uso_jurisprudencia, total_palabras
            FROM perfiles_cognitivos
            WHERE autor = 'Eduardo Barreira Delfino'
        """)
        
        resultado = cur.fetchone()
        conn.close()
        
        if filas_actualizadas > 0 and resultado:
            print(f"✅ Actualizado correctamente ({filas_actualizadas} registro)")
            print("\n🔍 VERIFICACIÓN:")
            print(f"  • Formalismo:              {resultado[0]:.3f}")
            print(f"  • Creatividad:             {resultado[1]:.3f}")
            print(f"  • Dogmatismo:              {resultado[2]:.3f}")
            print(f"  • Empirismo:               {resultado[3]:.3f}")
            print(f"  • Interdisciplinariedad:   {resultado[4]:.3f}")
            print(f"  • Nivel de Abstracción:    {resultado[5]:.3f}")
            print(f"  • Complejidad Sintáctica:  {resultado[6]:.3f}")
            print(f"  • Uso de Jurisprudencia:   {resultado[7]:.3f}")
            print(f"  • Total Palabras:          {resultado[8]}")
            return True
        else:
            print(f"❌ ERROR: No se actualizó ningún registro")
            return False
            
    except Exception as e:
        print(f"❌ ERROR actualizando base de datos: {e}")
        return False

if __name__ == "__main__":
    exito = actualizar_perfil_cognitivo()
    
    if exito:
        print(f"\n{'='*60}")
        print("✅ PERFIL REPROCESADO EXITOSAMENTE")
        print(f"{'='*60}\n")
        print("💡 Ahora puedes ver el perfil actualizado en:")
        print("   http://127.0.0.1:5002/autores")
    else:
        print(f"\n{'='*60}")
        print("❌ FALLÓ EL REPROCESAMIENTO")
        print(f"{'='*60}\n")
    
    sys.exit(0 if exito else 1)
