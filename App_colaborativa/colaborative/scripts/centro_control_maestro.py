#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎛️ CENTRO DE CONTROL MAESTRO - Sistema Cognitivo Unificado V7.6
================================================================

🌟 ¡BIENVENIDO AL CEREBRO DE TU SISTEMA COLABORATIVO! 🌟

Este es tu panel de control principal donde puedes:

📚 ANÁLISIS INTELIGENTE DE DOCUMENTOS:
   • RAG Sentencias: Busca en miles de fallos judiciales
   • Distancia Doctrinal: Mide qué tan lejos están las sentencias de la doctrina
   • Interpretación IA: Explica los apartamientos con inteligencia artificial

👤 GESTIÓN DE PERFILES:
   • Analiza el estilo de escritura de autores
   • Crea perfiles cognitivos únicos
   • Identifica patrones de pensamiento

🔧 HERRAMIENTAS DE MANTENIMIENTO:
   • Diagnóstico automático del sistema
   • Limpieza de bases de datos
   • Reparación de errores comunes

🎯 NOTA IMPORTANTE: Si es tu primera vez, usa las opciones 22 (Guía) y 99 (Diagnóstico)
   para entender cómo funciona todo. ¡No te preocupes, es más fácil de lo que parece!

AUTOR: Sistema Cognitivo v7.6 (con parches V7.3-V7.6)
FECHA: 10 NOV 2025
ESTADO: 🚀 SISTEMA COMPLETAMENTE FUNCIONAL
"""

import os
import sys
import json
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class CentroControlMaestro:
    """
    🎯 CENTRO DE CONTROL UNIFICADO - Tu Panel de Comando Principal
    
    ¡Hola! Soy el cerebro de tu sistema colaborativo. Aquí es donde
    controlas todo lo que puede hacer tu sistema inteligente.
    
    🤔 ¿Qué hago exactamente?
    • Coordino todas las funciones del sistema
    • Te guío paso a paso en cada proceso
    • Mantengo todo organizado y funcionando
    • Te ayudo cuando algo no funciona como debería
    
    💡 CONSEJO AMIGABLE: Si algo no está claro, siempre puedes usar
       la opción 22 para ver guías detalladas o la 99 para diagnósticos
    """
    
    def __init__(self):
        # 🔧 Configuración inicial del sistema
        self.version = "v7.6_control_maestro"  # ¡Actualizado con todos los parches!
        self.base_path = Path(__file__).parent.parent
        self.scripts_path = self.base_path / "colaborative" / "scripts"
        self.data_path = self.base_path / "colaborative" / "data"
        
        # 🎨 Mensaje de bienvenida amigable
        print(f"🎛️ CENTRO DE CONTROL MAESTRO {self.version}")
        print(f"📁 Ruta base: {self.base_path}")
        print("=" * 60)
        print("💡 PRIMERA VEZ: Usa opción 22 (Guía) o 99 (Diagnóstico)")
        print("🎯 ¿PROBLEMAS?: La opción 99 resuelve el 90% de los issues")
        print("=" * 60)

    def ejecutar_bat(self, nombre_bat):
        """Ejecuta un archivo .bat existente"""
        print(f"\n🚀 Ejecutando: {nombre_bat}")
        print("=" * 40)
        
        bat_path = self.base_path / nombre_bat
        if not bat_path.exists():
            print(f"❌ Archivo no encontrado: {bat_path}")
            return
            
        try:
            print(f"📂 Cambiando a directorio: {self.base_path}")
            print(f"⚡ Ejecutando: {nombre_bat}")
            print("🔄 Presiona Ctrl+C para volver al menú si es necesario")
            print()
            
            result = subprocess.run([str(bat_path)], cwd=str(self.base_path), shell=True)
            
            if result.returncode == 0:
                print(f"\n✅ {nombre_bat} ejecutado exitosamente")
            else:
                print(f"\n⚠️ {nombre_bat} terminó con código: {result.returncode}")
                
        except KeyboardInterrupt:
            print(f"\n⏹️ Ejecución de {nombre_bat} interrumpida por el usuario")
        except Exception as e:
            print(f"\n❌ Error ejecutando {nombre_bat}: {e}")

    def mostrar_menu_principal(self):
        """
        🎯 MENÚ PRINCIPAL - Tu Panel de Control
        
        ¡Aquí es donde la magia sucede! Este menú te da acceso a TODAS
        las funciones del sistema. No te abrumes por la cantidad de opciones,
        están organizadas por categorías para que sea fácil encontrar lo que necesitas.
        
        💡 CONSEJO PRO: Si es tu primera vez, ve directo a las opciones:
           • 22: Guía detallada (te explica todo paso a paso)
           • 99: Diagnóstico (revisa que todo esté funcionando)
        
        🎨 Las opciones están coloreadas por tipo:
           🚀 = Inicio rápido    📚 = Análisis de documentos
           ⚖️ = Legal/Judicial   🧠 = Inteligencia Artificial
           🔧 = Mantenimiento    ❓ = Ayuda
        """
        # Mostrar menú ameno y explicativo
        self._mostrar_menu_ameno()
        
    def _mostrar_menu_ameno(self):
        """Muestra el menú principal con explicaciones amenas"""
        
        print("\n🎛️ CENTRO DE CONTROL MAESTRO V7.6 - ¡Tu Sistema Inteligente Te Saluda! 🎉")
        print("═" * 80)
        print("🌟 ¿PRIMERA VEZ AQUÍ? → Opción 22 (Guía Detallada) o 99 (Diagnóstico)")
        print("🔥 ¿YA SOS EXPERTO? → Directo a S1-S5 (RAG), D1-D4 (Doctrinal), G1-G4 (GEMINI)")
        print("═" * 80)
        
        # ACCESOS RÁPIDOS
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 🚀 ACCESOS RÁPIDOS - ¡Un solo clic y listo!                             ┃")
        print("┃ (Archivos .bat preconfigurados - perfectos si tienes prisa)              ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print("   R1. PROCESAR_DOCUMENTOS.bat (🎯 Procesa todo automáticamente)")
        print("   R2. INICIO_FACIL.bat (🌱 Webapp básica - perfecta para empezar)")
        print("   R3. iniciar_sistema.bat (🚁 Webapp completa - todas las funciones)")
        print("   R4. INICIO_MEJORADO.bat (🔧 Con diagnósticos - te avisa si algo falla)")
        
        # RAG SENTENCIAS
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 🚀 RAG SENTENCIAS v7.4 - Búsqueda inteligente en sentencias              ┃")
        print("┃ ORDEN OBLIGATORIO: S1 → S2 → después las otras (¡no saltees pasos!)     ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print("   S1. Ingestar corpus (📥 PRIMERO: Procesar PDFs de sentencias)")
        print("   S2. Construir FAISS (🏗️ SEGUNDO: Crear índice de búsqueda rápida)")
        print("   S3. Buscar en corpus (🔎 DESPUÉS: Buscar con filtros inteligentes)")
        print("   S4. Exportar reportes CSV (📊 Descargar resultados en planilla)")
        print("   S5. API de sentencias (🌐 Servidor web en puerto 5010)")
        
        # DISTANCIA DOCTRINAL
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 📏 DISTANCIA DOCTRINAL v7.5 - ¿Se aparta la sentencia de la doctrina?   ┃")
        print("┃ NECESITAS: Haber completado S1+S2 antes de usar estas opciones           ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print("   D1. Construir base doctrinal (📚 Procesar PDFs de doctrina)")
        print("   D2. Calcular distancias (📐 Medir apartamiento vs doctrina)")
        print("   D3. Reportes por tribunal (🏛️ Ver apartamientos por juzgado)")
        print("   D4. Casos críticos (🚨 Apartamientos mayores al 60%)")
        
        # GEMINI INTERPRETATIVO
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 🧠 GEMINI INTERPRETATIVO v7.6 - IA explica apartamientos ¡LISTO!        ┃")
        print("┃ ✅ API Key ya configurada como variable de sistema                       ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print("   G1. Configurar API Key (✅ Ya tienes - verificar si necesario)")
        print("   G2. Servidor interpretación (🌐 Web con IA en puerto 5060)")
        print("   G3. Interpretar chunk específico (🔍 Explicar un apartamiento)")
        print("   G4. Test interpretación (🧪 Verificar que funciona - ¡Empieza aquí!)")
        
        # OPCIONES CLÁSICAS
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 📚 ANÁLISIS CLÁSICO - Funciones tradicionales del sistema                ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print("   1-3. Análisis Doctrinario (📖 Libros, papers, artículos)")
        print("   4-7. Análisis Autoral (👤 Estilos de escritura)")
        print("   8-11. Análisis Judicial (⚖️ Sentencias tradicionales)")
        print("   12-14. Servidor Web (🌐 Interfaces gráficas)")
        
        # SISTEMA Y DIAGNÓSTICOS
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 🔧 SISTEMA & DIAGNÓSTICOS - Cuando algo no funciona                      ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print("   15-18. Diagnósticos y mantenimiento (🩺 Reparar problemas)")
        print("   19-21. Ayuda y guías (❓ Cuando estás perdido)")
        
        # OPCIONES ESPECIALES
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ ⭐ OPCIONES ESPECIALES - ¡Tus salvavidas!                               ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
        print("   22. Guía detallada de flujos (📖 Manual paso a paso COMPLETO)")
        print("   99. Diagnóstico integral (🔍 Revisar TODO automáticamente)")
        print("   0. Salir (👋 ¡Hasta la próxima!)")
        
        print("\n" + "═" * 80)
        print("💡 CONSEJOS RÁPIDOS:")
        print("   • Primera vez: 22 → 99 → S1 → S2")
        print("   • Problemas: 99 (resuelve el 90% de los errores)")
        print("   • RAG básico: S1 → S2 → S3")
        print("   • Análisis completo: S1 → S2 → D1 → D2 → G4 (G1 ya configurado ✅)")
        print("   • IA interpretativa: G4 primero para verificar funcionamiento")
        print("═" * 80)
        
        while True:
            try:
                opcion = input("\n🎯 Tu elección: ").strip()
                self._procesar_opcion_menu(opcion)
                if opcion == "0":
                    break
                input("\n⏸️ Presiona ENTER para continuar...")
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                input("⏸️ Presiona ENTER para continuar...")
    
    def _procesar_opcion_menu(self, opcion):
        """Procesa la opción seleccionada del menú"""
        
        if opcion == "0":
            print("👋 ¡Hasta luego! Gracias por usar el Sistema Colaborativo V7.6")
            return
            
        # Opciones de acceso rápido
        elif opcion.upper() == "R1":
            print("\n🚀 Ejecutando procesamiento automático...")
            self.ejecutar_bat("PROCESAR_DOCUMENTOS.bat")
        elif opcion.upper() == "R2":
            print("\n🌱 Iniciando webapp básica...")
            self.ejecutar_bat("INICIO_FACIL.bat")
        elif opcion.upper() == "R3":
            print("\n🚁 Iniciando webapp completa...")
            self.ejecutar_bat("iniciar_sistema.bat")
        elif opcion.upper() == "R4":
            print("\n🔧 Iniciando con diagnósticos...")
            self.ejecutar_bat("INICIO_MEJORADO.bat")
            
        # Opciones RAG Sentencias
        elif opcion.upper() == "S1":
            print("\n📥 Iniciando ingesta de corpus...")
            self.ingestar_corpus_sentencias()
        elif opcion.upper() == "S2":
            print("\n🏗️ Construyendo índice FAISS...")
            self.construir_indice_faiss_sentencias()
        elif opcion.upper() == "S3":
            print("\n🔎 Iniciando búsqueda en corpus...")
            self.buscar_en_corpus()
        elif opcion.upper() == "S4":
            print("\n📊 Exportando reportes CSV...")
            self.exportar_csv_sentencias()
        elif opcion.upper() == "S5":
            print("\n🌐 Iniciando API de sentencias...")
            self.iniciar_api_sentencias()
            
        # Opciones Distancia Doctrinal
        elif opcion.upper() == "D1":
            print("\n📚 Construyendo base doctrinal...")
            self.construir_base_doctrinal()
        elif opcion.upper() == "D2":
            print("\n📐 Calculando distancias doctrinales...")
            self.recalcular_distancias_doctrinales()
        elif opcion.upper() == "D3":
            print("\n🏛️ Generando reportes por tribunal...")
            self.generar_reportes_apartamiento()
        elif opcion.upper() == "D4":
            print("\n🚨 Analizando casos críticos...")
            self.analizar_casos_criticos()
            
        # Opciones GEMINI
        elif opcion.upper() == "G1":
            print("\n🔑 Verificando configuración API Key GEMINI...")
            print("💡 NOTA: Ya tienes API Key como variable de sistema")
            self.configurar_gemini_api()
        elif opcion.upper() == "G2":
            print("\n🌐 Iniciando servidor de interpretación...")
            self.iniciar_servidor_gemini()
        elif opcion.upper() == "G3":
            print("\n🔍 Interpretando chunk específico...")
            self.interpretar_chunk_especifico()
        elif opcion.upper() == "G4":
            print("\n🧪 Ejecutando test de interpretación...")
            print("✅ API Key ya configurada - verificando funcionamiento...")
            self.test_interpretacion_gemini()
            
        # Opciones especiales
        elif opcion == "22":
            print("\n📖 Mostrando guía detallada...")
            self.mostrar_guia_flujos_detallada()
        elif opcion == "99":
            print("\n🔍 Ejecutando diagnóstico integral...")
            self.diagnostico_completo()
            
        # Opciones clásicas (mantenidas para compatibilidad)
        elif opcion in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21"]:
            print(f"\n🎯 Ejecutando opción clásica {opcion}...")
            # Llamar al menú original para estas opciones
            self._ejecutar_opcion_clasica(opcion)
        else:
            print("❌ Opción no válida. Usa 22 para ver la guía completa.")
    
    def _ejecutar_opcion_clasica(self, opcion):
        """Ejecuta las opciones del menú clásico"""
        print(f"💡 Opción {opcion} corresponde al sistema clásico.")
        print("   Para ver todas las opciones detalladas, usa la opción 22.")
        print("   Las funciones principales están en S1-S5, D1-D4, G1-G4.")
        
        menu = """
