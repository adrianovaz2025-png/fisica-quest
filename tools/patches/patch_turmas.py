import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
UI=r'''
/* ============ VISÃO POR TURMA (aba ALUNOS) — painel para orientar cada turma ============ */
function turmaResumo(tid,E){const rows=(AD.rows||[]).filter(r=>tid==='all'||r.turma===tid),T={};for(const m in MATN)T[m]={sim:0,q:0,ac:0,tp:{}};
 const al=[];let tq=0,tt=0;
 for(const r of rows){const x=E[String(r.nick).toLowerCase()],S=statsDe(x&&x.enem);let q=0,ac=0;
  for(const m in MATN){const a=S.R[m],b=T[m];b.sim+=a.sim;b.q+=a.q;b.ac+=a.ac;q+=a.q;ac+=a.ac;for(const k in a.tp){b.tp[k]=b.tp[k]||[0,0];b.tp[k][0]+=a.tp[k][0];b.tp[k][1]+=a.tp[k][1]}}
  let hq=0,ht=0;for(const h of S.hist){hq+=h.n||0;ht+=h.t||0}tq+=hq;tt+=ht;
  al.push({r,n:S.n,q,ac,p:q?Math.round(ac/q*100):null,spq:hq?ht/hq:null})}
 const ativos=al.filter(a=>a.n>0),q=al.reduce((a,b)=>a+b.q,0),ac=al.reduce((a,b)=>a+b.ac,0);
 const crit=[];for(const m in MATN)for(const k in T[m].tp){const v=T[m].tp[k];if(v[1]>=8)crit.push({m,k,n:(TEMAS[m]&&TEMAS[m][k])||k,ac:v[0],q:v[1],p:Math.round(v[0]/v[1]*100)})}crit.sort((a,b)=>a.p-b.p);
 return{rows,al,T,ativos,q,ac,p:q?Math.round(ac/q*100):0,spq:tq?tt/tq:null,crit,pts:rows.reduce((a,r)=>a+(+r.pontos||0),0)}}
function sugestoes(X){const S=[],nunca=X.al.filter(a=>!a.n).length,N=X.rows.length;
 if(!N)return['Nenhum aluno desta turma se cadastrou ainda. Vale passar o QR code e o código da tribo em sala.'];
 if(nunca/N>=.3)S.push(`<b>Engajamento:</b> ${nunca} de ${N} alunos ainda não fizeram nenhum simulado. Um desafio em sala (ex.: 10 questões valendo ponto extra) pode puxar quem está parado.`);
 if(X.spq!=null&&X.spq<25)S.push(`<b>Chute:</b> a turma gasta em média só ${Math.round(X.spq)} s por questão (no ENEM real são ~3 min). Oriente a ler o enunciado com calma; o limite de 20 erros por dia já freia o chute.`);
 const ch=X.al.filter(a=>a.q>=20&&a.p<25);if(ch.length)S.push(`<b>Possível chute em massa:</b> ${ch.map(a=>a.r.nome||a.r.nick).slice(0,6).join(', ')}${ch.length>6?'…':''} têm menos de 25% de acerto com muitas questões (25% é o que se acerta chutando 1 em 5 até menos).`);
 X.crit.slice(0,3).forEach((c,i)=>{if(c.p<50)S.push(`<b>Revisar ${c.n}</b> (${MATN[c.m]}): ${c.p}% de acerto em ${c.q} questões${i===0?' — é o ponto mais fraco da turma':''}.`)});
 const fis=X.T.fis;if(fis.q>=20&&fis.q/X.q<.25&&X.q>60)S.push('<b>Física pouco treinada:</b> a turma está fazendo mais simulados das outras matérias; vale indicar a Torre ENEM de Física como tarefa.');
 if(X.p>=60&&X.ativos.length/N>=.6)S.push('<b>Turma em bom ritmo:</b> aproveitamento acima de 60% e boa participação. Dá para subir o nível com simulados de 20 questões no modo PROVA.');
 if(!S.length)S.push('Sem alertas por enquanto. Continue acompanhando: os tópicos ficam mais confiáveis conforme a turma faz mais simulados.');return S}
async function renderTurmas(B){let E;try{E=await adEnem()}catch(e){B.appendChild(el('p','esub','Não foi possível carregar: '+errPT(e)));return}
 const tid=AD.tv||'all',W=el('div','adw tview');
 /* comparativo de todas as turmas */
 let h='<h3>COMPARATIVO DAS TURMAS</h3><table class="sst"><tr><th>TURMA</th><th class="n">ALUNOS</th><th class="n">ATIVOS</th><th class="n">SIMULADOS</th><th class="n">QUESTÕES</th><th class="n">ACERTO</th><th class="n">S/QUESTÃO</th><th>PONTO MAIS FRACO</th></tr>';
 for(const t of TURMAS){const X=turmaResumo(t.id,E),sim=X.al.reduce((a,b)=>a+b.n,0),c=X.crit[0];
  h+=`<tr class="clk" data-t="${t.id}"><td><b>${t.nome}</b> · ${t.tribo}</td><td class="n">${X.rows.length}</td><td class="n">${X.ativos.length}${X.rows.length?` (${Math.round(X.ativos.length/X.rows.length*100)}%)`:''}</td><td class="n">${sim}</td><td class="n">${X.q}</td><td class="n" style="color:${X.q?pctC(X.p):'inherit'}">${X.q?X.p+'%':'—'}</td><td class="n">${X.spq!=null?Math.round(X.spq)+' s':'—'}</td><td>${c?`${c.n} <span class="sdim2">(${MATN[c.m]}, ${c.p}%)</span>`:'—'}</td></tr>`}
 h+='</table><p class="sdim">Toque numa turma para ver o detalhe. "Ativos" = fizeram pelo menos 1 simulado. "S/questão" = tempo médio gasto por questão (pouco tempo indica chute).</p>';
 const tabs=[['all','TODAS'],...TURMAS.map(t=>[t.id,t.nome])];h+='<div class="stabs">'+tabs.map(([k,n])=>`<button class="sm${k===tid?' on':''}" data-t="${k}">${n}</button>`).join('')+'</div>';
 const X=turmaResumo(tid,E),nome=tid==='all'?'TODAS AS TURMAS':TURMA(tid).nome+' · '+TURMA(tid).tribo;
 h+=`<h2>${nome}</h2><div class="estats"><span>ALUNOS<b>${X.rows.length}</b></span><span>ATIVOS<b>${X.ativos.length}</b></span><span>QUESTÕES<b>${X.q}</b></span><span>ACERTO MÉDIO<b>${X.q?X.p+'%':'—'}</b></span><span>TEMPO/QUESTÃO<b>${X.spq!=null?Math.round(X.spq)+' s':'—'}</b></span><span>PONTOS<b>${X.pts}</b></span></div>`;
 h+='<h3>SUGESTÕES PARA ORIENTAR A TURMA</h3><ul class="sug">'+sugestoes(X).map(t=>`<li>${t}</li>`).join('')+'</ul>';
 if(X.q){h+='<h3>POR MATÉRIA</h3>'+subjHTML(X.T);
  h+='<h3>TÓPICOS MAIS DIFÍCEIS (TODAS AS MATÉRIAS)</h3>'+(X.crit.length?'<table class="sst">'+X.crit.slice(0,8).map(c=>`<tr><td>${c.n} <span class="sdim2">${MATN[c.m]}</span></td><td class="n">${c.ac}/${c.q}</td><td class="n">${c.p}%</td><td class="b">${bar(c.p)}</td></tr>`).join('')+'</table>':'<p class="sdim">Ainda poucos dados por tópico (mínimo de 8 questões por tópico).</p>');
  for(const m in MATN)if(X.T[m].q)h+=`<details><summary>${MATN[m]} · todos os tópicos</summary>${topicsHTML(m,X.T[m].tp)}</details>`}
 const com=X.al.filter(a=>a.q>=10).sort((a,b)=>b.p-a.p),top=com.slice(0,5),bx=com.slice(-5).reverse().filter(a=>!top.includes(a)),nunca=X.al.filter(a=>!a.n);
 const lst=(L,f)=>'<table class="sst">'+L.map(a=>`<tr class="clk" data-n="${a.r.nick}"><td>${a.r.nome||a.r.nick}${tid==='all'?` <span class="sdim2">${TURMA(a.r.turma).nome}</span>`:''}</td>${f(a)}</tr>`).join('')+'</table>';
 if(top.length)h+='<h3>DESTAQUES (MAIOR ACERTO, 10+ QUESTÕES)</h3>'+lst(top,a=>`<td class="n">${a.q} q</td><td class="n">${a.p}%</td><td class="b">${bar(a.p)}</td>`);
 if(bx.length)h+='<h3>PRECISAM DE ATENÇÃO (MENOR ACERTO)</h3>'+lst(bx,a=>`<td class="n">${a.q} q</td><td class="n">${a.p}%</td><td class="b">${bar(a.p)}</td>`);
 if(nunca.length)h+=`<h3>AINDA NÃO FIZERAM SIMULADO (${nunca.length})</h3><p class="sdim">${nunca.map(a=>a.r.nome||a.r.nick).join(', ')}</p>`;
 W.innerHTML=h;B.appendChild(W);
 W.querySelectorAll('[data-t]').forEach(e=>e.onclick=()=>{AD.tv=e.dataset.t;renderAdmin()});
 W.querySelectorAll('[data-n]').forEach(e=>e.onclick=()=>{const r=AD.rows.find(x=>x.nick===e.dataset.n);if(r)adAluno(r)})}
'''
rep("function renderAdmin(){",UI+"\nfunction renderAdmin(){")
rep("h.appendChild(eBtn('📊 ANÁLISE POR TURMA','sm',()=>adTurma('all')));",
    "h.appendChild(eBtn(AD.view==='turmas'?'👤 VER ALUNOS':'🏫 VISÃO POR TURMA','sm'+(AD.view==='turmas'?' on':''),()=>{AD.view=AD.view==='turmas'?'':'turmas';renderAdmin()}));")
