# Оригинальные линейные иллюстрации для карточек (viewBox 320x200), белые линии на цветном фоне
S=''
G='<g stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">'
F='fill="#fff" fill-opacity=".18"'
def ground(): return f'<line x1="20" y1="170" x2="300" y2="170" {S}/>'
def win(x,y,w=14,h=22,arch=False):
    if arch: return f'<path d="M{x} {y+h} V{y+w/2} A{w/2} {w/2} 0 0 1 {x+w} {y+w/2} V{y+h} Z" {S} stroke-width="2"/>'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {S} stroke-width="2"/>'
def gable():  # фасад с декоративным фронтоном
    o=[ground(),f'<rect x="80" y="80" width="160" height="90" {S} {F}/>',f'<path d="M70 80 L160 38 L250 80 Z" {S}/>',f'<circle cx="160" cy="64" r="9" {S} stroke-width="2"/>']
    o+= [win(96+i*30,104,arch=True) for i in range(5)]
    o.append(f'<path d="M145 170 V138 A15 15 0 0 1 175 138 V170" {S}/>'); return o
def classic():  # колоннада с портиком
    o=[ground(),f'<path d="M60 76 L160 36 L260 76 Z" {S} {F}/>',f'<line x1="56" y1="82" x2="264" y2="82" {S}/>',f'<line x1="56" y1="162" x2="264" y2="162" {S}/>']
    o+= [f'<line x1="{76+i*28}" y1="88" x2="{76+i*28}" y2="156" {S} stroke-width="5"/>' for i in range(7)]; return o
def warehouse():  # кирпичный склад с арками
    o=[ground(),f'<rect x="40" y="70" width="240" height="100" {S} {F}/>',f'<line x1="40" y1="90" x2="280" y2="90" {S} stroke-width="2"/>']
    o+= [win(56+i*38,104,22,50,arch=True) for i in range(6)]; return o
def modern():  # прямоугольный объём с прозрачным фасадом
    o=[ground(),f'<rect x="50" y="64" width="220" height="106" {S}/>',f'<rect x="50" y="64" width="220" height="26" {S} {F}/>']
    o+= [f'<line x1="{50+i*27.5}" y1="90" x2="{50+i*27.5}" y2="170" {S} stroke-width="1.5"/>' for i in range(1,8)]
    o.append(f'<circle cx="250" cy="40" r="12" {S} stroke-width="2"/>'); return o
def books():  # стеллажи с книгами
    import random; r=random.Random(7); o=[]
    for row in range(3):
        y=50+row*42; o.append(f'<line x1="50" y1="{y+36}" x2="270" y2="{y+36}" {S}/>'); x=56
        while x<258:
            w=r.choice([8,10,12,14]); h=r.choice([26,30,34]); tilt=r.random()<.12
            o.append(f'<rect x="{x}" y="{y+36-h}" width="{w}" height="{h}" {S} stroke-width="2" {F if r.random()<.4 else ""}{" transform=\"rotate(-12 %d %d)\""%(x,y+36) if tilt else ""}/>'); x+=w+3
    return o
def globe():  # книги на разных языках: глобус и раскрытая книга
    return [ground(),f'<circle cx="120" cy="92" r="46" {S} {F}/>',f'<ellipse cx="120" cy="92" rx="20" ry="46" {S} stroke-width="2"/>',f'<line x1="74" y1="92" x2="166" y2="92" {S} stroke-width="2"/>',
            f'<path d="M80 70 H160 M80 114 H160" {S} stroke-width="2"/>',f'<line x1="120" y1="138" x2="120" y2="170" {S}/>',
            f'<path d="M190 150 Q220 136 250 150 V100 Q220 86 190 100 Z" {S}/>',f'<path d="M250 150 Q280 136 300 150 V100 Q280 86 250 100" {S}/>',
            f'<text x="205" y="80" fill="#fff" font-family="Arial" font-size="18" font-weight="700">Aa Я</text>']
def mansion():  # старинный особняк с мезонином
    o=[ground(),f'<rect x="60" y="96" width="200" height="74" {S} {F}/>',f'<rect x="120" y="66" width="80" height="30" {S}/>',f'<path d="M112 66 L160 44 L208 66" {S}/>']
    o+= [win(74+i*36,112,16,28) for i in range(6) if i!=2 and i!=3]+[f'<path d="M146 170 V128 H174 V170" {S}/>',f'<line x1="40" y1="170" x2="40" y2="110" {S}/>',f'<circle cx="40" cy="98" r="16" {S} {F}/>']; return o
