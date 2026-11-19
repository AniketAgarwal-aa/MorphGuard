import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
reg_path = ROOT / 'models/metadata/model_registry.json'
registry = json.loads(reg_path.read_text(encoding='utf-8'))
models_map = {m['model_name']: m for m in registry.get('models', [])}

meta_dir = ROOT / 'models/metadata'
for p in meta_dir.glob('*.json'):
    if p.name == 'model_registry.json':
        continue
    m_data = json.loads(p.read_text(encoding='utf-8'))
    models_map[m_data['model_name']] = m_data

registry['models'] = list(models_map.values())
registry['total_models'] = len(registry['models'])
reg_path.write_text(json.dumps(registry, indent=2), encoding='utf-8')
print("Successfully synced all models into model_registry.json. Total models:", len(registry['models']))
