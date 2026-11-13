"""Recorte das questões da EPCAR (PDF A4 com 2 colunas, moldura fixa).
uso: python3 x3_epcar.py PDF ANO OUT
Gera OUT/ep{ANO}_{n}.webp e OUT/rel_{ANO}.json (id, num, txt, osz).
Cada questão = seu trecho; se citar Texto I..IV (ou tiver 'Direction' cobrindo-a) leva o texto junto (empilhado em cima)."""
import pymupdf, re, io, json, os, sys
import numpy as np
from PIL import Image

pdf, ANO, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
os.makedirs(OUT, exist_ok=True)
Z = 2.6
d = pymupdf.open(pdf)
TOP, BOT = 40, 813
COLS = {0: (27, 294), 1: (300, 568)}
QH = re.compile(r'^\s*(\d{2})\s*-\s')
TX = re.compile(r'^\s*TEXTO\s+(I{1,3}|IV)\s*$')
DIR = re.compile(r'Direction:\s*(?:Consider|Read)\s+(?:the\s+)?[Tt]ext[s]?\s+([IVX]+(?:\s*(?:and|,|&)\s*[IVX]+)*)\s+to\s+answer\s+questions?\s+(\d+)(?:\s+to\s+(\d+))?', re.I)
ROM = {'I': 1, 'II': 2, 'III': 3, 'IV': 4}

anc = []   # (page, col, y, kind, data)
lastq = len(d)
for pi, p in enumerate(d):
    if pi == 0: continue
    full = p.get_text()
    if re.search(r'PROVA DE REDA', full): lastq = pi; break
    MID = p.rect.width / 2
    for b in p.get_text('dict')['blocks']:
        if b['type']: continue
        for l in b['lines']:
            t = ''.join(s['text'] for s in l['spans']).strip()
            y = l['bbox'][1]
            if y < TOP - 2: continue
            col = 1 if l['bbox'][0] > MID else 0
            x0 = l['bbox'][0] - COLS[col][0]
            if x0 < 8 and QH.match(t):
                anc.append((pi, col, y - 3, 'Q', int(QH.match(t).group(1))))
            elif TX.match(t):
                anc.append((pi, col, y - 3, 'T', ROM[TX.match(t).group(1)]))
            elif x0 < 8 and DIR.search(t):
                m = DIR.search(t)
                nums = [ROM[x] for x in re.findall(r'[IVX]+', m.group(1))]
                a, z = int(m.group(2)), int(m.group(3) or m.group(2))
                anc.append((pi, col, y - 3, 'D', (nums, a, z)))
anc.sort(key=lambda a: (a[0], a[1], a[2]))

pix = {}
def page_img(pi):
    if pi not in pix:
        p = d[pi]
        pm = p.get_pixmap(matrix=pymupdf.Matrix(Z, Z), colorspace=pymupdf.csGRAY)
        a = np.frombuffer(pm.samples, np.uint8).reshape(pm.h, pm.w).copy()
        # apaga RASCUNHO
        for b in p.get_text('dict')['blocks']:
            if b['type']: continue
            for l in b['lines']:
                if 'RASCUNHO' in ''.join(s['text'] for s in l['spans']):
                    x0, y0, x1, y1 = [int(v * Z) for v in l['bbox']]
                    a[max(0, y0 - 4):y1 + 4, max(0, x0 - 4):x1 + 4] = 255
        pix[pi] = a
    return pix[pi]

def piece(pi, col, y0, y1):
    a = page_img(pi)
    x0, x1 = [int(v * Z) for v in COLS[col]]
    sub = a[int(max(y0, TOP) * Z):int(min(y1, BOT) * Z), x0:x1]
    if sub.shape[0] < 4: return None
    rows = np.where((sub < 200).sum(1) > 0)[0]
    if len(rows) == 0: return None
    r0, r1 = max(0, rows[0] - 6), min(sub.shape[0], rows[-1] + 8)
    return sub[r0:r1]

