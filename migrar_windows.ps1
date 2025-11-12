# ============================================================================
# SCRIPT DE MIGRACIÓN DEL SISTEMA JUDICIAL - WINDOWS
# ============================================================================

param(
    [string]$RepoOriginal = "C:\Users\USUARIO\Programacion\V4 SENTENCIA AUTORAL\V3 APP AUTORAL\App_colaborativa",
    [string]$RepoDescargado = ""
)

# Colores para output
function Write-Success { param($msg) Write-Host "✓ $msg" -ForegroundColor Green }
function Write-Error { param($msg) Write-Host "✗ $msg" -ForegroundColor Red }
function Write-Warning { param($msg) Write-Host "⚠ $msg" -ForegroundColor Yellow }
function Write-Info { param($msg) Write-Host "ℹ $msg" -ForegroundColor Cyan }
function Write-Section { param($msg) Write-Host "`n========================================" -ForegroundColor Blue; Write-Host $msg -ForegroundColor Blue; Write-Host "========================================" -ForegroundColor Blue }

# ============================================================================
# VERIFICACIONES INICIALES
# ============================================================================

Write-Section "MIGRACIÓN DEL SISTEMA JUDICIAL - WINDOWS"

Write-Info "Repositorio original: $RepoOriginal"

if (-not (Test-Path $RepoOriginal)) {
    Write-Error "Repositorio original no encontrado: $RepoOriginal"
    Write-Info "Uso: .\migrar_windows.ps1 -RepoOriginal 'ruta' -RepoDescargado 'ruta'"
    exit 1
}

if ($RepoDescargado -eq "") {
    Write-Warning "No se especificó ruta del repositorio descargado"
    $RepoDescargado = Read-Host "Ingresa la ruta donde descargaste/clonaste el repositorio sentency"
}

if (-not (Test-Path $RepoDescargado)) {
    Write-Error "Repositorio descargado no encontrado: $RepoDescargado"
    exit 1
}

Write-Success "Repositorios encontrados"

# ============================================================================
# PASO 1: CREAR BACKUP
# ============================================================================

Write-Section "PASO 1: Crear Backup"

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "$RepoOriginal" + "_backup_$timestamp"

Write-Info "Creando backup en: $backupPath"

try {
    Copy-Item -Path $RepoOriginal -Destination $backupPath -Recurse -Force
    Write-Success "Backup creado exitosamente"
} catch {
    Write-Error "Error creando backup: $_"
    exit 1
}

# Confirmar continuación
$continue = Read-Host "`n¿Continuar con la migración? (S/N)"
if ($continue -ne "S" -and $continue -ne "s") {
    Write-Warning "Migración cancelada"
    exit 0
}

# ============================================================================
# PASO 2: ELIMINAR ARCHIVOS DE AUTORES
# ============================================================================

Write-Section "PASO 2: Eliminar Archivos de Autores"

$scriptsDir = Join-Path $RepoOriginal "colaborative\scripts"

$archivosAutores = @(
    "sistema_autor_centrico.py",
    "visualizador_autor_centrico.py",
    "comparador_mentes.py",
    "gestor_unificado_autores.py",
    "detector_autor_y_metodo.py",
    "agregar_nuevo_autor.py",
    "verificar_autores.py",
    "analizador_perfiles.py",
    "ingesta_cognitiva.py",
    "ingesta_cognitiva_v3.py",
    "ingesta_enriquecida.py",
    "motor_ingesta_pensamiento.py",
    "reparar_rasgos_cognitivos.py",
    "actualizar_db_analyser.py",
    "analizador_multicapa_pensamiento.py"
)

$eliminados = 0

foreach ($archivo in $archivosAutores) {
    $rutaArchivo = Join-Path $scriptsDir $archivo
    if (Test-Path $rutaArchivo) {
        try {
            Remove-Item $rutaArchivo -Force
            Write-Success "Eliminado: $archivo"
            $eliminados++
        } catch {
            Write-Error "Error eliminando $archivo : $_"
        }
    }
}

Write-Info "Archivos de autores eliminados: $eliminados"

