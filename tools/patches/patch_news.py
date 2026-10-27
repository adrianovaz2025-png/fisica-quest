import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(f,a[:60]);s=s.replace(a,b)
rep('<div class="ov" id="emq"><div class="box">','<div class="ov" id="news" style="z-index:8"><div class="box nwb"><button class="x" id="nwX">X</button><div id="nwC"></div></div></div>\n<div class="ov" id="emq"><div class="box">')
rep("\nfunction enterGame(){setTimeout(pedirEmail,4000);","""
/* ============================ NOVIDADES (pop-up 1x por versão) ============================ */
const NEWS={v:'2026-10-27',t:'📜 NOVIDADES NO IMPÉRIO!',it:[
 ['🏰','A TORRE AGORA É A CIDADELA DAS PROVAS','A aba ENEM virou VESTIBULARES. Lá você escolhe para qual prova quer treinar.'],
 ['🎖️','CHEGOU A ESPCEX','Provas de 2025 e 2026 completas: 1º e 2º dia, ou só a matéria que você quiser.'],
 ['🏫','CHEGOU O IF SUL DE MINAS','Provas de 2025 e 2026 do técnico integrado: Português e Matemática.'],
 ['📖','RESOLUÇÕES COMENTADAS','Errou? Depois de responder, toque em VER RESOLUÇÃO. Já disponível em Física, Química e Biologia do ENEM.'],
 ['⏳','CONTAGEM REGRESSIVA','__CD__']]};
function newsCD(){return PROVAS_DATAS.filter(p=>p[2]&&diasAte(p[2])>=0).map(p=>{const k=diasAte(p[2]);return `${p[1]}: <b>${k===0?'HOJE':k===1?'AMANHÃ':k+' DIAS'}</b>`}).join(' · ')||'Confira as datas na Cidadela.'}
function showNews(force){if(!me)return;const k='fq_news_'+String(me.nick).toLowerCase();let seen='';try{seen=localStorage.getItem(k)||''}catch(e){}if(!force&&(seen===NEWS.v||document.querySelector('.ov.on')))return;
 const C=$('nwC');C.innerHTML=`<h2 class="center">${NEWS.t}</h2>`+NEWS.it.map(([ic,h,d])=>`<div class="nwi"><span class="nwic">${ic}</span><div><b>${h}</b><p>${d==='__CD__'?newsCD():d}</p></div></div>`).join('')+'<button class="big" id="nwGo">🏰 IR PARA A CIDADELA</button><button class="lnk" id="nwOk">Depois eu vejo</button>';
 const close=()=>{$('news').classList.remove('on');try{localStorage.setItem(k,NEWS.v)}catch(e){}};$('nwX').onclick=close;$('nwOk').onclick=close;$('nwGo').onclick=()=>{close();ES.scr='home';setTab('enem')};$('news').classList.add('on')}
function enterGame(){setTimeout(()=>showNews(),1800);setTimeout(pedirEmail,4000);""")
rep(".lnk{display:block;",".nwb{width:min(600px,94vw)}.nwi{display:flex;gap:12px;align-items:flex-start;padding:9px 0;border-top:2px solid #3a2a1a}.nwi:first-of-type{border-top:0}.nwic{font-size:20px;line-height:1}.nwi b{color:#f8d870;font-size:9px;line-height:1.6}.nwi p{margin:3px 0 0;font-size:8px;line-height:1.7;color:#e8d8b8}.nwi p b{font-size:9px}\n.lnk{display:block;")
open(f,'w',encoding='utf-8').write(s);print('news ok',f)
