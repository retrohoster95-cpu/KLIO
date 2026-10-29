import html, shutil, pathlib, urllib.parse, json, os, sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from illus import svg, MOTIF, G
def svgdata(i):
    x='<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 -20 400 240">'+G+''.join(MOTIF[i]())+'</g></svg>'
    return 'data:image/svg+xml,'+urllib.parse.quote(x)
E=html.escape
OUT=pathlib.Path(os.environ.get('OUT',HERE.parent)); OUT.mkdir(exist_ok=True); (OUT/'img').mkdir(exist_ok=True)
EVF=HERE/'events.json'
EV=json.loads(EVF.read_text(encoding='utf-8')) if EVF.exists() else {"updated":None,"places":{}}
def events(i): return EV.get("places",{}).get(str(i),[])
def evitem(e,place=None):
    t=E(e["title"]); t=f'<a href="{E(e["url"])}" target="_blank" rel="noopener">{t}</a>' if e.get("url") else t
    pl=f'<span class="evplace">{E(place)}</span>' if place else ""
    fr='<span class="free">бесплатно</span>' if e.get("free") else ""
    return f'<li><span class="evdate">{E(e["when"])}</span><span class="evtitle">{t}{pl}</span>{fr}</li>'
def evblock(i):
    ev=events(i)
    if not ev: return ""
    return '<div class="ev"><b>Ближайшие события</b><ul>'+"".join(evitem(e) for e in ev)+'</ul></div>'