def plant():  # электростанция с трубами
    return [ground(),f'<rect x="40" y="96" width="240" height="74" {S} {F}/>',f'<path d="M40 96 L80 76 L120 96 L160 76 L200 96 L240 76 L280 96" {S}/>',
            f'<rect x="96" y="26" width="14" height="50" {S}/>',f'<rect x="210" y="26" width="14" height="50" {S}/>',
            f'<path d="M60 170 V120 H260 V170" {S} stroke-width="1.5"/>']+[f'<line x1="{60+i*20}" y1="120" x2="{60+i*20}" y2="170" {S} stroke-width="1.5"/>' for i in range(1,10)]
def gallery():  # рамы картин на стене
    return [ground(),f'<rect x="40" y="50" width="70" height="90" {S} {F}/>',f'<rect x="126" y="40" width="80" height="60" {S}/>',f'<rect x="126" y="112" width="80" height="34" {S} {F}/>',
            f'<rect x="222" y="60" width="58" height="80" {S}/>',f'<path d="M52 126 L72 96 L88 116 L98 104" {S} stroke-width="2"/>',f'<circle cx="170" cy="70" r="12" {S} stroke-width="2"/>',
            f'<line x1="230" y1="120" x2="272" y2="80" {S} stroke-width="2"/>']
def bottle():  # флакон и заводской корпус
    return [ground(),f'<path d="M100 170 V108 Q100 92 116 86 V60 H136 V86 Q152 92 152 108 V170 Z" {S} {F}/>',f'<rect x="112" y="48" width="28" height="12" {S}/>',
            f'<rect x="176" y="92" width="110" height="78" {S}/>']+[win(186+i*24,106,14,18) for i in range(4)]+[f'<line x1="40" y1="170" x2="40" y2="120" {S}/>',f'<path d="M30 120 H50" {S}/>']
def park():  # скульптуры среди деревьев
    return [ground(),f'<circle cx="70" cy="96" r="30" {S} {F}/>',f'<line x1="70" y1="126" x2="70" y2="170" {S}/>',f'<circle cx="258" cy="104" r="26" {S} {F}/>',f'<line x1="258" y1="130" x2="258" y2="170" {S}/>',
            f'<rect x="136" y="146" width="48" height="24" {S}/>',f'<circle cx="160" cy="70" r="12" {S}/>',f'<path d="M160 82 V128 M160 96 L140 112 M160 96 L182 84 M160 128 L146 146 M160 128 L174 146" {S}/>']
def card():  # банковская карта и билеты
    return [f'<rect x="70" y="50" width="180" height="110" rx="14" {S} {F}/>',f'<rect x="90" y="76" width="32" height="24" rx="4" {S} stroke-width="2"/>',
            f'<line x1="90" y1="128" x2="200" y2="128" {S} stroke-width="2"/>',f'<line x1="90" y1="142" x2="150" y2="142" {S} stroke-width="2"/>',
            f'<path d="M210 30 H290 V56 A8 8 0 0 0 290 72 V98 H210 V72 A8 8 0 0 0 210 56 Z" {S} transform="rotate(12 250 64)"/>']
def people():  # группа студентов
    o=[ground()]
    for i,(x,h) in enumerate([(90,0),(130,-10),(170,-4),(210,-12),(250,0)]):
        o+= [f'<circle cx="{x}" cy="{96+h}" r="14" {S} {F if i%2 else ""}/>',f'<path d="M{x-22} 170 V{140+h} Q{x-22} {116+h} {x} {116+h} Q{x+22} {116+h} {x+22} {140+h} V170" {S}/>']
    o.append(f'<path d="M60 40 L60 80 M60 40 H96 L88 50 L96 60 H60" {S} stroke-width="2"/>'); return o
MOTIF={1:gable,2:classic,3:warehouse,4:modern,5:books,6:globe,7:mansion,8:plant,9:gallery,10:bottle,11:park,12:card,13:people}
def svg(i): return '<svg class="ill" viewBox="0 0 320 200" aria-hidden="true">'+"".join(MOTIF[i]())+'</svg>'
