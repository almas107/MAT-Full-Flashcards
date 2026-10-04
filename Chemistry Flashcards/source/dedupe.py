"""Merge cards with identical fronts (after normalisation) within one source file.
The first occurrence keeps its place; later answers are appended with ' || ' if they add text; years are merged."""
import re, sys
def norm(s): return re.sub(r'[\s\?।,;:\-—–\'"‘’“”()]+', '', s).lower()
path = sys.argv[1]
lines = open(path, encoding='utf-8').read().split('\n')
cards, out = {}, []   # out: list of either str (header/blank) or card dict
i = 0
while i < len(lines):
    l = lines[i]
    if l.startswith('Q: '):
        q = l[3:]; a = lines[i+1][3:]; y = ''
        i += 2
        if i < len(lines) and lines[i].startswith('Y: '):
            y = lines[i][3:]; i += 1
        k = norm(q)
        if k in cards:
            c = cards[k]
            if norm(a) not in norm(c['a']):
                c['a'] += ' || ' + a
            if y:
                ys = [s.strip() for s in (c['y'] + ', ' + y).split(',') if s.strip()]
                c['y'] = ', '.join(dict.fromkeys(ys))
            print('merged:', q[:60])
        else:
            c = {'q': q, 'a': a, 'y': y}; cards[k] = c; out.append(c)
    else:
        out.append(l); i += 1
res = []
for o in out:
    if isinstance(o, dict):
        res += ['Q: ' + o['q'], 'A: ' + o['a']] + (['Y: ' + o['y']] if o['y'] else [])
    else:
        res.append(o)
open(path, 'w', encoding='utf-8').write('\n'.join(res))
