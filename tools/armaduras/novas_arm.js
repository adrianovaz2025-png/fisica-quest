/* protótipo: duas armaduras novas (médico da peste + geada eterna) */
Object.assign(ARMT,{
 medico:{lv:4,dk:.12,b:'#1c1a20',a:'#7a6e60',gem:'#8ae060',g2:'#d8c8a0',g3:'#8ae060',ne:[120,220,110]},
 geada:{lv:4,dk:.06,b:'#dceefa',a:'#3e9ad6',gem:'#a8f4ff',g2:'#ffffff',g3:'#60d4ff',ne:[150,225,255]}});
TIERN.medico='FÍSICO DA PESTE';TIERN.geada='GEADA ETERNA';
for(const a of[
 ['elmo_medico','MÁSCARA','Máscara do Físico da Peste','cabeca',4,'t','medico','',''],
 ['arm_medico','SOBRETUDO','Sobretudo do Físico da Peste','peito',4,'t','medico','',''],
 ['botas_medico','BOTAS','Botas do Físico da Peste','botas',4,'t','medico','',''],
 ['elmo_geada','TIARA','Tiara da Geada Eterna','cabeca',4,'t','geada','',''],
 ['arm_geada','ARMADURA','Armadura da Geada Eterna','peito',4,'t','geada','',''],
 ['botas_geada','GREVAS','Grevas da Geada Eterna','botas',4,'t','geada','','']]){const o={id:a[0],n:a[1],full:a[2],slot:a[3],r:a[4],f:a[5],t:a[6]};IT[o.id]=o}

const _peito=eqPeito,_cab=eqCabeca,_bot=eqBotas,_dor=eqDorso;
const prep=t=>{const A=ARMT[t];RIMN=A.ne||null;DKN=A.dk;SOFTN=0};
const BONE='#cbbd9a',LEATHER='#2e221a';

/* ---------- FÍSICO DA PESTE ---------- */
function medDorso(G){const{x,Y}=G;paint(x,mk2(m=>mPoly(m,[[21,Y(31)],[43,Y(31)],[49,56],[46.4,58.6],[44,56.6],[41,59],[38,56.8],[35,59.2],[32,57],[29,59.2],[26,56.8],[23,59],[20,56.6],[17.6,58.6],[15,56]])),armP('medico').b,'cloth',41)}
function medPeito(G){const{x,Y}=G,P=armP('medico');prep('medico');
 /* sobretudo longo, aberto na frente */
 paint(x,mk2(m=>{mPoly(m,[[22,Y(31.4)],[42,Y(31.4)],[43.4,Y(45)],[46.4,56],[44.4,54.4],[42.6,57],[40.4,54.6],[38.2,57.2],[35.4,55],[33,Y(46)],[31,Y(46)],[28.6,55],[25.8,57.2],[23.6,54.6],[21.4,57],[19.6,54.4],[17.6,56],[20.6,Y(45)]]);
  mEll(m,20.4,Y(35.6),4,3.4);mRect(m,16.8,Y(35),6.6,11.4);mEll(m,43.6,Y(35.6),4,3.4);mRect(m,40.6,Y(35),6.6,11.4)}),P.b,'cloth',42);
 /* lapelas e barra mais clara */
 paint(x,mk2(m=>{mPoly(m,[[26,Y(31.4)],[31.2,Y(31.4)],[31.2,Y(44)],[28.4,Y(38)]]);mPoly(m,[[38,Y(31.4)],[32.8,Y(31.4)],[32.8,Y(44)],[35.6,Y(38)]])}),mixH(P.b,1.35),'cloth',43);
 paint(x,mk2(m=>{mRect(m,16.8,Y(44),6.6,2.2);mRect(m,40.6,Y(44),6.6,2.2)}),mixH(P.b,1.35),'cloth',44);
 /* capinha nos ombros */
 paint(x,mk2(m=>mPoly(m,[[23,Y(30.4)],[41,Y(30.4)],[46.6,Y(35)],[45.6,Y(38.6)],[32,Y(37)],[18.4,Y(38.6)],[17.4,Y(35)]])),mixH(P.b,.82),'cloth',45);
 /* cinto de couro, fivela e bolsinhas */
 paint(x,mk2(m=>mRect(m,20.6,Y(42.4),22.8,2.4)),LEATHER,'cloth',46);
 cel(x,mk2(m=>mRect(m,30.4,Y(42),3.2,3.2)),P.a,{chrome:1});
 paint(x,mk2(m=>{mRect(m,22.4,Y(44.4),3.6,3.6);mRect(m,38,Y(44.4),3.6,3.6)}),'#6a4a2e','cloth',47);
 /* frasco de remédio verde na cintura */
 cel(x,mk2(m=>mRect(m,35.2,Y(43.2),1.6,1.4)),P.a,{flat:1});cel(x,mk2(m=>mEll(m,36,Y(46.4),1.8,2.2)),P.gem,{glow:1});
 /* botões de latão */
 for(const yy of[34,37.4,40.4])cel(x,mk2(m=>mEll(m,32,Y(yy),.9,.9)),P.a,{flat:1});
 /* luvas de couro */
 paint(x,mk2(m=>{mRect(m,17.2,Y(46.2),5.8,2.6);mRect(m,41,Y(46.2),5.8,2.6)}),LEATHER,'cloth',48)}