rep(" const rows=AD.rows.filter(r=>!AD.q||(r.nome+' '+r.nick).toLowerCase().includes(AD.q.toLowerCase()));\n",
    " if(AD.view==='turmas'){renderTurmas(B);return}\n const rows=AD.rows.filter(r=>!AD.q||(r.nome+' '+r.nick).toLowerCase().includes(AD.q.toLowerCase()));\n")
rep("PAINEL DO PROFESSOR · ALUNOS CADASTRADOS'","PAINEL DO PROFESSOR · '+(AD.view==='turmas'?'VISÃO POR TURMA':'ALUNOS CADASTRADOS')")
rep(".adt tr.clk{cursor:pointer}",".adt tr.clk{cursor:pointer}.tview{padding:10px 12px;background:#2a1d14}.tview h2{font-size:11px;color:#f8d870;margin:14px 0 8px}.tview h3{font-size:8px;color:#f8d870;margin:16px 0 6px}.tview .sst tr.clk{cursor:pointer}.tview .sst tr.clk:hover td{background:#3a2a1e}.sdim2{color:#a89878;font-size:11px}.sug{margin:4px 0;padding-left:18px;font:13px/1.5 system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:#f4e4c0}.sug li{margin:4px 0}.sug b{color:#f8d870}.tview details{margin:6px 0;font:13px system-ui,sans-serif}.tview summary{cursor:pointer;color:#e8c070;padding:4px 0}")
open(f,'w',encoding='utf-8').write(s);print('turmas ok',f)
