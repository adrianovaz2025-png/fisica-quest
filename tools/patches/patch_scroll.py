import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
a="function renderEnem(){const B=$('eBody');B.innerHTML='';B.className='ebody s-'+ES.scr;({home:eHome,mat:eMat,qtd:eQtd,quiz:eQuiz,res:eRes,perf:ePerf})[ES.scr](B)}"
assert s.count(a)==1
s=s.replace(a,"""function renderEnem(){const B=$('eBody'),key=ES.scr+':'+ES.cur+':'+(ES.rev?1:0),same=ES._sk===key;ES._sk=key;
 /* guarda a rolagem de tudo (página, imagem da questão, colunas) para não voltar ao topo ao marcar uma alternativa */
 const keep=same?[B.scrollTop,...[...B.querySelectorAll('*')].map(e=>e.scrollTop)]:null,hk=same?[B.parentNode&&B.parentNode.scrollTop,document.scrollingElement&&document.scrollingElement.scrollTop]:null;
 B.innerHTML='';B.className='ebody s-'+ES.scr;({home:eHome,mat:eMat,qtd:eQtd,quiz:eQuiz,res:eRes,perf:ePerf})[ES.scr](B);
 if(keep){const put=()=>{const L=[...B.querySelectorAll('*')];if(keep[0])B.scrollTop=keep[0];L.forEach((e,i)=>{const v=keep[i+1];if(v&&e.scrollTop!==v)e.scrollTop=v});if(hk[0]&&B.parentNode)B.parentNode.scrollTop=hk[0];if(hk[1]&&document.scrollingElement)document.scrollingElement.scrollTop=hk[1]};
  put();requestAnimationFrame(put);B.querySelectorAll('img').forEach(im=>{if(!im.complete)im.addEventListener('load',put,{once:true})})}}""")
open(f,'w',encoding='utf-8').write(s);print('scroll ok',f)
