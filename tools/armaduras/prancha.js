const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/t.html');await p.waitForTimeout(2000);
await p.addScriptTag({path:'novas_arm.js'});
await p.evaluate(()=>{
 const W=1600,H=1000,cv=document.createElement('canvas');cv.width=W;cv.height=H;cv.id='pr';Object.assign(cv.style,{position:'fixed',left:0,top:0,zIndex:99999});document.body.appendChild(cv);
 const x=cv.getContext('2d');x.fillStyle='#1a1220';x.fillRect(0,0,W,H);
 const SETS=[['medico','FÍSICO DA PESTE','Máscara de bico, chapéu de aba larga, sobretudo de couro, cinto com frasco de remédio',LOOKS[0],[['#3a2a4a','#d0b060'],['#5a1a1a','#c8c8c8']]],
             ['geada','GEADA ETERNA','Placas de gelo polido, coroa e ombreiras de cristal, floco de neve no peito, cristais nas costas',LOOKS[2],[['#2a3a6a','#e8f0ff'],['#e8e0f8','#a070e0']]]];
 const sp=(L,eq,fr,back,X,Y,S)=>{x.imageSmoothingEnabled=false;x.drawImage(sprite(L,eq,fr,back),X,Y,S,S)};
 const txt=(t,X,Y,sz,c,al='left',w='bold')=>{x.font=`${w} ${sz}px monospace`;x.fillStyle=c;x.textAlign=al;x.fillText(t,X,Y)};
 SETS.forEach(([t,nome,desc,L,vars],k)=>{const ox=k*800;const eq={cabeca:'elmo_'+t,peito:'arm_'+t,botas:'botas_'+t};
  x.fillStyle=k?'#141c2a':'#1e1810';x.fillRect(ox+10,10,780,980);x.strokeStyle='#5a3a22';x.lineWidth=4;x.strokeRect(ox+10,10,780,980);
  txt(nome,ox+400,56,30,'#f4d070','center');txt(desc,ox+400,84,12,'#c8b898','center','normal');
  const gr=x.createRadialGradient(ox+210,380,20,ox+210,380,220);gr.addColorStop(0,'rgba(248,216,112,.18)');gr.addColorStop(1,'rgba(0,0,0,0)');x.fillStyle=gr;x.fillRect(ox+20,100,400,520);
  sp(L,eq,0,false,ox+30,110,384);txt('FRENTE',ox+222,520,12,'#8a7a62','center');
  sp(L,eq,0,true,ox+440,140,256);txt('COSTAS',ox+568,400,12,'#8a7a62','center');
  for(let f=1;f<=3;f++)sp(L,eq,f,false,ox+30+(f-1)*130,540,128);txt('ANDANDO',ox+222,680,12,'#8a7a62','center');
  // tamanho real no jogo
  x.fillStyle='#2a4a2a';x.fillRect(ox+440,430,320,110);txt('TAMANHO NO JOGO',ox+600,560,12,'#8a7a62','center');
  for(let i=0;i<3;i++){x.imageSmoothingEnabled=true;x.imageSmoothingQuality='high';x.drawImage(sprite(LOOKS[i+1],eq,0,false),ox+470+i*95,445,64,64)}
  // peças
  const pcs=[['cabeca','CABEÇA'],['peito','PEITO'],['botas','PÉS']];pcs.forEach(([s,n],i)=>{x.fillStyle='#120c18';x.fillRect(ox+440+i*110,580,100,110);sp(LOOKS[0],{[s]:eq[s]},0,false,ox+446+i*110,580,88);txt(n,ox+490+i*110,684,10,'#8a7a62','center')});
  // variações de cor (personalização)
  txt('COM COR PERSONALIZADA (ALUNO PODE TROCAR)',ox+400,730,12,'#c8b898','center');
  vars.forEach(([cb,ca],i)=>{sp({...L,arm:{b:cb,a:ca}},eq,0,false,ox+130+i*290,740,240)});
  sp(LOOKS[3],eq,0,false,ox+300,800,170);
 });
 txt('PRANCHA PARA APROVAÇÃO · NOVAS ARMADURAS · IMPÉRIO',800,985,11,'#6a5a4a','center','normal');
});
await p.waitForTimeout(400);await p.screenshot({path:'/tmp/claude-0/-home-claude/9f3d9dab-90ee-573d-a3a2-0e204f59919c/scratchpad/shots/prancha.png'});
console.log(errs.slice(0,5));await b.close()})();