# ============================================================================
# PASO 3: ELIMINAR BASES DE DATOS DE AUTORES
# ============================================================================

Write-Section "PASO 3: Eliminar Bases de Datos de Autores"

$basesDir = Join-Path $RepoOriginal "colaborative\bases_rag\cognitiva"

$basesAutores = @(
    "autor_centrico.db",
    "perfiles_autorales.db",
    "multicapa_pensamiento.db",
    "pensamiento_integrado_v2.db"
)

$basesEliminadas = 0

if (Test-Path $basesDir) {
    foreach ($bd in $basesAutores) {
        $rutaBd = Join-Path $basesDir $bd
        if (Test-Path $rutaBd) {
            try {
                Remove-Item $rutaBd -Force
                Write-Success "Eliminada: $bd"
                $basesEliminadas++
            } catch {
                Write-Error "Error eliminando $bd : $_"
            }
        }
    }
}

Write-Info "Bases de datos eliminadas: $basesEliminadas"

# ============================================================================
# PASO 4: COPIAR ARCHIVOS JUDICIALES
# ============================================================================

Write-Section "PASO 4: Copiar Archivos del Sistema Judicial"

$origenScripts = Join-Path $RepoDescargado "App_colaborativa\colaborative\scripts"
$destinoScripts = Join-Path $RepoOriginal "colaborative\scripts"

$archivosJudiciales = @(
    # Fase 1
    "inicializar_bd_judicial.py",
    "ingesta_sentencias_judicial.py",
    "extractor_metadata_argentina.py",
    "schema_juez_centrico_arg.sql",

    # Fase 2
    "analizador_pensamiento_judicial_arg.py",
    "procesador_sentencias_completo.py",
    "agregador_perfiles_jueces.py",

    # Fase 3
    "analizador_lineas_jurisprudenciales.py",
    "extractor_citas_jurisprudenciales.py",
    "analizador_redes_influencia.py",

    # Fase 4
    "motor_predictivo_judicial.py",

    # Fase 5
    "generador_informes_judicial.py",
    "sistema_preguntas_judiciales.py",
    "motor_respuestas_judiciales.py",

    # Adaptador y webapp
    "analyser_judicial_adapter.py",
    "webapp_rutas_judicial.py"
)

$copiados = 0

foreach ($archivo in $archivosJudiciales) {
    $origen = Join-Path $origenScripts $archivo
    $destino = Join-Path $destinoScripts $archivo

    if (Test-Path $origen) {
        try {
            Copy-Item -Path $origen -Destination $destino -Force
            Write-Success "Copiado: $archivo"
            $copiados++
        } catch {
            Write-Error "Error copiando $archivo : $_"
        }
    } else {
        Write-Warning "No encontrado: $archivo"
    }
}

Write-Info "Archivos judiciales copiados: $copiados"

# ============================================================================
# PASO 5: COPIAR SCRIPTS DE UTILIDAD
# ============================================================================

Write-Section "PASO 5: Copiar Scripts de Utilidad"

$origenRaiz = Join-Path $RepoDescargado "App_colaborativa"

$utilidad = @(
    "limpiar_sistema_autores.py",
    "integrar_sistema_judicial.py",
    "limpieza_final_repositorio.py"
)

$utilidadCopiados = 0

foreach ($archivo in $utilidad) {
    $origen = Join-Path $origenRaiz $archivo
    $destino = Join-Path $RepoOriginal $archivo

    if (Test-Path $origen) {
        try {
            Copy-Item -Path $origen -Destination $destino -Force
            Write-Success "Copiado: $archivo"
            $utilidadCopiados++
        } catch {
            Write-Error "Error copiando $archivo : $_"
        }
    }
}

Write-Info "Scripts de utilidad copiados: $utilidadCopiados"

# ============================================================================
# PASO 6: COPIAR DOCUMENTACIÓN
# ============================================================================

Write-Section "PASO 6: Copiar Documentación"