CATS={"museum":("Музеи","Собрания искусства и истории"),"lib":("Библиотеки","Книги, читальные залы, клубы"),"art":("Арт-пространства","Выставки, мастерские, события"),"club":("Клубы и практики","Кружки, лекции и городские программы")}
P=[
 (1,"museum","Третьяковская галерея","ГТГ","Лаврушинский пер., 10","Третьяковская",240,232,False,
  "Главное собрание русского искусства: от икон до живописи начала XX века. Помимо экспозиции проходят лекции и кинопоказы.",
  "Знакомит с национальным культурным наследием и помогает понять, как искусство отражает историю общества.",
  "Есть льготные билеты и бесплатные дни для студентов и других категорий посетителей. Расписание — на сайте музея.","https://www.tretyakovgallery.ru/"),
 (2,"museum","ГМИИ им. А. С. Пушкина","ГМИИ","ул. Волхонка, 12","Кропоткинская",196,214,False,
  "Музей мирового искусства: античные слепки, европейская живопись, импрессионисты. Проводит лекции и молодёжные программы.",
  "Расширяет кругозор за пределы родной культуры и учит видеть связь эпох и стран.",
  "Для студентов российских вузов есть бесплатные дни, точные условия — на сайте музея.","https://pushkinmuseum.art/"),
 (3,"museum","Музей Москвы","ММ","Зубовский бульвар, 2","Парк культуры",150,262,True,
  "Музей истории города в бывших Провиантских складах: выставки о городе, лекции, книжный магазин и библиотека.",
  "Помогает лучше узнать историю своего города и почувствовать себя его частью.",
  "Студентам очной формы — бесплатный вход на выставки и лекции (уточняйте на сайте).","https://mosmuseum.ru/"),
 (4,"museum","Музей «Гараж»","G","ул. Крымский Вал, 9, стр. 32","Октябрьская",176,322,True,
  "Музей современного искусства в Парке Горького: выставки, открытое хранение, лекции, книжный магазин и библиотека по искусству.",
  "Учит понимать современную культуру и формулировать собственную позицию по отношению к ней.",
  "С 17 июня 2026 года вход в открытое хранение бесплатный для студентов любых вузов по студенческому или ISIC.","https://garagemca.org/"),
 (5,"lib","Российская государственная библиотека","РГБ","ул. Воздвиженка, 3/5","Библиотека им. Ленина",198,192,True,
  "«Ленинка» — крупнейшая библиотека страны. Читальные залы, редкие издания, электронные ресурсы, тихие места для учёбы.",
  "Даёт доступ к знаниям и формирует привычку к самостоятельной исследовательской работе.",
  "Запись и читательский билет бесплатны, нужен паспорт.","https://www.rsl.ru/"),
 (6,"lib","Библиотека иностранной литературы","ВГБИЛ","ул. Николоямская, 1","Таганская",282,200,True,
  "«Иностранка»: книги на десятках языков, бесплатные разговорные клубы, культурные центры разных стран, лекции.",
  "Помогает выучить язык и познакомиться с другими культурами, а это основа межкультурного диалога.",
  "Запись бесплатная; разговорные клубы обычно бесплатны, расписание на сайте.","https://libfl.ru/"),
 (7,"lib","Библиотека-читальня им. И. С. Тургенева","ТУРГ","Бобров пер., 6, стр. 1","Чистые пруды",262,156,True,
  "Одна из старейших публичных библиотек Москвы в историческом особняке: книжные клубы, лекции, концерты, места для работы.",
  "Камерная среда для чтения и обсуждений, где легко найти своих по интересам.",
  "Вход и запись бесплатные, большинство мероприятий бесплатные по регистрации.",""),
 (8,"art","Дом культуры «ГЭС-2»","ГЭС-2","Болотная наб., 15","Кропоткинская",214,236,True,
  "Бывшая электростанция, ставшая домом культуры: выставки, кинопоказы, библиотека, мастерские «Своды».",
  "Пространство, где можно не только смотреть, но и пробовать самому: мастерские, лаборатории, открытые программы.",
  "Вход бесплатный, нужна регистрация на сайте. Ежедневно 11:00–22:00.","https://ges-2.org/"),
 (9,"art","Центр современного искусства «Винзавод»","ВИН","4-й Сыромятнический пер., 1/8","Курская",344,186,True,
  "Галереи, мастерские художников, «Открытые студии» для молодых авторов, магазины и события.",
  "Показывает, как устроена профессиональная арт-среда, и даёт молодым авторам первую площадку.",
  "Вход на территорию и в большинство галерей бесплатный.","https://winzavod.ru/"),
 (10,"art","Дизайн-завод «Флакон»","ФЛ","ул. Большая Новодмитровская, 36","Дмитровская",196,52,True,
  "Креативный кластер на месте бывшего стекольного завода: студии дизайнеров, маркеты, лекции, фестивали.",
  "Знакомит с творческими профессиями и показывает, что культура может стать делом жизни.",
  "Вход на территорию свободный, большинство событий бесплатные.","https://flacon.ru/"),
 (11,"art","Парк искусств «Музеон»","МУЗ","ул. Крымский Вал, 2","Парк культуры",198,290,True,
  "Парк скульптуры под открытым небом у Крымского моста: более тысячи скульптур, летние фестивали и лекции.",
  "Свободная среда для прогулок с искусством, где культура становится частью повседневности.",
  "Вход бесплатный.","https://muzeon.ru/"),
 (12,"club","Пушкинская карта","₽","Онлайн: приложение «Госуслуги Культура»","",None,None,True,
  "Государственная программа для молодёжи 14–22 лет: 5000 ₽ в год на билеты в музеи, театры, концерты и кино (до 2000 ₽ на кино).",
  "Снимает финансовый барьер и даёт возможность попробовать разные виды культуры.",
  "Для граждан РФ 14–22 лет. С 2026 года карту выпускает ВТБ, оформить можно через Госуслуги. Остаток сгорает 31 декабря.","https://www.culture.ru/pushkinskaya-karta"),
 (13,"club","Культурный центр ЗИЛ","ЗИЛ","ул. Восточная, 4, корп. 1","Автозаводская",300,334,True,
  "Городской культурный центр: творческие лаборатории живописи, фотографии и театра, открытые лекции, кинопоказы, библиотека и разговорный клуб.",
  "Здесь интерес превращается в регулярное занятие, а занятие — в круг общения и сообщество единомышленников.",
  "Многие лекции и клубы бесплатны или недороги, программа и запись — на сайте центра.","https://zilcc.ru/"),
]
FAV="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='15' fill='%232A44D8'/%3E%3Ctext x='16' y='21' font-size='15' text-anchor='middle' fill='white' font-family='Arial' font-weight='700'%3EК%3C/text%3E%3C/svg%3E"
NAV=[("index.html","Главная"),("catalog.html","Каталог мест"),("afisha.html","Афиша"),("lichnost.html","Как это влияет на личность"),("team.html","Команда")]
def head(title,desc):
    return f'''<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="icon" href="{FAV}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&family=Golos+Text:wght@400;500;600&family=PT+Mono&display=swap">
<link rel="stylesheet" href="style.css">'''
def chrome(cur,body):
    nav="".join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a>' for h,t in NAV)
    return f'''<div class="progress" aria-hidden="true"></div>
<header class="top"><div class="wrap">
<a class="logo" href="index.html"><span>К</span>КультКарта</a>
<nav aria-label="Разделы сайта">{nav}</nav>
</div></header>
<main class="wrap">
{body}
</main>
<footer>
 <div class="lines" aria-hidden="true"><i style="background:var(--c-museum)"></i><i style="background:var(--c-lib)"></i><i style="background:var(--c-art)"></i><i style="background:var(--c-club)"></i></div>
 <div class="wrap">
  <div class="wordmark" aria-hidden="true">КультКарта</div>
  <div class="fgrid">
   <div><h4>О проекте</h4><p>Культурный путеводитель по Москве. Учебный проект по дисциплине «Культура личности и общества», группа ОБ26-30.</p></div>
   <div><h4>Разделы</h4>{"".join(f'<a href="{h}">{t}</a>' for h,t in NAV)}</div>
   <div><h4>Категории</h4>{"".join(f'<a href="catalog.html#cat-{k}">{n}</a>' for k,(n,_) in CATS.items())}</div>
   <div><h4>Данные</h4><p>Сведения о местах проверены 29.10.2026.<br>{"Афиша обновлена " + EV["updated"] if EV.get("updated") else "Афиша обновляется каждый день в 06:00"}.</p><a href="team.html#feedback">Оставить отзыв →</a></div>
  </div>
  <div class="fbottom"><span>© 2026 · КультКарта</span><span>Источники: официальные сайты учреждений, 2ГИС, KudaGo</span></div>
 </div>
</footer>'''
def full(title,desc,cur,body):
    return f'<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head(title,desc)}\n</head>\n<body>\n{chrome(cur,body)}\n</body>\n</html>\n'
