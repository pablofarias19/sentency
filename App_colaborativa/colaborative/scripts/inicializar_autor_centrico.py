#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 INICIALIZADOR DEL SISTEMA AUTOR-CÉNTRICO MULTI-CAPA
======================================================

Script unificado que inicializa y prepara todos los sistemas enfocados
en el análisis de PENSAMIENTO AUTORAL:

1. Sistema Autor-Céntrico (metodologías y comparativas)
2. Analizador Multi-Capa (pensamiento profundo)
3. Bases de datos especializadas
4. Migración de datos existentes

ENFOQUE: Centralizar en el AUTOR y su FORMA DE PENSAR

AUTOR: Sistema Cognitivo v5.0 - Inicializador Unificado
FECHA: 9 NOV 2025
"""

import os
import sys
import time
from datetime import datetime

def print_header():
    """Imprime header del sistema"""
    print("=" * 70)
    print("🧠 INICIALIZADOR SISTEMA AUTOR-CÉNTRICO MULTI-CAPA")
    print("=" * 70)
    print("Enfoque: PENSAMIENTO AUTORAL • Metodologías • Meta-Análisis")
    print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 70)

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print("\n🔍 VERIFICANDO DEPENDENCIAS...")
    
    dependencias = [
        'pandas', 'numpy', 'sqlite3', 'plotly', 'networkx',
        'json', 'collections', 're', 'dataclasses'
    ]
    
    dependencias_faltantes = []
    
    for dep in dependencias:
        try:
            if dep == 'sqlite3':
                import sqlite3
            elif dep == 'pandas':
                import pandas
            elif dep == 'numpy':
                import numpy
            elif dep == 'plotly':
                import plotly
            elif dep == 'networkx':
                import networkx
            elif dep == 'json':
                import json
            elif dep == 'collections':
                import collections
            elif dep == 're':
                import re
            elif dep == 'dataclasses':
                from dataclasses import dataclass
            
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep}")
            dependencias_faltantes.append(dep)
    
    if dependencias_faltantes:
        print(f"\n⚠️ DEPENDENCIAS FALTANTES: {', '.join(dependencias_faltantes)}")
        print("Ejecuta: pip install " + " ".join(dependencias_faltantes))
        return False
    
    print("✅ Todas las dependencias están disponibles")
    return True

def inicializar_sistema_autor_centrico():
    """Inicializa el sistema autor-céntrico"""
    print("\n🎯 INICIALIZANDO SISTEMA AUTOR-CÉNTRICO...")
    
    try:
        from sistema_autor_centrico import SistemaAutorCentrico
        
        sistema = SistemaAutorCentrico()
        print("  ✅ Base de datos autor-céntrica creada")
        
        # Migrar datos existentes
        print("  🔄 Migrando datos existentes...")
        sistema.migrar_datos_existentes()
        
        # Generar reporte
        reporte = sistema.generar_reporte_autor_centrico()
        print("  📊 Reporte generado:")
        print("     " + reporte.replace('\n', '\n     '))
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error inicializando sistema autor-céntrico: {e}")
        return False

def inicializar_analizador_multicapa():
    """Inicializa el analizador multi-capa"""
    print("\n🧠 INICIALIZANDO ANALIZADOR MULTI-CAPA...")
    
    try:
        from analizador_multicapa_pensamiento import AnalizadorMultiCapa
        
        analizador = AnalizadorMultiCapa()
        print("  ✅ Base de datos multi-capa creada")
        
        # Obtener autores disponibles para análisis
        import sqlite3
        import pandas as pd
        
        conn = sqlite3.connect(analizador.db_cognitiva)
        autores = pd.read_sql_query("SELECT DISTINCT autor FROM perfiles_cognitivos ORDER BY autor", conn)
        conn.close()
        
        if not autores.empty:
            print(f"  📊 Encontrados {len(autores)} autores para análisis")
            
            # Analizar primeros 3 autores como ejemplo
            for i, row in autores.head(3).iterrows():
                autor = row['autor']
                print(f"  🔬 Analizando: {autor[:30]}...")
                
                perfil = analizador.analizar_autor_multicapa(autor)
                
                if perfil:
                    print(f"     ✅ Completado - Patrón: {perfil.firma_intelectual.get('patron_dominante', 'N/A')}")
                else:
                    print(f"     ⚠️ No se pudo analizar")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error inicializando analizador multi-capa: {e}")
        return False

def verificar_integracion_webapp():
    """Verifica que la integración con webapp esté correcta"""
    print("\n🌐 VERIFICANDO INTEGRACIÓN WEBAPP...")
    
    try:
        # Verificar imports en webapp
        with open('end2end_webapp.py', 'r', encoding='utf-8') as f:
            contenido_webapp = f.read()
        
        # Verificar que estén los imports necesarios
        if 'from sistema_autor_centrico import' in contenido_webapp:
            print("  ✅ Import sistema autor-céntrico encontrado")
        else:
            print("  ⚠️ Import sistema autor-céntrico no encontrado")
        
        if 'from analizador_multicapa_pensamiento import' in contenido_webapp:
            print("  ✅ Import analizador multi-capa encontrado")
        else:
            print("  ⚠️ Import analizador multi-capa no encontrado")
        
        # Verificar rutas
        if '@app.route(\'/autores\'' in contenido_webapp:
            print("  ✅ Ruta /autores encontrada")
        else:
            print("  ⚠️ Ruta /autores no encontrada")
        
        if '@app.route(\'/pensamiento\'' in contenido_webapp:
            print("  ✅ Ruta /pensamiento encontrada")
        else:
            print("  ⚠️ Ruta /pensamiento no encontrada")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error verificando integración: {e}")
        return False

def generar_documentacion():
    """Genera documentación del sistema"""
    print("\n📚 GENERANDO DOCUMENTACIÓN...")
    
    documentacion = f"""
