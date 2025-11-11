@echo off
echo.
echo 📄 PROCESADOR DE DOCUMENTOS - RAPIDO Y SIMPLE
echo ============================================
echo.
echo 📁 PASO 1: ¿Tienes PDFs nuevos para procesar?
echo    - SI: Copia los PDFs a: colaborative\data\pdfs\general\
echo    - NO: Presiona ENTER para continuar
echo.
pause

echo.
echo ✅ Activando entorno virtual...
call .venv\Scripts\activate.bat

echo.
echo 🧠 PROCESANDO DOCUMENTOS...
echo ⏰ Esto puede tardar 1-3 minutos dependiendo del tamaño
echo.

python colaborative/scripts/ingesta_cognitiva.py

echo.
echo ✅ PROCESAMIENTO COMPLETADO
echo.
echo 🎯 ARCHIVOS DISPONIBLES AHORA:
python -c "
import os
pdfs_path = 'colaborative/data/pdfs/general'
if os.path.exists(pdfs_path):
    pdfs = [f for f in os.listdir(pdfs_path) if f.endswith('.pdf')]
    for i, pdf in enumerate(pdfs, 1):
        print(f'   {i}. {pdf}')
else:
    print('   ❌ No se encontró la carpeta de PDFs')
"

echo.
echo 🌐 ¿Quieres iniciar el sistema web ahora? (S/N)
set /p respuesta="> "
if /i "%respuesta%"=="S" (
    call INICIO_FACIL.bat
) else (
    echo ✅ Procesamiento completado. Usa INICIO_FACIL.bat cuando quieras usar el sistema.
)

pause