def fragment(title,desc,cur,body):  # для публикации главной страницы как артефакта
    return head(title,desc)+"\n"+chrome(cur,body)+"\n"

COL={"museum":"var(--c-museum)","lib":"var(--c-lib)","art":"var(--c-art)","club":"var(--c-club)"}
def svgmap():
    h=['<svg viewBox="0 0 440 400" role="img" aria-label="Схема центра Москвы с местами из каталога">',
       '<rect width="440" height="400" fill="var(--surface)"/>',
       '<circle class="map-ring" cx="220" cy="200" r="120" fill="none" stroke="var(--ring)" stroke-width="10" transform="rotate(-90 220 200)"/>',
       '<circle cx="220" cy="200" r="58" fill="none" stroke="var(--ring)" stroke-width="3" stroke-dasharray="6 6"/>',
       '<path class="map-river" d="M10 150 C 90 140, 120 250, 190 262 S 250 210, 300 250 S 360 360, 430 330" fill="none" stroke="var(--river)" stroke-width="16" stroke-linecap="round"/>',
       '<text x="402" y="318" font-family="PT Mono, monospace" font-size="11" fill="var(--muted)" text-anchor="end">р. Москва</text>',
       '<rect x="208" y="186" width="18" height="18" rx="3" fill="none" stroke="var(--muted)" stroke-width="1.5"/>',
       '<text x="232" y="182" font-family="PT Mono, monospace" font-size="10" fill="var(--muted)">Кремль</text>',
       '<text x="352" y="96" font-family="PT Mono, monospace" font-size="10" fill="var(--muted)">Садовое кольцо</text>']
    for p in P:
        if p[6] is None: continue
        h.append(f'<a class="pin" href="catalog.html#place-{p[0]}"><title>{p[0]}. {E(p[2])}</title><g style="--d:{p[0]}"><circle cx="{p[6]}" cy="{p[7]}" r="13" fill="var(--marker)" stroke="{COL[p[1]]}" stroke-width="3"/><text x="{p[6]}" y="{p[7]+4}" text-anchor="middle" font-family="Unbounded, sans-serif" font-weight="700" font-size="11" fill="#141B33">{p[0]}</text></g></a>')
    x=14
    for k,(n,_) in CATS.items():
        h.append(f'<circle cx="{x+5}" cy="368" r="5" fill="{COL[k]}"/><text x="{x+14}" y="372" font-family="Golos Text, sans-serif" font-size="11" fill="var(--ink)">{n}</text>')
        x+=len(n)*6.2+30
    h.append('</svg>'); return "\n".join(h)

