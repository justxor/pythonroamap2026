# Этап 5. Стандартная библиотека

> 🎯 «Если функция есть в stdlib — не тащи зависимость».
> ⏱ 3 недели.

[← К оглавлению](README.md)

## Содержание

- [Урок 1. pathlib, shutil, tempfile](#урок-1-pathlib-shutil-tempfile)
- [Урок 2. collections, datetime, Decimal](#урок-2-collections-datetime-decimal)
- [Урок 3. logging](#урок-3-logging)
- [Урок 4. argparse и CLI](#урок-4-argparse-и-cli)
- [Урок 5. subprocess безопасно](#урок-5-subprocess-безопасно)
- [Упражнения](#упражнения)

---

## Урок 1. pathlib, shutil, tempfile

```python
from pathlib import Path

p = Path("data") / "users.json"
print(p.exists(), p.is_file(), p.suffix)

# Чтение/запись
text = p.read_text(encoding="utf-8")
p.write_text("hello", encoding="utf-8")

# Создание директорий
(Path("logs") / "2026" / "11").mkdir(parents=True, exist_ok=True)

# Поиск
for py in Path(".").rglob("*.py"):
    print(py)
```

### shutil

```python
import shutil

shutil.copy("a.txt", "b.txt")
shutil.copytree("src", "dst", dirs_exist_ok=True)
shutil.move("a.txt", "archive/")
shutil.rmtree("temp")
shutil.make_archive("backup", "zip", "src")
shutil.unpack_archive("backup.zip", "out")
```

### tempfile

```python
import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tf:
    tf.write(b"hello")
    path = Path(tf.name)

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "x.txt"
    p.write_text("hi")
# d удалён
```

---

## Урок 2. collections, datetime, Decimal

### collections

```python
from collections import Counter, defaultdict, deque, ChainMap

# Counter
words = "to be or not to be".split()
print(Counter(words).most_common(2))   # [('to',2),('be',2)]

# defaultdict
groups = defaultdict(list)
for word in ["apple", "ant", "bee"]:
    groups[word[0]].append(word)
# {'a': ['apple', 'ant'], 'b': ['bee']}

# deque — O(1) на обоих концах
q = deque([1, 2, 3])
q.append(4); q.appendleft(0)

# С ограничением
last_5 = deque(maxlen=5)
for i in range(100): last_5.append(i)
# deque([95,96,97,98,99], maxlen=5)

# ChainMap
cfg = ChainMap({"x": 1}, {"x": 0, "y": 2})
print(cfg["x"])    # 1 (берётся из первого)
```

### datetime + zoneinfo

```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

now = datetime.now(ZoneInfo("Europe/Moscow"))
ny = now.astimezone(ZoneInfo("America/New_York"))

tomorrow = now + timedelta(days=1)
print(now.isoformat())
parsed = datetime.fromisoformat("2026-05-26T12:00:00+03:00")
```

### Decimal — для денег

```python
from decimal import Decimal

a = Decimal("0.1")
b = Decimal("0.2")
print(a + b)   # 0.3 точно
```

---

## Урок 3. logging

### Базовый вариант

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)
log.info("server started")
log.error("DB timeout", exc_info=True)
```

### dictConfig (для проектов)

```python
import logging.config

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"format": '{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}'},
    },
    "handlers": {
        "stdout": {"class": "logging.StreamHandler", "formatter": "json"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 10_000_000,
            "backupCount": 5,
            "formatter": "json",
        },
    },
    "root": {"level": "INFO", "handlers": ["stdout", "file"]},
})
```

### Уровни

- `DEBUG` — для разработки
- `INFO` — нормальный поток
- `WARNING` — странное, но работает
- `ERROR` — ошибка
- `CRITICAL` — система не работает

---

## Урок 4. argparse и CLI

### Базовый CLI

```python
import argparse

p = argparse.ArgumentParser(description="Анализатор файлов")
p.add_argument("path")
p.add_argument("-v", "--verbose", action="store_true")
p.add_argument("--limit", type=int, default=10)
p.add_argument("--mode", choices=["fast", "full"], default="fast")
args = p.parse_args()
```

### Подкоманды

```python
parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="cmd", required=True)

p_add = sub.add_parser("add"); p_add.add_argument("title")
p_list = sub.add_parser("list"); p_list.add_argument("--all", action="store_true")

args = parser.parse_args()
match args.cmd:
    case "add":  print(f"add {args.title}")
    case "list": print(f"list all={args.all}")
```

Если CLI сложнее 4 команд — берём `typer`:

```python
import typer
app = typer.Typer()

@app.command()
def add(title: str): print(f"add {title}")

if __name__ == "__main__":
    app()
```

---

## Урок 5. subprocess безопасно

### Правило: никогда не shell=True с пользовательским вводом

```python
import subprocess

# ❌ shell injection
subprocess.run(f"git clone {url}", shell=True)

