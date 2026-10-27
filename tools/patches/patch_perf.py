import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b,opt=False):
    global s
    n=s.count(a)
    if opt and n==0:return False
    assert n==1,(n,a[:70]);s=s.replace(a,b);return True

# 1) resolução da tela: no máximo 2x e ~2,1 milhões de pixels; cai sozinha se o aparelho estiver lento
rep("function resize(){const d=window.devicePixelRatio||1;",
    "let RESQ=1,PERF={n:0,t:0,slow:0};\nfunction resize(){let d=Math.min(2,window.devicePixelRatio||1)*RESQ;")
rep("const k=Math.min(innerWidth/VW,innerHeight/VH);K=k*d;",
    "const k=Math.min(innerWidth/VW,innerHeight/VH);{const px=VW*k*d*VH*k*d;if(px>2.1e6)d*=Math.sqrt(2.1e6/px);d=Math.max(1,d)}K=k*d;")
rep("function frameBody(now){const dt=Math.min(50,now-last);",
    "function perfTick(dt){if(screen!=='game')return;PERF.n++;PERF.t+=dt;if(PERF.n>=90){const avg=PERF.t/PERF.n;PERF.n=0;PERF.t=0;if(avg>26&&RESQ>.55){RESQ=Math.max(.55,RESQ-.15);resize()}}}\nfunction frameBody(now){perfTick(now-last);const dt=Math.min(50,now-last);")

# 2) personagens: guarda a versão já reduzida de cada sprite (antes reduzia com qualidade alta a cada quadro)
rep(" const sc=x.getTransform?Math.abs(x.getTransform().a)||1:1;if(32*s*sc<MS*.98){x.imageSmoothingEnabled=true;x.imageSmoothingQuality='high'}\n x.drawImage(img,Math.round(px-16*s),Math.round(py-31*s),32*s,32*s);x.imageSmoothingEnabled=false;",
    " const sc=x.getTransform?Math.abs(x.getTransform().a)||1:1,tp=Math.round(32*s*sc);if(tp<MS*.98&&img!==GLC){img=scaledSpr(img,tp);x.imageSmoothingEnabled=false}else if(tp<MS*.98){x.imageSmoothingEnabled=true;x.imageSmoothingQuality='high'}\n x.drawImage(img,Math.round(px-16*s),Math.round(py-31*s),32*s,32*s);x.imageSmoothingEnabled=false;")
rep("function drawChar(x,ch,eq,fr,px,py,s=1,back=false){",
    "const SCC=new WeakMap();let SCN=0;function scaledSpr(img,tp){let m=SCC.get(img);if(!m){m=new Map();SCC.set(img,m)}let o=m.get(tp);if(o)return o;if(m.size>6)m.clear();if(SCN++>4000){SCN=0}o=mk(tp,tp);const q=o.getContext('2d');q.imageSmoothingEnabled=true;q.imageSmoothingQuality='high';\n let src=img,w=img.width;while(w/2>=tp*1.4){const h=mk(Math.ceil(w/2),Math.ceil(w/2)),hq=h.getContext('2d');hq.imageSmoothingEnabled=true;hq.imageSmoothingQuality='high';hq.drawImage(src,0,0,w,w,0,0,h.width,h.width);src=h;w=h.width}\n q.drawImage(src,0,0,w,w,0,0,tp,tp);m.set(tp,o);return o}\nfunction drawChar(x,ch,eq,fr,px,py,s=1,back=false){")

# 3) mundo afastado (zoom < 1): redução com qualidade 'low' em vez de 'high' (era o mais pesado na vista geral)
rep("if(Z<1){g.imageSmoothingEnabled=true;g.imageSmoothingQuality='high'}","if(Z<1){g.imageSmoothingEnabled=true;g.imageSmoothingQuality=Z<.75?'medium':'low'}")