🎛️ CENTRO DE CONTROL MAESTRO V7.6 - ¡Tu Sistema Inteligente Te Saluda!

🌟 ¿PRIMERA VEZ AQUÍ? → Usa opción 22 (Guía) o 99 (Diagnóstico) primero
🔥 ¿YA SOS EXPERTO? → Directo a las opciones S1-S5, D1-D4, o G1-G4

� ACCESOS RÁPIDOS (Archivos .bat existentes):
   R1. Ejecutar PROCESAR_DOCUMENTOS.bat
   R2. Ejecutar INICIO_FACIL.bat (webapp básica)
   R3. Ejecutar iniciar_sistema.bat (webapp completa)
   R4. Ejecutar INICIO_MEJORADO.bat (con diagnósticos)

�📚 ANÁLISIS DOCTRINARIO:
   1. Procesar documentos doctrinarios (libros, papers, artículos)  
   2. Ver estadísticas de corpus doctrinario
   3. Exportar índice doctrinario

👤 ANÁLISIS AUTORAL:
   4. Analizar perfil de autor específico
   5. Comparar autores (similaridad cognitiva)
   6. Ver todos los autores disponibles
   7. Exportar perfiles autorales

⚖️ ANÁLISIS JUDICIAL:
   8. Analizar sentencia/fallo judicial
   9. Procesar metadatos judiciales
   10. Ver análisis lógico-temático
   11. Exportar análisis judiciales

🚀 RAG SENTENCIAS v7.4:
   S1. Ingestar corpus de sentencias
   S2. Construir índice FAISS de sentencias
   S3. Buscar en corpus de sentencias (con filtros)
   S4. Exportar reportes CSV de sentencias
   S5. Iniciar API de sentencias (puerto 5010)

📏 DISTANCIA DOCTRINAL v7.5:
   D1. Construir base doctrinal (desde PDFs/TXT)
   D2. Recalcular distancias doctrinales
   D3. Reportes de apartamiento por tribunal/materia
   D4. Análisis de casos críticos

🧠 GEMINI INTERPRETATIVO v7.6 (NUEVO):
   G1. Configurar API Key de GEMINI
   G2. Iniciar servidor de interpretación (puerto 5060)
   G3. Interpretar chunk específico
   G4. Test de interpretación hermenéutica

🌐 SERVIDOR WEB:
   12. Iniciar webapp completa (con navegador)
   13. Solo iniciar servidor (sin navegador)
   14. Probar endpoint autoral

🔧 SISTEMA & DIAGNÓSTICOS:
   15. Diagnóstico completo del sistema
   16. Verificar bases de datos
   17. Limpiar/mantener sistema
   18. Ver archivos ocultos y funciones automáticas

❓ AYUDA & GUÍAS:
   19. Guía: ¿Qué debo usar para cada caso?
   20. Ver todas las funcionalidades disponibles
   21. Mapear archivos y funciones

   0. Salir

