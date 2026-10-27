import json,re,unicodedata,collections,sys
def norm(s):return unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()
R={
'mat':[('EST','Estatística e probabilidade',r'probabilidade|media |media,|media\.|media aritmetica|mediana|moda |desvio padrao|grafico|tabela|pesquisa|frequencia|sorte|aleatori|chance|percentual de entrevist'),
       ('GEO','Geometria',r'area|perimetro|volume|cilindr|cubo|esfera|triangul|retangul|circunfer|raio|diametro|angulo|prisma|piramide|cone|poligono|quadrado|hexagon|metros quadrados|m2|semelhan|teorema de pitagoras|planta|maquete|escala'),
       ('FUN','Funções e gráficos',r'funcao|f\(x\)|grafico da|parabola|exponencial|logaritm|crescente|decrescente|reta |coeficiente|equacao do'),
       ('PRO','Razão, proporção e porcentagem',r'porcent|%|razao|proporc|regra de tres|juros|desconto|aumento|lucro|taxa|velocidade media|consumo|litros|km |preco|custo|reais'),
       ('CON','Contagem e combinatória',r'quantas maneiras|de quantas formas|anagrama|combinac|permutac|arranjo|possibilidades distintas'),
       ('ARI','Aritmética e álgebra',r'.')],
'qui':[('ORG','Química orgânica',r'carbono|organic|hidrocarbon|alcool|etanol|ester|polimer|funcao organica|isomer|benzen|cadeia|acido carboxil|amina|cetona|aldeid|metano|biodiesel|glicer'),
       ('ELE','Eletroquímica',r'pilha|eletrolis|oxirreducao|redox|oxida|reduc|eletrodo|anodo|catodo|bateria|corrosao|potencial de reducao'),
       ('SOL','Soluções e estequiometria',r'concentrac|mol|massa molar|solucao|diluic|g/l|estequiometr|rendimento|reagente limitante|ppm'),
       ('EQU','Equilíbrio, ácidos e bases',r'equilibrio|ph|acid|basic|neutraliz|tampao|hidrolise|le chatelier|constante de'),
       ('TER','Termoquímica e cinética',r'entalpia|calor|exotermic|endotermic|energia de ativacao|velocidade da reacao|catalis|combustao'),
       ('AMB','Química ambiental e materiais',r'ambient|poluic|chuva acida|efeito estufa|camada de ozonio|reciclag|metal|lixo|agua potavel|tratamento'),
       ('GER','Química geral',r'.')],
'bio':[('ECO','Ecologia e meio ambiente',r'ecossistem|cadeia alimentar|teia|populac|bioma|desmatamento|ambient|especie invasora|nicho|predador|polinizac|mutualismo|parasit|ciclo do|aquecimento|biodiversidade|extincao'),
       ('GEN','Genética e evolução',r'gene|dna|rna|cromossom|heranca|alelo|hereditar|mutac|evoluc|selecao natural|darwin|lamarck|transgenic|clonag|crispr|genotipo|fenotipo'),
       ('CEL','Citologia e bioquímica',r'celula|mitocondr|membrana|organela|ribossom|proteina|enzima|fotossintese|respiracao celular|atp|glicose|lipid'),
       ('FIS','Fisiologia humana e saúde',r'sangue|coracao|pulmao|rim|hormonio|insulina|sistema imun|vacina|anticorpo|virus|bacteria|doenca|infecc|saude|digest|neuron|musculo|sistema nervoso'),
       ('BOT','Botânica e zoologia',r'planta|vegetal|folha|raiz|semente|flor|fruto|animal|inseto|mamifero|peixe|anfibio|reptil|ave'),
       ('GER','Biologia geral',r'.')],
}
FN={'mat':'matematica','qui':'quimica','bio':'biologia'}
out={}
for k,fn in FN.items():
  d=json.load(open(f'/home/claude/fisica-quest/q/{fn}.json',encoding='utf-8'))
  c=collections.Counter()
  for x in d:
    TX=json.load(open('textos.json',encoding='utf-8')) if 'TX' not in globals() else TX
    t=norm(TX.get(f"{x['ano']}_{x['num']}",'')+' '+' '.join(p.get('t','') for p in x['parts'])+' '+' '.join((a.get('h') or '') for a in x.get('alts',[])))
    t=re.sub(r'<[^>]+>',' ',t)
    best=None
    sc=[(len(re.findall(rx,t)),code) for code,_,rx in R[k][:-1]]
    sc.sort(reverse=True)
    code=sc[0][1] if sc[0][0]>0 else R[k][-1][0]
    x['tema']=code;c[code]+=1
  out[fn]=d;print(k,dict(c))
if len(sys.argv)>1:
  for fn,d in out.items():
    raw=open(f'/home/claude/fisica-quest/q/{fn}.json',encoding='utf-8').read()
    compact='": ' not in raw[:800]
    open(f'/home/claude/fisica-quest/q/{fn}.json','w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,separators=(',',':')) if compact else json.dumps(d,ensure_ascii=False))
  json.dump({k:[[c,n] for c,n,_ in v] for k,v in R.items()},open('temas.json','w'),ensure_ascii=False)