function medBotas(G){const{x,lL,lR}=G,P=armP('medico');prep('medico');
 paint(x,mk2(m=>{mRect(m,24.8,47+lL,6.6,9);mEll(m,28,57+lL,4.6,2.6);mRect(m,32.6,47+lR,6.6,9);mEll(m,36,57+lR,4.6,2.6)}),LEATHER,'cloth',49);
 paint(x,mk2(m=>{mRect(m,24.2,46.4+lL,7.8,2.4);mRect(m,32,46.4+lR,7.8,2.4)}),'#6a4a2e','cloth',50);
 cel(x,mk2(m=>{mRect(m,26.6,52+lL,3,1.4);mRect(m,34.4,52+lR,3,1.4)}),P.a,{flat:1})}
function medCab(G){const{x,Y,back}=G,P=armP('medico');prep('medico');
 /* capuz que cobre a cabeça e o pescoço */
 paint(x,mk2(m=>{mEll(m,32,Y(18.6),14,11.8);mPoly(m,[[20.4,Y(22)],[43.6,Y(22)],[41,Y(31.6)],[23,Y(31.6)]])}),mixH(P.b,1.12),'cloth',51);
 if(!back){/* sombra do capuz em volta da máscara */
  paint(x,mk2(m=>mEll(m,32,Y(20.4),10.4,9.4)),'#0c0a0e','cloth',58);
  /* máscara de couro claro envelhecido */
  paint(x,mk2(m=>mEll(m,32,Y(20),8.8,7.6)),BONE,'cloth',52);
  /* bico longo e levemente curvo, descendo até o peito */
  const BK=[[26.4,Y(20.6)],[37.6,Y(20.6)],[37,Y(25)],[35.4,Y(30)],[33.8,Y(35)],[32.6,Y(39.4)],[31.6,Y(41.4)],[31,Y(39)],[29.8,Y(34)],[28.4,Y(29)],[27,Y(25)]];
  paint(x,mk2(m=>mPoly(m,BK)),BONE,'cloth',53);
  paint(x,mk2(m=>mPoly(m,[[32,Y(22)],[33.4,Y(22)],[33,Y(30)],[32.2,Y(37)],[31.8,Y(37)],[31.6,Y(30)]])),mixH(BONE,.62),'cloth',54);
  /* costura e tiras de couro */
  paint(x,mk2(m=>{mRect(m,26.6,Y(23.4),10.8,1.2);mRect(m,28.2,Y(28),7.6,1)}),LEATHER,'cloth',59);
  for(const yy of[31.4,34.4])cel(x,mk2(m=>mEll(m,32.2,Y(yy),.6,.6)),'#2a2420',{flat:1});
  /* lentes de vidro vermelho, com brilho sinistro */
  for(const cx of[27.6,36.4]){cel(x,mk2(m=>mEll(m,cx,Y(18.4),3.2,3)),P.a,{chrome:1});cel(x,mk2(m=>mEll(m,cx,Y(18.4),2.2,2)),'#d02a1e',{glow:1})}
  cel(x,mk2(m=>mRect(m,30.4,Y(17.8),3.2,1)),P.a,{flat:1})}
 /* chapéu de aba larga */
 paint(x,mk2(m=>mPoly(m,[[9,Y(11.6)],[14,Y(8.4)],[24,Y(7)],[40,Y(7)],[50,Y(8.4)],[55,Y(11.6)],[50,Y(13.6)],[40,Y(14.2)],[24,Y(14.2)],[14,Y(13.6)]])),P.b,'cloth',55);
 paint(x,mk2(m=>mPoly(m,[[23.4,Y(10.6)],[40.6,Y(10.6)],[39.4,Y(-3.4)],[37,Y(-4.6)],[27,Y(-4.6)],[24.6,Y(-3.4)]])),mixH(P.b,1.1),'cloth',56);
 paint(x,mk2(m=>mRect(m,23.6,Y(7.6),16.8,2.4)),'#4a1418','cloth',57);
 if(!G.solo)paint(x,mk2(m=>{mEll(m,20,Y(47.5),2.9,2.8);mEll(m,44,Y(47.5),2.9,2.8)}),LEATHER,'cloth',60)}

