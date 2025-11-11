import sqlite3

conn = sqlite3.connect('colaborative/bases_rag/cognitiva/metadatos.db')
cur = conn.cursor()

cur.execute('''
    SELECT autor, total_palabras, formalismo, creatividad, 
           nivel_abstraccion, complejidad_sintactica 
    FROM perfiles_cognitivos 
    ORDER BY autor
''')

print('\n' + '='*90)
print('📊 VERIFICACIÓN FINAL - TODOS LOS PERFILES COGNITIVOS')
print('='*90 + '\n')
print(f"{'Autor':<32} {'Palabras':>10} {'Formal':>7} {'Creativ':>7} {'Abstr':>7} {'Complex':>7}")
print('─'*90)

total_palabras = 0
perfiles_completos = 0
perfiles_incompletos = 0

for a, p, f, c, ab, co in cur.fetchall():
    p = p or 0
    f = f or 0
    c = c or 0
    ab = ab or 0.5
    co = co or 0
    
    total_palabras += p
    
    if p > 0 and f > 0:
        estado = '✅'
        perfiles_completos += 1
    else:
        estado = '⚠️'
        perfiles_incompletos += 1
    
    print(f"{estado} {a:<30} {p:>10,} {f:>6.1%} {c:>6.1%} {ab:>6.1%} {co:>6.1%}")

print('─'*90)
print(f"{'TOTALES':<32} {total_palabras:>10,}")
print('\n' + '='*90)
print(f'✅ Perfiles completos:    {perfiles_completos}/9')
print(f'⚠️  Perfiles incompletos:  {perfiles_incompletos}/9')
print('='*90 + '\n')

conn.close()

def verificar_perfiles():
    """Función para importar desde otros scripts. Retorna número de incompletos."""
    conn = sqlite3.connect('colaborative/bases_rag/cognitiva/metadatos.db')
    cur = conn.cursor()
    
    cur.execute('''
        SELECT COUNT(*) FROM perfiles_cognitivos 
        WHERE formalismo IS NULL OR creatividad IS NULL OR total_palabras IS NULL
    ''')
    
    incompletos = cur.fetchone()[0]
    conn.close()
    
    return incompletos