# 🧠 SISTEMA AUTOR-CÉNTRICO MULTI-CAPA
## Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## 🎯 OBJETIVOS DEL SISTEMA

### ENFOQUE PRINCIPAL
- **PENSAMIENTO AUTORAL**: Análisis del CÓMO PIENSA el autor
- **META-ANÁLISIS**: Capas profundas de análisis cognitivo  
- **COMPARATIVAS**: Metodologías y firmas intelectuales
- **EVOLUCIÓN**: Cambios temporales en el pensamiento

### ARQUITECTURA DEL SISTEMA

#### 1. SISTEMA AUTOR-CÉNTRICO (/autores)
- Base de datos: `autor_centrico.db`
- Enfoque: Metodologías, similitudes, comparativas
- Visualizaciones: Mapas 3D, redes de influencia
- Funciones: Migración, comparativas, dashboard

#### 2. ANALIZADOR MULTI-CAPA (/pensamiento)  
- Base de datos: `multicapa_pensamiento.db`
- Enfoque: 5 capas de análisis de pensamiento
- Visualizaciones: Mapas cognitivos, arquitectura argumentativa
- Funciones: Análisis profundo, evolución temporal

### CAPAS DE ANÁLISIS

1. **CAPA SEMÁNTICA**: Base de contenido existente
2. **CAPA COGNITIVA**: Patrones de razonamiento  
3. **CAPA METODOLÓGICA**: Estructura argumentativa
4. **CAPA EVOLUTIVA**: Cambios temporales
5. **CAPA RELACIONAL**: Redes de influencia

### RUTAS WEBAPP DISPONIBLES

- `/` - Sistema principal RAG
- `/cognitivo` - Sistema ANALYSER
- `/radar` - Radar cognitivo 
- `/autores` - Sistema autor-céntrico (NUEVO)
- `/pensamiento` - Análisis multi-capa (NUEVO)
- `/perfiles` - Perfiles PCA
- `/autoevaluaciones` - Sistema de aprendizaje

### FLUJO DE USO

1. **PREPARACIÓN**:
   - Ejecutar: `python inicializar_autor_centrico.py`
   - Verificar migración de datos

2. **ANÁLISIS AUTOR-CÉNTRICO**:
   - Ir a `/autores`
   - Migrar datos si es necesario
   - Generar visualizaciones comparativas

3. **ANÁLISIS MULTI-CAPA**:
   - Ir a `/pensamiento` 
   - Seleccionar autor
   - Ejecutar análisis profundo
   - Generar dashboard completo