/* ---------- GEADA ETERNA ---------- */
const crystal=(cx,by,h,w,tilt=0)=>[[cx-w,by],[cx-w+tilt*.4,by-h*.72],[cx+tilt,by-h],[cx+w+tilt*.4,by-h*.72],[cx+w,by]];
function geaDorso(G){const{x,Y}=G,P=armP('geada');prep('geada');
 /* cristais de gelo atrás dos ombros (prismas retos, sem asas) */
 const C=[[17,Y(34),15,2.2,-3],[13,Y(37),11,1.9,-4.4],[21.6,Y(33),11,1.8,-1.4]];
 cel(x,mk2(m=>C.forEach(c=>SYM(m,crystal(...c)))),P.a,{chrome:1});
 cel(x,mk2(m=>C.forEach(([a,b,h,w,t])=>SYM(m,crystal(a,b-1,h*.7,w*.5,t*.7)))),P.gem,{glow:1})}
function geaPeito(G,id){const{x,Y}=G,P=armP('geada');_peito(G,id);prep('geada');
 /* cristais nas ombreiras */
 cel(x,mk2(m=>{SYM(m,crystal(17.6,Y(32),6.4,1.5,-1.6));SYM(m,crystal(20.6,Y(31.4),4.6,1.2,-.6))}),P.gem,{glow:1});
 /* floco de neve no peito */
 const fl=mk2(m=>{for(let k=0;k<6;k++){const a=k*Math.PI/3,cx=32,cy=Y(36.4);mPoly(m,[[cx+Math.cos(a+1.57)*.55,cy+Math.sin(a+1.57)*.55],[cx+Math.cos(a)*3.6+Math.cos(a+1.57)*.55,cy+Math.sin(a)*3.6+Math.sin(a+1.57)*.55],[cx+Math.cos(a)*3.6-Math.cos(a+1.57)*.55,cy+Math.sin(a)*3.6-Math.sin(a+1.57)*.55],[cx-Math.cos(a+1.57)*.55,cy-Math.sin(a+1.57)*.55]])}});
 cel(x,mk2(m=>mEll(m,32,Y(36.4),4.6,4.4)),P.a,{chrome:1});cel(x,fl,'#ffffff',{glow:1})}
function geaBotas(G,id){const{x,lL,lR}=G,P=armP('geada');_bot(G,id);prep('geada');
 cel(x,mk2(m=>{mPoly(m,crystal(28,48.6+lL,4.4,1.2,-1.2));mPoly(m,crystal(36,48.6+lR,4.4,1.2,1.2))}),P.gem,{glow:1})}
function geaCab(G){const{x,Y,back}=G,P=armP('geada');prep('geada');
 /* tiara: protetores laterais, coroa de cristais e gema de gelo */
 cel(x,mk2(m=>SYM(m,[[19.4,Y(15.6)],[24,Y(16.4)],[24.2,Y(25)],[21.6,Y(28)],[19.6,Y(24)]])),P.b,{chrome:1});
 cel(x,mk2(m=>{mPoly(m,crystal(32,Y(12.6),11,2.2));SYM(m,crystal(26.6,Y(13.4),7.6,1.7,-1.4));SYM(m,crystal(22.4,Y(15),5,1.4,-1.6))}),P.a,{chrome:1});
 cel(x,mk2(m=>{mPoly(m,crystal(32,Y(12),7.6,1.1));SYM(m,crystal(26.6,Y(12.8),5,.8,-1))}),P.gem,{glow:1});
 cel(x,mk2(m=>mPoly(m,[[20.4,Y(15.8)],[26,Y(12.2)],[32,Y(11.2)],[38,Y(12.2)],[43.6,Y(15.8)],[43.8,Y(18)],[38,Y(15.2)],[32,Y(14.4)],[26,Y(15.2)],[20.2,Y(18)]])),P.b,{chrome:1});
 if(!back)cel(x,mk2(m=>mPoly(m,[[32,Y(12.6)],[33.6,Y(14.6)],[32,Y(16.8)],[30.4,Y(14.6)]])),P.gem,{glow:1})}

eqPeito=function(G,id){const t=armT(id);if(t==='medico')return medPeito(G);if(t==='geada')return geaPeito(G,id);return _peito(G,id)};
eqCabeca=function(G,id){const t=armT(id);if(t==='medico')return medCab(G);if(t==='geada')return geaCab(G);return _cab(G,id)};
eqBotas=function(G,id){const t=armT(id);if(t==='medico')return medBotas(G);if(t==='geada')return geaBotas(G,id);return _bot(G,id)};
eqDorso=function(G,id){const t=armT(id);if(t==='medico')return medDorso(G);if(t==='geada')return geaDorso(G);return _dor(G,id)};
/* cabelo some sob o capuz do físico */
const _sprite=sprite;sprite=function(L,eq,fr,back,solo){const e=normEq(eq);if(e&&IT[e.cabeca]&&IT[e.cabeca].t==='medico'&&L&&L.hair&&L.hair.s!=='raspado')L={...L,hair:{...L.hair,s:'raspado'}};return _sprite(L,eq,fr,back,solo)};
