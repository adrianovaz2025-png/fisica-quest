import json, re, shutil, sys, unicodedata, importlib.util
sys.path.insert(0, '/home/claude/work/tema')
Q = '/home/claude/fisica-quest/q/'
G = {  # gabaritos oficiais (2025: modelo A / D; 2026: versão 1, definitivo)
 (2025, 1): 'C' + 'NADCEABBDCABBDEEBCC' + 'DDCECBBEABCA' + 'DBCECABEDCAE',
 (2025, 2): 'ACBADBEDDDDBABCEADCE' + 'ECABCEBBDECE' + 'DBAECAEECEAB' + 'ABEACEDEBDCB',
 (2026, 1): 'ABECDBBEACDBCBEDACCBAEDCECABDBCBEDAEBCCADEBA',
 (2026, 2): 'BACDEADBNECBCADEDEBCCEADBBCAEDAECBDCEABAEDBDCAECDBBEAEED',
}
assert all(len(v) in (44, 56) for v in G.values()), {k: len(v) for k, v in G.items()}
def subj(dia, n):
    if dia == 1: return ('lin', 'POR') if n <= 20 else ('fis', None) if n <= 32 else ('qui', None)
    return ('mat', None) if n <= 20 else ('hum', 'GEO') if n <= 32 else ('hum', 'HIS') if n <= 44 else ('lin', 'ING')
def norm(s): return unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode()
spec = importlib.util.spec_from_file_location('cls', '/home/claude/work/tema/cls.py')
src = open('/home/claude/work/tema/cls.py', encoding='utf-8').read().split('FN={')[0]
ns = {}; exec(src, ns); R = ns['R']
R['fis'] = [('ELE', '', r'corrente eletric|resistor|resistencia eletric|eletric|campo magnet|\bima\b|imas\b|induc|capacitor|circuito|\bvolt|ampere|\bohm|lampada|carga eletric'),
            ('TER', '', r'calor|temperatura|termic|gas ideal|isobar|isoterm|adiabat|dilat|calorim|fusao|vaporiz|entropia|maquina termica|ciclo'),
            ('OPT', '', r'espelho|lente|refrac|reflex|luz|optic|imagem|foco|prisma|indice de refracao'),
            ('OND', '', r'onda|frequencia|som|acust|ressonan|comprimento de onda|doppler|interferencia|vibra'),
            ('MOD', '', r'foton|quant|relativ|nuclear|radioativ|efeito fotoeletrico|atomo'),
            ('MEC', '', r'.')]
R['fis'].insert(0,('MEC','',r'velocidade|aceleracao|forca|atrito|massa|plano inclinado|energia cinetica|energia potencial|movimento|queda|lancamento|colisao|impulso|quantidade de movimento|torque|equilibrio|empuxo|pressao|densidade|gravita|orbita|polia|mola'))
out = {k: [] for k in ['linguagens', 'humanas', 'matematica', 'quimica', 'questoes']}
FN = {'lin': 'linguagens', 'hum': 'humanas', 'mat': 'matematica', 'qui': 'quimica', 'fis': 'questoes'}
for (ano, dia), gab in G.items():
    rel = json.load(open(f'out/rel_{ano}_{dia}.json'))
    for r in rel:
        n = r['num']; g = gab[n - 1]; mt, tema = subj(dia, n)
        if not tema:
            t = norm(r['txt']); sc = sorted(((len(re.findall(rx, t)), c) for c, _, rx in R[mt][:-1]), reverse=True)
            tema = sc[0][1] if sc[0][0] > 0 else R[mt][-1][0]
        q = dict(id=r['id'], ano=ano, num=n, dia=dia, banca='espcex', area={'lin': 'LIN', 'hum': 'HUM', 'mat': 'MAT', 'qui': 'QUI', 'fis': tema}[mt],
                 lg='', parts=[], alts=[{'l': l, 'h': ''} for l in 'ABCDE'], orig=r['id'] + '.webp', osz=r['osz'], modo='img',
                 gab=None if g == 'N' else g, gsrc='oficial', tema=tema)
        if g == 'N': q['anulada'] = True
        out[FN[mt]].append(q)
        shutil.copy(f"out/{r['id']}.webp", Q + 'orig/' + r['id'] + '.webp')
for fn, add in out.items():
    raw = open(Q + fn + '.json', encoding='utf-8').read(); a = json.loads(raw)
    a = [x for x in a if x.get('banca') != 'espcex'] + add
    compact = '": ' not in raw[:800]
    open(Q + fn + '.json', 'w', encoding='utf-8').write(json.dumps(a, ensure_ascii=False, separators=(',', ':')) if compact else json.dumps(a, ensure_ascii=False))
    print(fn, len(add), {t: sum(1 for x in add if x['tema'] == t) for t in sorted({x['tema'] for x in add})})