nfree=sum(1 for p in P if p[8])
NAME={p[0]:p[2] for p in P}
allev=sorted(((e,i) for i in NAME for e in events(i)),key=lambda x:x[0].get("ts",0))
upd=EV.get("updated")
updnote=f'Обновлено {upd} · источник: KudaGo' if upd else 'Афиша обновляется автоматически каждый день в 06:00'
soon=('<section class="sec"><div class="sec-head rv"><div style="display:grid;gap:14px"><span class="eyebrow">Афиша · обновляется каждый день</span><h2>Скоро в городе</h2></div><a class="btn ghost" href="afisha.html">Вся афиша <span class="arr">→</span></a></div>'
      +(f'<ul class="evlist rv">{"".join(evitem(e,NAME[i]) for e,i in allev[:6])}</ul>' if allev else '<div class="empty rv"><span class="clock" aria-hidden="true"></span><div><b>Афиша загружается каждое утро в 06:00</b><p class="note">Здесь появятся ближайшие выставки, лекции и концерты в местах из каталога.</p></div></div>')
      +f'<p class="note">{updnote}.</p></section>')
WORDS=["музеи","библиотеки","лекции","выставки","мастерские","разговорные клубы","кино","концерты","книжные клубы","экскурсии"]
marq="".join(f"<span>{w}</span>" for w in WORDS*2)
marq2="".join(f"<span>{w}</span>" for w in (["Третьяковка","ГЭС-2","Винзавод","Ленинка","Музеон","Гараж","Флакон","Иностранка","ЗИЛ","Музей Москвы"])*2)
home=f'''<section class="hero">
 <div class="hero-lines" aria-hidden="true"><svg viewBox="0 0 1400 560" preserveAspectRatio="none">
  <path d="M-20 430 C 420 430, 640 430, 820 300 S 1100 80, 1420 60" stroke="var(--c-museum)" style="--len:1700"/>
  <path d="M-20 460 C 440 460, 670 460, 860 330 S 1130 130, 1420 120" stroke="var(--c-lib)" style="--len:1700;animation-delay:.15s"/>
  <path d="M-20 490 C 460 490, 700 490, 900 360 S 1160 180, 1420 180" stroke="var(--c-art)" style="--len:1700;animation-delay:.3s"/>
  <path d="M-20 520 C 480 520, 730 520, 940 390 S 1190 230, 1420 240" stroke="var(--c-club)" style="--len:1700;animation-delay:.45s"/>
 </svg></div>
 <div class="hero-text">
  <span class="live"><i></i>{"Афиша обновлена " + upd if upd else "Афиша обновляется каждый день в 06:00"}</span>
  <h1>Где расти <br>в&nbsp;<span class="hl">Москве<svg viewBox="0 0 300 30" preserveAspectRatio="none" aria-hidden="true"><path d="M4 22 C 80 6, 200 4, 296 16"/></svg></span></h1>
  <p class="lead">«КультКарта» собирает в одном месте музеи, библиотеки, арт-пространства и клубы Москвы, где можно учиться, творить и находить единомышленников.</p>
  <p>Мы сделали этот сайт для всех москвичей: студентов, школьников, работающих и тех, кто недавно переехал в город. Мы отбирали места, которые доступны каждому: бесплатно, по льготному билету или по Пушкинской карте. Номер на карточке совпадает с точкой на схеме. Условия посещения меняются, поэтому перед походом проверьте их на официальном сайте места.</p>
  <div class="btns"><a class="btn primary" href="catalog.html">Открыть каталог <span class="arr">→</span></a><a class="btn ghost" href="afisha.html">Афиша на неделю</a></div>
  <div class="legend">{"".join(f'<a class="c-{k}" href="catalog.html#cat-{k}"><b>{sum(1 for p in P if p[1]==k)}</b>{n}</a>' for k,(n,_) in CATS.items())}</div>
 </div>
 <div class="mapwrap">
  <div class="badge b1"><b>{len(P)}</b>мест на схеме</div>
  <div class="badge b2"><b>06:00</b>обновление афиши</div>
  <div class="badge b3"><b>{nfree}</b>бесплатно или по льготе</div>
  <figure class="mapbox">{svgmap()}<figcaption><span>Схема условная, не в масштабе</span><span>Нажмите на станцию, чтобы открыть место</span></figcaption></figure>
 </div>
</section>
<div class="marquee" aria-hidden="true"><div>{marq}</div><div>{marq2}</div></div>
<div class="stats stagger">
 <div class="stat c-museum"><b class="count" style="--to:{len(P)}"><span class="v">{len(P)}</span></b><span>мест и практик в каталоге</span></div>
 <div class="stat c-lib"><b class="count" style="--to:4"><span class="v">4</span></b><span>категории, как линии метро</span></div>
 <div class="stat c-art"><b class="count" style="--to:{nfree}"><span class="v">{nfree}</span></b><span>с бесплатным входом или льготами</span></div>
 <div class="stat c-club"><b class="count" style="--to:3"><span class="v">3</span></b><span>готовых маршрута выходного дня</span></div>
</div>
{soon}
<section class="sec">
 <div class="rv" style="display:grid;gap:14px"><span class="eyebrow">Как пользоваться сайтом</span><h2>Четыре шага</h2></div>
 <ol class="steps stagger">
  <li><b>Выберите категорию</b><span>В каталоге есть фильтр: музеи, библиотеки, арт-пространства, клубы.</span></li>
  <li><b>Изучите карточку</b><span>Адрес, метро, что там делать и чем это полезно для развития.</span></li>
  <li><b>Проверьте условия</b><span>Бесплатные дни и льготы — по ссылке на официальный сайт места.</span></li>
  <li><b>Сходите и расскажите</b><span>Оставьте отзыв о сайте, чтобы мы сделали его лучше.</span></li>
 </ol>
</section>
<section class="sec">
 <div class="sec-head rv"><div style="display:grid;gap:14px"><span class="eyebrow">Готовые маршруты</span><h2>Куда пойти на выходных</h2></div><p>Каждый маршрут — как ветка метро: станции идут в удобном порядке.</p></div>
 <div class="routes stagger">
  <div class="route c-museum"><span class="rtag"><i>1</i>≈ 5 часов · пешком</span><h3>Набережные и искусство</h3><ol>
   <li><span>8</span><a href="catalog.html#place-8">ГЭС-2</a></li><li><span>1</span><a href="catalog.html#place-1">Третьяковская галерея</a></li><li><span>11</span><a href="catalog.html#place-11">Музеон</a></li><li><span>4</span><a href="catalog.html#place-4">Музей «Гараж»</a></li></ol>
   <p>От Болотной набережной через Замоскворечье к Парку Горького.</p></div>
  <div class="route c-lib"><span class="rtag"><i>2</i>≈ 4 часа · метро и пешком</span><h3>День с книгой</h3><ol>
   <li><span>5</span><a href="catalog.html#place-5">Российская государственная библиотека</a></li><li><span>7</span><a href="catalog.html#place-7">Читальня им. Тургенева</a></li><li><span>6</span><a href="catalog.html#place-6">Библиотека иностранной литературы</a></li></ol>
   <p>Утро в читальном зале, днём книжный клуб, вечером разговорный клуб на иностранном языке.</p></div>
  <div class="route c-art"><span class="rtag"><i>3</i>≈ 4 часа · метро</span><h3>Современная культура</h3><ol>
   <li><span>9</span><a href="catalog.html#place-9">Винзавод</a></li><li><span>10</span><a href="catalog.html#place-10">Флакон</a></li><li><span>3</span><a href="catalog.html#place-3">Музей Москвы</a></li></ol>
   <p>Галереи молодых художников, дизайн-студии и история города.</p></div>
 </div>
</section>
<section class="sec">
 <div class="rv" style="display:grid;gap:14px"><span class="eyebrow">Категории</span><h2>С чего начать</h2></div>
 <div class="cats stagger">
  {"".join(f'<a class="catlink c-{k}" href="catalog.html#cat-{k}"><em>{sum(1 for p in P if p[1]==k):02d}</em><b>{n}</b><span>{d}</span></a>' for k,(n,d) in CATS.items())}
 </div>
</section>
<section class="sec"><div class="feedback rv-z"><span class="eyebrow">Начните сегодня</span><h2>Выберите место на выходные</h2><p>Тринадцать адресов, три маршрута и свежая афиша каждое утро.</p><div class="btns"><a class="btn primary" href="catalog.html">Открыть каталог <span class="arr">→</span></a></div></div></section>'''