def segment(i):
    pi, col, y, kind, data = anc[i]
    if i + 1 < len(anc):
        npi, ncol, ny = anc[i + 1][:3]
    else:
        npi, ncol, ny = lastq, 0, TOP
    out = []
    cur = (pi, col); first = True
    while True:
        y0 = y if first else TOP
        if cur == (npi, ncol):
            y1 = ny - 2
        else:
            y1 = BOT
        if y1 > y0 + 3:
            im = piece(cur[0], cur[1], y0, y1)
            if im is not None: out.append(im)
        if cur == (npi, ncol): break
        cur = (cur[0], 1) if cur[1] == 0 else (cur[0] + 1, 0)
        first = False
        if cur[0] > npi or (cur[0] == npi and cur[1] > ncol): break
    return out

def seg_text(i):
    pi, col, y, kind, data = anc[i]
    if i + 1 < len(anc): npi, ncol, ny = anc[i + 1][:3]
    else: npi, ncol, ny = lastq, 0, TOP
    s = []
    cur = (pi, col)
    while True:
        p = d[cur[0]]
        for b in p.get_text('dict')['blocks']:
            if b['type']: continue
            for l in b['lines']:
                yy = l['bbox'][1]; cc = 1 if l['bbox'][0] > p.rect.width / 2 else 0
                if cc != cur[1]: continue
                lo = y if cur == (pi, col) else TOP
                hi = ny - 2 if cur == (npi, ncol) else BOT
                if lo <= yy + 1 < hi + 2: s.append(''.join(sp['text'] for sp in l['spans']))
        if cur == (npi, ncol): break
        cur = (cur[0], 1) if cur[1] == 0 else (cur[0] + 1, 0)
        if cur[0] > npi or (cur[0] == npi and cur[1] > ncol): break
    return ' '.join(s)

def stack(parts):
    W = max(p.shape[1] for p in parts)
    gap = 14
    H = sum(p.shape[0] for p in parts) + gap * (len(parts) - 1)
    canvas = np.full((H, W), 255, np.uint8)
    y = 0
    for p in parts:
        canvas[y:y + p.shape[0], :p.shape[1]] = p
        y += p.shape[0] + gap
    return canvas

texts = {}      # numero do texto -> lista de partes (o mais recente)
dirs = []       # (lista de textos, a, z, partes)
for i, (pi, col, y, kind, data) in enumerate(anc):
    if kind == 'T': texts[data] = segment(i)
    elif kind == 'D':
        nums, a, z = data
        if len(nums) == 1:
            texts[('E', nums[0])] = segment(i); parts = texts[('E', nums[0])]
        else:
            parts = [p for k in nums for p in texts.get(('E', k), [])]
        dirs.append((nums, a, z, parts))

rel = []; seen = set()
for i, (pi, col, y, kind, data) in enumerate(anc):
    if kind != 'Q': continue
    n = data
    if n in seen: continue
    seen.add(n)
    own = segment(i); stem = seg_text(i)
    pre = []
    for nums, a, z, parts in dirs:
        if a <= n <= z: pre += parts
    if not pre and n >= 33 or (n >= 33 and not any(a <= n <= z for _, a, z, _ in dirs)):
        refs = sorted({ROM[x] for x in re.findall(r'[Tt]exto[s]?\s+(I{1,3}|IV)\b', stem)})
        if not refs and i and anc[i-1][3] == 'T': refs = [anc[i-1][4]]
        for r in refs:
            if r in texts: pre += texts[r]
    parts = pre + own
    if not parts: print('SEM CONTEUDO', n); continue
    im = Image.fromarray(stack(parts))
    fn = f'ep{ANO}_{n}.webp'
    im.save(os.path.join(OUT, fn), 'WEBP', quality=82, method=6)
    rel.append(dict(id=f'ep{ANO}_{n}', num=n, txt=stem[:1500], osz=[im.width, im.height], com_texto=bool(pre)))
rel.sort(key=lambda r: r['num'])
json.dump(rel, open(os.path.join(OUT, f'rel_{ANO}.json'), 'w'), ensure_ascii=False)
print(ANO, len(rel), 'questoes; faltando:', sorted(set(range(1, 49)) - seen))
