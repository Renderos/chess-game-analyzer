# Uso: python3 build.py moves.json notes.json meta.json template.html salida.html
# notes.json: {"1": {"note": "...", "cls": "teoria"}, ...}  (cls opcional = override)
# meta.json:  {"title": "...", "h1": "...", "keys_html": "<p><b>Apertura:</b> ...</p>..."}
import json, sys
D = json.load(open(sys.argv[1])); notes = json.load(open(sys.argv[2])); meta = json.load(open(sys.argv[3]))
def auto(d):
    if d['isbest']: return 'mejor'
    l = d['loss']
    return 'excelente' if l < 2 else 'buena' if l < 5 else 'imprecision' if l < 10 else 'error' if l < 20 else 'grave'
for i, d in enumerate(D[1:], 1):
    n = notes.get(str(i), {})
    d['cls'] = n.get('cls') or auto(d); d['note'] = n.get('note', '')
t = open(sys.argv[4]).read()
t = (t.replace('__DATA__', json.dumps(D, ensure_ascii=False)).replace('__TITLE__', meta['title'])
      .replace('__H1__', meta['h1']).replace('__KEYS__', meta['keys_html']))
open(sys.argv[5], 'w').write(t)
from collections import Counter
for c, name in ((1, 'Blancas'), (0, 'Negras')):
    print(name, dict(Counter(d['cls'] for i, d in enumerate(D[1:], 1) if i % 2 == c)))