def card(p):
    i,c,name,glyph,addr,metro,_,_,free,desc,why,stud,site=p
    links=[]
    if site: links.append(f'<a href="{site}" target="_blank" rel="noopener">Официальный сайт →</a>')
    if metro: links.append(f'<a href="https://2gis.ru/moscow/search/{urllib.parse.quote(addr)}" target="_blank" rel="noopener">На карте 2ГИС →</a>')
    m=f'<span class="metro"><b>М</b>{E(metro)}</span>' if metro else ""
    return f'''<article class="card c-{c}" id="place-{i}">
 <div class="photo" role="img" aria-label="{E(name)}" style="--img:url(img/{i:02d}.jpg),url(&quot;{svgdata(i)}&quot;),linear-gradient(135deg,var(--c),color-mix(in srgb,var(--c) 50%,#000))"><span class="num">{i}</span><span class="line">{CATS[c][0]}</span></div>
 <div class="body">
  <span class="tag">{CATS[c][0]}</span>
  <h3>{E(name)}</h3>
  <div class="addr"><span>{E(addr)}</span>{m}</div>
  <p class="desc">{E(desc)}</p>
  <p class="why"><strong>Для личности:</strong> {E(why)}</p>
  <p class="stud"><strong>Условия:</strong> {E(stud)}</p>
  {evblock(i)}
  <div class="links">{"".join(links)}</div>
 </div>
</article>'''
radios=f'<input type="radio" name="f" id="f-all" checked><label for="f-all">Все · {len(P)}</label>'+"".join(
 f'<input type="radio" name="f" id="f-{k}"><label for="f-{k}" id="cat-{k}"><i style="background:{COL[k]}"></i>{n} · {sum(1 for p in P if p[1]==k)}</label>' for k,(n,_) in CATS.items())
