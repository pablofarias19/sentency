#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🎯 SCRIPT DEFINITIVO: Agregar Jesús Alberto Aybar como nuevo autor
Extrae el PDF de Arbitraje_en_Latam y lo agrega a la BD de autores
"""

import sys
import sqlite3
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / 'colaborative/scripts'))

def extraer_contenido_pdf():
    """Extrae texto del PDF"""
    try:
        import fitz
        pdf_path = Path("colaborative/data/pdfs/general/Arbitraje_en_Latam.pdf")
        
        if not pdf_path.exists():
            print(f"❌ PDF no encontrado: {pdf_path}")
            return None
        
        doc = fitz.open(str(pdf_path))
        texto = ""
        for page in doc:
            texto += page.get_text()
        doc.close()
        
        print(f"✅ PDF extraído: {len(texto):,} caracteres")
        return texto
        
    except Exception as e:
        print(f"❌ Error extrayendo PDF: {e}")
        return None

def analizar_con_orchestrador(texto):
    """Ejecuta análisis cognitivo con orchestrador"""
    try:
        from orchestrador_maestro_integrado import OrchestadorMaestroIntegrado
        
        print("\n🧠 Inicializando ORCHESTRADOR MAESTRO...")
        orch = OrchestadorMaestroIntegrado()
        
        print("📊 Ejecutando análisis cognitivo...")
        perfil = orch.analizar_documento_completo(
            texto=texto,
            autor="Jesús Alberto Aybar",
            fuente="Arbitraje_en_Latam.pdf"
        )
        
        print(f"✅ Análisis completado")
        return perfil
        
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        import traceback
        traceback.print_exc()
        return None

def insertar_en_bd_autorales(perfil):
    """Inserta perfil en la BD de autores (autor_centrico.db)"""
    try:
        db_path = Path("colaborative/bases_rag/cognitiva/autor_centrico.db")
        
        if not db_path.exists():
            print(f"❌ BD no encontrada: {db_path}")
            return False
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Extraer datos del perfil
        autor = perfil.get('autor', 'Jesús Alberto Aybar')
        fuente = perfil.get('fuente', 'Arbitraje_en_Latam.pdf')
        
        # Crear fila para inserción
        insert_data = {
            'autor': autor,
            'fuente': fuente,
            'razonamiento_dominante': perfil.get('razonamiento_dominante', 'mixto'),
            'modalidad_epistemica': perfil.get('modalidad_epistemica', 'dialéctico'),
            'estilo_dominante': perfil.get('estilo_dominante', 'técnico-jurídico'),
            'perfil_completo': json.dumps(perfil),
            'timestamp': datetime.now().isoformat(),
        }
        
        # Intentar inserción
        try:
            cursor.execute("""
                INSERT INTO perfiles_autorales_expandidos 
                (autor, fuente, razonamiento_dominante, modalidad_epistemica, 
                 estilo_dominante, perfil_completo, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                insert_data['autor'],
                insert_data['fuente'],
                insert_data['razonamiento_dominante'],
                insert_data['modalidad_epistemica'],
                insert_data['estilo_dominante'],
                insert_data['perfil_completo'],
                insert_data['timestamp']
            ))
            conn.commit()
            print(f"✅ {autor} insertado en perfiles_autorales_expandidos")
            
        except sqlite3.OperationalError as e:
            print(f"⚠️ Error con tabla perfiles_autorales_expandidos: {e}")
            print("   Intentando insertar de forma alternativa...")
            
            # Obtener esquema de la tabla
            cursor.execute("PRAGMA table_info(perfiles_autorales_expandidos)")
            columnas = cursor.fetchall()
            col_names = [c[1] for c in columnas]
            
            # Construir INSERT dinámico
            cols_disponibles = []
            valores = []
            for k, v in insert_data.items():
                if k in col_names:
                    cols_disponibles.append(k)
                    valores.append(v)
            
            if cols_disponibles:
                placeholders = ','.join(['?'] * len(cols_disponibles))
                sql = f"INSERT INTO perfiles_autorales_expandidos ({','.join(cols_disponibles)}) VALUES ({placeholders})"
                cursor.execute(sql, valores)
                conn.commit()
                print(f"✅ Inserción alternativa exitosa")
            else:
                print(f"❌ No hay columnas compatibles")
                conn.close()
                return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error insertando en BD: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*70)
    print("🎯 AGREGAR NUEVO AUTOR AL SISTEMA")
    print("="*70)
    
    # PASO 1: Extraer PDF
    print("\n📄 PASO 1: Extrayendo contenido del PDF...")
    texto = extraer_contenido_pdf()
    if not texto:
        return False
    
    # PASO 2: Analizar
    print("\n🧠 PASO 2: Ejecutando análisis cognitivo...")
    perfil = analizar_con_orchestrador(texto)
    if not perfil:
        return False
    
    # PASO 3: Insertar en BD
    print("\n💾 PASO 3: Guardando en base de datos de autores...")
    success = insertar_en_bd_autorales(perfil)
    
    if success:
        print("\n" + "="*70)
        print("✅ NUEVO AUTOR AGREGADO EXITOSAMENTE")
        print("="*70)
        print(f"\n👤 Autor: Jesús Alberto Aybar")
        print(f"📄 Fuente: Arbitraje_en_Latam.pdf")
        print(f"🧠 Razonamiento: {perfil.get('razonamiento_dominante', 'N/A')}")
        print(f"📊 Modalidad: {perfil.get('modalidad_epistemica', 'N/A')}")
        print(f"✍️  Estilo: {perfil.get('estilo_dominante', 'N/A')}")
        
        print("\n🚀 PRÓXIMOS PASOS:")
        print("1. Inicia la webapp: python colaborative/scripts/end2end_webapp.py")
        print("2. Abre: http://127.0.0.1:5002/autores")
        print("3. Ahora verás 5 autores (incluido Jesús Alberto Aybar)")
        
        return True
    else:
        print("\n❌ Error al guardar en BD")
        return False

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
