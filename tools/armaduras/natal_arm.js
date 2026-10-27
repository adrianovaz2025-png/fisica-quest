/* protótipo: armadura natalina (Guardião do Natal) */
ARMT.natal={lv:4,dk:.06,b:'#c0202c',a:'#e8c040',gem:'#3cb04c',g2:'#ffffff',g3:'#ffe070',ne:[255,140,120]};
TIERN.natal='GUARDIÃO DO NATAL';
for(const a of[['elmo_natal','GORRO','Gorro do Guardião do Natal','cabeca'],['arm_natal','CASACO','Casaco do Guardião do Natal','peito'],['botas_natal','BOTAS','Botas do Guardião do Natal','botas']])IT[a[0]]={id:a[0],n:a[1],full:a[2],slot:a[3],r:4,f:'t',t:'natal'};
const FUR='#f4f0ea',FURD='#d8d0c8';
function natDorso(G){const{x,Y}=G,P=armP('natal');prep('natal');
 paint(x,mk2(m=>mPoly(m,[[21,Y(31)],[43,Y(31)],[47,Y(50)],[17,Y(50)]])),mixH(P.b,.8),'cloth',61);
 paint(x,mk2(m=>mRect(m,17,Y(49),30,2.2)),FUR,'cloth',62)}
function natPeito(G){const{x,Y}=G,P=armP('natal');prep('natal');
 /* casaco vermelho até o quadril */
 paint(x,mk2(m=>{mPoly(m,[[22,Y(31.4)],[42,Y(31.4)],[43.4,Y(41)],[44.6,Y(47.6)],[19.4,Y(47.6)],[20.6,Y(41)]]);
  mEll(m,20.4,Y(35.6),4,3.4);mRect(m,16.8,Y(35),6.6,10.6);mEll(m,43.6,Y(35.6),4,3.4);mRect(m,40.6,Y(35),6.6,10.6)}),P.b,'cloth',63);
 /* pelúcia branca: barra, faixa central, punhos e gola */
 paint(x,mk2(m=>{mRect(m,19,Y(46.4),26,2.6);mRect(m,30.6,Y(31.6),2.8,15);mRect(m,16.4,Y(44.6),7.4,2.4);mRect(m,40.2,Y(44.6),7.4,2.4);mEll(m,32,Y(31.6),6.4,1.8)}),FUR,'cloth',64);
 paint(x,mk2(m=>{mRect(m,19,Y(48.2),26,.8);mRect(m,16.4,Y(46.2),7.4,.8);mRect(m,40.2,Y(46.2),7.4,.8)}),FURD,'cloth',65);
 /* cinto preto com fivela dourada */
 paint(x,mk2(m=>mRect(m,20.6,Y(42),22.8,2.6)),'#1c1418','cloth',66);
 cel(x,mk2(m=>{mRect(m,29.4,Y(41.4),5.2,3.8)}),P.a,{chrome:1});paint(x,mk2(m=>mRect(m,30.8,Y(42.4),2.4,1.8)),'#1c1418','cloth',67);
 /* ramo de azevinho no peito */
 cel(x,mk2(m=>{mPoly(m,[[23.4,Y(35.2)],[25.6,Y(33.6)],[27.4,Y(34)],[26.6,Y(35.6)],[24.4,Y(36.4)]]);mPoly(m,[[27.2,Y(35)],[28.4,Y(33.2)],[29.6,Y(34.4)],[29,Y(36.4)],[27.6,Y(36.8)]])}),P.gem,{flat:1});
 cel(x,mk2(m=>{mEll(m,26.6,Y(36.2),.95,.95);mEll(m,28.2,Y(37),.95,.95);mEll(m,27,Y(37.8),.9,.9)}),'#e8202c',{glow:1});
 /* luvas verdes */
 paint(x,mk2(m=>{mRect(m,17.2,Y(46.6),5.8,2.4);mRect(m,41,Y(46.6),5.8,2.4)}),'#1e6a2c','cloth',68)}