catalog=f'''<section class="catalog">
 <div class="cat-head">
  <div class="page-title"><span class="eyebrow">Каталог мест</span>
  <h1>Куда пойти и&nbsp;чем заняться</h1><p class="lead">13 мест в четырёх категориях. Выберите линию, чтобы оставить только её станции.</p></div>
 </div>
 <div class="filter" role="radiogroup" aria-label="Фильтр по категориям">{radios}</div>
 <div class="grid">
{"".join(card(p) for p in P)}
 </div>
<p class="note rv" style="margin-top:28px">Данные собраны из открытых источников (официальные сайты учреждений, 2ГИС, KudaGo, Афиша) и проверены 29 октября 2026 года. Условия посещения могут измениться, уточняйте их на официальном сайте места.</p>
</section>'''

lich='''<section class="essay">
 <div class="text">
  <div class="page-title"><span class="eyebrow">Аналитический вывод</span>
  <h1>Как культурная среда влияет на личность</h1></div>
  <p class="main rv">Культурная среда — это не фон, а пространство, в котором личность формируется и включается в общество. Посещая музеи и библиотеки, человек осваивает культурное наследие и учится понимать ценности и смыслы, накопленные обществом. Арт-пространства и мастерские дают возможность не только потреблять культуру, но и создавать её самому, а именно в творчестве человек проверяет свои способности и находит собственный голос. Клубы, лектории и культурные центры превращают интерес в общее дело: здесь появляются единомышленники, навыки общения и опыт ответственности за результат. Для тех, кто недавно переехал в Москву, такие места особенно важны, потому что ускоряют адаптацию и помогают почувствовать себя частью города. Таким образом, доступная и знакомая культурная инфраструктура напрямую поддерживает социализацию и самореализацию личности.</p>
  <div class="terms rv" aria-label="Понятия курса"><span>культурная среда</span><span>социализация</span><span>самореализация</span><span>культурные практики</span><span>сообщество</span><span>культурное наследие</span></div>
 </div>
 <aside class="flow rv-r" aria-label="Путь от посещения к самореализации">
  <span class="eyebrow">От посещения к самореализации</span>
  <div class="steps-in stagger" style="display:grid">
  <div class="step"><span class="n">1</span><div><h3>Знакомство</h3><p>Музей, библиотека: человек узнаёт культурное наследие и ценности общества.</p></div></div>
  <div class="step"><span class="n">2</span><div><h3>Интерес</h3><p>Выставка или лекция показывает, что ему действительно интересно.</p></div></div>
  <div class="step"><span class="n">3</span><div><h3>Практика</h3><p>Мастерская, разговорный клуб, студия: интерес становится навыком.</p></div></div>
  <div class="step"><span class="n">4</span><div><h3>Сообщество</h3><p>Единомышленники, клубы и культурные центры: включение в общество.</p></div></div>
  <div class="step"><span class="n">5</span><div><h3>Самореализация</h3><p>Собственные проекты, выступления, волонтёрство, вклад в культуру.</p></div></div>
  </div>
 </aside>
</section>
<section class="sec">
 <div class="rv" style="display:grid;gap:14px"><span class="eyebrow">Что даёт каждая категория</span><h2>Место и его роль для личности</h2></div>
 <div class="pairs stagger">
  <div class="pair c-museum"><b>Музеи</b><span>Приобщение к культурному наследию, понимание истории и ценностей общества.</span></div>
  <div class="pair c-lib"><b>Библиотеки</b><span>Самообразование, навык работы с информацией, языки и межкультурный диалог.</span></div>
  <div class="pair c-art"><b>Арт-пространства</b><span>Творчество и самовыражение, знакомство с творческими профессиями.</span></div>
  <div class="pair c-club"><b>Клубы и практики</b><span>Сообщество единомышленников, командная работа, ответственность.</span></div>
 </div>
</section>
<section class="sec">
 <div class="rv" style="display:grid;gap:14px"><span class="eyebrow">Полезные советы</span><h2>Как начать</h2></div>
 <ul class="tips stagger">
  <li><b>Узнайте про льготы</b><span>У студентов, школьников, пенсионеров и многодетных семей есть бесплатные дни и скидки — документ берите с собой.</span></li>
  <li><b>Оформите Пушкинскую карту</b><span>Если вам 14–22 года: 5000 ₽ в год на билеты в музеи, театры и на концерты.</span></li>
  <li><b>Подпишитесь на афиши</b><span>Лекции, мастерские и клубы часто требуют регистрации, места быстро заканчиваются.</span></li>
  <li><b>Ходите не в одиночку</b><span>Позовите друзей, коллег или семью: так интереснее обсуждать увиденное.</span></li>
  <li><b>Пробуйте разное</b><span>Музей, мастерская, разговорный клуб — так быстрее понять, что по-настоящему интересно.</span></li>
  <li><b>Запишитесь в клуб</b><span>Театральная студия, разговорный или книжный клуб помогают превратить интерес в дело.</span></li>
 </ul>
</section>
<section class="sec"><div class="btns rv"><a class="btn primary" href="catalog.html">Перейти к каталогу <span class="arr">→</span></a><a class="btn ghost" href="afisha.html">Посмотреть афишу</a></div></section>'''

