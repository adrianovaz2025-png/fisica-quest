"""Recorte das questões da EsPCEx (PDF com texto). uso: python3 x3.py PDF ANO DIA OUT"""
import pymupdf, re, io, json, os, sys
import numpy as np
from PIL import Image
pdf, ANO, DIA, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
os.makedirs(OUT, exist_ok=True)
Z = 2.6
d = pymupdf.open(pdf)
FOOT = re.compile(r'INSTITUTO FEDERAL|PROCESSO SELETIVO|Quest[õo]es de \d+ a \d+|^\s*(MATEM[ÁA]TICA|L[ÍI]NGUA PORTUGUESA)\s*$|EPCE\d|Confidencial|^\s*P[áa]g\.?\s*\d|Modelo\s+[A-F]\s*$|^\s*\d{1,2}\s*$|Prova de .*Modelo|Provas de ', re.I)
HDR = re.compile(r'^\s*QUEST[ÃA]O[\s  ]*(\d{1,2})\s*$', re.I)
SHARE = re.compile(r'(?:responder|answer|As)[^0-9]{0,60}?quest(?:ões|ions)?\s*(?:de\s*|from\s*)?(\d{1,2})\s*(?:a|e|to|and|-)\s*(\d{1,2})', re.I)
SKIPPG = re.compile(r'PROPOSTA DE REDA|RASCUNHO|FOLHA DE REDA|Tabela Peri[óo]dica|INSTRU[ÇC][ÕO]ES PARA A REDA', re.I)
ALTE = re.compile(r'(?m)^\s*d\)')
pages = []
for pi, p in enumerate(d):
    W, H = p.rect.width, p.rect.height
    L = []
    for b in p.get_text('dict')['blocks']:
        if b['type']: continue
        for l in b['lines']:
            t = ''.join(s['text'] for s in l['spans'])
            if t.strip(): L.append((l['bbox'], t))
    body = [(bb, t) for bb, t in L if not ((bb[1] > H - 60 or bb[3] < 60) and FOOT.search(t))]
    imgs = [b['bbox'] for b in p.get_text('dict')['blocks'] if b['type'] == 1]
    ys = [bb[1] for bb, t in body] + [r[1] for r in imgs]; ye = [bb[3] for bb, t in body] + [r[3] for r in imgs]
    top = (min(ys) - 3) if ys else 40; bot = (max(ye) + 3) if ye else H - 40
    MID = W / 2
    right = sum(1 for bb, t in body if bb[0] > MID + 5); wide = sum(1 for bb, t in body if bb[0] < MID - 40 and bb[2] > MID + 40)
    two = right > 8 and wide < 6
    txt = p.get_text()
    pages.append(dict(W=W, H=H, top=top, bot=bot, two=two, MID=MID, L=body, skip=bool(SKIPPG.search(txt)) and not HDR.search(txt)))
# âncoras
anc = []
expect = 1
for pi, P in enumerate(pages):
    if pi == 0: continue
    for bb, t in P['L']:
        col = 1 if (P['two'] and bb[0] > P['MID'] - 5) else 0
        m = HDR.match(t)
        if m: anc.append(dict(n=int(m.group(1)), p=pi, col=col, y=bb[1])); continue
        ms = SHARE.search(t)
        if ms and int(ms.group(1)) < int(ms.group(2)) <= int(ms.group(1)) + 12:
            anc.append(dict(n=0, share=(int(ms.group(1)), int(ms.group(2))), p=pi, col=col, y=bb[1] - 2)); continue
        if re.search(r'Final da Prova|^\s*PROVA DE [A-ZÁÉÍÓÚÇÊ]+\s*$', t):
            anc.append(dict(n=0, cut=1, p=pi, col=col, y=bb[1] - 2)); continue
        if re.search(r'(?!x)x', t, re.I) and not HDR.search(t):
            anc.append(dict(n=0, share='open', p=pi, col=col, y=bb[1] - 2)); continue
        # formato antigo: número sozinho na margem esquerda (caixinha)
        if re.match(r'^\s*\d{1,2}\s*$', t) and bb[0] < 60 and not P['two']:
            anc.append(dict(n=int(t), p=pi, col=0, y=bb[1], box=1))