# 4) espuma e brilho da água: só percorre a parte que está na tela (separados em blocos de 128 px)
rep(" wb.fillStyle=W.shimC;for(const s of W.shim){const x=s[0]-cx,y=s[1]-cy;if(x<-3||y<0||x>RW||y>RH)continue;",
    " if(!W._fb){const B=(arr)=>{const m=new Map();for(const p of arr){const k=((p[0]>>7)<<12)|(p[1]>>7);let a=m.get(k);if(!a)m.set(k,a=[]);a.push(p)}return m};W._fb=B(W.foam);W._sb=B(W.shim)}\n const inV=(m,fn)=>{for(let bx=(cx>>7)-1;bx<=((cx+RW)>>7);bx++)for(let by=(cy>>7)-1;by<=((cy+RH)>>7);by++){const a=m.get((bx<<12)|by);if(a)for(const p of a)fn(p)}};\n wb.fillStyle=W.shimC;inV(W._sb,s=>{const x=s[0]-cx,y=s[1]-cy;if(x<-3||y<0||x>RW||y>RH)return;")
rep("const a=Math.sin(T0/420+s[2]);if(a>.62)wb.fillRect(x,y,a>.9?3:2,1)}\n","const a=Math.sin(T0/420+s[2]);if(a>.62)wb.fillRect(x,y,a>.9?3:2,1)});\n")
rep(" const fcol=W.foamC;for(const f of W.foam){const x=f[0]-cx,y=f[1]-cy;if(x<0||y<0||x>=RW||y>=RH)continue;const a=Math.sin(T0/650+f[2]);if(a>.3){wb.fillStyle=a>.82?'#ffffff':fcol;wb.fillRect(x,y,1,1)}}",
    " const fcol=W.foamC;wb.fillStyle=fcol;const FW=[];inV(W._fb,f=>{const x=f[0]-cx,y=f[1]-cy;if(x<0||y<0||x>=RW||y>=RH)return;const a=Math.sin(T0/650+f[2]);if(a>.3){if(a>.82)FW.push(x,y);else wb.fillRect(x,y,1,1)}});wb.fillStyle='#ffffff';for(let i=0;i<FW.length;i+=2)wb.fillRect(FW[i],FW[i+1],1,1);")

# 5) oclusão dos personagens: laço simples sem criar listas a cada quadro
rep("W._hi.push({...s.hi,px,py,occ:vis.filter(o=>o.img&&o.dep>s.dep&&o.x<px+16&&o.x+o.w>px-16&&o.y<py+2&&o.y+o.h>py-31)});continue}",
    "const occ=[];for(let j=vis.length-1;j>=0;j--){const o=vis[j];if(o.dep<=s.dep)break;if(o.img&&o.x<px+16&&o.x+o.w>px-16&&o.y<py+2&&o.y+o.h>py-31)occ.push(o)}occ.reverse();W._hi.push({...s.hi,px,py,occ});continue}")

# 6) mini mapa menor (só na página com mini mapa)
if rep("const mw=128,CX0=W.w*.2","const mw=96,CX0=W.w*.2",opt=True):
    rep("x0=VW-mw-48,y0=30;","x0=VW-mw-44,y0=28;")
    rep("dot(T2[0],T2[1],TURMAS[i].cor.f,3,TURMAS[i].tribo.slice(0,4))","dot(T2[0],T2[1],TURMAS[i].cor.f,2,'')")
    rep("T('VOCÊ',a,b-12,4,'#fff','center')","T('VOCÊ',a,b-10,3,'#fff','center')")
    rep("if(W.C)dot(W.C[0],W.C[1],'#9ae8ff',2,'ENEM');if(W.ISL)dot(W.ISL[0],W.ISL[1],'#b890ff',2,'MAGO');if(W.CID)dot(W.CID[0],W.CID[1],'#fff0b0',2,'MESTRE');",
        "if(W.C)dot(W.C[0],W.C[1],'#9ae8ff',2,'');if(W.ISL)dot(W.ISL[0],W.ISL[1],'#b890ff',1,'');if(W.CID)dot(W.CID[0],W.CID[1],'#fff0b0',1,'');")
    rep("strokeRect(Math.round(a-6),Math.round(b-6),12,12)","strokeRect(Math.round(a-4),Math.round(b-4),8,8)")
open(f,'w',encoding='utf-8').write(s);print('perf ok',f)

