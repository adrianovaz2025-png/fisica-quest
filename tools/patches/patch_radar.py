import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
RAD=r'''
/* gráfico de radar (estilo ficha de jogador) por matéria */
const RAX=[['fis','FÍSICA'],['qui','QUÍMICA'],['bio','BIOLOGIA'],['mat','MATEMÁTICA'],['lin','LINGUAGENS'],['hum','HUMANAS']];
function radarSVG(R,cor,size=300){const c=size/2,Rr=size/2-58,n=RAX.length,pt=(i,v)=>{const a=-Math.PI/2+i*2*Math.PI/n;return[c+Math.cos(a)*Rr*v/100,c+Math.sin(a)*Rr*v/100]},val=m=>R[m].q?Math.round(R[m].ac/R[m].q*100):null;
 let h=`<svg viewBox="0 0 ${size} ${size}" width="100%" style="max-width:${size}px;display:block;margin:0 auto" role="img" aria-label="Radar de acerto por matéria">`;
 for(const v of[25,50,75,100])h+=`<polygon points="${RAX.map((_,i)=>pt(i,v).join(',')).join(' ')}" fill="${v===100?'#1a1220':'none'}" stroke="#4a3a2e" stroke-width="${v===100?2:1}"/>`;
 RAX.forEach(([m,l],i)=>{const[x,y]=pt(i,100),[lx,ly]=pt(i,124),v=val(m);h+=`<line x1="${c}" y1="${c}" x2="${x}" y2="${y}" stroke="#4a3a2e"/><text x="${lx}" y="${ly+3}" font-size="11" font-weight="700" text-anchor="middle" fill="${v==null?'#8a7a62':'#f4e4c0'}" font-family="system-ui,sans-serif">${l}</text>`;if(v==null)h+=`<text x="${lx}" y="${ly+16}" font-size="9" text-anchor="middle" fill="#8a7a62" font-family="system-ui,sans-serif">sem dados</text>`});
 const P=RAX.map(([m],i)=>pt(i,val(m)??0));h+=`<polygon points="${P.map(p=>p.join(',')).join(' ')}" fill="${cor}" fill-opacity=".32" stroke="${cor}" stroke-width="3"/>`;
 RAX.forEach(([m],i)=>{const v=val(m);if(v==null)return;const[x,y]=P[i],low=R[m].q<10;h+=`<circle cx="${x}" cy="${y}" r="5" fill="${low?'#1a1220':cor}" stroke="${cor}" stroke-width="2"/><text x="${x}" y="${y-9}" font-size="12" font-weight="700" text-anchor="middle" fill="#fff" font-family="system-ui,sans-serif">${v}%</text>`});
 return h+'</svg>'}
function fortesHTML(R){const L=RAX.filter(([m])=>R[m].q>=10).map(([m,l])=>({l,v:Math.round(R[m].ac/R[m].q*100)})).sort((a,b)=>b.v-a.v);if(L.length<2)return'<p class="sdim">Ainda poucos dados para apontar pontos fortes e fracos (mínimo de 10 questões por matéria).</p>';
 return`<div class="rfw"><div><b style="color:#5ac86a">PONTOS FORTES</b><br>${L.slice(0,2).map(x=>`${x.l} — ${x.v}%`).join('<br>')}</div><div><b style="color:#e8584a">A MELHORAR</b><br>${L.slice(-2).reverse().map(x=>`${x.l} — ${x.v}%`).join('<br>')}</div></div>`}
function radarBloco(R,cor){return`<div class="rbox">${radarSVG(R,cor)}${fortesHTML(R)}<p class="sdim" style="font-size:11px">Cada ponta é uma matéria; quanto mais longe do centro, maior o acerto. Ponto vazado = menos de 10 questões naquela matéria.</p></div>`}
/* estatísticas do próprio aluno (aberto pela lista da tribo) */
function minhasStats(){const S=statsDe(enemState()),R=S.R,qt=Object.values(R).reduce((a,v)=>a+v.q,0),ac=Object.values(R).reduce((a,v)=>a+v.ac,0),cor=(TURMA(me.turma)||{cor:{f:'#e8c070'}}).cor.f;
 let h=`<h2>MEU DESEMPENHO</h2><p class="sdim">${me.nick} · ${me.pontos||0} pontos</p><div class="estats"><span>SIMULADOS<b>${S.n}</b></span><span>QUESTÕES<b>${qt}</b></span><span>ACERTO<b>${qt?Math.round(ac/qt*100):0}%</b></span><span>MELHOR<b>${S.best}%</b></span></div>`;
 if(!qt){adStatsOpen(h+'<p class="sdim">Faça simulados na Torre ENEM para ver seu gráfico aqui.</p>');return}
 h+=radarBloco(R,cor)+'<h3>POR MATÉRIA</h3>'+subjHTML(R);for(const m in MATN)if(R[m].q)h+=`<h3>${MATN[m]} · POR TÓPICO</h3>`+topicsHTML(m,R[m].tp);adStatsOpen(h)}
'''
rep("async function adAluno(r){",RAD+"async function adAluno(r){")
# radar na ficha do aluno (professor)
rep(" h+='<h3>POR MATÉRIA</h3>'+subjHTML(R);if(S.semMat)",
    " h+=radarBloco(R,(TURMA(r.turma)||{cor:{f:'#e8c070'}}).cor.f)+'<h3>POR MATÉRIA</h3>'+subjHTML(R);if(S.semMat)")
# radar também na visão por turma
rep(" if(X.q){h+='<h3>POR MATÉRIA</h3>'+subjHTML(X.T);",
    " if(X.q){h+='<h3>RADAR DA TURMA</h3>'+radarBloco(X.T,tid==='all'?'#e8c070':TURMA(tid).cor.f)+'<h3>POR MATÉRIA</h3>'+subjHTML(X.T);")
# clique na lista da tribo
rep("const r2=document.createElement('span');r2.textContent=m.pontos+' pts';row.appendChild(l);row.appendChild(r2);$('tList').appendChild(row)})}",
    "const r2=document.createElement('span');r2.textContent=m.pontos+' pts';row.appendChild(l);row.appendChild(r2);\n"
    "   if(isAdm()||(me&&m.nick===me.nick)){row.classList.add('clk');row.title='Ver estatísticas';row.onclick=async()=>{if(me&&m.nick===me.nick&&!isAdm()){minhasStats();return}if(!AD.rows){try{AD.rows=await API.alunos()}catch(e){}}const rr=(AD.rows||[]).find(x=>x.nick===m.nick)||{nick:m.nick,nome:'',turma:t.id,pontos:m.pontos};adAluno(rr)}}\n"
    "   $('tList').appendChild(row)})}")
rep(".adt tr.clk{cursor:pointer}",".adt tr.clk{cursor:pointer}.rk.clk{cursor:pointer}.rk.clk:hover{background:#3a2a1e}.rbox{background:#1a1220;border:3px solid #5a3a22;padding:10px;margin:10px 0}.rfw{display:flex;gap:18px;justify-content:center;font:13px/1.6 system-ui,sans-serif;margin-top:6px;color:#f4e4c0}")
open(f,'w',encoding='utf-8').write(s);print('radar ok',f)