TEAM=[("ВР","Волков Р. М.","Руководитель проекта, автор текстов, технический редактор"),("ЧН","Чернышев Н. А.","Контент-исследователь"),("ТА","Товбоев А.","Контент-исследователь"),("ЛА","Локотош А. В.","Автор текстов, аналитик"),("КВ","Касько В. Г.","Фоторедактор"),("МГ","Москалев Г. Д.","Технический редактор")]
team=f'''<section style="display:grid;gap:24px">
 <div class="page-title"><span class="eyebrow">Команда проекта</span>
 <h1>Кто сделал «КультКарту»</h1>
 <p class="lead">Учебный проект по дисциплине «Культура личности и общества» (КЛИО), группа ОБ26-30.</p></div>
 <div class="team stagger">{"".join(f'<div class="member"><span class="av">{a}</span><b>{n}</b><span>{r}</span></div>' for a,n,r in TEAM)}</div>
</section>
<section class="sec">
 <div class="rv" style="display:grid;gap:14px"><span class="eyebrow">О проекте</span><h2>Зачем мы это сделали</h2></div>
 <div class="about stagger">
  <div class="box"><b>Цель</b><p>Создать сайт-путеводитель, который помогает москвичам найти в городе места и практики для самореализации и показывает связь культурной среды с развитием личности.</p></div>
  <div class="box"><b>Задачи</b><ul><li>Отобрать 10–15 доступных культурных мест Москвы</li><li>Собрать о них сведения из открытых источников</li><li>Подготовить тексты, фото и аналитический вывод</li><li>Сверстать сайт на HTML и CSS и опубликовать его</li><li>Собрать отзывы пользователей и доработать сайт</li></ul></div>
 </div>
</section>
<section class="sec">
 <div class="rv" style="display:grid;gap:14px"><span class="eyebrow">Этапы работы</span><h2>Контрольные точки</h2></div>
 <ol class="timeline stagger">
  <li class="done"><b>КТ 2</b><span>Инициирование</span><small>Тема, команда, роли, паспорт проекта</small></li>
  <li><b>КТ 3</b><span>Сбор данных</span><small>Критерии отбора, список мест, сведения</small></li>
  <li><b>КТ 4</b><span>Разработка</span><small>Тексты карточек, вёрстка сайта</small></li>
  <li><b>КТ 5</b><span>Тестирование</span><small>Публикация, опрос, правки</small></li>
  <li><b>КТ 6</b><span>Защита</span><small>Финальная версия и презентация</small></li>
 </ol>
</section>
<section class="sec"><dl class="meta stagger">
 <div><dt>Группа</dt><dd>ОБ26-30</dd></div>
 <div><dt>Преподаватель</dt><dd>Замай Вера Васильевна</dd></div>
 <div><dt>Дисциплина</dt><dd>Культура личности и общества</dd></div>
</dl></section>
<section class="sec" id="feedback">
 <div class="feedback rv-z">
  <span class="eyebrow">Обратная связь</span>
  <h2>Был ли сайт полезен?</h2>
  <p>Мы проводим короткий опрос среди посетителей сайта, чтобы улучшить каталог. Вот вопросы, на которые мы просим ответить:</p>
  <ol class="qs">
   <li>Как давно вы живёте в Москве?</li>
   <li>Какие места из каталога вы уже посещали?</li>
   <li>Какие места хотите посетить после знакомства с сайтом?</li>
   <li>Насколько сайт был полезен (от 1 до 5)?</li>
   <li>Какое место стоит добавить в каталог?</li>
  </ol>
  <span class="soon">Ссылка на анкету появится здесь после публикации сайта</span>
 </div>
</section>
<section class="sec sources rv">
 <span class="eyebrow">Источники</span>
 <p>Официальные сайты учреждений, 2ГИС, KudaGo, Афиша. Данные проверены 29 октября 2026 года.</p>
 <ul>
  <li><a href="https://kudago.com/msk/list/besplatnoe-poseshenie-muzeev-dlya-studentov/" target="_blank" rel="noopener">KudaGo: бесплатное посещение музеев для студентов</a></li>
  <li><a href="https://daily.afisha.ru/news/110606-s-17-iyunya-vhod-v-otkrytoe-hranenie-muzeya-garazh-stanet-besplatnym-dlya-studentov-vuzov/" target="_blank" rel="noopener">Афиша Daily: бесплатный вход в открытое хранение «Гаража» для студентов</a></li>
  <li><a href="https://www.sravni.ru/text/pushkinskaya-karta-2026" target="_blank" rel="noopener">Сравни: Пушкинская карта в 2026 году</a></li>
  <li><a href="https://tonkosti.ru/ГЭС-2" target="_blank" rel="noopener">Тонкости туризма: ГЭС-2</a></li>
 </ul>
</section>'''

