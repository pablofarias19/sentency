@echo off
cls
echo.
echo ================================================================
echo 🚀 SISTEMA RAG COGNITIVO V7.7 - INICIO AUTOMÁTICO
echo ================================================================
echo.
echo 🎉 MEJORAS V7.7 (11 NOV 2025):
echo    ✅ Vectorizador cognitivo integrado (8 rasgos completos)
echo    ✅ Verificación automática de integridad
echo    ✅ Análisis estructural de sentencias (VISTO-CONSIDERANDO-RESUELVO)
echo    ✅ Integración mejorada con GEMINI AI
echo    ✅ Sistema de mantenimiento automático
echo.

REM Activar entorno virtual
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️ Advertencia: No se encontró el entorno virtual
    echo    Continuando sin activación...
)

echo.
echo 🔧 Verificando integridad del sistema...
echo ================================================================
python verificar_perfiles.py

echo.
echo 💡 Si encontraste perfiles incompletos, ejecuta:
echo    python mantener_sistema.py
echo.
echo ================================================================
echo 🌐 Iniciando servidor web...
echo ⏰ Espera 15-20 segundos para carga completa
echo.
echo 📊 RUTAS WEB DISPONIBLES:
echo    🏠 http://127.0.0.1:5002/          → Página principal (RAG)
echo    � http://127.0.0.1:5002/autores   → Perfiles y comparación
echo    � http://127.0.0.1:5002/radar     → Radar cognitivo interactivo
echo    🧠 http://127.0.0.1:5002/cognitivo → Análisis ANALYSER
echo    🔬 http://127.0.0.1:5002/pensamiento → Análisis multi-capa
echo    📚 http://127.0.0.1:5002/biblioteca → Biblioteca cognitiva
echo.
echo 🚀 Abriendo navegador automáticamente...
echo 📖 Para ayuda completa: GUIA_RAPIDA_DEFINITIVA.md
echo ⏹️  Presiona Ctrl+C para detener el servidor
echo.
echo ================================================================
echo.

start http://127.0.0.1:5002
python colaborative/scripts/end2end_webapp.py

echo.
echo 🎉 ¡Sistema iniciado correctamente!
echo 💡 Presiona cualquier tecla para cerrar esta ventana
pause