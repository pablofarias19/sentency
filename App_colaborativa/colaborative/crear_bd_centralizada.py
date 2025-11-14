#!/usr/bin/env python3
"""
Script de Creación de Base de Datos Centralizada
=================================================

Crea la base de datos única centralizada (judicial_system.db) con
todas las tablas necesarias para el sistema judicial argentino.

Esta BD reemplaza a todas las BDs fragmentadas anteriores:
- juez_centrico_arg.db
- metadatos.db
- perfiles.db
- cognitivo.db
- etc.

Versión: 1.0
Fecha: 2025-11-14
Autor: Sistema de Análisis Judicial Argentino
"""

import sqlite3
import sys
from pathlib import Path

# Importar configuración centralizada
try:
    from config import DATABASE_PATH, ensure_directories
except ImportError:
    print("ERROR: No se pudo importar config.py")
    print("Asegúrese de ejecutar este script desde el directorio colaborative/")
    sys.exit(1)


def crear_bd_centralizada():
    """
    Crea la base de datos centralizada con todas las tablas del sistema
    """

    print("\n" + "=" * 80)
    print(" CREACIÓN DE BASE DE DATOS CENTRALIZADA - SISTEMA JUDICIAL ARGENTINO")
    print("=" * 80 + "\n")

    # Asegurar que los directorios existen
    ensure_directories()

    # Verificar si la BD ya existe
    if DATABASE_PATH.exists():
        respuesta = input(f"\n⚠️  La BD ya existe en: {DATABASE_PATH}\n¿Desea recrearla? (s/N): ")
        if respuesta.lower() != 's':
            print("❌ Operación cancelada")
            return False

        # Backup de BD existente
        backup_path = DATABASE_PATH.with_suffix('.db.backup')
        print(f"\n📦 Creando backup en: {backup_path}")
        DATABASE_PATH.rename(backup_path)

    # Crear conexión
    print(f"\n🔧 Creando nueva BD en: {DATABASE_PATH}")
    conexion = sqlite3.connect(str(DATABASE_PATH))
    cursor = conexion.cursor()

    try:
        # =====================================================================
        # TABLA PRINCIPAL: SENTENCIAS POR JUEZ ARGENTINO
        # =====================================================================

        print("\n📋 Creando tabla: sentencias_por_juez_arg")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentencias_por_juez_arg (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                -- Identificación única
                sentencia_id TEXT UNIQUE NOT NULL,
                juez TEXT NOT NULL,
                archivo_original TEXT,

                -- Metadata temporal
                fecha_sentencia DATE,
                fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                -- Metadata del expediente
                expediente TEXT,
                caratula TEXT,
                fuero TEXT,
                instancia TEXT,
                jurisdiccion TEXT,
                tribunal TEXT,
                secretaria INTEGER,

                -- Tipo de sentencia
                tipo_sentencia TEXT,  -- Definitiva, Interlocutoria, Homologatoria
                tipo_proceso TEXT,    -- Ordinario, Sumarísimo, Ejecutivo, etc.
                materia TEXT,         -- Civil, Laboral, Penal, etc.
                submateria TEXT,      -- Daños, Divorcio, Despido, etc.

                -- Partes
                actor TEXT,
                demandado TEXT,
                terceros TEXT,

                -- Resultado
                resultado TEXT,           -- Hace lugar, Rechaza, Hace lugar parcial
                condena_costas TEXT,      -- Al actor, Al demandado, Por su orden
                monto_condena REAL,       -- Monto en pesos (si aplica)

                -- Composición del tribunal
                juez_ponente TEXT,
                jueces_firmantes TEXT,    -- JSON list
                votos_disidentes TEXT,    -- JSON list
                votos_concurrentes TEXT,  -- JSON list

                -- Contenido
                texto_completo TEXT,
                ruta_chunks TEXT,         -- Ruta donde se guardaron los chunks

                -- Análisis cognitivo
                perfil_cognitivo TEXT,           -- JSON con perfil cognitivo del juez
                razonamientos_identificados TEXT, -- JSON list
                falacias_detectadas TEXT,        -- JSON list

                -- Referencias normativas
                normas_citadas TEXT,         -- JSON list
                jurisprudencia_citada TEXT,  -- JSON list
                doctrina_citada TEXT,        -- JSON list
                tratados_citados TEXT,       -- JSON list

                -- Técnicas jurídicas aplicadas
                tests_aplicados TEXT,        -- JSON list (ej: test de proporcionalidad)
                principios_invocados TEXT,   -- JSON list

                -- Métricas de calidad
                complejidad_argumental REAL,     -- 0.0 a 1.0
                extension_palabras INTEGER,
                claridad_redaccion REAL,         -- 0.0 a 1.0
                solidez_argumentativa REAL,      -- 0.0 a 1.0
                innovacion_juridica REAL,        -- 0.0 a 1.0
                impacto_estimado REAL,           -- 0.0 a 1.0

                -- Predicción
                factores_decision TEXT,          -- JSON con factores que influyeron
                prediccion_confianza REAL,       -- 0.0 a 1.0

                -- Relaciones procesales
                sentencia_previa TEXT,           -- ID de sentencia de instancia anterior
                sentencia_posterior TEXT,        -- ID de sentencia en alzada
                recursos_interpuestos TEXT,      -- JSON list
                estado_procesal TEXT,            -- Firme, Apelada, En trámite, etc.

                -- Tags y clasificación
                tags_tematicos TEXT,             -- JSON list
                linea_jurisprudencial_id INTEGER,

                -- Profesionales intervinientes
                abogados TEXT DEFAULT '[]',      -- JSON list
                peritos TEXT DEFAULT '[]',       -- JSON list

                -- Índices
                FOREIGN KEY (linea_jurisprudencial_id) REFERENCES lineas_jurisprudenciales(id)
            )
        """)

        # Índices para optimizar búsquedas
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_juez
            ON sentencias_por_juez_arg(juez)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_fecha_sentencia
            ON sentencias_por_juez_arg(fecha_sentencia)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_materia
            ON sentencias_por_juez_arg(materia)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tribunal
            ON sentencias_por_juez_arg(tribunal)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sentencia_id
            ON sentencias_por_juez_arg(sentencia_id)
        """)

        # =====================================================================
        # TABLA: PERFILES JUDICIALES ARGENTINOS
        # =====================================================================

        print("📋 Creando tabla: perfiles_judiciales_argentinos")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS perfiles_judiciales_argentinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                -- Identificación
                juez TEXT UNIQUE NOT NULL,
                tribunal TEXT,
                jurisdiccion TEXT,

                -- Estadísticas básicas
                total_sentencias INTEGER DEFAULT 0,
                fecha_primera_sentencia DATE,
                fecha_ultima_sentencia DATE,

                -- Perfil cognitivo agregado
                perfil_cognitivo TEXT,  -- JSON con perfil promedio

                -- Patrones de decisión
                patrones_decision TEXT,     -- JSON
                tendencias_materia TEXT,    -- JSON por materia

                -- Métricas agregadas
                complejidad_promedio REAL,
                claridad_promedio REAL,
                solidez_promedio REAL,
                innovacion_promedio REAL,

                -- Estilo judicial
                frecuencia_citas_doctrina REAL,
                frecuencia_citas_jurisprudencia REAL,
                frecuencia_votos_disidentes REAL,

                -- Análisis temporal
                evolucion_temporal TEXT,  -- JSON con evolución de métricas

                -- Metadata
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # =====================================================================
        # TABLA: PERFILES COGNITIVOS
        # =====================================================================

        print("📋 Creando tabla: perfiles_cognitivos")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS perfiles_cognitivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                -- Relación con sentencia
                sentencia_id TEXT,
                juez TEXT,

                -- Análisis cognitivo
                tipo_razonamiento TEXT,        -- Deductivo, Inductivo, Analógico, etc.
                nivel_abstraccion TEXT,        -- Concreto, Intermedio, Abstracto
                enfoque_argumentacion TEXT,    -- Formalista, Realista, Pragmático

                -- Sesgos detectados
                sesgos_identificados TEXT,     -- JSON list

                -- Complejidad cognitiva
                profundidad_analisis INTEGER,  -- Niveles de análisis
                amplitud_consideraciones INTEGER,

                -- Metadata
                fecha_analisis TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                confianza_analisis REAL,

                FOREIGN KEY (sentencia_id) REFERENCES sentencias_por_juez_arg(sentencia_id)
            )
        """)

        # =====================================================================
        # TABLA: LÍNEAS JURISPRUDENCIALES
        # =====================================================================

        print("📋 Creando tabla: lineas_jurisprudenciales")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lineas_jurisprudenciales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                -- Identificación
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT,
                materia TEXT,

                -- Sentencias que conforman la línea
                sentencias_ids TEXT,  -- JSON list de sentencia_ids

                -- Caracterización
                criterio_unificador TEXT,
                doctrina_aplicada TEXT,

                -- Evolución
                fecha_inicio DATE,
                fecha_ultima_actualizacion DATE,
                estado TEXT,  -- Vigente, Modificada, Superada

                -- Metadata
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # =====================================================================
        # TABLA: REDES DE INFLUENCIA JUDICIAL
        # =====================================================================

        print("📋 Creando tabla: redes_influencia_judicial")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS redes_influencia_judicial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                -- Nodos de la red
                juez_origen TEXT,
                juez_destino TEXT,

                -- Métricas de influencia
                citas_directas INTEGER DEFAULT 0,
                citas_indirectas INTEGER DEFAULT 0,
                coincidencia_criterios REAL,

                -- Metadata
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # =====================================================================
        # TABLA: FACTORES PREDICTIVOS
        # =====================================================================

        print("📋 Creando tabla: factores_predictivos")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS factores_predictivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                -- Contexto
                juez TEXT,
                materia TEXT,
                tipo_proceso TEXT,

                -- Factores
                factor_nombre TEXT,
                factor_peso REAL,
                factor_descripcion TEXT,

                -- Validación
                precisión_historica REAL,
                casos_evaluados INTEGER,

                -- Metadata
                fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # =====================================================================
        # TABLA: METADATOS (para compatibilidad con sistema anterior)
        # =====================================================================

        print("📋 Creando tabla: metadatos")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id TEXT UNIQUE NOT NULL,
                tipo TEXT,  -- sentencia, perfil, etc.
                metadata TEXT,  -- JSON con metadata adicional
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # =====================================================================
        # CONFIRMAR CAMBIOS
        # =====================================================================

        conexion.commit()

        # Verificar tablas creadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tablas = cursor.fetchall()

        print("\n✅ Base de datos creada exitosamente!")
        print(f"\n📊 Tablas creadas ({len(tablas)}):")
        for tabla in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla[0]}")
            count = cursor.fetchone()[0]
            print(f"   • {tabla[0]}: {count} registros")

        print(f"\n📍 Ubicación: {DATABASE_PATH}")
        print(f"📏 Tamaño: {DATABASE_PATH.stat().st_size / 1024:.2f} KB")

        print("\n" + "=" * 80)
        print(" SIGUIENTE PASO: Ejecutar script de migración de datos")
        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n❌ Error al crear la BD: {e}")
        conexion.rollback()
        return False

    finally:
        conexion.close()


def verificar_integridad():
    """Verifica la integridad de la BD creada"""

    if not DATABASE_PATH.exists():
        print(f"❌ BD no encontrada en: {DATABASE_PATH}")
        return False

    conexion = sqlite3.connect(str(DATABASE_PATH))
    cursor = conexion.cursor()

    try:
        # Verificar que las tablas principales existen
        tablas_requeridas = [
            'sentencias_por_juez_arg',
            'perfiles_judiciales_argentinos',
            'perfiles_cognitivos',
            'lineas_jurisprudenciales',
            'redes_influencia_judicial',
            'factores_predictivos',
            'metadatos'
        ]

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas_existentes = [t[0] for t in cursor.fetchall()]

        faltantes = set(tablas_requeridas) - set(tablas_existentes)

        if faltantes:
            print(f"❌ Faltan tablas: {', '.join(faltantes)}")
            return False

        print("✅ Integridad verificada - Todas las tablas presentes")
        return True

    except Exception as e:
        print(f"❌ Error al verificar integridad: {e}")
        return False

    finally:
        conexion.close()


if __name__ == "__main__":
    print("\n🚀 Iniciando creación de base de datos centralizada...\n")

    if crear_bd_centralizada():
        print("\n🔍 Verificando integridad...")
        if verificar_integridad():
            print("\n✅ ¡Proceso completado exitosamente!")
            print("\nPuede ahora:")
            print("  1. Migrar datos existentes (si los hay)")
            print("  2. Ejecutar scripts de ingesta")
            print("  3. Iniciar la webapp")
        else:
            print("\n⚠️  Advertencia: Verificación de integridad falló")
            sys.exit(1)
    else:
        print("\n❌ Fallo en la creación de la BD")
        sys.exit(1)
