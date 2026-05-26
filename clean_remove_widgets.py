import json
from pathlib import Path

root = Path('.')
count = 0
for p in root.glob('**/*.ipynb'):
    try:
        j = json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        print('SKIP', p, 'read error', e)
        continue
    changed = False
    if 'metadata' in j and 'widgets' in j['metadata']:
        del j['metadata']['widgets']
        changed = True
    # also clean cell metadata
    if 'cells' in j:
        for c in j['cells']:
            if 'metadata' in c and 'widgets' in c['metadata']:
                del c['metadata']['widgets']
                changed = True
    # ensure nbformat fields
    if 'nbformat' not in j:
        j['nbformat'] = 4
        changed = True
    if 'nbformat_minor' not in j:
        j['nbformat_minor'] = 5
        changed = True
    if changed:
        p.write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding='utf-8')
        print('CLEANED', p)
        count += 1
print('Done. cleaned', count, 'files')