# 7) vista afastada: usa uma "foto" do reino já montada (meia resolução) em vez de redesenhar ~1000 construções por quadro
s=open(f,encoding='utf-8').read()
FAR=r'''function farBake(W){const cv=mk(Math.ceil(W.w/2),Math.ceil(W.h/2)),x=cv.getContext('2d');x.imageSmoothingEnabled=true;x.imageSmoothingQuality='high';x.drawImage(W.dec,0,0,cv.width,cv.height);
 for(const o of W.spr.slice().sort((a,b)=>a.dep-b.dep)){if(o.hi)continue;if(o.img)x.drawImage(o.img,o.x/2,o.y/2,o.img.width/2,o.img.height/2);else if(o.draw){x.save();x.scale(.5,.5);try{o.draw(x,0,0,1000)}catch(e){}x.restore()}}
 W._hiS=W.spr.filter(o=>o.hi);return cv}
function renderFar(W,extra){const Z=ZM(W),RW=Math.ceil(VW/Z),RH=Math.ceil(VH/Z),cx=Math.round(W.cam.x),cy=Math.round(W.cam.y);if(!W.far)W.far=farBake(W);
 g.fillStyle='#1a3a5a';g.fillRect(0,0,VW,VH);g.imageSmoothingEnabled=true;g.imageSmoothingQuality='low';g.drawImage(W.far,cx/2,cy/2,RW/2,RH/2,0,0,VW,VH);g.imageSmoothingEnabled=false;
 const vis=[];for(const s of W._hiS){const[px,py]=s.hi.P;if(px-cx>-20&&px-cx<RW+20&&py-cy>-40&&py-cy<RH+40)vis.push(s)}
 for(const u of W.units){const[ox,oy]=ringPos(u),X=u.tx+ox,Y=u.ty+oy,[px,py]=W.P(X,Y);if(px-cx<-10||px-cx>RW+10||py-cy<-14||py-cy>RH+14)continue;vis.push({dep:X+Y,draw:(x)=>{const f=u.pause>0?0:Math.floor(T0/180+u.s*3)%2;x.drawImage(villager(u.col,u.sold,f),Math.round(px-cx-5),Math.round(py-cy-13))}})}
 for(const b of W.boats){const X=b.x!=null?b.x:b.C[0]+Math.cos(b.a)*b.r,Y=b.x!=null?b.y:b.C[1]+Math.sin(b.a)*b.r,[px,py]=W.Pf(X,Y);if(px-cx<-40||px-cx>RW+40||py-cy<-40||py-cy>RH+20)continue;const dX=b.x!=null?Math.cos(b.h):-Math.sin(b.a)*Math.sign(b.sp),dY=b.x!=null?Math.sin(b.h):Math.cos(b.a)*Math.sign(b.sp);vis.push({dep:X+Y,draw:x=>drawBoat(x,px-cx,py-cy,(dX-dY)<0,b.col,T0)})}
 if(extra)vis.push(...extra);vis.sort((a,b)=>a.dep-b.dep);W._hi=[];W._cx=cx;W._cy=cy;
 g.setTransform(Z,0,0,Z,0,0);for(const s of vis){if(s.hi){const[px,py]=s.hi.P;W._hi.push({...s.hi,px,py,occ:[]});continue}if(s.img)g.drawImage(s.img,Math.round(s.x-cx),Math.round(s.y-cy));else s.draw(g,cx,cy,T0)}g.setTransform(1,0,0,1,0,0)}
function renderWorld(W,extra){
 if(W===tribeWorld&&ZM(W)<=.56){clampCam(W);return renderFar(W,extra)}
 if(W===tribeWorld&&!W.far&&!W._farQ){W._farQ=1;setTimeout(()=>{if(!W.far&&tribeWorld===W)W.far=farBake(W)},2500)}'''
a="function renderWorld(W,extra){\n"
assert s.count(a)==1;s=s.replace(a,FAR+"\n")
# espuma/brilho somem com zoom bem afastado (pixels pequenos demais para ver)
a=" wb.fillStyle=W.shimC;inV(W._sb,"
assert s.count(a)==1;s=s.replace(a," if(Z>=.7){wb.fillStyle=W.shimC;inV(W._sb,")
a="for(let i=0;i<FW.length;i+=2)wb.fillRect(FW[i],FW[i+1],1,1);"
assert s.count(a)==1;s=s.replace(a,a+"}")
open(f,'w',encoding='utf-8').write(s);print('far ok')