groups="".join(f'<section class="evgroup c-{p[1]}"><h3><span class="num-s">{p[0]}</span><a href="catalog.html#place-{p[0]}">{E(p[2])}</a></h3><ul class="evlist">{"".join(evitem(e) for e in events(p[0]))}</ul></section>' for p in P if events(p[0]))
afisha=f'''<section class="page-title">
 <span class="eyebrow">Афиша</span>
 <h1>События на ближайшие две недели</h1>
 <p class="lead">Выставки, лекции, концерты и мастер-классы в местах из нашего каталога. Афиша обновляется автоматически каждый день в 06:00 по московскому времени.</p>
 <span class="live"><i></i>{updnote}</span>
</section>
<div class="evgroups stagger">{groups or '<div class="empty"><span class="clock" aria-hidden="true"></span><div><b>События появятся после ближайшего обновления</b><p class="note">Пока можно посмотреть программу на официальных сайтах мест в <a href="catalog.html">каталоге</a>.</p></div></div>'}</div>
<p class="note rv" style="margin-top:24px">Перед посещением проверьте время и условия входа на странице события.</p>'''
pages=[("index.html","КультКарта Москвы","Культурный путеводитель по Москве: музеи, библиотеки, арт-пространства и клубы",home),
 ("catalog.html","Каталог мест — КультКарта","Музеи, библиотеки, арт-пространства и клубы Москвы",catalog),
 ("afisha.html","Афиша — КультКарта","Ближайшие события в музеях, библиотеках и арт-пространствах Москвы",afisha),
 ("lichnost.html","Как это влияет на личность — КультКарта","Аналитический вывод о влиянии культурной среды на личность",lich),
 ("team.html","Команда — КультКарта","Команда проекта КультКарта, группа ОБ26-30",team)]
for fn,t,d,b in pages:
    (OUT/fn).write_text(full(t,d,fn,b),encoding='utf-8')
(OUT/'img'/'КАК_ДОБАВИТЬ_ФОТО.txt').write_text("Положите в эту папку фотографии мест в формате JPG с именами 01.jpg, 02.jpg ... 13.jpg.\nНомер файла = номер карточки в каталоге. Фото автоматически появятся на сайте.\nРекомендуемый размер: 1200x750 пикселей (пропорция 16:10).\n",encoding='utf-8')
if os.environ.get('PUB'):
    pathlib.Path(os.environ['PUB']).write_text(fragment(pages[0][1],pages[0][2],"index.html",home),encoding='utf-8')
print("built")