anc.sort(key=lambda a: (a['p'], a['col'], a['y']))
# filtra números soltos fora de sequência (tabelas, etc.)
clean = []; last = 0
for a in anc:
    if a.get('box') and a['n'] != last + 1: continue
    if a['n']: last = a['n']
    clean.append(a)
anc = clean
def xr(P, col):
    if not P['two']: return (20, P['W'] - 20)
    return (20, P['MID'] - 3) if col == 0 else (P['MID'] + 3, P['W'] - 20)
def render(p, r):
    pix = d[p].get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=r, alpha=False)
    im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    g = np.asarray(im).min(axis=2) < 160
    A = np.asarray(im).copy()
    for c in np.nonzero(g.mean(0) > 0.7)[0]: A[:, max(0, c - 1):c + 2] = 255   # bordas verticais
    for rr in np.nonzero(g.mean(1) > 0.85)[0]: A[max(0, rr - 1):rr + 2, :] = 255  # bordas horizontais
    im = Image.fromarray(A)
    a = np.asarray(im).min(axis=2) < 225; ys, xs = np.nonzero(a)
    if not len(ys): return None
    return im.crop((max(0, xs.min() - 8), max(0, ys.min() - 8), min(im.width, xs.max() + 9), min(im.height, ys.max() + 9)))
rel = []; SH = {}; OPEN = None
for i, a in enumerate(anc):
    nx = anc[i + 1] if i + 1 < len(anc) else None
    p, col, y = a['p'], a['col'], a['y'] - (9 if a.get('box') else 3)
    segs = []; txt = ''
    while True:
        P = pages[p]; x0, x1 = xr(P, col)
        stop = nx and nx['p'] == p and nx['col'] == col
        y1 = (nx['y'] - (3 if nx.get('share') else 9)) if stop else P['bot']
        r = pymupdf.Rect(x0, max(y, P['top']), x1, y1)
        if r.height > 6:
            tt = d[p].get_text('text', clip=r)
            if segs and not tt.strip(): pass
            else:
                im = render(p, r)
                if im: segs.append(im); txt += '\n' + tt
        if stop or (a['n'] and ALTE.search(txt)): break
        if P['two'] and col == 0: col = 1
        else:
            p += 1; col = 0
            if p >= len(d) or pages[p]['skip']: break
        y = pages[p]['top']
        if nx is None and p > a['p'] + 1: break
    if 'cut' in a: continue
    if a.get('share') == 'open': OPEN = (segs, txt); continue
    if 'share' in a:
        for k in range(a['share'][0], a['share'][1] + 1): SH[k] = (segs, txt)
        OPEN = None; continue
    n = a['n']
    if n not in SH and OPEN:
        if re.search(r'texto|text\b|autor|author|paragraph|par[áa]grafo|Machado|trecho', txt, re.I): SH[n] = OPEN
        else: OPEN = None
    if n in SH: segs = SH[n][0] + segs; txt = SH[n][1] + txt
    if not segs: continue
    Wt = max(s.width for s in segs); Ht = sum(s.height for s in segs) + 14 * (len(segs) - 1)
    cv = Image.new('RGB', (Wt, Ht), 'white'); yy = 0
    for s in segs: cv.paste(s, (0, yy)); yy += s.height + 14
    fn = f'f{ANO}_{n}.webp'; cv.save(os.path.join(OUT, fn), 'WEBP', quality=72, method=6)
    alts = ''.join(sorted(set(re.findall(r'(?m)^\s*([a-d])\)', txt))))
    rel.append(dict(id=f'f{ANO}_{n}', ano=ANO, dia=DIA, num=n, osz=[Wt, Ht], segs=len(segs), alts=alts, shared=n in SH, txt=txt[-1500:]))
json.dump(rel, open(os.path.join(OUT, f'rel_{ANO}_{DIA}.json'), 'w'))
print(ANO, DIA, len(rel), 'sem ABCDE:', [r['num'] for r in rel if r['alts'] != 'abcd'], 'faltando:', sorted(set(range(1, max(r['num'] for r in rel) + 1)) - {r['num'] for r in rel}))
