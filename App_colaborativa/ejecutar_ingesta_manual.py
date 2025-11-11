#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para ingestar manualmente el PDF de Arbitraje_en_Latam"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'colaborative/scripts'))

from end2end_webapp import procesar_documentos, crear_indice_vectorial

def main():
    print('🔄 Iniciando ingesta del PDF...')
    print('='*60)
    
    try:
        base = 'general'
        print(f'📂 Base: {base}')
        
        # Procesa los documentos
        docs = procesar_documentos(base)
        print(f'✅ Documentos procesados: {len(docs)} chunks totales')
        
        # Filtra chunks de Arbitraje_en_Latam
        arbitraje_docs = [d for d in docs if 'Arbitraje' in d['fuente']]
        print(f'✅ Chunks de Arbitraje_en_Latam.pdf: {len(arbitraje_docs)}')
        
        if arbitraje_docs:
            print(f'   Primeros 100 caracteres del primer chunk:')
            print(f'   {arbitraje_docs[0]["texto"][:100]}...')
        
        # Crea índice FAISS
        print(f'\n🔨 Creando índice FAISS...')
        crear_indice_vectorial(base)
        print(f'✅ Índice FAISS creado exitosamente')
        
        # Verifica que se guardó
        chunks_file = Path(f'colaborative/data/chunks/{base}/chunks.txt')
        if chunks_file.exists():
            with open(chunks_file, 'r', encoding='utf-8') as f:
                content = f.read()
                count = content.count('Arbitraje_en_Latam.pdf')
                print(f'✅ Arbitraje_en_Latam.pdf aparece {count} veces en chunks.txt')
        
        print(f'\n✅ INGESTA COMPLETADA EXITOSAMENTE')
        return True
        
    except Exception as e:
        import traceback
        print(f'❌ ERROR: {e}')
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