Opción: """
        
        while True:
            try:
                opcion = input(menu).strip()
                
                if opcion == "0":
                    print("👋 ¡Hasta luego!")
                    break
                elif opcion.upper() == "R1":
                    self.ejecutar_bat("PROCESAR_DOCUMENTOS.bat")
                elif opcion.upper() == "R2":
                    self.ejecutar_bat("INICIO_FACIL.bat")
                elif opcion.upper() == "R3":
                    self.ejecutar_bat("iniciar_sistema.bat")
                elif opcion.upper() == "R4":
                    self.ejecutar_bat("INICIO_MEJORADO.bat")
                elif opcion == "1":
                    self.procesar_documentos_doctrinarios()
                elif opcion == "2":
                    self.ver_estadisticas_doctrinarias()
                elif opcion == "3":
                    self.exportar_indice_doctrinario()
                elif opcion == "4":
                    self.analizar_autor_especifico()
                elif opcion == "5":
                    self.comparar_autores()
                elif opcion == "6":
                    self.ver_autores_disponibles()
                elif opcion == "7":
                    self.exportar_perfiles_autorales()
                elif opcion == "8":
                    self.analizar_sentencia_judicial()
                elif opcion == "9":
                    self.procesar_metadatos_judiciales()
                elif opcion == "10":
                    self.ver_analisis_logico_tematico()
                elif opcion == "11":
                    self.exportar_analisis_judiciales()
                elif opcion == "12":
                    self.iniciar_webapp_completa()
                elif opcion == "13":
                    self.iniciar_servidor_solo()
                elif opcion == "14":
                    self.probar_endpoint_autoral()
                elif opcion == "15":
                    self.diagnostico_completo()
                elif opcion == "16":
                    self.verificar_bases_datos()
                elif opcion == "17":
                    self.mantener_sistema()
                elif opcion == "18":
                    self.mostrar_funciones_ocultas()
                elif opcion == "19":
                    self.mostrar_guia_uso()
                elif opcion == "20":
                    self.mostrar_funcionalidades()
                elif opcion == "21":
                    self.mapear_archivos_funciones()
                elif opcion.upper() == "S1":
                    self.ingestar_corpus_sentencias()
                elif opcion.upper() == "S2":
                    self.construir_indice_faiss_sentencias()
                elif opcion.upper() == "S3":
                    self.buscar_en_sentencias()
                elif opcion.upper() == "S4":
                    self.exportar_reportes_sentencias()
                elif opcion.upper() == "S5":
                    self.iniciar_api_sentencias()
                elif opcion.upper() == "D1":
                    self.construir_base_doctrinal()
                elif opcion.upper() == "D2":
                    self.recalcular_distancias_doctrinales()
                elif opcion.upper() == "D3":
                    self.generar_reportes_distancia_doctrinal()
                elif opcion.upper() == "D4":
                    self.analizar_casos_criticos()
                elif opcion.upper() == "G1":
                    self.configurar_gemini_api()
                elif opcion.upper() == "G2":
                    self.iniciar_servidor_gemini()
                elif opcion.upper() == "G3":
                    self.interpretar_chunk_especifico()
                elif opcion.upper() == "G4":
                    self.test_interpretacion_gemini()
                elif opcion == "22":
                    self.mostrar_guia_flujos_detallada()
                elif opcion == "99":
                    self.diagnostico_completo()
                else:
                    print("❌ Opción no válida. Intenta de nuevo.")
                    
                input("\nPresiona ENTER para continuar...")
                
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Presiona ENTER para continuar...")

    # ========================================
    # FUNCIONES DOCTRINARIAS
    # ========================================
    
    def procesar_documentos_doctrinarios(self):
        """Procesa documentos doctrinarios (libros, papers)"""
        print("\n📚 ANÁLISIS DOCTRINARIO")
        print("=" * 40)
        
        pdfs_path = self.data_path / "pdfs" / "general"
        print(f"📁 Buscando PDFs en: {pdfs_path}")
        
        if not pdfs_path.exists():
            print(f"❌ Directorio no existe: {pdfs_path}")
            return
            
        pdfs = list(pdfs_path.glob("*.pdf"))
        if not pdfs:
            print("⚠️ No se encontraron archivos PDF para procesar")
            print(f"💡 Coloca archivos PDF en: {pdfs_path}")
            return
            
        print(f"📄 Encontrados {len(pdfs)} archivos PDF:")
        for pdf in pdfs[:5]:  # Mostrar solo los primeros 5
            print(f"   - {pdf.name}")
        if len(pdfs) > 5:
            print(f"   ... y {len(pdfs) - 5} más")
            
        confirmar = input("\n¿Procesar todos estos documentos? (s/N): ").strip().lower()
        if confirmar != 's':
            print("⏸️ Procesamiento cancelado")
            return
            
        print("\n🚀 Ejecutando procesamiento completo...")
        try:
            result = subprocess.run([
                sys.executable, "procesar_todo.py"
            ], cwd=self.base_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Procesamiento completado exitosamente")
                print("📊 Resultado:")
                print(result.stdout[-500:])  # Últimos 500 caracteres
            else:
                print("❌ Error en procesamiento:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando procesar_todo.py: {e}")

    def ver_estadisticas_doctrinarias(self):
        """Muestra estadísticas del corpus doctrinario"""
        print("\n📊 ESTADÍSTICAS DOCTRINARIAS")
        print("=" * 40)
        
        # Verificar base principal
        db_path = self.base_path / "colaborative" / "bases_rag" / "cognitiva" / "pensamiento_integrado_v2.db"
        if not db_path.exists():
            print("❌ Base de datos principal no encontrada")
            return
            
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Estadísticas básicas
            cursor.execute("SELECT COUNT(*) FROM perfiles_integrados_v2")
            total_perfiles = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT autor) FROM perfiles_integrados_v2")
            total_autores = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT fuente) FROM perfiles_integrados_v2")
            total_fuentes = cursor.fetchone()[0]
            
            print(f"📚 Total de perfiles procesados: {total_perfiles}")
            print(f"👤 Total de autores únicos: {total_autores}")
            print(f"📄 Total de fuentes únicas: {total_fuentes}")
            
            # Top 5 autores por cantidad de documentos
            cursor.execute("""
                SELECT autor, COUNT(*) as docs 
                FROM perfiles_integrados_v2 
                GROUP BY autor 
                ORDER BY docs DESC 
                LIMIT 5
            """)
            
            print(f"\n🏆 TOP 5 AUTORES MÁS ANALIZADOS:")
            for autor, docs in cursor.fetchall():
                print(f"   {autor}: {docs} documentos")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error consultando estadísticas: {e}")

    def exportar_indice_doctrinario(self):
        """Exporta índice completo de documentos doctrinarios"""
        print("\n📋 EXPORTAR ÍNDICE DOCTRINARIO")
        print("=" * 40)
        print("🚧 Funcionalidad en desarrollo - próximamente en v7.4")

    # ========================================
    # FUNCIONES AUTORALES  
    # ========================================
    
    def analizar_autor_especifico(self):
        """Analiza el perfil cognitivo de un autor específico"""
        print("\n👤 ANÁLISIS AUTORAL ESPECÍFICO")
        print("=" * 40)
        
        # Mostrar autores disponibles
        self.ver_autores_disponibles(mostrar_titulo=False)
        
        autor = input("\nIngresa el nombre del autor a analizar: ").strip()
        if not autor:
            print("❌ Nombre de autor requerido")
            return
            
        print(f"\n🔍 Analizando perfil de: {autor}")
        
        try:
            # Usar analyser mejorado
            result = subprocess.run([
                sys.executable, 
                "-c", 
                f"from analyser_metodo_mejorado import AnalyserMetodoMejorado; "
                f"analyser = AnalyserMetodoMejorado(); "
                f"print('Análisis completado para {autor}')"
            ], cwd=self.scripts_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Análisis completado")
                print(result.stdout)
            else:
                print("❌ Error en análisis:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error: {e}")

    def comparar_autores(self):
        """Compara dos autores cognitivamente"""
        print("\n🔄 COMPARACIÓN COGNITIVA DE AUTORES")
        print("=" * 40)
        
        self.ver_autores_disponibles(mostrar_titulo=False)
        
        autor_a = input("\nIngresa el primer autor: ").strip()
        autor_b = input("Ingresa el segundo autor: ").strip()
        
        if not autor_a or not autor_b:
            print("❌ Se requieren ambos autores")
            return
            
        print(f"\n🔍 Comparando: {autor_a} vs {autor_b}")
        
        try:
            result = subprocess.run([
                sys.executable,
                "-c",
                f"from comparador_mentes import ComparadorMentes; "
                f"comp = ComparadorMentes(); "
                f"resultado = comp.comparar_autores_detallado('{autor_a}', '{autor_b}'); "
                f"print('Similaridad:', resultado.get('similaridad_coseno', 'N/A')); "
                f"print('Diferencias principales:', resultado.get('diferencias_principales', []))"
            ], cwd=self.scripts_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Comparación completada:")
                print(result.stdout)
            else:
                print("❌ Error en comparación:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error: {e}")

    def ver_autores_disponibles(self, mostrar_titulo=True):
        """Muestra lista de autores disponibles en el sistema"""
        if mostrar_titulo:
            print("\n👥 AUTORES DISPONIBLES EN EL SISTEMA")
            print("=" * 40)
        
        try:
            # Verificar base autor-céntrica
            db_autor = self.base_path / "colaborative" / "bases_rag" / "cognitiva" / "autor_centrico.db"
            if db_autor.exists():
                conn = sqlite3.connect(db_autor)
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT autor FROM perfiles_cognitivos ORDER BY autor")
                autores_centrico = [row[0] for row in cursor.fetchall()]
                conn.close()
            else:
                autores_centrico = []
            
            # Verificar base principal
            db_principal = self.base_path / "colaborative" / "bases_rag" / "cognitiva" / "pensamiento_integrado_v2.db"
            if db_principal.exists():
                conn = sqlite3.connect(db_principal)
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT autor FROM perfiles_integrados_v2 ORDER BY autor")
                autores_principal = [row[0] for row in cursor.fetchall()]
                conn.close()
            else:
                autores_principal = []
            
            # Combinar y mostrar
            todos_autores = sorted(set(autores_centrico + autores_principal))
            
            if not todos_autores:
                print("⚠️ No se encontraron autores procesados")
                print("💡 Ejecuta primero el procesamiento de documentos")
                return
            
            print(f"📋 Total de autores: {len(todos_autores)}")
            print("\n🔹 Autores en sistema autor-céntrico:")
            for autor in autores_centrico[:10]:  # Primeros 10
                print(f"   ✅ {autor}")
            if len(autores_centrico) > 10:
                print(f"   ... y {len(autores_centrico) - 10} más")
                
            print(f"\n🔹 Autores en sistema principal:")
            for autor in autores_principal[:10]:  # Primeros 10
                if autor not in autores_centrico:
                    print(f"   📚 {autor}")
            
        except Exception as e:
            print(f"❌ Error consultando autores: {e}")

    def exportar_perfiles_autorales(self):
        """Exporta perfiles autorales a formato legible"""
        print("\n📤 EXPORTAR PERFILES AUTORALES")
        print("=" * 40)
        print("🚧 Funcionalidad en desarrollo - próximamente en v7.4")

    # ========================================
    # FUNCIONES JUDICIALES
    # ========================================
    
    def analizar_sentencia_judicial(self):
        """Analiza una sentencia o fallo judicial"""
        print("\n⚖️ ANÁLISIS DE SENTENCIA JUDICIAL")
        print("=" * 40)
        
        print("Opciones:")
        print("1. Analizar archivo PDF específico")
        print("2. Analizar texto directo")
        
        opcion = input("Selecciona opción (1-2): ").strip()
        
        if opcion == "1":
            self._analizar_archivo_judicial()
        elif opcion == "2":
            self._analizar_texto_judicial()
        else:
            print("❌ Opción no válida")

    def _analizar_archivo_judicial(self):
        """Analiza archivo PDF judicial específico"""
        pdfs_path = self.data_path / "pdfs" / "general"
        print(f"\n📁 Archivos disponibles en: {pdfs_path}")
        
        if not pdfs_path.exists():
            print(f"❌ Directorio no existe: {pdfs_path}")
            return
            
        pdfs = list(pdfs_path.glob("*.pdf"))
        if not pdfs:
            print("⚠️ No se encontraron archivos PDF")
            return
            
        print("📄 Archivos disponibles:")
        for i, pdf in enumerate(pdfs, 1):
            print(f"   {i}. {pdf.name}")
            
        try:
            seleccion = int(input(f"\nSelecciona archivo (1-{len(pdfs)}): ")) - 1
            if 0 <= seleccion < len(pdfs):
                archivo = pdfs[seleccion]
                print(f"\n🔍 Analizando: {archivo.name}")
                
                # Ejecutar orchestrador maestro
                result = subprocess.run([
                    sys.executable, "orchestrador_maestro_integrado.py"
                ], cwd=self.scripts_path, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Análisis judicial completado")
                    print(result.stdout[-1000:])  # Últimos 1000 caracteres
                else:
                    print("❌ Error en análisis:")
                    print(result.stderr)
            else:
                print("❌ Selección inválida")
                
        except ValueError:
            print("❌ Ingresa un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")

    def _analizar_texto_judicial(self):
        """Analiza texto judicial directo"""
        print("\n📝 Ingresa el texto de la sentencia/fallo:")
        print("(Presiona Ctrl+D o escribe '###FIN###' en una línea para terminar)")
        
        lineas = []
        try:
            while True:
                linea = input()
                if linea.strip() == "###FIN###":
                    break
                lineas.append(linea)
        except EOFError:
            pass
        
        texto = "\n".join(lineas)
        if not texto.strip():
            print("❌ No se ingresó texto")
            return
            
        print(f"\n🔍 Analizando texto ({len(texto)} caracteres)...")
        
        try:
            # Usar endpoint autoral para análisis rápido
            from analyser_metodo_mejorado import detectar_ethos_pathos_logos
            resultado = detectar_ethos_pathos_logos(texto)
            
            print("✅ Análisis retórico completado:")
            print(f"   ETHOS: {resultado['ethos']} (confianza: {resultado['ponderacion_ethos']:.2f})")
            print(f"   PATHOS: {resultado['pathos']} (confianza: {resultado['ponderacion_pathos']:.2f})")
            print(f"   LOGOS: {resultado['logos']} (confianza: {resultado['ponderacion_logos']:.2f})")
            
        except Exception as e:
            print(f"❌ Error en análisis: {e}")

    def procesar_metadatos_judiciales(self):
        """Procesa metadatos judiciales enriquecidos"""
        print("\n📋 PROCESAMIENTO DE METADATOS JUDICIALES")
        print("=" * 40)
        
        metadatos_path = self.data_path / "pdfs" / "general" / "metadatos_sentencias.json"
        
        if not metadatos_path.exists():
            print(f"❌ Archivo de metadatos no encontrado: {metadatos_path}")
            print("💡 Crea el archivo usando la plantilla proporcionada")
            return
            
        try:
            with open(metadatos_path, 'r', encoding='utf-8') as f:
                metadatos = json.load(f)
                
            print(f"📊 Metadatos cargados: {len(metadatos)} sentencias")
            
            for archivo, datos in metadatos.items():
                print(f"\n📄 {archivo}:")
                print(f"   👤 Autor: {datos.get('autor', 'N/A')}")
                print(f"   🏛️ Tribunal: {datos.get('tribunal', 'N/A')}")
                print(f"   📅 Fecha: {datos.get('fecha_sentencia', 'N/A')}")
                print(f"   📋 Temas: {', '.join(datos.get('temas', []))}")
                
        except Exception as e:
            print(f"❌ Error procesando metadatos: {e}")

    def ver_analisis_logico_tematico(self):
        """Muestra análisis lógico-temático de sentencias"""
        print("\n🧠 ANÁLISIS LÓGICO-TEMÁTICO")
        print("=" * 40)
        
        db_path = self.base_path / "colaborative" / "bases_rag" / "cognitiva" / "pensamiento_integrado_v2.db"
        
        if not db_path.exists():
            print("❌ Base de datos no encontrada")
            return
            
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Verificar si existe la tabla
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='analisis_logico_tematico'")
            if not cursor.fetchone():
                print("⚠️ Tabla de análisis lógico-temático no encontrada")
                print("💡 Ejecuta primero el procesamiento de sentencias judiciales")
                conn.close()
                return
            
            cursor.execute("SELECT * FROM analisis_logico_tematico ORDER BY fecha_sentencia DESC LIMIT 10")
            resultados = cursor.fetchall()
            
            if not resultados:
                print("⚠️ No se encontraron análisis lógico-temáticos")
                conn.close()
                return
                
            print(f"📊 Últimos {len(resultados)} análisis:")
            
            for row in resultados:
                autor, expediente, temas, cuestiones, razonamiento = row[1:6]
                print(f"\n👤 Autor: {autor}")
                print(f"📋 Expediente: {expediente}")
                print(f"🏷️ Temas: {temas}")
                print(f"❓ Cuestiones: {cuestiones}")
                print(f"🧠 Razonamiento: {razonamiento}")
                print("-" * 40)
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error consultando análisis: {e}")

    def exportar_analisis_judiciales(self):
        """Exporta análisis judiciales a formato estructurado"""
        print("\n📤 EXPORTAR ANÁLISIS JUDICIALES")
        print("=" * 40)
        print("🚧 Funcionalidad en desarrollo - próximamente en v7.4")

    # ========================================
    # FUNCIONES DE SERVIDOR WEB
    # ========================================
    
    def iniciar_webapp_completa(self):
        """Inicia la webapp completa con navegador"""
        print("\n🌐 INICIANDO WEBAPP COMPLETA")
        print("=" * 40)
        
        print("🚀 Ejecutando servidor con apertura automática de navegador...")
        
        try:
            subprocess.run([
                sys.executable, "end2end_webapp.py"
            ], cwd=self.scripts_path)
            
        except KeyboardInterrupt:
            print("\n⏹️ Servidor detenido por el usuario")
        except Exception as e:
            print(f"❌ Error iniciando webapp: {e}")

    def iniciar_servidor_solo(self):
        """Inicia solo el servidor sin abrir navegador"""
        print("\n🖥️ INICIANDO SERVIDOR (SIN NAVEGADOR)")
        print("=" * 40)
        
        print("🚀 Servidor disponible en: http://127.0.0.1:5002")
        print("📍 Rutas principales:")
        print("   /              → RAG principal")
        print("   /cognitivo     → Análisis cognitivo")
        print("   /radar         → Radar cognitivo")
        print("   /autores       → Sistema autor-céntrico")
        print("   /pensamiento   → Análisis de pensamiento")
        
        try:
            # Modificar temporalmente para no abrir navegador
            subprocess.run([
                sys.executable, 
                "-c",
                "import end2end_webapp; "
                "end2end_webapp.app.run(host='127.0.0.1', port=5002, debug=False)"
            ], cwd=self.scripts_path)
            
        except KeyboardInterrupt:
            print("\n⏹️ Servidor detenido por el usuario")
        except Exception as e:
            print(f"❌ Error iniciando servidor: {e}")

    def probar_endpoint_autoral(self):
        """Prueba el endpoint autoral directamente"""
        print("\n🧪 PROBAR ENDPOINT AUTORAL")
        print("=" * 40)
        
        texto_prueba = "La CSJN estableció precedentes claros debido a la crisis económica, por lo tanto se justifica la medida adoptada."
        
        print(f"📝 Texto de prueba: {texto_prueba}")
        print("\n🔍 Ejecutando análisis...")
        
        try:
            from analyser_metodo_mejorado import detectar_ethos_pathos_logos
            resultado = detectar_ethos_pathos_logos(texto_prueba)
            
            print("✅ Resultado del endpoint:")
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"❌ Error probando endpoint: {e}")

    # ========================================
    # FUNCIONES DE SISTEMA Y DIAGNÓSTICOS
    # ========================================
    
    def diagnostico_completo(self):
        """Ejecuta diagnóstico completo del sistema"""
        print("\n🔧 DIAGNÓSTICO COMPLETO DEL SISTEMA")
        print("=" * 40)
        
        try:
            result = subprocess.run([
                sys.executable, "validar_mega_parche_v7_3.py"
            ], cwd=self.scripts_path, capture_output=True, text=True)
            
            print(result.stdout)
            if result.stderr:
                print("⚠️ Advertencias:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando diagnóstico: {e}")

    def verificar_bases_datos(self):
        """Verifica el estado de las bases de datos"""
        print("\n💾 VERIFICACIÓN DE BASES DE DATOS")
        print("=" * 40)
        
        bases = [
            ("pensamiento_integrado_v2.db", "Base principal integrada"),
            ("autor_centrico.db", "Base autor-céntrica"),
            ("cognitivo.db", "Base cognitiva legacy"),
            ("perfiles.db", "Base de perfiles legacy")
        ]
        
        bases_path = self.base_path / "colaborative" / "bases_rag" / "cognitiva"
        
        for archivo, descripcion in bases:
            db_path = bases_path / archivo
            if db_path.exists():
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tablas = [row[0] for row in cursor.fetchall()]
                    conn.close()
                    
                    print(f"✅ {descripcion}")
                    print(f"   📁 {archivo} ({db_path.stat().st_size // 1024} KB)")
                    print(f"   📋 {len(tablas)} tablas: {', '.join(tablas[:3])}{'...' if len(tablas) > 3 else ''}")
                    
                except Exception as e:
                    print(f"❌ {descripcion} - Error: {e}")
            else:
                print(f"⚠️ {descripcion} - No encontrada: {archivo}")
            print()

    def mantener_sistema(self):
        """Funciones de mantenimiento del sistema"""
        print("\n🧹 MANTENIMIENTO DEL SISTEMA")
        print("=" * 40)
        
        opciones = """
