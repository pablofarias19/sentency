@echo off
chcp 65001 >nul
cls
echo.
echo 🎛️ CENTRO DE CONTROL - SISTEMA COGNITIVO UNIFICADO
echo ==================================================
echo.
echo 📋 SELECCIONA QUÉ QUIERES HACER:
echo.
echo 📚 PROCESAR DOCUMENTOS:
echo    1. Procesar documentos nuevos (PDFs)
echo.
echo 🌐 USAR SISTEMA WEB:
echo    2. Inicio rápido (webapp básica)
echo    3. Inicio completo (todas las funcionalidades)
echo    4. Inicio mejorado (con diagnósticos)
echo.
echo 🔧 ANÁLISIS AVANZADO:
echo    5. Centro de Control Maestro (menú completo)
echo.
echo    0. Salir
echo.
set /p opcion="Ingresa tu opcion (0-5): "

if "%opcion%"=="1" call PROCESAR_DOCUMENTOS.bat
if "%opcion%"=="2" call INICIO_FACIL.bat
if "%opcion%"=="3" call iniciar_sistema.bat
if "%opcion%"=="4" call INICIO_MEJORADO.bat
if "%opcion%"=="5" goto centro_maestro
if "%opcion%"=="0" exit /b

echo.
echo ❌ Opción no válida. Intenta de nuevo.
pause
goto inicio

:centro_maestro
echo.
echo 🎛️ Iniciando Centro de Control Maestro...
call .venv\Scripts\activate.bat
cd colaborative\scripts
python centro_control_maestro.py
goto fin

:inicio
%0

:fin
echo.
echo 👋 ¡Gracias por usar el sistema!
pause >nul