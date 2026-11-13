"""uso: python3 build_epcar.py ANO WORK JSON   (WORK = out_ANO do x3_epcar.py; JSON = epcar_ANO.json do pedido_5)"""
import json, re, shutil, sys, unicodedata
Q = '/home/claude/fisica-quest/q/'
ANO = int(sys.argv[1]); WORK = sys.argv[2]; J = json.load(open(sys.argv[3], encoding='utf-8'))
rel = json.load(open(f'{WORK}/rel_{ANO}.json'))
def norm(s): return unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode()
def disc(n):
    for d in J['dias']:
        for x in d['disciplinas']:
            if x['de'] <= n <= x['ate']: return x
    raise KeyError(n)
def tema_mat(txt):
    t = norm(txt)
    for c, rx in [('EST', r'probabilidade|media aritmetica|mediana|moda\b|desvio|pesquisa|grafico de barras|tabela'),
                  ('FUN', r'funcao|parabola|f\(x\)|vertice|zeros da'),
                  ('GEO', r'triangulo|circunferencia|quadrado|retangul|angulo|area|perimetro|volume|cilindro|esfera|poligono|losango|trapezio'),
                  ('PRO', r'progressao|razao|proporc|porcent|juros|regra de tres')]:
        if re.search(rx, t): return c
    return 'ARI'
out = {'linguagens': [], 'matematica': []}
for r in rel:
    n = r['num']; g = J['gabarito'][str(n)]; dd = disc(n)
    lin = dd['area'] == 'LIN'
    tema = ('ING' if dd['nome'].startswith('Ing') else 'POR') if lin else tema_mat(r['txt'])
    q = dict(id=r['id'], ano=ANO, num=n, dia=1, banca='epcar', area='LIN' if lin else 'MAT', lg='', parts=[],
             alts=[{'l': l, 'h': ''} for l in 'ABCD'], orig=r['id'] + '.webp', osz=r['osz'], modo='img',
             gab=None if g == 'ANULADA' else g, gsrc='oficial', tema=tema)
    if g == 'ANULADA': q['anulada'] = True
    out['linguagens' if lin else 'matematica'].append(q)
    shutil.copy(f"{WORK}/{r['id']}.webp", Q + 'orig/' + r['id'] + '.webp')
for fn, add in out.items():
    raw = open(Q + fn + '.json', encoding='utf-8').read(); a = json.loads(raw)
    a = [x for x in a if not (x.get('banca') == 'epcar' and x.get('ano') == ANO)] + add
    compact = '": ' not in raw[:800]
    open(Q + fn + '.json', 'w', encoding='utf-8').write(json.dumps(a, ensure_ascii=False, separators=(',', ':')) if compact else json.dumps(a, ensure_ascii=False))
    print(fn, len(add), sum(1 for x in add if x.get('anulada')), 'anuladas')
