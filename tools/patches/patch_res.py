import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
# carregamento das resoluções (q/res/<matéria>.json, sob demanda)
rep("function qRes(q){",
"""const RES={},RESL={};
function loadRes(m){if(!m||RES[m]||RESL[m])return;RESL[m]=fetch(QDIR+'res/'+m+'.json').then(r=>r.ok?r.json():{}).then(j=>{RES[m]=j||{};if(ES.scr==='quiz'||ES.scr==='res')renderEnem()}).catch(()=>{RES[m]={}})}
const qResOf=q=>q.e?((RES[q.X.mt]||{})[q.X.id]||null):null;
/* bloco de resolução comentada: botão que abre texto + esquema (+ link da aula, quando houver) */
function resBlock(q){const R=qResOf(q),w=el('div','eresw');
 if(!R){w.appendChild(el('p','eres0',qRes(q)));return w}
 const b=eBtn(q.resOpen?'▲ ESCONDER RESOLUÇÃO':'📖 VER RESOLUÇÃO','sm eresb'+(q.resOpen?' on':''),()=>{q.resOpen=!q.resOpen;renderEnem()});w.appendChild(b);
 if(q.resOpen){const bx=el('div','eresx');bx.appendChild(el('b',null,`RESOLUÇÃO · ENEM ${q.X.ano} Q${q.X.num} · RESPOSTA ${q.X.gab}`));
  for(const p of String(R.t||'').split('\\n')){if(!p.trim())continue;const e=el('p');e.innerHTML=fracH(p);bx.appendChild(e)}
  if(R.esq){const e=el('div','eresq');e.innerHTML=R.esq;bx.appendChild(e)}
  if(R.aula){const a=eBtn('▶ VER A AULA DESTE ASSUNTO','sm',()=>window.open(R.aula,'_blank'));bx.appendChild(a)}
  w.appendChild(bx)}
 return w}
function qRes(q){""")
rep("Resolução comentada em breve.`","Resolução comentada em breve.`")
# no treino: depois de confirmar
rep("f.appendChild(el('p',null,qRes(q)));tgt.appendChild(f)}",
    "if(q.e)f.appendChild(resBlock(q));else f.appendChild(el('p',null,qRes(q)));tgt.appendChild(f)}")
# na revisão do resultado
rep("if(!ok)d.appendChild(el('p','eans ok',`Correta: ${X.gab}`));d.appendChild(qOrigBtn(X,'📄 VER QUESTÃO COMPLETA'))}",
    "if(!ok)d.appendChild(el('p','eans ok',`Correta: ${X.gab}`));d.appendChild(qOrigBtn(X,'📄 VER QUESTÃO COMPLETA'));d.appendChild(resBlock(q))}")
# carrega ao começar o simulado
rep("ES.cur=0;ES.t0=Date.now();ES.confirmEnd=false;ES.confirmExit=false;ES.scr='quiz';ES.bank=qb;renderEnem()}",
    "ES.cur=0;ES.t0=Date.now();ES.confirmEnd=false;ES.confirmExit=false;ES.scr='quiz';ES.bank=qb;if(en)for(const m of new Set(ES.qs.map(x=>x.X.mt)))loadRes(m);renderEnem()}")
# estilo
rep(".adt tr.clk{cursor:pointer}",
    ".eresw{margin-top:8px}.eresb{margin-top:4px}.eresx{background:#1a1220;border:3px solid #5a3a22;padding:10px 12px;margin-top:8px;text-align:left}"
    ".eresx>b{display:block;color:#f4d070;font-size:9px;margin-bottom:6px}.eresx p{font:15px/1.55 system-ui,sans-serif;color:#f4e4c0;margin:6px 0}"
    ".eresq{background:#fff8e8;border-radius:4px;padding:8px;margin:8px 0;text-align:center}.eresq svg{max-width:100%;height:auto}.eres0{font:13px/1.5 system-ui,sans-serif}"
    ".adt tr.clk{cursor:pointer}")
open(f,'w',encoding='utf-8').write(s);print('res ok',f)
