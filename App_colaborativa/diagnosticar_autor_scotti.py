import sys
import sqlite3

sys.path.insert(0, 'colaborative/scripts')
from config_rutas import PENSAMIENTO_DB

conn = sqlite3.connect(PENSAMIENTO_DB)
cur = conn.cursor()

print("\n" + "="*70)
print("🔍 DIAGNÓSTICO: Luciana B. Scotti")
print("="*70 + "\n")

# Buscar registros con diferentes variaciones del nombre
variaciones = [
    'Luciana B. Scotti',
    'Luciana Scotti',
    'L. Scotti',
    'Scotti'
]

print("📋 Buscando variaciones del nombre...")
print("-" * 70)

for nombre in variaciones:
    cur.execute("SELECT COUNT(*) FROM perfiles_integrados_v2 WHERE autor LIKE ?", (f'%{nombre}%',))
    count = cur.fetchone()[0]
    print(f"'{nombre}': {count} registros")

# Buscar exactamente "Luciana B. Scotti"
print("\n📋 Datos específicos de 'Luciana B. Scotti'")
print("-" * 70)

cur.execute("SELECT COUNT(*) FROM perfiles_integrados_v2 WHERE autor = ?", ('Luciana B. Scotti',))
count = cur.fetchone()[0]
print(f"Registros totales: {count}")

if count > 0:
    cur.execute("""
        SELECT archivo, num_paginas, titulo_encontrado, timestamp_creacion 
        FROM perfiles_integrados_v2 
        WHERE autor = ?
    """, ('Luciana B. Scotti',))
    
    rows = cur.fetchall()
    print(f"\n📄 Documentos encontrados:")
    for i, row in enumerate(rows, 1):
        print(f"\n  {i}. Archivo: {row[0]}")
        print(f"     Páginas: {row[1]}")
        print(f"     Título: {row[2]}")
        print(f"     Fecha: {row[3]}")
    
    # Verificar campos críticos
    print("\n📊 Verificando campos críticos del primer registro...")
    cur.execute("""
        SELECT 
            formalismo, creatividad, empirismo, abstraccion,
            normativas, conceptuales, falacias,
            total_palabras, json_completo
        FROM perfiles_integrados_v2 
        WHERE autor = ?
        LIMIT 1
    """, ('Luciana B. Scotti',))
    
    row = cur.fetchone()
    if row:
        print(f"  Formalismo: {row[0]}")
        print(f"  Creatividad: {row[1]}")
        print(f"  Empirismo: {row[2]}")
        print(f"  Abstracción: {row[3]}")
        print(f"  Normativas: {row[4]}")
        print(f"  Conceptuales: {row[5]}")
        print(f"  Falacias: {row[6]}")
        print(f"  Total palabras: {row[7]}")
        print(f"  Rasgos JSON: {'✅ Presente' if row[8] else '❌ NULL'}")
        
        # Verificar si hay NULL en campos críticos
        nulls = []
        if row[0] is None: nulls.append('formalismo')
        if row[1] is None: nulls.append('creatividad')
        if row[2] is None: nulls.append('empirismo')
        if row[3] is None: nulls.append('abstraccion')
        if row[8] is None: nulls.append('rasgos_json')
        
        if nulls:
            print(f"\n⚠️ CAMPOS NULL DETECTADOS: {', '.join(nulls)}")
        else:
            print(f"\n✅ Todos los campos críticos tienen datos")
    
    # Verificar si json_completo tiene fragmentos
    print("\n📝 Verificando datos JSON completos...")
    cur.execute("""
        SELECT json_completo 
        FROM perfiles_integrados_v2 
        WHERE autor = ? 
        LIMIT 1
    """, ('Luciana B. Scotti',))
    
    json_row = cur.fetchone()
    if json_row and json_row[0]:
        import json
        try:
            data = json.loads(json_row[0])
            fragmentos = data.get('fragmentos_textuales', [])
            print(f"  Fragmentos en JSON: {len(fragmentos)}")
            if len(fragmentos) > 0:
                print(f"  ✅ Ejemplo: {fragmentos[0][:100]}...")
            else:
                print("  ⚠️ NO hay fragmentos textuales")
        except:
            print("  ⚠️ Error parseando JSON")
    else:
        print("  ❌ JSON completo está vacío o NULL")

else:
    print("\n❌ NO SE ENCONTRARON DATOS")
    print("\n💡 Verificando autores similares...")
    cur.execute("""
        SELECT DISTINCT autor 
        FROM perfiles_integrados_v2 
        WHERE autor LIKE '%Scotti%'
    """)
    similares = cur.fetchall()
    if similares:
        print("  Autores con 'Scotti' en el nombre:")
        for autor in similares:
            print(f"    • {autor[0]}")
    
    # Listar todos los autores disponibles
    print("\n💡 Listando primeros 10 autores en la base:")
    cur.execute("SELECT DISTINCT autor FROM perfiles_integrados_v2 LIMIT 10")
    autores = cur.fetchall()
    for autor in autores:
        print(f"    • {autor[0]}")

conn.close()

print("\n" + "="*70)
print("FIN DEL DIAGNÓSTICO")
print("="*70 + "\n")
