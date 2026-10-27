import sys
f=sys.argv[1];s=open(f,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(f,a[:60]);s=s.replace(a,b)
rep("Wd.ENEMT=[px,py,sp];return e}","Wd.ENEMT=[px,py,sp];Wd.ENEMC=C;return e}")
# aluno externo mora ao lado da Cidadela; posição do herói guardada para o botão "achar"
rep("T=i>=0?W.TP[i]:[W.PROF[0]-1.3,W.PROF[1]+1.2],hx2=T[0]+2.5,hy=T[1]-.4;",
    "T=i>=0?W.TP[i]:(isExt()&&W.ENEMC?[W.ENEMC[0]-.6,W.ENEMC[1]+2.4]:[W.PROF[0]-1.3,W.PROF[1]+1.2]),hx2=T[0]+2.5,hy=T[1]-.4;W.MEP=null;")
rep("isMe=me&&m.nick===me.nick;if(isMe)meOn=true;","isMe=me&&m.nick===me.nick;if(isMe){meOn=true;W.MEP=W.P(X,Y)}")
rep("if(!meOn&&!adm)ex.push({dep:hx2+hy,","if(!meOn&&!adm){W.MEP=W.P(hx2,hy)}if(!meOn&&!adm)ex.push({dep:hx2+hy,")
rep("function focusTribe(i){if(!tribeWorld||i<0)return;",
    "let FINDT=-1e9;function findMe(W){if(W&&W.MEP){centerOn(W,W.MEP[0],W.MEP[1]-16);FINDT=T0}else focusTribe(TURMAS.findIndex(t=>t.id===me.turma))}\nfunction focusTribe(i){if(tribeWorld&&i<0&&isExt()&&tribeWorld.ENEMC){const[px,py]=tribeWorld.P(tribeWorld.ENEMC[0]+1.9,tribeWorld.ENEMC[1]+2);centerOn(tribeWorld,px,py-20);return}if(!tribeWorld||i<0)return;")
rep("mapBtns(W,()=>focusTribe(TURMAS.findIndex(t=>t.id===me.turma)));","mapBtns(W,()=>findMe(W));")
# seta grande piscando por 4 s depois de tocar no botão
rep("if(h.arrow){const bb=Math.sin(T0/200)*2;c.fillStyle=GOLD;for(let k=0;k<4;k++)c.fillRect(vx-3*Z+k*Z,vy+(-36+bb+k)*Z,(7-2*k)*Z,Z)}",
    "if(h.arrow){const bb=Math.sin(T0/200)*2;c.fillStyle=GOLD;for(let k=0;k<4;k++)c.fillRect(vx-3*Z+k*Z,vy+(-36+bb+k)*Z,(7-2*k)*Z,Z);"
    "if(T0-FINDT<4500){const u=Math.max(2,Z*1.6),b2=Math.abs(Math.sin(T0/160))*6*u,ty=vy-44*Z-b2,AR=[[-3,-9],[3,-9],[3,-3],[7,-3],[0,5],[-7,-3],[-3,-3]];"
    "c.beginPath();AR.forEach(([a,b],k)=>{const X=vx+a*u,Y=ty+b*u;k?c.lineTo(X,Y):c.moveTo(X,Y)});c.closePath();c.fillStyle='#e8402a';c.fill();c.lineWidth=Math.max(2,u*.9);c.strokeStyle='#1a1020';c.stroke();"
    "c.fillStyle='#ffd860';c.fillRect(vx-1.6*u,ty-8*u,1.2*u,4.6*u);T('VOCÊ',vx,ty-9*u-9,7,'#fff','center')}}")
open(f,'w',encoding='utf-8').write(s);print('achar ok',f)
