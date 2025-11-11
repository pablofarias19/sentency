@echo off
REM ================================================================
REM 🚀 SISTEMA DE ANÁLISIS COGNITIVO AUTORAL - INICIO ÚNICO
REM    Versión 7.7 - 11 Noviembre 2025
REM ================================================================
cls

REM Colores y formato (usando caracteres especiales de Windows)
color 0A
title Sistema Cognitivo Autoral V7.7

echo.
echo ================================================================
echo     🚀 SISTEMA DE ANÁLISIS COGNITIVO AUTORAL V7.7
echo ================================================================
echo.
echo 💡 Este es el ÚNICO comando que necesitas para iniciar el sistema
echo.

REM ================================================================
REM PASO 1: VERIFICAR ENTORNO VIRTUAL
REM ================================================================
echo [1/4] Verificando entorno virtual...
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat >nul 2>&1
    echo       ✅ Entorno virtual activado
) else (
    echo       ⚠️  No se encontró entorno virtual
    echo       💡 Ejecuta primero: python -m venv .venv
    echo       💡 Luego instala dependencias con:
    echo          .venv\Scripts\Activate.ps1
    echo          pip install flask google-generativeai sentence-transformers faiss-cpu PyMuPDF transformers torch numpy scikit-learn
    echo.
    pause
    exit /b 1
)

REM ================================================================
REM PASO 2: VERIFICAR INTEGRIDAD DEL SISTEMA
REM ================================================================
echo.
echo [2/4] Verificando integridad del sistema...
echo ================================================================

python verificar_perfiles.py

if errorlevel 1 (
    echo.
    echo       ⚠️  Se detectaron problemas en el sistema
    echo       💡 Ejecuta: python mantener_sistema.py
    echo.
    set /p continuar="¿Continuar de todas formas? (s/n): "
    if /i not "%continuar%"=="s" (
        echo.
        echo       ❌ Inicio cancelado
        pause
        exit /b 1
    )
)

REM ================================================================
REM PASO 3: VERIFICAR DOCUMENTOS PROCESADOS
REM ================================================================
echo.
echo [3/4] Verificando documentos...
if exist "colaborative\data\pdfs\general\*.pdf" (
    echo       ✅ PDFs encontrados
    echo       💡 Ubicación: colaborative\data\pdfs\general\
) else (
    echo       ⚠️  No se encontraron PDFs
    echo       💡 Coloca archivos PDF en: colaborative\data\pdfs\general\
    echo       💡 Luego ejecuta: python procesar_todo.py
)

REM ================================================================
REM PASO 4: INICIAR SERVIDOR WEB
REM ================================================================
echo.
echo [4/4] Iniciando servidor web...
echo ================================================================
echo.
echo 🌐 El sistema se iniciará en: http://127.0.0.1:5002
echo ⏰ Espera 15-20 segundos para carga completa
echo.
echo 📊 RUTAS DISPONIBLES:
echo     • http://127.0.0.1:5002/          → Consultas RAG principales
echo     • http://127.0.0.1:5002/autores   → Perfiles y comparación
echo     • http://127.0.0.1:5002/radar     → Radar cognitivo interactivo
echo     • http://127.0.0.1:5002/cognitivo → Sistema ANALYSER avanzado
echo     • http://127.0.0.1:5002/pensamiento → Análisis multi-capa
echo     • http://127.0.0.1:5002/biblioteca → Biblioteca cognitiva
echo.
echo 📖 DOCUMENTACIÓN:
echo     • LEEME_PRIMERO.md           → Guía rápida
echo     • GUIA_RAPIDA_DEFINITIVA.md  → Guía completa
echo.
echo ⏹️  Para detener el servidor: Presiona Ctrl+C
echo.
echo ================================================================
echo.

REM Abrir navegador automáticamente después de 3 segundos
start "" /B timeout /t 3 /nobreak >nul && start http://127.0.0.1:5002

REM Iniciar servidor Flask
python colaborative\scripts\end2end_webapp.py

REM Si el servidor se detiene, mostrar mensaje
echo.
echo.
echo ================================================================
echo     ⏹️  Servidor detenido
echo ================================================================
echo.
pause