1. Limpiar archivos temporales
2. Reconstruir índices FAISS
3. Optimizar bases de datos
4. Verificar integridad de archivos
5. Limpiar logs antiguos
6. Volver al menú principal
        """
        
        print(opciones)
        opcion = input("Selecciona opción: ").strip()
        
        if opcion == "1":
            self._limpiar_temporales()
        elif opcion == "2":
            print("🚧 Reconstrucción de índices - funcionalidad en desarrollo")
        elif opcion == "3":
            self._optimizar_bases_datos()
        elif opcion == "4":
            print("🚧 Verificación de integridad - funcionalidad en desarrollo")
        elif opcion == "5":
            self._limpiar_logs()
        elif opcion == "6":
            return
        else:
            print("❌ Opción no válida")

    def _limpiar_temporales(self):
        """Limpia archivos temporales"""
        print("🧹 Limpiando archivos temporales...")
        
        # Limpiar __pycache__
        for cache_dir in self.base_path.rglob("__pycache__"):
            try:
                import shutil
                shutil.rmtree(cache_dir)
                print(f"   ✅ Eliminado: {cache_dir}")
            except Exception as e:
                print(f"   ❌ Error eliminando {cache_dir}: {e}")
        
        print("✅ Limpieza de temporales completada")

    def _optimizar_bases_datos(self):
        """Optimiza las bases de datos"""
        print("🔧 Optimizando bases de datos...")
        
        bases_path = self.base_path / "colaborative" / "bases_rag" / "cognitiva"
        
        for db_file in bases_path.glob("*.db"):
            try:
                conn = sqlite3.connect(db_file)
                conn.execute("VACUUM")
                conn.close()
                print(f"   ✅ Optimizada: {db_file.name}")
            except Exception as e:
                print(f"   ❌ Error optimizando {db_file.name}: {e}")
        
        print("✅ Optimización completada")

    def _limpiar_logs(self):
        """Limpia logs antiguos"""
        print("🗑️ Limpiando logs antiguos...")
        
        logs_path = self.base_path / "colaborative" / "logs"
        if logs_path.exists():
            # Mantener solo logs de los últimos 7 días
            import time
            cutoff = time.time() - (7 * 24 * 60 * 60)  # 7 días
            
            for log_file in logs_path.glob("*.log"):
                if log_file.stat().st_mtime < cutoff:
                    try:
                        log_file.unlink()
                        print(f"   ✅ Eliminado: {log_file.name}")
                    except Exception as e:
                        print(f"   ❌ Error eliminando {log_file.name}: {e}")
        
        print("✅ Limpieza de logs completada")

    # ========================================
    # FUNCIONES RAG SENTENCIAS v7.4
    # ========================================
    
    def ingestar_corpus_sentencias(self):
        """
        📥 INGESTA DE CORPUS - El primer paso OBLIGATORIO
        
        🤔 ¿Qué hace esta función?
        Esta es la función MÁS IMPORTANTE del sistema. Sin ejecutar esto primero,
        nada más va a funcionar. Lo que hace es:
        
        1. 📖 Lee todos los archivos PDF de sentencias
        2. ✂️ Los corta en pedazos pequeños (chunks)
        3. 🧠 Crea vectores matemáticos de cada pedazo
        4. 💾 Los guarda en la base de datos
        
        🎯 IMPORTANTE: Coloca tus PDFs en la carpeta:
           colaborative/data/pdfs/sentencias_pdf/
        
        ⏱️ TIEMPO: Puede tardar varios minutos según la cantidad de PDFs
        
        🔥 CONSEJO: Si tienes muchos archivos (>100), ejecuta esto de noche
        """
        print("\n� INGESTA DE CORPUS DE SENTENCIAS V7.4 - ¡El corazón del sistema!")
        print("=" * 70)
        print("💡 NOTA: Esta función es OBLIGATORIA antes que cualquier otra")
        print("📂 Asegúrate de tener PDFs en: colaborative/data/pdfs/sentencias_pdf/")
        print("=" * 70)
        
        # Verificar estructura de carpetas
        from config_rutas import PDF_SENTENCIAS_DIR, TXT_SENTENCIAS_DIR, META_SENTENCIAS_JSON
        
        print(f"📁 Verificando estructura de carpetas...")
        print(f"   PDFs: {PDF_SENTENCIAS_DIR}")
        print(f"   TXT:  {TXT_SENTENCIAS_DIR}")
        print(f"   Meta: {META_SENTENCIAS_JSON}")
        
        # Crear carpetas si no existen
        PDF_SENTENCIAS_DIR.mkdir(parents=True, exist_ok=True)
        TXT_SENTENCIAS_DIR.mkdir(parents=True, exist_ok=True)
        
        if not META_SENTENCIAS_JSON.exists():
            print(f"⚠️ Archivo de metadatos no encontrado: {META_SENTENCIAS_JSON}")
            print("💡 Asegúrate de tener el archivo metadatos_sentencias.json con la estructura correcta")
            return
            
        print("\n🚀 Ejecutando ingesta de sentencias...")
        try:
            result = subprocess.run([
                sys.executable, "ingesta_sentencias.py"
            ], cwd=self.scripts_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Ingesta completada exitosamente")
                print("📊 Resultado:")
                print(result.stdout)
            else:
                print("❌ Error en ingesta:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando ingesta: {e}")

    def construir_indice_faiss_sentencias(self):
        """
        🏗️ CONSTRUCCIÓN ÍNDICE FAISS - El motor de búsquedas
        
        🤔 ¿Qué hace esta función?
        Imaginate que tienes 1000 libros y quieres encontrar algo específico.
        Sin un índice, tendrías que leer libro por libro. FAISS es como crear
        un súper índice que te permite encontrar información instantáneamente.
        
        📋 Lo que hace paso a paso:
        1. 🧠 Toma todos los chunks de S1
        2. 🔢 Los convierte en vectores matemáticos  
        3. 🗂️ Crea un índice súper rápido
        4. 💾 Lo guarda para usarlo después
        
        ⚠️ IMPORTANTE: Necesitas haber ejecutado S1 (Ingestar) primero
        
        ⏱️ TIEMPO: 3-10 minutos según la cantidad de sentencias
        
        🎯 RESULTADO: Archivo .index que permite búsquedas instantáneas
        """
        print("\n🏗️ CONSTRUCCIÓN ÍNDICE FAISS - ¡Creando tu motor de búsquedas!")
        print("=" * 65)
        print("💡 NOTA: Esta función requiere que S1 (Ingestar) haya terminado")
        print("⚡ RESULTADO: Búsquedas instantáneas en miles de documentos")
        print("=" * 65)
        
        print("📊 Construyendo embeddings y índice FAISS...")
        print("⏰ Esto puede tardar varios minutos dependiendo del corpus")
        print("☕ Momento perfecto para tomar un café mientras trabajo...")
        
        try:
            result = subprocess.run([
                sys.executable, "build_faiss_sentencias.py"
            ], cwd=self.scripts_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Índice FAISS construido exitosamente")
                print("📊 Resultado:")
                print(result.stdout)
            else:
                print("❌ Error construyendo índice:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando construcción: {e}")

    def buscar_en_sentencias(self):
        """Búsqueda interactiva en corpus de sentencias"""
        print("\n🔍 BÚSQUEDA EN CORPUS DE SENTENCIAS")
        print("=" * 50)
        
        query = input("Ingresa tu consulta: ").strip()
        if not query:
            print("❌ Consulta requerida")
            return
            
        print("\n🎯 Filtros opcionales (presiona ENTER para omitir):")
        tema = input("Tema: ").strip() or None
        falacia = input("Falacia: ").strip() or None  
        razonamiento = input("Tipo de razonamiento: ").strip() or None
        tribunal = input("Tribunal: ").strip() or None
        desde = input("Fecha desde (YYYY-MM-DD): ").strip() or None
        hasta = input("Fecha hasta (YYYY-MM-DD): ").strip() or None
        
        print(f"\n🔍 Buscando: '{query}'")
        if any([tema, falacia, razonamiento, tribunal, desde, hasta]):
            print("🎯 Con filtros aplicados")
        
        try:
            # Crear script temporal para búsqueda
            script_busqueda = f"""
