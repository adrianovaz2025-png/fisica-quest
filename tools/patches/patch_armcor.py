import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:70]);s=s.replace(a,b)
# ---- renderização: cor própria da armadura (L.arm={b,a}) ----
rep("const armT=id=>{","let ARMO=null;/* cor personalizada da armadura do personagem sendo desenhado */\nconst armP=t=>{const Q0=ARMT[t];if(!ARMO||!Q0)return Q0;return{...Q0,b:ARMO.b||Q0.b,a:ARMO.a||Q0.a}};\nconst armT=id=>{")
rep("const P=ARMT[t]","const P=armP(t)",4)
rep(" L=L&&L.hair?L:LOOKS[0];eq=normEq(eq);const key=JSON.stringify(L)+eqKey(eq)+fr+(back?1:0)+(solo?'s':'');if(SPR[key])return SPR[key];",
    " L=L&&L.hair?L:LOOKS[0];eq=normEq(eq);const key=JSON.stringify(L)+eqKey(eq)+fr+(back?1:0)+(solo?'s':'');if(SPR[key])return SPR[key];ARMO=L.arm&&(L.arm.b||L.arm.a)?L.arm:null;")
# elmo de chão usa o boneco padrão: leva a cor junto
rep("const hs=sprite(LOOKS[0],{cabeca:id},0,false,true)","const hs=sprite(ARMO?{...LOOKS[0],arm:ARMO}:LOOKS[0],{cabeca:id},0,false,true)")

# ---- editor de guardiões ----
rep('<label>PELE</label><select id="geSk"',
    '<label>ARMADURA COR</label><span style="display:flex;gap:6px;align-items:center"><input type="color" id="geAb" title="Cor principal"><input type="color" id="geAa" title="Cor de detalhe"><button id="geAr" style="font:inherit;font-size:7px;padding:4px 6px">ORIGINAL</button></span>\n<label>PELE</label><select id="geSk"')
rep("if(o.hc)L.hair.c1=o.hc;\n","if(o.hc)L.hair.c1=o.hc;if(o.ab||o.aa)L.arm={b:o.ab||null,a:o.aa||null};\n")
rep("$('geHc').value=o.hc||gd.L.hair.c1;$('geFala').value=o.fala||'';b.classList.add('on');geDraw()}",
    "$('geHc').value=o.hc||gd.L.hair.c1;geArmIn(curSet,o.ab,o.aa);$('geFala').value=o.fala||'';b.classList.add('on');geDraw()}\n"
    "function geArmIn(set,ab,aa){const P=ARMT[set]||ARMT.prata;$('geAb').value=ab||P.b;$('geAa').value=aa||P.a;$('geAb').dataset.c=ab?1:'';$('geAa').dataset.c=aa?1:''}")
rep("hc:$('geHc').value,skin:$('geSk').value,",
    "hc:$('geHc').value,ab:$('geAb').dataset.c?$('geAb').value:null,aa:$('geAa').dataset.c?$('geAa').value:null,skin:$('geSk').value,")
rep("L.skin=o.skin;L.hair.s=o.hs;L.hair.c1=o.hc;const eq=gEq(o.set);",
    "L.skin=o.skin;L.hair.s=o.hs;L.hair.c1=o.hc;if(o.ab||o.aa)L.arm={b:o.ab,a:o.aa};const eq=gEq(o.set);")
rep("['geSet','geArma','geHs','geHc','geSk'].forEach(i=>{$(i).oninput=geDraw;$(i).onchange=geDraw});",
    "['geSet','geArma','geHs','geHc','geSk'].forEach(i=>{$(i).oninput=geDraw;$(i).onchange=geDraw});\n"
    "['geAb','geAa'].forEach(i=>{$(i).oninput=$(i).onchange=()=>{$(i).dataset.c=1;geDraw()}});\n"
    "$('geSet').addEventListener('change',()=>{const P=ARMT[$('geSet').value];if(!P)return;if(!$('geAb').dataset.c)$('geAb').value=P.b;if(!$('geAa').dataset.c)$('geAa').value=P.a;geDraw()});\n"
    "$('geAr').onclick=()=>{geArmIn($('geSet').value,null,null);geDraw()};")

# ---- personalização do herói (aluno) ----
rep("const CTABS=[['cabelo','CABELO'],['roupa','ROUPA'],['pele','PELE'],['olhos','OLHOS']];",
    "const CTABS=[['cabelo','CABELO'],['roupa','ROUPA'],['pele','PELE'],['olhos','OLHOS'],['armadura','ARMADURA']];")
rep("olhos:[['eyes.c','COR DOS OLHOS']]};","olhos:[['eyes.c','COR DOS OLHOS']],armadura:[['arm.b','PRINCIPAL'],['arm.a','DETALHE']]};\n"
    "function armBase(){const e=me?eqNow():{},t=['peito','cabeca','botas'].map(k=>armT(e[k])).find(Boolean)||'aco';return ARMT[t]}")
rep("const getP=(o,p)=>p.split('.').reduce((a,k)=>a[k],o);",
    "const getP=(o,p)=>{if(p.startsWith('arm.')){const k=p.slice(4);return(o.arm&&o.arm[k])||armBase()[k]}return p.split('.').reduce((a,k)=>a[k],o)};")
rep("function setP(o,p,v){","function setP(o,p,v){if(p.startsWith('arm.')){o.arm={...(o.arm||{}),[p.slice(4)]:v};return}")
rep(" grid.style.display=items.length?'':'none';",
    " if(t==='armadura'){if(!cust.eq&&me){cust.eq=true;$('cEq').classList.add('on')}items.push(['orig','COR ORIGINAL',()=>{const v=clone(L);delete v.arm;return v},!L.arm,null,false])}\n"
    " grid.style.display=items.length?'':'none';")
rep("  b.onclick=()=>{pushUndo();setP(cust.look,path,id);changed(760);refreshCust()};grid.appendChild(b)}",
    "  b.onclick=()=>{pushUndo();if(path)setP(cust.look,path,id);else delete cust.look.arm;changed(760);refreshCust()};grid.appendChild(b)}")
open(f,'w',encoding='utf-8').write(s);print('armcor ok',f)