function natBotas(G){const{x,lL,lR}=G;prep('natal');
 paint(x,mk2(m=>{mRect(m,24.8,48+lL,6.6,8);mEll(m,28,57+lL,4.6,2.6);mRect(m,32.6,48+lR,6.6,8);mEll(m,36,57+lR,4.6,2.6)}),'#18121a','cloth',69);
 paint(x,mk2(m=>{mRect(m,24,47+lL,8.2,3);mRect(m,31.8,47+lR,8.2,3)}),FUR,'cloth',70);
 cel(x,mk2(m=>{mRect(m,27,53.4+lL,2,1.4);mRect(m,34.8,53.4+lR,2,1.4)}),'#e8c040',{flat:1})}
function natCab(G){const{x,Y,back}=G,P=armP('natal');prep('natal');
 /* gorro vermelho caído para o lado, com pompom */
 paint(x,mk2(m=>mPoly(m,[[20.6,Y(14.2)],[23,Y(7.4)],[28,Y(3.6)],[35,Y(3)],[41,Y(4.6)],[46,Y(7.6)],[49.4,Y(12)],[50.6,Y(17)],[47.6,Y(16)],[44,Y(11)],[43.4,Y(14.2)]])),P.b,'cloth',71);
 paint(x,mk2(m=>mPoly(m,[[35,Y(3.6)],[41,Y(5.2)],[46,Y(8.2)],[49,Y(12.6)],[47,Y(12)],[43,Y(8.6)],[38,Y(6.2)]])),mixH(P.b,1.25),'cloth',72);
 paint(x,mk2(m=>mEll(m,50.2,Y(18.6),3.3,3.1)),FUR,'cloth',73);
 /* faixa de pelúcia e estrela dourada */
 paint(x,mk2(m=>mPoly(m,[[19.6,Y(13)],[26,Y(11)],[32,Y(10.6)],[38,Y(11)],[44.4,Y(13)],[44.6,Y(17)],[38,Y(15.4)],[32,Y(15)],[26,Y(15.4)],[19.4,Y(17)]])),FUR,'cloth',74);
 paint(x,mk2(m=>mPoly(m,[[19.4,Y(16.2)],[26,Y(14.6)],[32,Y(14.2)],[38,Y(14.6)],[44.6,Y(16.2)],[44.6,Y(17)],[38,Y(15.4)],[32,Y(15)],[26,Y(15.4)],[19.4,Y(17)]])),FURD,'cloth',75);
 if(!back){const st=[];for(let k=0;k<10;k++){const a=-Math.PI/2+k*Math.PI/5,r=k%2?1.2:2.8;st.push([32+Math.cos(a)*r,Y(12.9)+Math.sin(a)*r])}cel(x,mk2(m=>mPoly(m,st)),P.a,{glow:1})}
 if(!G.solo)paint(x,mk2(m=>{mEll(m,20,Y(47.6),2.9,2.8);mEll(m,44,Y(47.6),2.9,2.8)}),'#1e6a2c','cloth',76)}
{const p0=eqPeito,c0=eqCabeca,b0=eqBotas,d0=eqDorso;
eqPeito=function(G,id){return armT(id)==='natal'?natPeito(G):p0(G,id)};
eqCabeca=function(G,id){return armT(id)==='natal'?natCab(G):c0(G,id)};
eqBotas=function(G,id){return armT(id)==='natal'?natBotas(G):b0(G,id)};
eqDorso=function(G,id){return armT(id)==='natal'?natDorso(G):d0(G,id)};}
/* penteados altos ficam sob o gorro */
{const s0=sprite,HM={topete:'franjao',moicano:'franjao',coque:'franjao',rabo:'chanel'};sprite=function(L,eq,fr,back,solo){const e=normEq(eq);if(e&&IT[e.cabeca]&&IT[e.cabeca].t==='natal'&&L&&L.hair&&HM[L.hair.s])L={...L,hair:{...L.hair,s:HM[L.hair.s]}};return s0(L,eq,fr,back,solo)}}
