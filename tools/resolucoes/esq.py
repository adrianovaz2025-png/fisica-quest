import json,math
def arrow(x1,y1,x2,y2,c,w=3,h=9):
    a=math.atan2(y2-y1,x2-x1);bx,by=x2-h*math.cos(a),y2-h*math.sin(a)
    p=[(x2,y2),(bx+h*.5*math.sin(a),by-h*.5*math.cos(a)),(bx-h*.5*math.sin(a),by+h*.5*math.cos(a))]
    return f"<line x1='{x1}' y1='{y1}' x2='{bx:.1f}' y2='{by:.1f}' stroke='{c}' stroke-width='{w}'/><polygon points='{' '.join(f'{x:.1f},{y:.1f}' for x,y in p)}' fill='{c}'/>"
def T(x,y,s,c='#222',sz=13,anc='middle',b=False):return f"<text x='{x}' y='{y}' fill='{c}' font-size='{sz}' text-anchor='{anc}'{' font-weight=\"bold\"' if b else ''}>{s}</text>"
def svg(w,h,body):return f"<svg viewBox='0 0 {w} {h}' width='{w}' xmlns='http://www.w3.org/2000/svg' font-family='sans-serif'>{body}</svg>"
B,R,G,K='#2266aa','#cc3333','#2a8a3a','#333'
E={}
# slackline
E['2019_106']=svg(300,125,"<line x1='10' y1='30' x2='290' y2='30' stroke='#aaa' stroke-dasharray='4'/><line x1='10' y1='30' x2='150' y2='55' stroke='#333' stroke-width='3'/><line x1='290' y1='30' x2='150' y2='55' stroke='#333' stroke-width='3'/>"
  +arrow(150,55,95,45,B)+arrow(150,55,205,45,B)+arrow(150,55,150,112,R)+"<circle cx='150' cy='55' r='5' fill='#333'/>"
  +T(92,62,'T',B,b=True)+T(210,62,'T',B,b=True)+T(158,110,'P = 800 N',R,anc='start')+T(52,26,'10°')+T(150,20,'2·T·sen 10° = P',K,12))
# caminhão
E['2023_114']=svg(360,150,"<rect x='5' y='5' width='155' height='140' fill='none'/>"+T(85,18,'ARRANCANDO (a = 3 m/s²)',K,11,b=True)
  +"<rect x='55' y='60' width='50' height='40' fill='#bbb' stroke='#333'/>"+T(80,85,'M')+arrow(105,75,150,75,B)+T(130,68,'T₂ = 200',B,11)+arrow(80,100,125,108,G)+T(118,125,'atrito 400',G,11)
  +T(80,140,'soma = 600 N = M·a',K,11)
  +T(268,18,'FREANDO (a = 5 m/s²)',K,11,b=True)+"<rect x='255' y='60' width='50' height='40' fill='#bbb' stroke='#333'/>"+T(280,85,'M')+arrow(255,75,205,75,B)+T(228,68,'T₁ = 600',B,11)+arrow(280,100,235,108,G)+T(245,125,'atrito 400',G,11)
  +T(275,140,'soma = 1 000 N = M·a',K,11))
# nadador
E['2024_119']=svg(300,150,arrow(30,75,30,125,R)+T(36,95,'corrente 30',R,11,'start')+arrow(120,120,160,90,B)+T(166,88,'nadador 50',B,11,'start')
  +"<line x1='120' y1='120' x2='160' y2='120' stroke='#999' stroke-dasharray='3'/><line x1='160' y1='120' x2='160' y2='90' stroke='#999' stroke-dasharray='3'/>"
  +T(140,136,'40 (avança)',G,11)+T(166,108,'30 (anula a corrente)',K,11,'start')+T(150,20,'Nos lados de 800 m:',K,12,b=True)+T(150,38,'√(50² − 30²) = 40 m/min',K,12))
# parabola da bolinha
pts=' '.join(f"{60+x:.0f},{40+0.0031*x*x:.0f}" for x in range(0,181,10))
E['2020_113']=svg(300,150,"<rect x='10' y='34' width='52' height='6' fill='#999'/><line x1='36' y1='40' x2='36' y2='140' stroke='#999' stroke-width='5'/><line x1='5' y1='140' x2='295' y2='140' stroke='#333'/>"
  +f"<polyline points='{pts}' fill='none' stroke='{B}' stroke-width='2.5' stroke-dasharray='6 4'/>"+arrow(60,30,110,30,G,2)+T(85,24,'V₀ (constante)',G,11)+arrow(250,60,250,110,R,2)+T(256,90,'g',R,13,'start'))
# vant
E['2019_131']=svg(300,140,"<line x1='10' y1='120' x2='290' y2='120' stroke='#333' stroke-width='2'/>"
  +"<line x1='150' y1='25' x2='60' y2='120' stroke='#999' stroke-dasharray='4'/><line x1='150' y1='25' x2='240' y2='120' stroke='#999' stroke-dasharray='4'/><line x1='150' y1='25' x2='150' y2='120' stroke='#999'/>"
  +"<polygon points='140,25 160,25 150,18' fill='#333'/>"+T(158,75,'H = 1 000 m',K,11,'start')+T(150,136,'cobre 2 · H · tg 45° = 2 000 m',B,12)+T(128,108,'45°',K,11))
# calvin
E['2024_121']=svg(260,140,"<line x1='10' y1='110' x2='250' y2='110' stroke='#333' stroke-width='2'/><circle cx='130' cy='106' r='5' fill='#333'/>"
  +arrow(130,106,130,40,B)+T(124,40,'N',B,12,'end')+arrow(130,106,190,106,G)+T(195,100,'atrito',G,11,'start')+arrow(130,106,185,45,R,3)+T(190,44,'resultante',R,11,'start')
  +arrow(90,80,60,98,'#888',2)+T(40,75,'movimento',  '#888',10))
json.dump(E,open('esq.json','w'),ensure_ascii=False)
print(len(E))
