import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60])
    s=s.replace(a,b)
GAP=r"""
/* ============ GAP DE CONHECIMENTO (piloto: só alunos de GAP_PILOTO) ============
   Rede de dependências: base de Matemática -> tópicos de Física. As setas são HIPÓTESE (ver GAP_E);
   a prova de nivelamento vai refinar os nós e confirmar as ligações. */
const GAP_PILOTO=['2braphael'];
const GAP_M=[['PRO','Razão e proporção'],['ARI','Aritmética e álgebra'],['FUN','Funções e gráficos'],['GEO','Geometria']];
const GAP_F=[['MEC','Mecânica'],['OND','Ondas'],['OPT','Óptica'],['ELE','Eletricidade'],['TER','Termologia'],['MOD','Física Moderna']];
const GAP_E=[['PRO','MEC'],['PRO','TER'],['PRO','ELE'],['PRO','OND'],['ARI','MEC'],['ARI','ELE'],['ARI','TER'],['ARI','MOD'],['FUN','MEC'],['FUN','OND'],['FUN','TER'],['GEO','OPT'],['GEO','MEC'],['GEO','OND']];
function gapOk(r){return GAP_PILOTO.includes(String(r.nick).toLowerCase())}
function gapDados(R){const N={};for(const[k,n]of GAP_M){const t=(R.mat.tp||{})[k]||[0,0];N['m'+k]={id:'m'+k,k,n,m:'mat',ac:t[0],q:t[1]}}
 for(const[k,n]of GAP_F){const t=(R.fis.tp||{})[k]||[0,0];N['f'+k]={id:'f'+k,k,n,m:'fis',ac:t[0],q:t[1]}}
 for(const i in N){const x=N[i];x.p=x.q?Math.round(x.ac/x.q*100):null;x.low=x.q>=4&&x.p<50;x.few=x.q<6}
 const E=GAP_E.map(([a,b])=>({a:'m'+a,b:'f'+b}));for(const e of E){const A=N[e.a],B=N[e.b];e.st=A.low&&B.low?'r':A.low?'a':'n'}
 for(const i in N){const x=N[i];if(x.m==='mat')x.gar=x.low&&E.some(e=>e.a===i&&e.st==='r')}
 return{N,E}}
function gapSVG(G,sel){const W=760,Hh=470,MX=250,FX=510,pos={};
 GAP_M.forEach(([k],i)=>pos['m'+k]=[MX,70+i*(Hh-140)/(GAP_M.length-1)]);GAP_F.forEach(([k],i)=>pos['f'+k]=[FX,50+i*(Hh-100)/(GAP_F.length-1)]);
 const rad=x=>16+Math.min(14,x.q/3),rel=new Set();if(sel){rel.add(sel);for(const e of G.E)if(e.a===sel||e.b===sel){rel.add(e.a);rel.add(e.b)}}
 let h=`<svg id="gapSvg" viewBox="0 0 ${W} ${Hh}" width="100%" style="display:block;margin:0 auto;max-width:${W}px" role="img" aria-label="Rede de dependências entre Matemática e Física"><rect width="${W}" height="${Hh}" rx="6" fill="#1a1220"/>
 <text x="${MX}" y="22" font-size="11" font-weight="700" text-anchor="middle" fill="#f8d870" font-family="system-ui,sans-serif">BASE · MATEMÁTICA</text><text x="${FX}" y="22" font-size="11" font-weight="700" text-anchor="middle" fill="#f8d870" font-family="system-ui,sans-serif">FÍSICA</text>`;
 for(const e of G.E){const[x1,y1]=pos[e.a],[x2,y2]=pos[e.b],r1=rad(G.N[e.a]),r2=rad(G.N[e.b]),on=!sel||(e.a===sel||e.b===sel),c=e.st==='r'?'#e8584a':e.st==='a'?'#e8b030':'#6a5644',w=e.st==='r'?4:e.st==='a'?2.5:1.6,mx=(x1+x2)/2;
  h+=`<path d="M${x1+r1},${y1} C${mx},${y1} ${mx},${y2} ${x2-r2},${y2}" fill="none" stroke="${c}" stroke-width="${w}" opacity="${on?(e.st==='n'?.55:.95):.1}"/>`}
 for(const i in G.N){const x=G.N[i],[px,py]=pos[i],r=rad(x),on=!sel||rel.has(i),fil=x.q<3?'#3a2e26':pctC(x.p),isM=x.m==='mat',lbl=isM?`<text x="${px-r-10}" y="${py-1}" text-anchor="end"`:`<text x="${px+r+10}" y="${py-1}"`,lb2=isM?`<text x="${px-r-10}" y="${py+14}" text-anchor="end"`:`<text x="${px+r+10}" y="${py+14}"`;
  h+=`<g data-n="${i}" style="cursor:pointer" opacity="${on?1:.2}">`+(x.gar?`<circle cx="${px}" cy="${py}" r="${r+9}" fill="none" stroke="#e8584a" stroke-width="2" opacity=".55"/><circle cx="${px}" cy="${py}" r="${r+5}" fill="none" stroke="#e8584a" stroke-width="1.5" opacity=".9"/>`:'')+
  `<circle cx="${px}" cy="${py}" r="${r}" fill="${fil}" fill-opacity="${x.few?.55:1}" stroke="${x.q<3?'#6a5644':'#f4e4c0'}" stroke-width="${i===sel?4:2}" ${x.few?'stroke-dasharray="4 3"':''}/>`+
  `<text x="${px}" y="${py+4}" font-size="12" font-weight="700" text-anchor="middle" fill="#fff" stroke="#1a1220" stroke-width="3" paint-order="stroke" font-family="system-ui,sans-serif">${x.q?x.p+'%':'—'}</text>`+
  `${lbl} font-size="13" font-weight="700" fill="#f4e4c0" font-family="system-ui,sans-serif">${x.n}</text>${lb2} font-size="11" fill="#c8b898" font-family="system-ui,sans-serif">${x.q?x.ac+'/'+x.q+' questões':'sem questões'}</text></g>`}
 return h+'</svg>'}
function gapResumo(G){const gs=Object.values(G.N).filter(x=>x.gar).map(x=>({x,fx:G.E.filter(e=>e.a===x.id&&e.st==='r').map(e=>G.N[e.b])})).sort((a,b)=>b.fx.length-a.fx.length||a.x.p-b.x.p);
 if(!gs.length)return'<p class="sdim"><b style="color:#5ac86a">Nenhum gargalo claro</b> na base de Matemática (ou ainda poucos dados: é preciso pelo menos 4 questões no tópico).</p>';
 return gs.map(g=>`<p class="sdim"><b style="color:#e8584a">⚠ Provável gargalo: ${g.x.n}</b> (${g.x.p}%, ${g.x.ac}/${g.x.q}). Pode estar travando: ${g.fx.map(f=>`${f.n} (${f.p}%)`).join(', ')}.</p>`).join('')}
function gapDet(G,i){const x=G.N[i];if(!x)return'<p class="sdim">Toque num círculo para ver o que ele sustenta ou do que depende.</p>';
 const L=(x.m==='mat'?G.E.filter(e=>e.a===i).map(e=>G.N[e.b]):G.E.filter(e=>e.b===i).map(e=>G.N[e.a])).map(y=>`${y.n} (${y.q?y.p+'%':'sem dados'})`).join(', ');
 return`<p class="sdim"><b style="color:#f8d870">${x.n}</b> · ${x.q?x.ac+'/'+x.q+' ('+x.p+'%)':'sem questões'}${x.few&&x.q?' · poucos dados':''}<br>${x.m==='mat'?'Sustenta':'Depende de'}: ${L}</p>`}
function gapView(r,R){const G=gapDados(R);let sel=null;
 adStatsOpen(`<button class="sm" id="gapBack">◀ VOLTAR À FICHA</button><h2 style="margin-top:10px">GAP DE CONHECIMENTO</h2><p class="sdim">${r.nome||r.nick} · ${TURMA(r.turma).nome}</p><div id="gapRes">${gapResumo(G)}</div><div id="gapBox"></div><div id="gapDet" style="min-height:44px"></div>
 <p class="sdim" style="font-size:11px">Cor: acerto (vermelho abaixo de 40%, amarelo até 60%, verde acima). Tamanho: nº de questões. Tracejado: menos de 6 questões, pouca confiança. Linha vermelha: base fraca ligada a tópico fraco; amarela: base fraca. As ligações são uma hipótese de pré-requisito, não uma prova; a prova de nivelamento vai confirmar. Matemática só conta a partir de 21/10.</p>`);
 const draw=()=>{$('gapBox').innerHTML=gapSVG(G,sel);$('gapDet').innerHTML=gapDet(G,sel);$('gapSvg').onclick=e=>{const g=e.target.closest('[data-n]');sel=g?(g.dataset.n===sel?null:g.dataset.n):null;draw()}};
 draw();$('gapBack').onclick=()=>adAluno(r)}
"""
rep("/* estatísticas do próprio aluno (aberto pela lista da tribo) */", GAP.lstrip('\n')+"/* estatísticas do próprio aluno (aberto pela lista da tribo) */")
rep(" h+=radarBloco(R,(TURMA(r.turma)||{cor:{f:'#e8c070'}}).cor.f)+'<h3>POR MATÉRIA</h3>'+subjHTML(R);if(S.semMat)",
    " if(gapOk(r))h+='<div style=\"margin:10px 0\"><button class=\"sm\" id=\"gapBt\">🕸 GAP DE CONHECIMENTO</button></div>';h+=radarBloco(R,(TURMA(r.turma)||{cor:{f:'#e8c070'}}).cor.f)+'<h3>POR MATÉRIA</h3>'+subjHTML(R);if(S.semMat)")
rep(" adStatsOpen(h);senhaWire(r);$('foraBt').onclick=",
    " adStatsOpen(h);senhaWire(r);if($('gapBt'))$('gapBt').onclick=()=>gapView(r,R);$('foraBt').onclick=")
open(f,'w',encoding='utf-8').write(s);print('gap ok',f)
