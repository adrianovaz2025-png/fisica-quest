import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
rep("function toggleManut(){const e=eqState();e.manut=!e.manut;",
    "let MCONF=0;function toggleManut(){const e=eqState();if(!e.manut&&Date.now()-MCONF>5000){MCONF=Date.now();toast('TOQUE DE NOVO PARA CONFIRMAR: OS ALUNOS NÃO VÃO CONSEGUIR JOGAR',4000);renderAdmin();return}MCONF=0;e.manut=!e.manut;")
rep("h.appendChild(eBtn(me&&me.equip&&me.equip.manut?'🔧 DESLIGAR MANUTENÇÃO':'🔧 MODO MANUTENÇÃO','sm',toggleManut));",
    "h.appendChild(eBtn(me&&me.equip&&me.equip.manut?'🔧 DESLIGAR MANUTENÇÃO':Date.now()-MCONF<5000?'⚠ CONFIRMAR MANUTENÇÃO?':'🔧 MODO MANUTENÇÃO','sm'+(me&&me.equip&&me.equip.manut?' on':''),toggleManut));")
# aviso fixo no topo do painel quando a manutenção está ligada
rep(" if(AD.err){B.appendChild(el('p','esub',AD.err));return}if(!AD.rows)",
    " if(me&&me.equip&&me.equip.manut){const w=el('div','codrow');w.style.borderColor='#c84a3c';w.innerHTML='<p style=\"color:#ffb0a0\"><b>⚠ MODO MANUTENÇÃO LIGADO:</b> os alunos estão vendo o aviso de manutenção e não conseguem jogar. Toque em DESLIGAR MANUTENÇÃO quando terminar.</p>';B.appendChild(w)}\n if(AD.err){B.appendChild(el('p','esub',AD.err));return}if(!AD.rows)")
open(f,'w',encoding='utf-8').write(s);print('manut2 ok',f)
