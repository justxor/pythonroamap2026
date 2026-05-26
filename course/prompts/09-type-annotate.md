# 🏷️ Промпт 09 — Добавить type hints

> Используй когда: достался нетипизированный код, нужно сделать pyright --strict.

---

```
[CONTEXT]
Python 3.13, pyright --strict.
Стек: <твой стек>.

[UNTYPED CODE]
[ВСТАВЬ КОД БЕЗ ТИПОВ]

[TASK]
Добавь type hints. Код должен пройти pyright --strict.

[RULES]
- НИКАКИХ Any. Если без Any нельзя — TODO-комментарий с обоснованием.
- НИКАКИХ cast() без TODO.
- Используй современный синтаксис: list[int] вместо List[int], X | None вместо Optional[X].
- Generic-функции: новый PEP 695 синтаксис: def f[T](x: T) -> T: ...
- Protocol для duck-typed зависимостей.
- TypedDict / dataclass / Pydantic v2 для структур данных — выбери уместное.
- Sequence / Mapping / Iterable в параметрах (LSP-friendly), конкретные типы в возвращаемом значении.
- collections.abc.Callable[[Args], Ret] для функций.

[LENS]
1) **Типизированный код** целиком.
2) **Список спорных мест** — где пришлось ввести Protocol/TypeVar/Union и почему.
3) **Команда проверки**: \`uv run pyright <file>\`.
```
