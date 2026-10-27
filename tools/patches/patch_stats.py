import sys,json
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
TEM=json.load(open('/home/claude/work/tema/temas.json',encoding='utf-8'))
TEMAS={'fis':{'MEC':'Mecânica','TER':'Termologia','OPT':'Óptica','OND':'Ondas','ELE':'Eletricidade','MOD':'Energia e Física Moderna'}}
for k,v in TEM.items():TEMAS[k]={c:n for c,n in v}
# 1) estatística por matéria e tópico em cada simulado (guardada no perfil do aluno)
rep(" st.n++;if(!parc)st.best=Math.max(st.best,pct);",
    " {if(!st.mt){st.mt={};st.mt0=st.n}const M=st.mt[ES.mat]=st.mt[ES.mat]||{n:0,q:0,ac:0,tp:{}};M.n++;M.q+=n;M.ac+=ac;for(const q of qs){const k=q.e?(q.X.tema||q.X.area):ES.bank[q.i][0];M.tp[k]=M.tp[k]||[0,0];M.tp[k][1]++;if(isOk(q))M.tp[k][0]++}}\n st.n++;if(!parc)st.best=Math.max(st.best,pct);")
# 2) dados para o professor
rep("async alunos(){if(!this.me()||!this.me().admin)return[];",
    "async enemTodos(){if(!this.me()||!this.me().admin)return[];return Object.values(this.db.users).filter(u=>u.turma!=='PROF').map(u=>({nick:u.nick,turma:u.turma,enem:(u.equip&&u.equip.enem)||{}}))},\nasync alunos(){if(!this.me()||!this.me().admin)return[];")
rep("async alunos(){const{data,error}=await this.sb.rpc('admin_alunos');",
    "async enemTodos(){const{data,error}=await this.sb.rpc('admin_enem');if(error)throw error;return data||[]},\nasync alunos(){const{data,error}=await this.sb.rpc('admin_alunos');")
