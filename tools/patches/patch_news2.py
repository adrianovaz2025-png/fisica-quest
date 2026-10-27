import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(f,a[:60]);s=s.replace(a,b)
i=s.index("/* ============================ NOVIDADES");j=s.index("function enterGame(){")
s=s[:i]+r"""/* ============================ NOVIDADES (cartaz, 1x por versão) ============================ */
const NEWS={v:'2026-10-27',sub:'ATUALIZAÇÃO DE OUTUBRO',arm:1,cards:[
 ['🏰','CIDADELA DAS PROVAS','A Torre ENEM cresceu! A aba agora é VESTIBULARES: escolha a prova e treine.','#e8b840'],
 ['🎖️','ESPCEX','Provas 2025 e 2026 completas. Faça o 1º dia, o 2º dia ou só uma matéria.','#7ac850'],
 ['🏫','IF SUL DE MINAS','Provas 2025 e 2026 do técnico integrado: Português e Matemática.','#5aa8e8'],
 ['📖','RESOLUÇÕES','Errou? Toque em VER RESOLUÇÃO e entenda a questão. Física, Química e Biologia do ENEM.','#c878e8']]};
const NARM=[['medico','FÍSICO DA PESTE',0,[120,220,110]],['geada','GEADA ETERNA',2,[150,225,255]]];
let NWA=0;
function nwPoster(cv){const x=cv.getContext('2d'),W=680,H=330,R=2;cv.width=W*R;cv.height=H*R;
 const rnd=(a=>()=>(a=(a*16807)%2147483647)/2147483647)(7);
 const st=[...Array(70)].map(()=>[rnd()*W,rnd()*150,rnd()*6]),fog=[...Array(26)].map(()=>[rnd(),rnd(),rnd()]),snow=[...Array(40)].map(()=>[rnd(),rnd(),rnd()]);
 const arm=NEWS.arm&&NARM.every(a=>ARMT[a[0]]);const FN="'Press Start 2P',monospace";
 const txt=(t,X,Y,sz,c,o='#1a1020',al='center')=>{x.font=`${sz}px ${FN}`;x.textAlign=al;x.fillStyle=o;for(const[dx,dy]of[[-2,0],[2,0],[0,-2],[0,2],[2,2],[0,4],[2,4]])x.fillText(t,X+dx,Y+dy);x.fillStyle=c;x.fillText(t,X,Y)};
 const frame=()=>{if(!$('news').classList.contains('on')){NWA=0;return}const t=performance.now();x.setTransform(R,0,0,R,0,0);x.imageSmoothingEnabled=false;
  let g=x.createLinearGradient(0,0,0,H);g.addColorStop(0,'#07051a');g.addColorStop(.6,'#1c1440');g.addColorStop(1,'#2a1c3a');x.fillStyle=g;x.fillRect(0,0,W,H);
  for(const[a,b,c]of st){x.globalAlpha=.35+.65*Math.abs(Math.sin(t/700+c));x.fillStyle='#fff';x.fillRect(a|0,b|0,c>4?2:1,c>4?2:1)}x.globalAlpha=1;
  x.fillStyle='#f4ecc8';x.beginPath();x.arc(W-70,52,20,0,7);x.fill();x.fillStyle='#07051a';x.beginPath();x.arc(W-62,46,18,0,7);x.fill();
  // cidadela ao fundo
  const cx=W/2,by=268;x.fillStyle='#120c26';
  x.fillRect(cx-150,by-40,300,40);for(let k=-150;k<150;k+=16)x.fillRect(cx+k,by-48,9,8);
  for(const[ox,w,h]of[[-120,34,80],[86,34,80],[-60,30,100],[30,30,100]]){x.fillRect(cx+ox,by-h,w,h);for(let k=0;k<w;k+=10)x.fillRect(cx+ox+k,by-h-7,6,7)}
  x.fillRect(cx-22,by-150,44,150);x.beginPath();x.moveTo(cx-30,by-150);x.lineTo(cx,by-196);x.lineTo(cx+30,by-150);x.fill();
  const pu=.55+.45*Math.sin(t/500);g=x.createLinearGradient(0,0,0,by-196);g.addColorStop(0,'rgba(160,200,255,0)');g.addColorStop(1,`rgba(160,200,255,${.25*pu+.1})`);x.fillStyle=g;x.fillRect(cx-6,0,12,by-196);
  x.fillStyle=`rgba(200,230,255,${.6+.4*pu})`;x.beginPath();x.arc(cx,by-200,5,0,7);x.fill();
  x.fillStyle='#f8d860';for(const[wx,wy]of[[-8,-120],[4,-120],[-8,-90],[4,-90],[-48,-70],[40,-70],[-108,-55],[98,-55]]){x.globalAlpha=.5+.5*Math.sin(t/300+wx);x.fillRect(cx+wx,by+wy,4,6)}x.globalAlpha=1;
  x.fillStyle='#0c0818';x.fillRect(0,by,W,H-by);
  // título
  txt('NOVIDADES',cx,56,30,'#f8d860');txt('NO IMPÉRIO',cx,84,12,'#f4e4c0');
  x.fillStyle='#c8902a';x.fillRect(cx-112,98,224,20);x.fillStyle='#8a5a14';x.fillRect(cx-112,114,224,4);x.fillStyle='#1a1020';x.font=`8px ${FN}`;x.textAlign='center';x.fillText(NEWS.sub,cx,112);
  if(arm)NARM.forEach(([id,nm,lk,c],k)=>{const px=k?W-118:118,py=by+8,[r,gg,b]=c,pl=.6+.4*Math.sin(t/400+k*2);
   let rg=x.createRadialGradient(px,py-70,6,px,py-70,120);rg.addColorStop(0,`rgba(${r},${gg},${b},${.35*pl})`);rg.addColorStop(1,`rgba(${r},${gg},${b},0)`);x.fillStyle=rg;x.fillRect(px-130,py-200,260,220);
   if(!k)for(const[a,bb,cc]of fog){const yy=(bb*200-t*(.012+cc*.012))%200;const Y=py-((yy+200)%200);x.globalAlpha=.6*(1-((yy+200)%200)/200);x.fillStyle='#8ae060';x.fillRect(px-70+a*140,Y,cc>.6?3:2,cc>.6?3:2)}
   else for(const[a,bb,cc]of snow){const Y=((bb*230+t*(.015+cc*.02))%230)+py-220;x.globalAlpha=.8;x.fillStyle='#e8f8ff';x.fillRect(px-80+a*160+Math.sin(t/600+cc*9)*6,Y,cc>.6?3:2,cc>.6?3:2)}
   x.globalAlpha=1;
   x.fillStyle='#3a3048';x.fillRect(px-58,py-6,116,14);x.fillStyle='#5a4e6a';x.fillRect(px-58,py-6,116,4);x.fillStyle='#262034';x.fillRect(px-48,py+8,96,10);
   drawChar(x,LOOKS[lk],{cabeca:'elmo_'+id,peito:'arm_'+id,botas:'botas_'+id},Math.floor(t/450+k*.7)%2?3:0,px,py-6,4.6);
   const pw=nm.length*8+22;x.fillStyle='#1a1020';x.fillRect(px-pw/2-2,by+28,pw+4,24);x.fillStyle=k?'#2a6a9a':'#3a6a2a';x.fillRect(px-pw/2,by+30,pw,20);x.fillStyle=k?'#c8f4ff':'#c8f8a8';x.font=`8px ${FN}`;x.textAlign='center';x.fillText(nm,px,by+44);
  });
  if(arm){x.save();x.translate(cx,by+40);txt('★ NOVAS ARMADURAS ★',0,0,10,'#f8d860');x.restore()}
  NWA=requestAnimationFrame(frame)};
 cancelAnimationFrame(NWA);(document.fonts?document.fonts.load(`10px ${FN}`):Promise.resolve()).then(frame,frame)}
function showNews(force){if(!me)return;const k='fq_news_'+String(me.nick).toLowerCase();let seen='';try{seen=localStorage.getItem(k)||''}catch(e){}if(!force&&(seen===NEWS.v||document.querySelector('.ov.on')))return;
 const C=$('nwC');C.innerHTML='';const cv=document.createElement('canvas');cv.className='nwcv';C.appendChild(cv);
 if(NEWS.arm)C.insertAdjacentHTML('beforeend','<p class="nwarm">Duas armaduras inéditas chegam ao Império. <b>Fique de olho!</b></p>');
 C.insertAdjacentHTML('beforeend','<div class="nwg">'+NEWS.cards.map(([ic,h,d,c])=>`<div class="nwc" style="--c:${c}"><div class="nwch"><span>${ic}</span><b>${h}</b></div><p>${d}</p></div>`).join('')+'</div>');
 C.insertAdjacentHTML('beforeend','<div class="nwcd"><div class="nwcdt">⏳ CONTAGEM REGRESSIVA</div><div class="nwcdr">'+PROVAS_DATAS.map(([ic,n,dt])=>{const d=dt?diasAte(dt):null;return `<div><small>${ic} ${n}</small><b>${d===null?'SET/27':d<0?'—':d===0?'HOJE':d}</b><i>${d===null?'próxima prova':d>0?(d===1?'DIA':'DIAS'):''}</i></div>`}).join('')+'</div></div>');
 C.insertAdjacentHTML('beforeend','<button class="big" id="nwGo">🏰 IR PARA A CIDADELA</button><button class="lnk" id="nwOk">Depois eu vejo</button>');
 const close=()=>{$('news').classList.remove('on');try{localStorage.setItem(k,NEWS.v)}catch(e){}};$('nwX').onclick=close;$('nwOk').onclick=close;$('nwGo').onclick=()=>{close();ES.scr='home';setTab('enem')};$('news').classList.add('on');nwPoster(cv)}
"""+s[j:]
a=s[s.index(".nwb{"):s.index("\n.lnk{display:block;")]
s=s.replace(a,""".nwb{width:min(720px,96vw);padding:34px 14px 12px}.nwcv{display:block;width:100%;aspect-ratio:680/330;border:3px solid #1a1020;box-shadow:0 0 0 3px #e8c070,0 0 0 6px #5a3a22;margin:4px 0 12px;image-rendering:pixelated}
.nwarm{text-align:center;font-size:8px;line-height:1.8;color:#e8d8b8;margin:0 0 12px}.nwarm b{color:#f8d870}
.nwg{display:grid;grid-template-columns:1fr 1fr;gap:8px}.nwc{background:#1e140e;border:3px solid #1a1020;box-shadow:inset 4px 0 0 var(--c);padding:9px 10px 9px 14px}.nwch{display:flex;align-items:center;gap:8px}.nwch span{font-size:18px}.nwch b{font-size:8px;color:var(--c);line-height:1.5}.nwc p{margin:6px 0 0;font-size:7px;line-height:1.8;color:#e8d8b8}
.nwcd{margin-top:10px;background:#1a1430;border:3px solid #4a3a7a;padding:8px}.nwcdt{font-size:7px;color:#b8a8e8;text-align:center;margin-bottom:6px}.nwcdr{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;text-align:center}.nwcdr div{background:#120e24;padding:6px 2px;display:flex;flex-direction:column;gap:5px}.nwcdr small{font-size:6px;color:#c8b8f0;line-height:1.5}.nwcdr b{font-size:16px;color:#f8d860}.nwcdr i{font-style:normal;font-size:6px;color:#9a8ac8}
@media(max-width:560px){.nwg{grid-template-columns:1fr}}""")
open(f,'w',encoding='utf-8').write(s);print('news2 ok',f)