### ARCHIVOS PRINCIPALES

- `sistema_autor_centrico.py` - Sistema autor-céntrico
- `visualizador_autor_centrico.py` - Visualizaciones autor-céntricas  
- `analizador_multicapa_pensamiento.py` - Analizador multi-capa
- `visualizador_pensamiento_multicapa.py` - Visualizaciones multi-capa
- `inicializar_autor_centrico.py` - Este inicializador
- `end2end_webapp.py` - Webapp integrada

### BASES DE DATOS

- `autor_centrico.db`:
  - `perfiles_autorales_expandidos`
  - `comparativas_autorales`
  - `redes_influencia`
  - `escuelas_pensamiento`

- `multicapa_pensamiento.db`:
  - `analisis_multicapa`
  - `redes_conceptuales`
  - `firmas_intelectuales`
  - `evolucion_pensamiento`

### PRÓXIMOS PASOS

1. Probar sistema en webapp
2. Analizar más autores
3. Generar comparativas
4. Crear reportes avanzados
5. Implementar mejoras basadas en uso

---
🎉 **SISTEMA AUTOR-CÉNTRICO MULTI-CAPA LISTO PARA USO**
    """
    
    try:
        with open('DOCUMENTACION_AUTOR_CENTRICO.md', 'w', encoding='utf-8') as f:
            f.write(documentacion)
        print("  ✅ Documentación guardada en: DOCUMENTACION_AUTOR_CENTRICO.md")
        return True
    except Exception as e:
        print(f"  ❌ Error generando documentación: {e}")
        return False

def main():
    """Función principal del inicializador"""
    print_header()
    
    # Cambiar al directorio de scripts
    if not os.path.basename(os.getcwd()) == 'scripts':
        if os.path.exists('colaborative/scripts'):
            os.chdir('colaborative/scripts')
            print("📁 Cambiado al directorio de scripts")
        else:
            print("⚠️ No se encontró el directorio de scripts")
    
    # Pasos de inicialización
    pasos = [
        ("Verificación de dependencias", verificar_dependencias),
        ("Sistema autor-céntrico", inicializar_sistema_autor_centrico),
        ("Analizador multi-capa", inicializar_analizador_multicapa),
        ("Integración webapp", verificar_integracion_webapp),
        ("Documentación", generar_documentacion)
    ]
    
    resultados = []
    
    for nombre, funcion in pasos:
        print(f"\n{'='*50}")
        print(f"🔄 EJECUTANDO: {nombre.upper()}")
        print(f"{'='*50}")
        
        inicio = time.time()
        exito = funcion()
        duracion = time.time() - inicio
        
        resultados.append((nombre, exito, duracion))
        
        if exito:
            print(f"✅ {nombre} completado en {duracion:.2f}s")
        else:
            print(f"❌ {nombre} falló después de {duracion:.2f}s")
    
    # Resumen final
    print(f"\n{'='*70}")
    print("📊 RESUMEN DE INICIALIZACIÓN")
    print(f"{'='*70}")
    
    exitosos = sum(1 for _, exito, _ in resultados if exito)
    total = len(resultados)
    
    for nombre, exito, duracion in resultados:
        estado = "✅" if exito else "❌"
        print(f"{estado} {nombre:<30} ({duracion:.2f}s)")
    
    print(f"\n🎯 RESULTADO: {exitosos}/{total} pasos completados exitosamente")
    
    if exitosos == total:
        print("\n🎉 ¡SISTEMA AUTOR-CÉNTRICO MULTI-CAPA INICIALIZADO CORRECTAMENTE!")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Ejecutar webapp: python end2end_webapp.py")  
        print("2. Ir a: http://127.0.0.1:5002/autores")
        print("3. Ir a: http://127.0.0.1:5002/pensamiento")
        print("4. Probar análisis de autores")
    else:
        print("\n⚠️ Algunos pasos fallaron. Revisa los errores arriba.")
    
    print(f"\n📚 Documentación completa en: DOCUMENTACION_AUTOR_CENTRICO.md")
    print("=" * 70)

if __name__ == "__main__":
    main()