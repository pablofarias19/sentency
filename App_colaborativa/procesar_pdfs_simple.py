"""
Script simple para procesar PDFs nuevos sin dependencias complejas
"""
import sys
import os
from pathlib import Path

# Agregar rutas necesarias
sys.path.insert(0, str(Path(__file__).parent / 'colaborative' / 'scripts'))

try:
    from ingesta_cognitiva import GestorIngesta
    
    print("="*70)
    print("📄 PROCESADOR SIMPLE DE DOCUMENTOS NUEVOS")
    print("="*70)
    
    # Inicializar gestor
    print("\n🔧 Inicializando gestor de ingesta...")
    gestor = GestorIngesta()
    
    # Obtener PDFs en carpeta
    pdf_dir = Path("colaborative/data/pdfs/general")
    pdfs_carpeta = list(pdf_dir.glob("*.pdf"))
    print(f"\n📚 PDFs encontrados: {len(pdfs_carpeta)}")
    
    # Procesar cada PDF
    for pdf_path in pdfs_carpeta:
        print(f"\n📄 Procesando: {pdf_path.name}")
        try:
            gestor.procesar_documento(str(pdf_path))
            print(f"  ✅ Completado")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n" + "="*70)
    print("✅ PROCESAMIENTO COMPLETADO")
    print("="*70)
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\nIntentando método alternativo...")
    
    # Método alternativo sin GestorIngesta
    print("\n📝 Usando procesamiento básico...")
    
    import sqlite3
    import fitz  # PyMuPDF
    from sentence_transformers import SentenceTransformer
    
    # Conectar a BD
    db_path = "colaborative/bases_rag/cognitiva/metadatos.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Verificar PDFs ya procesados
    c.execute("SELECT archivo FROM perfiles_cognitivos")
    procesados = {Path(r[0]).name for r in c.fetchall()}
    
    # Obtener PDFs nuevos
    pdf_dir = Path("colaborative/data/pdfs/general")
    pdfs_nuevos = [p for p in pdf_dir.glob("*.pdf") if p.name not in procesados]
    
    print(f"\n📚 PDFs nuevos para procesar: {len(pdfs_nuevos)}")
    
    if pdfs_nuevos:
        print("\n⚠️ Se encontraron PDFs nuevos pero falta configuración completa.")
        print("PDFs detectados:")
        for pdf in pdfs_nuevos:
            print(f"   - {pdf.name}")
        
        print("\n💡 Soluciones:")
        print("   1. Ejecutar desde la web: Ir a /cognitivo y usar botón 'Procesar Documentos'")
        print("   2. Usar script batch: .\\PROCESAR_DOCUMENTOS.bat")
        print("   3. Contactar soporte técnico")
    else:
        print("\n✅ Todos los PDFs ya están procesados")
    
    conn.close()