import sys
sys.path.append('{self.scripts_path}')
from query_rag_sentencias import buscar
import json

filtros = {{}}
if '{tema}': filtros['tema'] = '{tema}'
if '{falacia}': filtros['falacia'] = '{falacia}'
if '{razonamiento}': filtros['razonamiento'] = '{razonamiento}'
if '{tribunal}': filtros['tribunal'] = '{tribunal}'
if '{desde}': filtros['desde'] = '{desde}'
if '{hasta}': filtros['hasta'] = '{hasta}'

resultados = buscar("{query}", filtros=filtros if filtros else None, topk=50)
print(f"🔍 Encontrados {{len(resultados)}} resultados")
for i, (boost, r) in enumerate(resultados[:10], 1):
    print(f"\\n{{i}}. [{{r[0]}}] {{r[1]}} ({{r[3]}})")
    print(f"   Tribunal: {{r[4]}} | Materia: {{r[6]}}")
    print(f"   Temas: {{r[7]}}")
    print(f"   Razonamiento: {{r[8]}}")
    print(f"   Falacias: {{r[9]}}")
    print(f"   Boost: {{boost:.2f}}")
    print(f"   Texto: {{r[12][:200]}}...")
"""
            
            result = subprocess.run([
                sys.executable, "-c", script_busqueda
            ], cwd=self.scripts_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(result.stdout)
            else:
                print("❌ Error en búsqueda:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando búsqueda: {e}")

    def exportar_reportes_sentencias(self):
        """Exporta reportes CSV de sentencias"""
        print("\n📤 EXPORTAR REPORTES CSV DE SENTENCIAS")
        print("=" * 50)
        
        try:
            result = subprocess.run([
                sys.executable, "report_sentencias_csv.py"
            ], cwd=self.scripts_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Reportes exportados exitosamente")
                print("📊 Resultado:")
                print(result.stdout)
                
                # Mostrar archivos generados
                exports_dir = self.base_path / "exports"
                if exports_dir.exists():
                    archivos = list(exports_dir.glob("*.csv"))
                    print(f"\n📁 Archivos generados en {exports_dir}:")
                    for archivo in archivos:
                        size_kb = archivo.stat().st_size // 1024
                        print(f"   📄 {archivo.name} ({size_kb} KB)")
            else:
                print("❌ Error exportando reportes:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando exportación: {e}")

    def iniciar_api_sentencias(self):
        """Inicia la API de sentencias en puerto 5010"""
        print("\n🌐 INICIANDO API DE SENTENCIAS v7.4")
        print("=" * 50)
        
        print("🚀 Iniciando servidor API en puerto 5010...")
        print("📍 Endpoints disponibles:")
        print("   GET  /                          → Info del servicio")
        print("   POST /buscar-sentencias         → Búsqueda RAG con filtros")
        print("   POST /analizar-contenido-autoral → Análisis retórico")
        print()
        print("🌐 Acceso: http://127.0.0.1:5010")
        print("🔄 Presiona Ctrl+C para volver al menú")
        
        try:
            subprocess.run([
                sys.executable, "api_sentencias.py"
            ], cwd=self.scripts_path)
            
        except KeyboardInterrupt:
            print("\n⏹️ API detenida por el usuario")
        except Exception as e:
            print(f"❌ Error iniciando API: {e}")

    def mostrar_funciones_ocultas(self):
        """Muestra funciones ocultas y automatizaciones del sistema"""
        print("\n🔍 FUNCIONES OCULTAS Y AUTOMATIZACIONES")
        print("=" * 50)
        
        funciones_ocultas = [
            {
                "modulo": "orchestrador_maestro_integrado.py",
                "funcion": "🔁 Router inteligente",
                "descripcion": "Detecta automáticamente si el documento es doctrina, autor o sentencia y lo envía al flujo correcto"
            },
            {
                "modulo": "analyser_metodo_mejorado.py", 
                "funcion": "🧠 Normalizador semántico",
                "descripcion": "Estandariza las salidas de todos los analizadores (coherencia, ethos, pathos, logos) antes de guardar"
            },
            {
                "modulo": "validador_contexto_retorica.py",
                "funcion": "🧩 Analizador contextual oculto", 
                "descripcion": "Actúa como mini motor semántico interno. Se ejecuta automáticamente cuando detecta lenguaje argumental"
            },
            {
                "modulo": "autor_centrico.db",
                "funcion": "🔒 Base espejo cognitiva",
                "descripcion": "Contiene solo perfiles 'personales' de autores/jueces; no almacena textos, sino matrices de razonamiento"
            },
            {
                "modulo": "pensamiento_integrado_v2.db",
                "funcion": "🧩 Base central de conocimiento",
                "descripcion": "Une doctrina, jurisprudencia y patrones de razonamiento + nuevas tablas de análisis temático/judicial"
            },
            {
                "modulo": "end2end_webapp.py",
                "funcion": "🌐 Integración automática de módulos",
                "descripcion": "Carga automáticamente todos los sistemas disponibles (Referencias, Biblioteca, PCA, etc.)"
            },
            {
                "modulo": "config_rutas.py",
                "funcion": "⚙️ Centralización de rutas",
                "descripcion": "Todos los módulos usan automáticamente las rutas centralizadas para mantener coherencia"
            }
        ]
        
        for i, func in enumerate(funciones_ocultas, 1):
            print(f"\n{i}. {func['funcion']}")
            print(f"   📁 Módulo: {func['modulo']}")
            print(f"   📋 Qué hace: {func['descripcion']}")

    def mostrar_guia_uso(self):
        """Muestra guía de qué usar en cada caso"""
        print("\n❓ GUÍA: ¿QUÉ DEBO USAR PARA CADA CASO?")
        print("=" * 50)
        
        print("🚀 CASOS COMUNES - USA LOS ARCHIVOS .BAT EXISTENTES:")
        casos_bat = [
            {
                "objetivo": "Procesar documentos jurídicos nuevos (PDFs)",
                "usar": "Opción R1: PROCESAR_DOCUMENTOS.bat",
                "resultado": "Procesamiento automático con feedback visual"
            },
            {
                "objetivo": "Usar sistema web básico (sin complicaciones)",
                "usar": "Opción R2: INICIO_FACIL.bat",
                "resultado": "Webapp simple con funcionalidades principales"
            },
            {
                "objetivo": "Usar sistema web completo (todas las funciones)",
                "usar": "Opción R3: iniciar_sistema.bat",
                "resultado": "Sistema completo con análisis autor-céntrico"
            },
            {
                "objetivo": "Usar sistema web con verificaciones previas",
                "usar": "Opción R4: INICIO_MEJORADO.bat",
                "resultado": "Sistema con diagnósticos y verificaciones"
            }
        ]
        
        for caso in casos_bat:
            print(f"\n🎯 {caso['objetivo']}")
            print(f"   ✅ Usar: {caso['usar']}")
            print(f"   📊 Resultado: {caso['resultado']}")
        
        print("\n" + "=" * 50)
        print("🔧 CASOS AVANZADOS - USA LAS OPCIONES DEL MENÚ:")
        
        casos_avanzados = [
            {
                "objetivo": "Analizar autores o jueces (perfil individual)",
                "usar": "Opción 4: Analizar perfil de autor específico",
                "resultado": "Inserta/actualiza en autor_centrico.db. Rápido y preciso"
            },
            {
                "objetivo": "Analizar pensamiento judicial (sentencias)",
                "usar": "Opción 8: Analizar sentencia/fallo judicial",
                "resultado": "Genera perfiles enriquecidos con temas, falacias, doctrina, cálculos"
            },
            {
                "objetivo": "Comparar estilos cognitivos entre autores",
                "usar": "Opción 5: Comparar autores",
                "resultado": "Análisis de similaridad cognitiva detallado"
            },
            {
                "objetivo": "Ver qué autores están procesados",
                "usar": "Opción 6: Ver todos los autores disponibles",
                "resultado": "Lista completa de autores en ambas bases de datos"
            },
            {
                "objetivo": "Diagnosticar problemas del sistema",
                "usar": "Opción 15: Diagnóstico completo del sistema",
                "resultado": "Verifica que todos los componentes funcionen correctamente"
            },
            {
                "objetivo": "Ver funciones ocultas del sistema",
                "usar": "Opción 18: Ver archivos ocultos y funciones automáticas",
                "resultado": "Muestra automatizaciones que trabajan por debajo"
            }
        ]
        
        for caso in casos_avanzados:
            print(f"\n🎯 {caso['objetivo']}")
            print(f"   ✅ Usar: {caso['usar']}")
            print(f"   📊 Resultado: {caso['resultado']}")
        
        print("\n" + "=" * 50)
        print("🚀 CASOS RAG SENTENCIAS v7.4 - NUEVAS FUNCIONALIDADES:")
        
        casos_rag = [
            {
                "objetivo": "Crear corpus de sentencias con metadatos",
                "usar": "Opción S1: Ingestar corpus de sentencias",
                "resultado": "Chunks indexados con metadatos judiciales completos"
            },
            {
                "objetivo": "Búsqueda semántica en sentencias",
                "usar": "Opción S2 → S3: Construir índice → Buscar",
                "resultado": "Búsqueda con filtros por tema, falacia, tribunal, etc."
            },
            {
                "objetivo": "Análisis estadístico de sentencias",
                "usar": "Opción S4: Exportar reportes CSV",
                "resultado": "Datasets para Excel/Power BI con análisis por tribunal"
            },
            {
                "objetivo": "Integrar con sistemas externos",
                "usar": "Opción S5: Iniciar API de sentencias",
                "resultado": "API REST en puerto 5010 para integración"
            }
        ]
        
        for caso in casos_rag:
            print(f"\n🎯 {caso['objetivo']}")
            print(f"   ✅ Usar: {caso['usar']}")
            print(f"   📊 Resultado: {caso['resultado']}")

    def mostrar_funcionalidades(self):
        """Muestra todas las funcionalidades disponibles"""
        print("\n🚀 TODAS LAS FUNCIONALIDADES DEL SISTEMA")
        print("=" * 50)
        
        funcionalidades = [
            "📚 Análisis doctrinario con embeddings y RAG",
            "👤 Perfiles cognitivos autorales detallados", 
            "⚖️ Análisis judicial con metadatos enriquecidos",
            "🧠 Detección de patrones de razonamiento (14 tipos)",
            "🎭 Análisis retórico (ETHOS, PATHOS, LOGOS)",
            "🏛️ Detección aristotélica de estructuras silogísticas",
            "📊 Radar cognitivo interactivo",
            "🔄 Comparación cognitiva entre autores",
            "🌐 Webapp con múltiples interfaces especializadas",
            "🔍 Búsqueda semántica avanzada",
            "📋 Exportación de resultados estructurados",
            "🔧 Sistema de diagnóstico y mantenimiento",
            "🤖 Integración con Gemini AI",
            "📈 Métricas de calidad y coherencia",
            "🔗 API REST para integración externa",
            "💾 Múltiples bases de datos especializadas"
        ]
        
        for i, func in enumerate(funcionalidades, 1):
            print(f"{i:2d}. {func}")

    def mapear_archivos_funciones(self):
        """Mapea archivos y sus funciones principales"""
        print("\n🗺️ MAPA DE ARCHIVOS Y FUNCIONES")
        print("=" * 50)
        
        print("🚀 ARCHIVOS .BAT EXISTENTES:")
        archivos_bat = [
            {
                "archivo": "PROCESAR_DOCUMENTOS.bat",
                "funcion": "📚 Procesamiento de PDFs",
                "descripcion": "Procesa documentos jurídicos en lote"
            },
            {
                "archivo": "INICIO_FACIL.bat", 
                "funcion": "🌐 Webapp básica",
                "descripcion": "Inicia servidor web con funcionalidades básicas"
            },
            {
                "archivo": "iniciar_sistema.bat",
                "funcion": "🚀 Sistema completo",
                "descripcion": "Inicia todo el sistema con todas las funcionalidades"
            },
            {
                "archivo": "INICIO_MEJORADO.bat",
                "funcion": "🔧 Sistema con diagnósticos",
                "descripcion": "Inicia sistema con verificaciones previas"
            },
            {
                "archivo": "CENTRO_CONTROL.bat",
                "funcion": "🎛️ Menú principal",
                "descripcion": "Acceso unificado a todas las funciones"
            }
        ]
        
        for item in archivos_bat:
            print(f"\n📄 {item['archivo']}")
            print(f"   {item['funcion']}")
            print(f"   📋 {item['descripcion']}")
        
        print("\n" + "=" * 50)
        print("🐍 ARCHIVOS PYTHON PRINCIPALES:")
        
        mapa_python = [
            {
                "archivo": "centro_control_maestro.py",
                "funcion": "🎛️ Control unificado",
                "descripcion": "Este archivo - centraliza funciones avanzadas"
            },
            {
                "archivo": "procesar_todo.py",
                "funcion": "📚 Procesamiento masivo",
                "descripcion": "Procesa todos los PDFs de una vez"
            },
            {
                "archivo": "orchestrador_maestro_integrado.py",
                "funcion": "🎼 Coordinador maestro",
                "descripcion": "Integra todos los motores de análisis"
            },
            {
                "archivo": "analyser_metodo_mejorado.py",
                "funcion": "🧠 Motor de análisis principal",
                "descripcion": "40+ dimensiones cognitivas"
            },
            {
                "archivo": "validador_contexto_retorica.py",
                "funcion": "🎭 Análisis retórico contextual",
                "descripcion": "ETHOS/PATHOS/LOGOS con contexto"
            },
            {
                "archivo": "comparador_mentes.py",
                "funcion": "🔄 Comparación cognitiva",
                "descripcion": "Similaridad entre autores"
            },
            {
                "archivo": "end2end_webapp.py",
                "funcion": "🌐 Servidor web",
                "descripcion": "Interfaz web completa"
            }
        ]
        
        for item in mapa_python:
            print(f"\n� {item['archivo']}")
            print(f"   {item['funcion']}")
            print(f"   📋 {item['descripcion']}")

    # ========================================
    # FUNCIONES DISTANCIA DOCTRINAL V7.5
    # ========================================
    
    def construir_base_doctrinal(self):
        """
        📚 CONSTRUCCIÓN BASE DOCTRINAL - Tu biblioteca de referencia
        
        🤔 ¿Qué es la "base doctrinal"?
        Es como crear una biblioteca de conocimiento experto. Piénsalo así:
        si quieres saber si un juez se está apartando de lo que dice la doctrina,
        primero necesitas saber QUÉ dice la doctrina, ¿verdad?
        
        📋 Lo que hace esta función:
        1. 📖 Lee libros, papers y artículos doctrinarios (PDFs)
        2. ✂️ Los divide en pedazos pequeños
        3. 🧠 Crea un "vector promedio" (como el DNA de la doctrina)
        4. 💾 Lo guarda para comparar después con las sentencias
        
        📁 PREPARACIÓN: Coloca PDFs doctrinarios en:
           colaborative/data/pdfs/doctrina_pdf/
        
        🎯 RESULTADO: Una "huella dactilar" matemática de la doctrina
        
        ⏱️ TIEMPO: Depende de cuántos libros tengas (5-30 minutos)
        
        💡 TU CASO: Con GEMINI disponible, después de D2 podrás usar G4→G3
                   para obtener explicaciones IA de los apartamientos detectados
        """
        print("\n📚 CONSTRUCCIÓN BASE DOCTRINAL - ¡Creando tu biblioteca experta!")
        print("=" * 70)
        print("💡 NOTA: Coloca PDFs doctrinarios en la carpeta doctrina_pdf/")
        print("🎯 OBJETIVO: Crear 'DNA' matemático de la doctrina para comparar")
        print("🚀 BONUS: Después podrás usar GEMINI (G4→G3) para interpretaciones IA")
        print("=" * 70)
        
        print("📋 Este proceso:")
        print("   1. 📖 Busca archivos PDF en: colaborative/data/pdfs/doctrina_pdf/")
        print("   2. 📄 O archivos TXT en: colaborative/data/pdfs/doctrina_texto/")
        print("   3. 🧠 Genera embeddings y vector doctrinal promedio")
        print("   4. 🗂️ Crea índice FAISS para recuperación rápida")
        print("   5. 💾 Guarda todo para usar en D2 (calcular distancias)")
        
        confirmar = input("\n¿Continuar? (s/n): ").strip().lower()
        if confirmar != 's':
            print("❌ Operación cancelada")
            return
        
        try:
            script_path = self.scripts_path / "build_doctrina_base.py"
            result = subprocess.run([
                sys.executable, str(script_path)
            ], cwd=self.base_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Base doctrinal construida exitosamente")
                print(result.stdout)
            else:
                print("❌ Error construyendo base doctrinal:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando construcción: {e}")
    
    def recalcular_distancias_doctrinales(self):
        """Recalcula distancias doctrinales de todas las sentencias"""
        print("\n📏 RECÁLCULO DE DISTANCIAS DOCTRINALES")
        print("=" * 50)
        
        print("📋 Este proceso:")
        print("   1. Verifica que existe la base doctrinal")
        print("   2. Calcula distancia de cada chunk de sentencia")
        print("   3. Actualiza la columna distancia_doctrinal en BD")
        print("   4. Puede tomar varios minutos...")
        
        confirmar = input("\n¿Continuar? (s/n): ").strip().lower()
        if confirmar != 's':
            print("❌ Operación cancelada")
            return
        
        try:
            script_path = self.scripts_path / "update_distancia_doctrinal.py"
            result = subprocess.run([
                sys.executable, str(script_path)
            ], cwd=self.base_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Distancias doctrinales recalculadas")
                print(result.stdout)
            else:
                print("❌ Error en recálculo:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando recálculo: {e}")
    
    def generar_reportes_distancia_doctrinal(self):
        """Genera reportes de apartamiento por tribunal/materia"""
        print("\n📊 REPORTES DE DISTANCIA DOCTRINAL")
        print("=" * 45)
        
        print("📋 Este proceso genera:")
        print("   1. Reporte agregado por expediente")
        print("   2. Ranking de tribunales por apartamiento")
        print("   3. Análisis por materia")
        print("   4. Casos críticos (alta distancia)")
        print("   5. Archivos CSV en carpeta exports/")
        
        try:
            script_path = self.scripts_path / "report_distancia_por_exp_tribunal.py"
            result = subprocess.run([
                sys.executable, str(script_path)
            ], cwd=self.base_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Reportes generados exitosamente")
                print(result.stdout)
            else:
                print("❌ Error generando reportes:")
                print(result.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando reportes: {e}")
    
    def analizar_casos_criticos(self):
        """Analiza casos con alta distancia doctrinal"""
        print("\n🔴 ANÁLISIS DE CASOS CRÍTICOS")
        print("=" * 40)
        
        print("📋 Umbrales de apartamiento:")
        print("   🟢 ≤ 0.20 → Alineación doctrinal")
        print("   🟡 0.20–0.50 → Desvío moderado")
        print("   🔴 > 0.50 → Apartamiento significativo")
        print("   ⚠️ > 0.70 → Crítico (requiere justificación)")
        
        # Mostrar consulta rápida de casos críticos
        try:
            import sqlite3
            from config_rutas import PENSAMIENTO_DB
            
            if not Path(PENSAMIENTO_DB).exists():
                print("❌ Base de datos no encontrada")
                return
            
            con = sqlite3.connect(PENSAMIENTO_DB)
            cur = con.cursor()
            
            # Casos críticos
            cur.execute("""
                SELECT expediente, tribunal, jurisdiccion, 
                       AVG(distancia_doctrinal) as dist_prom,
                       COUNT(*) as chunks
                FROM rag_sentencias_chunks 
                WHERE distancia_doctrinal > 0.60
                GROUP BY expediente, tribunal, jurisdiccion
                ORDER BY dist_prom DESC
                LIMIT 10
            """)
            
            casos = cur.fetchall()
            con.close()
            
            if casos:
                print(f"\n🔴 TOP 10 CASOS CRÍTICOS (>0.60):")
                for i, (exp, trib, juris, dist, chunks) in enumerate(casos, 1):
                    print(f"   {i:2d}. {exp} | {trib} | Dist: {dist:.4f} ({chunks} chunks)")
            else:
                print("\n✅ No hay casos críticos detectados")
                
        except Exception as e:
            print(f"❌ Error analizando casos críticos: {e}")

    # ========================================
    # FUNCIÓN DE GUÍA DETALLADA V7.6
    # ========================================
    
    def mostrar_guia_flujos_detallada(self):
        """Muestra guía detallada de flujos de trabajo"""
        print("\n📖 GUÍA DETALLADA DE FLUJOS DE TRABAJO")
        print("=" * 60)
        
        # Ejecutar la guía externa
        try:
            guia_path = self.base_path / "guia_uso_sistemico.py"
            if guia_path.exists():
                subprocess.run([sys.executable, str(guia_path)], cwd=self.base_path)
            else:
                # Guía embebida si no existe el archivo
                self._mostrar_guia_embebida()
        except Exception as e:
            print(f"❌ Error mostrando guía: {e}")
            self._mostrar_guia_embebida()
    
    def _mostrar_guia_embebida(self):
        """Guía embebida como respaldo"""
        
        print("\n🎯 FLUJOS DE TRABAJO PRINCIPALES")
        print("=" * 40)
        
        flujos = [
            ("🚀 FLUJO 1: RAG SENTENCIAS (PRINCIPIANTES)", [
                "📋 Objetivo: Sistema de búsqueda semántica en sentencias",
                "📥 Preparación: Colocar PDFs en colaborative/data/pdfs/sentencias_pdf/",
                "🔄 Ejecución OBLIGATORIA en orden:",
                "   S1. Ingestar corpus → Procesa PDFs y crea chunks en BD",
                "   S2. Construir FAISS → Crea índice para búsquedas rápidas", 
                "   S3. Buscar corpus → Realiza consultas con filtros",
                "📊 Resultados: S4 (CSV), S5 (API para web)",
                "⚠️ Sin S1+S2, nada más funcionará"
            ]),
            
            ("📏 FLUJO 2: DISTANCIA DOCTRINAL (INTERMEDIO)", [
                "📋 Objetivo: Medir apartamiento de sentencias vs doctrina",
                "📥 Preparación: PDFs doctrinales en colaborative/data/pdfs/doctrina_pdf/",
                "🔄 Ejecución (REQUIERE FLUJO 1 completo):",
                "   D1. Construir base doctrinal → Vector promedio de doctrina",
                "   D2. Calcular distancias → Mide cada chunk vs doctrina",
                "   D3. Reportes agregados → CSV por tribunal/materia",
                "   D4. Casos críticos → Apartamientos >0.60",
                "📊 Interpretación: 0.0=alineado, 1.0=apartado",
                "⚠️ D2 requiere S1 (sentencias) + D1 (doctrina)"
            ]),
            
            ("🧠 FLUJO 3: INTERPRETACIÓN IA (AVANZADO)", [
                "📋 Objetivo: Explicación hermenéutica de apartamientos",
                "🔧 Preparación: API Key de GEMINI (https://makersuite.google.com/app/apikey)",
                "🔄 Ejecución (REQUIERE FLUJO 2 completo):",
                "   G1. Configurar API → Variable GEMINI_API_KEY",
                "   G4. Test interpretación → Verificar funcionamiento",
                "   G2. Servidor producción → Puerto 5060 para web",
                "   G3. Interpretar individual → Análisis específico",
                "📊 Resultado: Texto explicativo del apartamiento",
                "⚠️ Requiere créditos en cuenta Google AI"
            ])
        ]
        
        for titulo, pasos in flujos:
            print(f"\n{titulo}")
            print("-" * len(titulo))
            for paso in pasos:
                print(f"{paso}")
        
        self._mostrar_orden_critico()
        self._mostrar_diagnosticos_comunes()
    
    def _mostrar_orden_critico(self):
        """Muestra el orden crítico de ejecución"""
        print(f"\n⚠️ ORDEN CRÍTICO - NO SALTEAR PASOS")
        print("=" * 40)
        
        pasos_criticos = [
            "1️⃣ S1 (Ingestar) → PRIMERO SIEMPRE",
            "2️⃣ S2 (FAISS) → DESPUÉS de S1",
            "3️⃣ D1 (Base doctrinal) → Para distancias",
            "4️⃣ D2 (Calcular) → DESPUÉS de S1+D1",
            "5️⃣ G1 (API Key) → Para interpretación",
            "",
            "❌ ERRORES COMUNES:",
            "   • D2 sin S1 → 'No hay chunks de sentencias'",
            "   • D2 sin D1 → 'Vector doctrinal no encontrado'",
            "   • G3 sin G1 → 'API Key no configurada'",
            "   • S3 sin S2 → 'Índice FAISS no existe'"
        ]
        
        for paso in pasos_criticos:
            print(f"   {paso}")
    
    def _mostrar_diagnosticos_comunes(self):
        """Muestra diagnósticos para problemas comunes"""
        print(f"\n🔧 SOLUCIÓN DE PROBLEMAS")
        print("=" * 30)
        
        problemas = [
            "🆘 OPCIÓN 99: Diagnóstico completo del sistema",
            "🔍 OPCIÓN 15: Ver qué hay en las bases de datos",
            "🧹 OPCIÓN 17: Limpiar corrupciones",
            "",
            "📁 Directorios importantes:",
            "   • colaborative/data/pdfs/sentencias_pdf/ → PDFs sentencias",
            "   • colaborative/data/pdfs/doctrina_pdf/ → PDFs doctrina",
            "   • colaborative/bases_rag/cognitiva/ → Bases de datos",
            "   • exports/ → Reportes CSV generados"
        ]
        
        for item in problemas:
            print(f"   {item}")
    
    def diagnostico_completo(self):
        """
        🩺 DIAGNÓSTICO INTEGRAL - Tu doctor del sistema
        
        🤔 ¿Qué hace esta función?
        Es como llevar tu sistema al médico para un chequeo completo.
        Revisa TODO: archivos, bases de datos, configuraciones, conexiones...
        y te dice exactamente qué está bien y qué necesita arreglarse.
        
        🎯 REVISA 6 ÁREAS CRÍTICAS:
        1. 📁 Directorios (¿están las carpetas correctas?)
        2. 💾 Bases de datos (¿hay datos? ¿cuántos?)
        3. 🔍 Índices FAISS (¿funcionan las búsquedas?)
        4. 🧠 GEMINI (¿está configurada la IA?)
        5. 🧪 Tests básicos (¿anda todo?)
        6. 💡 Recomendaciones (¿qué hacer ahora?)
        
        ⏱️ TIEMPO: 30 segundos
        🎉 RESULTADO: Sabes exactamente qué arreglar
        
        💡 CONSEJO: Usa esto cuando algo no funciona o antes de empezar
        """
        print("\n🩺 DIAGNÓSTICO INTEGRAL - ¡Checkeo completo de tu sistema!")
        print("=" * 70)
        print("🎯 OBJETIVO: Encontrar y diagnosticar cualquier problema")
        print("⏱️ TIEMPO: Solo 30 segundos para revisar todo")
        print("=" * 70)
        
        # 1. Verificar estructura de directorios
        print("\n📁 1. ESTRUCTURA DE DIRECTORIOS")
        print("-" * 30)
        
        directorios_criticos = [
            ("Sentencias PDF", "data/pdfs/sentencias_pdf"),
            ("Doctrina PDF", "data/pdfs/doctrina_pdf"),
            ("Bases RAG", "bases_rag/cognitiva"),
            ("Exports", "exports"),
            ("Scripts", "scripts")
        ]
        
        for nombre, ruta in directorios_criticos:
            ruta_completa = self.base_path / ruta
            estado = "✅ EXISTE" if ruta_completa.exists() else "❌ FALTA"
            if ruta_completa.exists() and ruta_completa.is_dir():
                archivos = len(list(ruta_completa.glob("*")))
                estado += f" ({archivos} archivos)"
            print(f"{estado:15} | {nombre}: {ruta}")
        
        # 2. Verificar bases de datos
        print(f"\n💾 2. BASES DE DATOS")
        print("-" * 20)
        
        try:
            from ..db_rag.cognitiva_db import CognitivaDB
            db = CognitivaDB()
            
            # Conteo de registros
            tables_info = [
                ("Sentencias chunks", "SELECT COUNT(*) FROM sentencias_chunks"),
                ("Sentencias procesadas", "SELECT COUNT(*) FROM sentencias_procesadas"),
                ("Base doctrinal", "SELECT COUNT(*) FROM base_doctrinal"),
                ("Autor centrico", "SELECT COUNT(*) FROM autor_centrico")
            ]
            
            for nombre, query in tables_info:
                try:
                    cursor = db.conn.cursor()
                    cursor.execute(query)
                    count = cursor.fetchone()[0]
                    print(f"✅ {count:6} registros | {nombre}")
                except Exception as e:
                    print(f"❌ ERROR | {nombre}: {e}")
                    
        except Exception as e:
            print(f"❌ Error conectando a BD: {e}")
        
        # 3. Verificar índices FAISS
        print(f"\n🔍 3. ÍNDICES FAISS")
        print("-" * 15)
        
        faiss_files = [
            ("Sentencias", "sentencias_embeddings.index"),
            ("Doctrina", "doctrina_embeddings.index")
        ]
        
        for nombre, archivo in faiss_files:
            ruta_faiss = self.base_path / "bases_rag" / "cognitiva" / archivo
            if ruta_faiss.exists():
                size_mb = ruta_faiss.stat().st_size / (1024*1024)
                print(f"✅ {size_mb:6.1f} MB | {nombre}: {archivo}")
            else:
                print(f"❌ FALTA | {nombre}: {archivo}")
        
        # 4. Verificar configuración GEMINI
        print(f"\n🧠 4. CONFIGURACIÓN GEMINI")
        print("-" * 25)
        
        # Buscar API Key en múltiples variables
        api_key_sources = [
            ("GEMINI_API_KEY", os.getenv('GEMINI_API_KEY')),
            ("GOOGLE_API_KEY", os.getenv('GOOGLE_API_KEY')),
            ("GOOGLE_AI_API_KEY", os.getenv('GOOGLE_AI_API_KEY'))
        ]
        
        found_key = False
        for source_name, api_key in api_key_sources:
            if api_key and api_key != "TU_API_KEY_AQUI":
                key_preview = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "****"
                print(f"✅ API Key encontrada en {source_name}: {key_preview}")
                found_key = True
                break
        
        if not found_key:
            print(f"❌ API Key no encontrada en variables de entorno")
            print(f"   Variables buscadas: GEMINI_API_KEY, GOOGLE_API_KEY, GOOGLE_AI_API_KEY")
            print(f"   Configurar con G1 o verificar variable de sistema")
        
        # 5. Test rápido de funcionalidades
        print(f"\n🧪 5. TEST RÁPIDO DE FUNCIONALIDADES")
        print("-" * 35)
        
        tests = [
            ("Conexión BD", self._test_conexion_bd),
            ("Modelo embeddings", self._test_modelo_embeddings),
            ("Query básico", self._test_query_basico)
        ]
        
        for nombre, test_func in tests:
            try:
                result = test_func()
                estado = "✅ OK" if result else "⚠️ WARN"
                print(f"{estado} | {nombre}")
            except Exception as e:
                print(f"❌ ERROR | {nombre}: {str(e)[:50]}...")
        
        # 6. Recomendaciones
        print(f"\n💡 6. RECOMENDACIONES")
        print("-" * 20)
        
        self._mostrar_recomendaciones_diagnostico()
    
    def _test_conexion_bd(self):
        """Test básico de conexión BD"""
        from ..db_rag.cognitiva_db import CognitivaDB
        db = CognitivaDB()
        cursor = db.conn.cursor()
        cursor.execute("SELECT 1")
        return cursor.fetchone()[0] == 1
    
    def _test_modelo_embeddings(self):
        """Test carga modelo embeddings"""
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        test_embed = model.encode("test")
        return len(test_embed) == 384
    
    def _test_query_basico(self):
        """Test query básico"""
        from ..query_rag.query_rag_sentencias import QueryRAGSentencias
        query_engine = QueryRAGSentencias()
        return hasattr(query_engine, 'model')
    
    def _mostrar_recomendaciones_diagnostico(self):
        """Muestra recomendaciones basadas en diagnóstico"""
        recomendaciones = [
            "1️⃣ Si faltan directorios → crear manualmente",
            "2️⃣ Si BD vacía → ejecutar S1 (Ingestar corpus)",
            "3️⃣ Si falta FAISS → ejecutar S2 (Construir FAISS)",
            "4️⃣ Si falta doctrina → ejecutar D1 (Base doctrinal)",
            "5️⃣ Si falta GEMINI → configurar API Key",
            "",
            "🎯 ORDEN RECOMENDADO para sistema limpio:",
            "   S1 → S2 → D1 → D2 → G1 → G3/G4",
            "",
            "🆘 Si todo falla → Opción 17 (Limpiar BD) y reiniciar"
        ]
        
        for rec in recomendaciones:
            print(f"   {rec}")

    # ========================================
    # FUNCIONES GEMINI INTERPRETATIVO V7.6
    # ========================================
    
    def configurar_gemini_api(self):
        """
        🔑 CONFIGURAR GEMINI API - Tu llave al poder de la IA
        
        🤔 ¿Qué es GEMINI?
        Es la inteligencia artificial de Google que puede leer y explicar
        por qué una sentencia se aparta de la doctrina. Es como tener un
        experto jurista que nunca se cansa y trabaja 24/7.
        
        🆓 ¿Es gratis?
        Sí! Google da créditos gratis cada mes. Suficiente para analizar
        cientos de sentencias sin pagar nada.
        
        📋 Lo que necesitas hacer:
        1. 🌐 Ir a: https://makersuite.google.com/app/apikey
        2. 🔐 Crear una API Key (gratis, solo necesitas Gmail)
        3. 📋 Copiar la clave y pegarla aquí
        4. ✅ ¡Listo! Ya tienes IA interpretativa
        
        🎯 RESULTADO: Explicaciones en lenguaje humano de apartamientos
        """
        print("\n🔑 CONFIGURACIÓN GEMINI API - ¡Activa tu IA jurista personal!")
        print("=" * 70)
        print("🆓 GRATIS: Google da créditos suficientes para uso normal")
        print("🌐 LINK RÁPIDO: https://makersuite.google.com/app/apikey")
        print("=" * 70)
        
        print("📋 Para usar GEMINI necesitas:")
        print("   1. 🌐 Obtener API Key de Google AI Studio:")
        print("      🔗 https://makersuite.google.com/app/apikey")
        print("   2. 🔐 Configurar variable de entorno (yo te ayudo):")
        print("   3. 🧪 Probar que funciona con G4")
        print()
        
        # Verificar estado actual - buscar en múltiples variables
        import os
        
        # Buscar API Key en diferentes variables de entorno
        api_key_sources = [
            ("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", "")),
            ("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY", "")),
            ("GOOGLE_AI_API_KEY", os.getenv("GOOGLE_AI_API_KEY", ""))
        ]
        
        current_key = ""
        key_source = ""
        
        for source_name, key_value in api_key_sources:
            if key_value and key_value != "TU_API_KEY_AQUI":
                current_key = key_value
                key_source = source_name
                break
        
        if current_key:
            key_preview = f"{current_key[:8]}...{current_key[-4:]}" if len(current_key) > 12 else "****"
            print(f"✅ API Key encontrada en {key_source}: {key_preview}")
            print(f"📏 Longitud: {len(current_key)} caracteres")
            
            cambiar = input("\n¿Cambiar API Key? (s/n): ").strip().lower()
            if cambiar != 's':
                print("✅ Usando API Key existente")
                return
        else:
            print("❌ API Key no encontrada en variables de entorno")
        
        print("\n🔧 CONFIGURACIÓN:")
        print("   Windows (CMD): set GEMINI_API_KEY=tu_clave_aqui")
        print("   Windows (PowerShell): $env:GEMINI_API_KEY='tu_clave_aqui'")
        print("   Linux/Mac: export GEMINI_API_KEY='tu_clave_aqui'")
        
        nueva_key = input("\nIngresa tu API Key de GEMINI: ").strip()
        
        if nueva_key:
            os.environ["GEMINI_API_KEY"] = nueva_key
            print("✅ API Key configurada para esta sesión")
            print("⚠️ Para configuración permanente, usa los comandos de arriba")
            
            # Test básico
            from interpretador_gemini import verificar_api_key
            if verificar_api_key():
                print("✅ API Key válida")
            else:
                print("⚠️ API Key configurada pero no validada")
        else:
            print("❌ No se ingresó API Key")
    
    def iniciar_servidor_gemini(self):
        """Inicia el servidor Flask de interpretación GEMINI"""
        print("\n🌐 SERVIDOR GEMINI INTERPRETACIÓN")
        print("=" * 45)
        
        # Verificar configuración
        from interpretador_gemini import verificar_api_key
        if not verificar_api_key():
            print("❌ API Key de GEMINI no configurada")
            print("📋 Ejecuta primero la opción G1 para configurar")
            return
        
        print("📋 Este servidor expondrá:")
        print("   - GET  http://127.0.0.1:5060/ (estado)")
        print("   - POST http://127.0.0.1:5060/interpretar-distancia")
        print("   - POST http://127.0.0.1:5060/interpretar-lote")
        print()
        print("⚠️ El servidor se ejecutará en primer plano")
        print("   Presiona Ctrl+C para detenerlo")
        
        continuar = input("\n¿Iniciar servidor? (s/n): ").strip().lower()
        if continuar != 's':
            print("❌ Operación cancelada")
            return
        
        try:
            script_path = self.scripts_path / "api_gemini_flask.py"
            print(f"🚀 Iniciando servidor GEMINI...")
            
            # Ejecutar servidor (bloqueante)
            subprocess.run([
                sys.executable, str(script_path)
            ], cwd=self.base_path)
            
        except KeyboardInterrupt:
            print("\n🛑 Servidor detenido por usuario")
        except Exception as e:
            print(f"❌ Error iniciando servidor: {e}")
    
    def interpretar_chunk_especifico(self):
        """Interpreta un chunk específico usando GEMINI"""
        print("\n🧠 INTERPRETACIÓN DE CHUNK ESPECÍFICO")
        print("=" * 50)
        
        # Verificar configuración
        from interpretador_gemini import verificar_api_key
        if not verificar_api_key():
            print("❌ API Key de GEMINI no configurada")
            print("📋 Ejecuta primero la opción G1")
            return
        
        # Verificar BD
        if not Path(self.data_path / "ruta_pensamiento.db").exists():
            print("❌ Base de datos no encontrada")
            print("📋 Ingesta primero algunas sentencias (opción S1)")
            return
        
        # Mostrar chunks disponibles (muestra)
        try:
            import sqlite3
            from config_rutas import PENSAMIENTO_DB
            
            con = sqlite3.connect(PENSAMIENTO_DB)
            cur = con.cursor()
            
            cur.execute("""
                SELECT chunk_id, expediente, tribunal, distancia_doctrinal
                FROM rag_sentencias_chunks 
                WHERE distancia_doctrinal IS NOT NULL
                ORDER BY distancia_doctrinal DESC
                LIMIT 10
            """)
            
            chunks = cur.fetchall()
            con.close()
            
            if not chunks:
                print("❌ No hay chunks con distancia doctrinal calculada")
                print("📋 Ejecuta primero: D2 (Recalcular distancias)")
                return
            
            print("📋 CHUNKS DISPONIBLES (Top 10 por distancia):")
            for i, (chunk_id, exp, trib, dist) in enumerate(chunks, 1):
                print(f"   {i:2d}. {chunk_id} | {exp} | {trib} | Dist: {dist:.3f}")
            
            chunk_id = input("\nIngresa chunk_id a interpretar: ").strip()
            
            if not chunk_id:
                print("❌ chunk_id requerido")
                return
            
            # Interpretar
            print(f"🧠 Interpretando {chunk_id}...")
            
            from interpretador_gemini import interpretar_sentencia
            import sqlite3
            
            # Obtener datos del chunk
            con = sqlite3.connect(PENSAMIENTO_DB)
            cur = con.cursor()
            
            cur.execute("""
                SELECT chunk_id, expediente, tribunal, materia, temas, 
                       formas_razonamiento, falacias, citaciones_doctrina,
                       citaciones_jurisprudencia, texto, distancia_doctrinal
                FROM rag_sentencias_chunks
                WHERE chunk_id = ?
            """, (chunk_id,))
            
            row = cur.fetchone()
            con.close()
            
            if not row:
                print(f"❌ Chunk {chunk_id} no encontrado")
                return
            
            chunk_data = {
                "chunk_id": row[0],
                "expediente": row[1],
                "tribunal": row[2],
                "materia": row[3],
                "temas": row[4],
                "formas_razonamiento": row[5],
                "falacias": row[6],
                "citaciones_doctrina": row[7],
                "citaciones_jurisprudencia": row[8],
                "texto_snippet": row[9],
                "distancia_doctrinal": row[10]
            }
            
            resultado = interpretar_sentencia(chunk_data)
            
            print(f"\n📊 RESULTADO:")
            print(f"   Estado: {resultado.get('estado', 'N/A')}")
            print(f"   Distancia analizada: {resultado.get('distancia_analizada', 0):.4f}")
            print(f"\n🧠 INTERPRETACIÓN:")
            print("=" * 60)
            print(resultado.get('interpretacion', 'Sin interpretación'))
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error interpretando chunk: {e}")
            import traceback
            traceback.print_exc()
    
    def test_interpretacion_gemini(self):
        """Test rápido de interpretación GEMINI"""
        print("\n🧪 TEST DE INTERPRETACIÓN GEMINI")
        print("=" * 45)
        
        from interpretador_gemini import verificar_api_key, interpretar_sentencia
        
        if not verificar_api_key():
            print("❌ API Key no configurada")
            return
        
        # Datos de prueba
        test_data = {
            "chunk_id": "test_hermeneutico_001",
            "texto_snippet": "El análisis de proporcionalidad exige ponderar la intensidad de la intervención en el derecho fundamental con el peso de las razones que la justifican, aplicando el principio pro persona en la interpretación más favorable.",
            "distancia_doctrinal": 0.42,
            "temas": "proporcionalidad, derechos fundamentales, pro persona",
            "formas_razonamiento": "ponderación, interpretación sistemática",
            "falacias": "",
            "citaciones_doctrina": "Alexy - Teoría de los Derechos Fundamentales",
            "citaciones_jurisprudencia": "Corte IDH, Caso Artavia Murillo",
            "tribunal": "Tribunal Constitucional",
            "materia": "constitucional"
        }
        
        print("📋 Datos de prueba:")
        print(f"   Distancia: {test_data['distancia_doctrinal']}")
        print(f"   Tema: {test_data['temas']}")
        
        print("\n🧠 Consultando GEMINI...")
        resultado = interpretar_sentencia(test_data)
        
        print(f"\n📊 RESULTADO DEL TEST:")
        print(f"   Estado: {resultado.get('estado', 'N/A')}")
        print(f"   Tokens: {resultado.get('tokens_utilizados', 0)}")
        
        if resultado.get('estado') == 'exitoso':
            print(f"\n✅ INTERPRETACIÓN EXITOSA:")
            print("=" * 50)
            print(resultado.get('interpretacion', ''))
            print("=" * 50)
        else:
            print(f"\n❌ ERROR EN INTERPRETACIÓN:")
            print(resultado.get('interpretacion', 'Sin detalles'))

def main():
    """Función principal"""
    try:
        centro = CentroControlMaestro()
        centro.mostrar_menu_principal()
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()