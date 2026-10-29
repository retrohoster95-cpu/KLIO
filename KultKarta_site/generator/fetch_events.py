"""Загрузка ближайших событий для мест из каталога «КультКарты».

Источник: открытый API KudaGo (https://kudago.com/public-api/v1.4/), ключ не нужен.
Результат: generator/events.json. Если источник недоступен, файл не перезаписывается,
и сайт остаётся с последней удачной афишей.
"""
import json, sys, time, datetime, pathlib, urllib.parse, urllib.request

API = "https://kudago.com/public-api/v1.4"
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "events.json"
IDS = HERE / "place_ids.json"   # кэш найденных id мест; можно поправить вручную
DAYS = 14                       # на сколько дней вперёд показываем события
PER_PLACE = 3                   # сколько событий на одно место
MSK = datetime.timezone(datetime.timedelta(hours=3))

# номер карточки → поисковый запрос места на KudaGo
QUERIES = {
    1: "Третьяковская галерея Лаврушинский",
    2: "ГМИИ им. Пушкина",
    3: "Музей Москвы",
    4: "Музей Гараж",
    5: "Российская государственная библиотека",
    6: "Библиотека иностранной литературы",
    7: "Библиотека-читальня им. Тургенева",
    8: "ГЭС-2",
    9: "Винзавод",
    10: "Флакон",
    11: "Музеон",
    13: "Культурный центр ЗИЛ",
}


def get(path, **params):
    url = f"{API}/{path}/?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "KultKarta/1.0 (учебный проект)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except Exception as e:  # сеть, 5xx, таймаут — пробуем ещё раз
            err = e
            time.sleep(2 * (attempt + 1))
    raise err


def find_place(query):
    data = get("search", q=query, ctype="place", location="msk")
    for item in data.get("results", []):
        if item.get("ctype", "place") == "place" and item.get("id"):
            return item["id"]
    return None


def nice(text):
    text = (text or "").strip()
    return text[:1].upper() + text[1:] if text else text


def when(dates, now):
    """Ближайшая подходящая дата события в виде короткой подписи."""
    best = None
    for d in dates or []:
        start, end = d.get("start") or 0, d.get("end") or 0
        if end and end < now:
            continue
        if best is None or (start or 0) < (best[0] or 0):
            best = (start, end)
    if not best:
        return None, None
    start, end = best
    fmt = lambda ts: datetime.datetime.fromtimestamp(ts, MSK)
    if start and start > now:
        s = fmt(start)
        label = s.strftime("%d.%m")
        if s.hour or s.minute:
            label += s.strftime(", %H:%M")
        return start, label
    if end and end > now and end < now + 400 * 86400:
        return now, "идёт до " + fmt(end).strftime("%d.%m")
    return now, "идёт сейчас"


def main():
    now = int(time.time())
    ids = json.loads(IDS.read_text(encoding="utf-8")) if IDS.exists() else {}
    result, ok = {}, 0
    for num, query in QUERIES.items():
        key = str(num)
        try:
            if not ids.get(key):
                ids[key] = find_place(query)
            pid = ids.get(key)
            if not pid:
                print(f"[{num}] место не найдено: {query}")
                continue
            data = get("events", location="msk", place_id=pid,
                       actual_since=now, actual_until=now + DAYS * 86400,
                       fields="id,title,dates,site_url,is_free", page_size=20)
            ok += 1
            items = []
            for ev in data.get("results", []):
                ts, label = when(ev.get("dates"), now)
                if not label or not ev.get("title"):
                    continue
                items.append({"title": nice(ev["title"]), "url": ev.get("site_url") or "",
                              "when": label, "ts": ts, "free": bool(ev.get("is_free"))})
            items.sort(key=lambda x: x["ts"])
            result[key] = items[:PER_PLACE]
            print(f"[{num}] {query}: {len(result[key])} событий")
        except Exception as e:
            print(f"[{num}] ошибка: {e}")
    if ok == 0:
        print("Источник недоступен — оставляем прежнюю афишу.")
        sys.exit(1)
    IDS.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
    updated = datetime.datetime.now(MSK).strftime("%d.%m.%Y, %H:%M")
    OUT.write_text(json.dumps({"updated": updated, "source": "KudaGo", "places": result},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print("Готово:", updated)


if __name__ == "__main__":
    main()
