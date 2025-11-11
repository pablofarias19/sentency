# -*- coding: utf-8 -*-
"""
Modelo Cognitivo Persistente - Sistema ANALYSER
Almacena parámetros y configuración del análisis cognitivo
"""

import pickle
import json
from datetime import datetime
from pathlib import Path

# Configuración del modelo cognitivo
COGNITIVE_MODEL_CONFIG = {
    "version": "1.0.0",
    "created": datetime.now().isoformat(),
    "description": "Modelo cognitivo para análisis jurídico especializado",
    
    # Pesos para diferentes rasgos cognitivos
    "weights": {
        "formalismo": 1.0,
        "creatividad": 1.2,
        "dogmatismo": 0.8,
        "empirismo": 1.1,
        "interdisciplinariedad": 1.3,
        "nivel_abstraccion": 1.0,
        "complejidad_sintactica": 0.9,
        "uso_jurisprudencia": 1.1
    },
    
    # Umbrales para clasificación de tipos de pensamiento
    "thresholds": {
        "formalista": 0.3,
        "realista": 0.2,
        "interpretativo": 0.15,
        "tradicionalista": 0.1,
        "interdisciplinario": 0.05
    },
    
    # Configuración de embeddings
    "embedding_config": {
        "model_name": "all-mpnet-base-v2",
        "dimension": 768,
        "normalize": True
    },
    
    # Parámetros de análisis
    "analysis_params": {
        "min_text_length": 100,
        "max_sample_length": 1000,
        "enable_author_detection": True,
        "enable_year_detection": True,
        "enable_title_detection": True
    }
}

# Guardar configuración
model_path = Path(__file__).parent.parent / "models" / "cognitive_model.pkl"
model_path.parent.mkdir(parents=True, exist_ok=True)

with open(model_path, 'wb') as f:
    pickle.dump(COGNITIVE_MODEL_CONFIG, f)

print(f"✅ Modelo cognitivo guardado en: {model_path}")

# También guardar como JSON para legibilidad
json_path = model_path.with_suffix('.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(COGNITIVE_MODEL_CONFIG, f, indent=2, ensure_ascii=False)

print(f"✅ Configuración JSON guardada en: {json_path}")