# 3) tela de estatísticas
UI=r'''
/* ============ ESTATÍSTICAS DO ALUNO E DA TURMA (painel do professor) ============ */
const TEMAS=__TEMAS__,MATN={fis:'FÍSICA',mat:'MATEMÁTICA',qui:'QUÍMICA',bio:'BIOLOGIA'},LEGA={MAT:'mat',QUI:'qui',BIO:'bio'};
async function adEnem(force){if(AD.enem&&!force)return AD.enem;const L=await API.enemTodos();AD.enem={};for(const r of L)AD.enem[String(r.nick).toLowerCase()]=r;return AD.enem}
/* junta o histórico antigo (só totais) com o novo (matéria + tópico) */
function statsDe(st){st=st||{};const A=st.areas||{},mt=st.mt||{},R={};
 for(const m in MATN)R[m]={sim:0,q:0,ac:0,tp:{}};
 for(const k in A){const v=A[k];if(!v)continue;const m=LEGA[k]||'fis';R[m].q+=v[1];R[m].ac+=v[0];if(m==='fis'){R.fis.tp[k]=R.fis.tp[k]||[0,0];R.fis.tp[k][0]+=v[0];R.fis.tp[k][1]+=v[1]}}
 for(const m in mt){if(!R[m])continue;R[m].sim+=mt[m].n;if(m!=='fis')for(const k in mt[m].tp){R[m].tp[k]=R[m].tp[k]||[0,0];R[m].tp[k][0]+=mt[m].tp[k][0];R[m].tp[k][1]+=mt[m].tp[k][1]}}
 const nNovo=Object.values(mt).reduce((a,x)=>a+x.n,0),hist=st.hist||[];let semMat=Math.max(0,(st.n||0)-nNovo);
 hist.slice(nNovo).forEach(h=>{if(semMat>0&&R[h.mat]){R[h.mat].sim++;semMat--}});
 return{R,n:st.n||0,best:st.best||0,hist,semMat}}
const pctC=p=>p<40?'#e8584a':p<60?'#e8b030':'#5ac86a';
function bar(p){return`<span class="sbar"><i style="width:${p}%;background:${pctC(p)}"></i></span>`}
function topicsHTML(m,tp){const ks=Object.keys(tp).filter(k=>tp[k][1]>0);if(!ks.length)return'<p class="sdim">Sem questões respondidas por tópico ainda.</p>';
 const L=ks.map(k=>({k,n:(TEMAS[m]&&TEMAS[m][k])||k,ac:tp[k][0],q:tp[k][1],p:Math.round(tp[k][0]/tp[k][1]*100)})).sort((a,b)=>(a.q>=3?0:1)-(b.q>=3?0:1)||a.p-b.p);
 return'<table class="sst">'+L.map((t,i)=>`<tr><td>${t.n}${i===0&&t.q>=3&&t.p<60?' <em>⚠ mais dificuldade</em>':''}</td><td class="n">${t.ac}/${t.q}</td><td class="n">${t.p}%</td><td class="b">${bar(t.p)}</td></tr>`).join('')+'</table>'}
function subjHTML(R){let h='<table class="sst"><tr><th>MATÉRIA</th><th class="n">SIMULADOS</th><th class="n">QUESTÕES</th><th class="n">ACERTOS</th><th class="n">%</th><th></th></tr>';
 for(const m in MATN){const x=R[m];if(!x.q&&!x.sim)continue;const p=x.q?Math.round(x.ac/x.q*100):0;h+=`<tr><td>${MATN[m]}</td><td class="n">${x.sim}</td><td class="n">${x.q}</td><td class="n">${x.ac}</td><td class="n">${p}%</td><td class="b">${bar(p)}</td></tr>`}
 return h+'</table>'}
function adStatsOpen(html){let o=$('adst');if(!o){o=el('div','ov');o.id='adst';o.style.zIndex=8;o.innerHTML='<div class="box sbox"><button class="sm sx" id="adstX">✕</button><div id="adstB"></div></div>';document.body.appendChild(o);$('adstX').onclick=()=>o.classList.remove('on');o.onclick=e=>{if(e.target===o)o.classList.remove('on')}}
 $('adstB').innerHTML=html;o.classList.add('on')}
async function adAluno(r){adStatsOpen('<p class="sdim">Carregando estatísticas...</p>');let E;try{E=await adEnem()}catch(e){adStatsOpen(`<h2>${r.nome||r.nick}</h2><p class="sdim">Não foi possível carregar: ${errPT(e)}</p>`);return}
 const x=E[String(r.nick).toLowerCase()],S=statsDe(x&&x.enem),R=S.R,qt=Object.values(R).reduce((a,v)=>a+v.q,0),ac=Object.values(R).reduce((a,v)=>a+v.ac,0);
 let h=`<h2>${r.nome||r.nick}</h2><p class="sdim">${r.nick} · ${TURMA(r.turma).nome} · ${r.pontos||0} pontos</p>
  <div class="estats"><span>SIMULADOS<b>${S.n}</b></span><span>QUESTÕES<b>${qt}</b></span><span>ACERTOS<b>${ac}</b></span><span>APROVEITAMENTO<b>${qt?Math.round(ac/qt*100):0}%</b></span><span>MELHOR SIMULADO<b>${S.best}%</b></span></div>`;
 if(!qt){adStatsOpen(h+'<p class="sdim">Este aluno ainda não fez simulados na Torre ENEM.</p>');return}
 h+='<h3>POR MATÉRIA</h3>'+subjHTML(R);if(S.semMat)h+=`<p class="sdim">${S.semMat} simulado(s) antigo(s) sem matéria registrada.</p>`;
 for(const m in MATN){if(!R[m].q)continue;h+=`<h3>${MATN[m]} · POR TÓPICO</h3>`+topicsHTML(m,R[m].tp);if(m!=='fis'&&!Object.keys(R[m].tp).length)h+=''}
 if(['mat','qui','bio'].some(m=>R[m].q&&!Object.keys(R[m].tp).length))h+='<p class="sdim">Em Matemática, Química e Biologia os tópicos começam a ser contados a partir de hoje (21/10).</p>';
 if(S.hist.length){h+='<h3>ÚLTIMOS SIMULADOS</h3><table class="sst"><tr><th>DATA</th><th>MATÉRIA</th><th class="n">ACERTOS</th><th class="n">TEMPO</th></tr>'+S.hist.map(z=>`<tr><td>${z.d.split('-').reverse().join('/')}</td><td>${MATN[z.mat]||'—'}${z.src==='rap'?' (rápidas)':''}</td><td class="n">${z.ac}/${z.n}</td><td class="n">${fmtT(z.t)}</td></tr>`).join('')+'</table>'}
 adStatsOpen(h)}
async function adTurma(tid){adStatsOpen('<p class="sdim">Carregando...</p>');let E;try{E=await adEnem()}catch(e){adStatsOpen(`<p class="sdim">Não foi possível carregar: ${errPT(e)}</p>`);return}
 const tabs=[['all','TODAS'],...TURMAS.map(t=>[t.id,t.nome])];let h='<h2>ANÁLISE POR TURMA</h2><div class="stabs">'+tabs.map(([k,n])=>`<button class="sm${k===tid?' on':''}" data-t="${k}">${n}</button>`).join('')+'</div>';
 const rows=(AD.rows||[]).filter(r=>tid==='all'||r.turma===tid),T={};for(const m in MATN)T[m]={sim:0,q:0,ac:0,tp:{}};const worst=[];
 for(const r of rows){const x=E[String(r.nick).toLowerCase()];const S=statsDe(x&&x.enem);for(const m in MATN){const a=S.R[m],b=T[m];b.sim+=a.sim;b.q+=a.q;b.ac+=a.ac;for(const k in a.tp){b.tp[k]=b.tp[k]||[0,0];b.tp[k][0]+=a.tp[k][0];b.tp[k][1]+=a.tp[k][1]}}
  const f=S.R.fis.tp,ks=Object.keys(f).filter(k=>f[k][1]>=3);if(ks.length){ks.sort((a,b)=>f[a][0]/f[a][1]-f[b][0]/f[b][1]);const k=ks[0];worst.push([r,TEMAS.fis[k]||k,Math.round(f[k][0]/f[k][1]*100)])}}
 const qt=Object.values(T).reduce((a,v)=>a+v.q,0);h+=`<p class="sdim">${rows.length} aluno(s) · ${qt} questões respondidas</p>`;
 if(!qt)h+='<p class="sdim">Nenhum simulado feito por esta turma ainda.</p>';else{h+='<h3>POR MATÉRIA</h3>'+subjHTML(T);for(const m in MATN)if(T[m].q)h+=`<h3>${MATN[m]} · ONDE A TURMA TEM MAIS DIFICULDADE</h3>`+topicsHTML(m,T[m].tp);
  if(worst.length){worst.sort((a,b)=>a[2]-b[2]);h+='<h3>FÍSICA · TÓPICO MAIS DIFÍCIL DE CADA ALUNO</h3><table class="sst">'+worst.map(([r,t,p])=>`<tr><td>${r.nome||r.nick}</td><td>${t}</td><td class="n">${p}%</td><td class="b">${bar(p)}</td></tr>`).join('')+'</table>'}}
 adStatsOpen(h);$('adstB').querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>adTurma(b.dataset.t))}
'''.replace('__TEMAS__',json.dumps(TEMAS,ensure_ascii=False))
rep("function renderAdmin(){",UI+"\nfunction renderAdmin(){")
rep("h.appendChild(eBtn('↻ ATUALIZAR','sm',adminLoad));","h.appendChild(eBtn('↻ ATUALIZAR','sm',()=>{AD.enem=null;adminLoad()}));h.appendChild(eBtn('📊 ANÁLISE POR TURMA','sm',()=>adTurma('all')));")
rep("rows.forEach((r,i)=>{const t=el('tr');","rows.forEach((r,i)=>{const t=el('tr');t.className='clk';t.title='Ver estatísticas';t.onclick=()=>adAluno(r);")
rep("const tot=AD.rows.reduce(","B.appendChild(el('p','sdim','Clique em um aluno para ver as estatísticas dele por matéria e tópico.'));const tot=AD.rows.reduce(")
CSS=".sbox{width:min(760px,94vw)}.sbox h2{font-size:12px}.sbox h3{font-size:8px;color:#f8d870;margin:16px 0 6px}.sx{position:absolute;top:8px;right:8px}.sdim{font:13px/1.4 system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:#c8b898;margin:4px 0}.sst{width:100%;border-collapse:collapse;font:13px/1.35 system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif}.sst th{text-align:left;color:#f8d870;font-size:11px;padding:4px 6px;border-bottom:2px solid #5a3a22}.sst td{padding:5px 6px;border-bottom:1px solid #3a2a1e}.sst .n{text-align:right;white-space:nowrap}.sst .b{width:28%}.sst em{color:#ff9a8a;font-style:normal;font-size:11px}.sbar{display:block;height:9px;background:#1a1220;border:1px solid #5a3a22}.sbar i{display:block;height:100%}.stabs{display:flex;gap:4px;flex-wrap:wrap;margin:6px 0}.stabs .on{background:#e8c070;color:#2a1d14}.adt tr.clk{cursor:pointer}.adt tr.clk:hover td{background:#3a2a1e}"
rep(".ov.on{display:flex}",".ov.on{display:flex}"+CSS)
open(f,'w',encoding='utf-8').write(s);print('stats ok',f)