$docs = @(
    @{Origen="README.md"; Destino=".."},
    @{Origen="PLAN_MIGRACION_SISTEMA_JUDICIAL.md"; Destino=".."},
    @{Origen="LIMPIEZA_FINAL.md"; Destino=".."},
    @{Origen="PASOS_FINALES.md"; Destino=".."},
    @{Origen="verificar_migracion_completa.py"; Destino=".."}
)

$docsFases = @(
    "FASE1_README.md",
    "FASE2_README.md",
    "FASE3_README.md",
    "FASE4_README.md",
    "FASE5_README.md",
    "PROPUESTA_AJUSTADA_JUECES_ARG.md"
)

$docsCopiados = 0

# Docs en raíz
foreach ($doc in $docs) {
    $origen = Join-Path $RepoDescargado $doc.Origen
    $destinoDir = Join-Path $RepoOriginal $doc.Destino
    $destino = Join-Path $destinoDir (Split-Path $doc.Origen -Leaf)

    if (Test-Path $origen) {
        try {
            Copy-Item -Path $origen -Destination $destino -Force
            Write-Success "Copiado: $($doc.Origen)"
            $docsCopiados++
        } catch {
            Write-Error "Error copiando $($doc.Origen) : $_"
        }
    }
}

# Docs de fases
foreach ($doc in $docsFases) {
    $origen = Join-Path $RepoDescargado "App_colaborativa\$doc"
    $destino = Join-Path $RepoOriginal $doc

    if (Test-Path $origen) {
        try {
            Copy-Item -Path $origen -Destination $destino -Force
            Write-Success "Copiado: $doc"
            $docsCopiados++
        } catch {
            Write-Error "Error copiando $doc : $_"
        }
    }
}

Write-Info "Documentación copiada: $docsCopiados"

# ============================================================================
# PASO 7: INTEGRAR WEBAPP
# ============================================================================

Write-Section "PASO 7: Integrar Webapp"

$integrador = Join-Path $RepoOriginal "integrar_sistema_judicial.py"

if (Test-Path $integrador) {
    $continueIntegrar = Read-Host "¿Ejecutar script de integración de webapp? (S/N)"

    if ($continueIntegrar -eq "S" -or $continueIntegrar -eq "s") {
        try {
            Set-Location $RepoOriginal
            python $integrador
            Write-Success "Webapp integrada"
        } catch {
            Write-Error "Error integrando webapp: $_"
        }
    } else {
        Write-Warning "Integración de webapp omitida"
    }
}

# ============================================================================
# REPORTE FINAL
# ============================================================================

Write-Section "REPORTE FINAL"

Write-Info "`nEstadísticas de migración:"
Write-Host "  Archivos de autores eliminados: $eliminados" -ForegroundColor Cyan
Write-Host "  Bases de datos eliminadas: $basesEliminadas" -ForegroundColor Cyan
Write-Host "  Archivos judiciales copiados: $copiados" -ForegroundColor Cyan
Write-Host "  Scripts de utilidad copiados: $utilidadCopiados" -ForegroundColor Cyan
Write-Host "  Documentación copiada: $docsCopiados" -ForegroundColor Cyan

Write-Info "`nUbicaciones:"
Write-Host "  Repositorio original: $RepoOriginal" -ForegroundColor Cyan
Write-Host "  Backup creado en: $backupPath" -ForegroundColor Cyan

Write-Success "`n✅ MIGRACIÓN COMPLETADA"

Write-Info "`nPróximos pasos:"
Write-Host "  1. Verificar migración:" -ForegroundColor Yellow
Write-Host "     cd '$RepoOriginal\..'"-ForegroundColor Gray
Write-Host "     python verificar_migracion_completa.py" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Inicializar sistema:" -ForegroundColor Yellow
Write-Host "     cd '$RepoOriginal\colaborative\scripts'" -ForegroundColor Gray
Write-Host "     python inicializar_bd_judicial.py" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Iniciar webapp:" -ForegroundColor Yellow
Write-Host "     python end2end_webapp.py" -ForegroundColor Gray
Write-Host ""

Write-Info "Presiona Enter para salir..."
Read-Host
