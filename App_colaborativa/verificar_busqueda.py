#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para verificar que la búsqueda funciona con el nuevo PDF"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'colaborative/scripts'))

from end2end_webapp import buscar

print('🔍 Probando búsqueda en el índice nuevo...')
print('='*60)

try:
    # Prueba búsqueda
    query = 'arbitraje comercial'
    resultados = buscar(query, k=5, base='general')
    print(f'✅ Búsqueda de "{query}": {len(resultados)} resultados')
    
    for i, r in enumerate(resultados):
        fuente = r['fuente']
        score = r.get('score', 0)
        print(f'  {i+1}. [{fuente}] Score: {score:.3f}')
        print(f'     {r["texto"][:80]}...')
    
    # Específicamente buscar por Arbitraje_en_Latam
    arbitraje_results = [r for r in resultados if 'Arbitraje' in r['fuente']]
    print(f'\n✅ Resultados de Arbitraje_en_Latam.pdf: {len(arbitraje_results)}')
    
    if arbitraje_results:
        print('✅ El PDF está siendo encontrado en búsquedas')
    else:
        print('⚠️ No se encontraron resultados del PDF en esta búsqueda')
    
except Exception as e:
    import traceback
    print(f'❌ ERROR: {e}')
    traceback.print_exc()
