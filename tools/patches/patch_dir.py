import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
rep("h.appendChild(eBtn(me&&me.equip&&me.equip.manut?'🔧 DESLIGAR MANUTENÇÃO':'🔧 MODO MANUTENÇÃO','sm',toggleManut));B.appendChild(h);",
    "h.appendChild(eBtn('📈 PAINEL DO DIRETOR','sm',()=>window.open('diretor.html','_blank')));h.appendChild(eBtn('🔑 CÓDIGO DO DIRETOR','sm'+(AD.cod?' on':''),()=>{AD.cod=!AD.cod;renderAdmin()}));h.appendChild(eBtn(me&&me.equip&&me.equip.manut?'🔧 DESLIGAR MANUTENÇÃO':'🔧 MODO MANUTENÇÃO','sm',toggleManut));B.appendChild(h);\n"
    " if(AD.cod){const w=el('div','codrow');w.appendChild(el('p','sdim','O diretor abre <b>adrianovaz2025-png.github.io/fisica-quest/diretor.html</b> e digita o código. Ele vê só números por turma e série, sem nome de aluno. Para trocar o código (mínimo 8 caracteres):'));const i=el('input','inp');i.placeholder='Novo código do diretor';w.appendChild(i);w.appendChild(eBtn('SALVAR CÓDIGO','sm',async()=>{const v=i.value.trim();if(v.length<8){toast('O CÓDIGO PRECISA DE PELO MENOS 8 CARACTERES');return}try{if(API.codDiretor)await API.codDiretor(v);toast('CÓDIGO DO DIRETOR ATUALIZADO',3000);AD.cod=false;renderAdmin()}catch(e){toast(errPT(e))}}));B.appendChild(w)}")
rep("async enemTodos(){const{data,error}=await this.sb.rpc('admin_enem');","async codDiretor(c){const{error}=await this.sb.rpc('admin_codigo_diretor',{p_novo:c});if(error)throw error},\nasync enemTodos(){const{data,error}=await this.sb.rpc('admin_enem');")
rep(".adt tr.clk{cursor:pointer}",".adt tr.clk{cursor:pointer}.codrow{display:flex;gap:8px;flex-wrap:wrap;align-items:center;background:#1a1220;border:3px solid #5a3a22;padding:8px;margin:6px 0}.codrow p{flex:1 1 100%;margin:0}.codrow .inp{max-width:280px}")
open(f,'w',encoding='utf-8').write(s);print('dir ok',f)
