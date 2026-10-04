"""Insert/rename '# subdeck' headers in a card source so textbook cards merge into topic subdecks.
Usage: python3 regroup.py FILE 'LINE=Title' ...   (LINE is 1-based; a header line is renamed, a Q line gets a header inserted before it)"""
import sys
path, specs = sys.argv[1], sys.argv[2:]
lines = open(path, encoding='utf-8').read().split('\n')
for spec in sorted(specs, key=lambda s: -int(s.split('=', 1)[0])):
    n, title = spec.split('=', 1)
    i = int(n) - 1
    if lines[i].startswith('# '):
        lines[i] = '# ' + title
    elif lines[i].startswith('Q: '):
        lines.insert(i, '# ' + title)
    else:
        sys.exit(f'line {n} is neither header nor Q: {lines[i][:40]}')
open(path, 'w', encoding='utf-8').write('\n'.join(lines))