# ✅ список аргументов
subprocess.run(["git", "clone", url], check=True)
```

### Захват вывода

```python
result = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True, text=True, check=True, timeout=10,
)
print(result.stdout)
```

### Стриминг

```python
with subprocess.Popen(
    ["ping", "-c", "5", "google.com"],
    stdout=subprocess.PIPE, text=True,
) as p:
    for line in p.stdout:
        print(line.rstrip())
```

---

## Упражнения

### Упражнение 1. Backup-утилита

`backup.py`:
1. CLI: `backup.py <src> <dst> [--exclude PATTERN] [--dry-run]`.
2. Копирует с сохранением структуры.
3. Исключения по glob.
4. Логи INFO в stdout, DEBUG в файл.
5. Отчёт: файлов, размер, время.

#### Решение

```python
"""backup.py"""
import argparse, fnmatch, logging, shutil
from pathlib import Path
from time import perf_counter

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("backup")


def is_excluded(path: Path, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path.name, p) for p in patterns)


def backup(src: Path, dst: Path, excludes: list[str], dry: bool):
    files, size = 0, 0
    for path in src.rglob("*"):
        if path.is_dir(): continue
        if is_excluded(path, excludes): continue
        target = dst / path.relative_to(src)
        log.info("copy %s -> %s", path, target)
        if not dry:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        files += 1
        size += path.stat().st_size
    return files, size


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src", type=Path)
    p.add_argument("dst", type=Path)
    p.add_argument("--exclude", action="append", default=[])
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    start = perf_counter()
    f, s = backup(args.src, args.dst, args.exclude, args.dry_run)
    log.info("done: %d files, %.2f MB, %.2fs", f, s/1024/1024, perf_counter()-start)


if __name__ == "__main__":
    main()
```

### Упражнение 2. CLI tracker привычек

`habit.py` на SQLite:
- `habit add "пить воду"`
- `habit done <id>` — отметить сегодня
- `habit list` — все привычки и стрик
- `habit stats <id>` — последние 30 дней

#### Решение

```python
"""habit.py"""
import argparse, sqlite3
from datetime import date, timedelta
from pathlib import Path

DB = Path("habits.db")


def init():
    conn = sqlite3.connect(DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS habits (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);
        CREATE TABLE IF NOT EXISTS marks (habit_id INTEGER, day TEXT, PRIMARY KEY (habit_id, day));
    """)
    return conn


def streak(conn, habit_id):
    today = date.today()
    days = {date.fromisoformat(r[0]) for r in conn.execute(
        "SELECT day FROM marks WHERE habit_id = ?", (habit_id,))}
    n = 0
    while today - timedelta(days=n) in days: n += 1
    return n


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add"); p_add.add_argument("name")
    p_done = sub.add_parser("done"); p_done.add_argument("habit_id", type=int)
    sub.add_parser("list")
    p_stats = sub.add_parser("stats"); p_stats.add_argument("habit_id", type=int)
    args = p.parse_args()
    conn = init()

    match args.cmd:
        case "add":
            conn.execute("INSERT INTO habits(name) VALUES (?)", (args.name,))
        case "done":
            conn.execute("INSERT OR IGNORE INTO marks VALUES (?, ?)",
                         (args.habit_id, date.today().isoformat()))
        case "list":
            for hid, name in conn.execute("SELECT id, name FROM habits"):
                print(f"#{hid}  {name}  streak={streak(conn, hid)}")
        case "stats":
            for i in range(30):
                d = date.today() - timedelta(days=i)
                done = conn.execute("SELECT 1 FROM marks WHERE habit_id=? AND day=?",
                                    (args.habit_id, d.isoformat())).fetchone()
                print(f"{d}  {'✓' if done else '·'}")
    conn.commit()


if __name__ == "__main__":
    main()
```

---

## Чеклист и ресурсы

- [ ] Не пишу os.path в новом коде
- [ ] Настроил dictConfig для логов
- [ ] Применяю Counter/defaultdict/deque к месту
- [ ] Работаю с zoneinfo, не pytz
- [ ] Знаю разницу json.load vs json.loads

Ресурсы:

**🚀 Главные Telegram-источники:**

1. 🤖 [t.me/ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — Python, AI/ML, Big Data — практика и примеры кода.
2. 🐍 [t.me/pythonl](https://t.me/pythonl) — главный канал по Python: новости, «задача дня», вакансии.
3. 📚 [Папка Python-каналов →](https://t.me/addlist/8vDUwYRGujRmZjFi) — кураторская подборка по Python / ML / DS / AI.

**📘 Доп. источники:**
- 📘 [PyMOTW-3](https://pymotw.com/3/) — главный справочник
- 📘 [docs.python.org/3/library](https://docs.python.org/3/library/)
- 📝 [Real Python — pathlib](https://realpython.com/python-pathlib/)
- 🎥 [Anthony Sottile](https://www.youtube.com/@anthonywritescode)
- 💬 [t.me/pythonl](https://t.me/pythonl)

---

[← Этап 4](stage-04-typing.md) · [К оглавлению](README.md) · [Этап 6 →](stage-06-async.md)
