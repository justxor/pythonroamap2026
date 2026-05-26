# 🏎️ Сравнение AI-моделей для кода (Python) — актуально на 2026

> Шпаргалка-сравнение моделей кода, доступных Python-разработчику в 2026 году. Какую брать когда — с упором на **практическую применимость**, а не маркетинговые цифры.

> ⚠️ Бенчмарки меняются каждые 2-3 месяца. Эта таблица — снимок на начало 2026. Сверяйся со свежими источниками (см. внизу).

---

## 🎯 TL;DR — что брать прямо сейчас

| Сценарий | Рекомендация | Почему |
|---|---|---|
| **Архитектура, ревью, сложное мышление** | **Claude Sonnet 4.5 / Opus 4** | Лучшее качество reasoning, длинный контекст 200k+, хороший русский. |
| **Агент-режим в IDE / CLI** | **Claude Code, Cursor (Sonnet)** | Лучшее tool use, аккуратные правки кода, не ломает несвязанное. |
| **Автодополнение в VS Code** | **GitHub Copilot (GPT-5 mini)** или **Supermaven** | Быстро, дёшево, интегрировано. |
| **Бесплатно онлайн** | **DeepSeek V3.1 / Qwen3** | Open-weights, доступны через бесплатные чаты. |
| **Локально на ноутбуке (16-32 GB RAM)** | **Qwen3-Coder 14B / DeepSeek-Coder 16B Q4** | Лучшее качество в этом классе, поддержка длинного контекста. |
| **Локально автодополнение (≤ 8 GB)** | **Qwen2.5-Coder 1.5B / 3B** | Шустро, мало памяти, приемлемое качество. |
| **Совсем простые задачи / эксперименты** | **GPT-5 mini / Claude Haiku** | Быстрые и дешёвые. |

---

## 📊 Сравнительная таблица (по моделям)

| Модель | Тип | Контекст | Сильное | Слабое | Цена/доступ |
|---|---|---|---|---|---|
| **Claude Opus 4** | Frontier, закрытая | 200k+ | Архитектура, длинные задачи, reasoning, tool use | Дороже Sonnet | Подписка Pro/Max, API |
| **Claude Sonnet 4.5** | Sweet spot, закрытая | 200k+ | Лучшее соотношение цена/качество для кода. Aгент-режим. | — | Подписка, API, бесплатный лимит |
| **Claude Haiku 4** | Лёгкая, закрытая | 200k | Быстро, дёшево, для простого | Слабее на сложных задачах | API, дешёвая |
| **GPT-5** | Frontier, закрытая | 256k | Универсал, мультимодальность | Менее аккуратен в больших правках | ChatGPT Plus, API |
| **GPT-5 mini** | Лёгкая, закрытая | 256k | Дёшево, быстро | Reasoning хуже | API |
| **Gemini 2.5 Pro** | Frontier, закрытая | 1M+ | Гигантский контекст, хороший для целого репо | Местами галлюцинирует имена API | AI Studio (бесплатно с лимитами) |
| **DeepSeek V3.1** | Open-weights | 128k | Открытые веса, сильный код, бесплатно через chat.deepseek.com | Цензура, иногда странные ответы на нестандартное | Бесплатно (chat), open-weights |
| **DeepSeek-Coder-V3** | Open-weights, code | 128k | Заточена под код, FIM (fill-in-the-middle) | Слабее общий reasoning | Open-weights |
| **Qwen3** (Coder/Instruct) | Open-weights | 128k+ | Очень сильна на коде, мультиязычность, free | Документация частично только на китайском | Open-weights |
| **Qwen3-Coder 7B/14B/32B** | Open-weights, code | 32-128k | Лучшая локальная модель кода (по бенчам HumanEval/MBPP) | Большие веса требуют GPU/Mac M-серии | ollama, llama.cpp |
| **Codestral 25B** | Open-weights, code (Mistral) | 32k | Хорошая базовая модель для FIM | Уступает Qwen3-Coder | ollama |
| **Llama 3.3 70B** | Open-weights | 128k | Большой generalist | Не специализирована на код | Groq (быстро), ollama |

---

## 🛠 Сравнение инструментов вайбкодинга

| Инструмент | Под капотом | Сильное | Слабое | Цена |
|---|---|---|---|---|
| **Claude Code (CLI)** | Anthropic Claude Sonnet/Opus | Терминал, агент пишет/правит файлы, запускает команды, читает stderr | Только CLI, привыкать к новому workflow | Подписка Claude или per-token API |
| **Cursor** | На выбор: Claude/GPT/Gemini | IDE (форк VS Code), Cmd+K, Cmd+L, Composer, `.cursorrules` | Платный, иногда лагает на больших репо | $20/мес Pro |
| **Windsurf** | Claude/GPT | Похож на Cursor, агент Cascade | Молодой проект | $15/мес |
| **GitHub Copilot** | GPT-5/Claude (выбираемо) | Глубокая интеграция с GitHub, Workspaces, Copilot Chat в VS Code/JetBrains | Иногда упрямый | $10/мес (бесплатно студентам, OSS) |
| **Aider (CLI)** | Любая через API | Open-source, любая модель, git-diff voice-friendly | Без GUI, требует настройки | Бесплатно (только цена токенов) |
| **Continue.dev** | Любая (включая ollama) | Open-source, любая модель локально или в облаке, VS Code + JetBrains | Меньше UI-фич чем у Cursor | Бесплатно |
| **Codeium / Supermaven** | Свои модели | Очень быстрое автодополнение | Меньше «умного» агентского поведения | Бесплатный тариф |
| **Tabby** | Open-source self-hosted | Полностью self-hosted, без передачи кода наружу | Требует своего сервера/GPU | Бесплатно |

---

## 🧠 Когда какая модель лучше — практический разбор

### Архитектура и проектирование
**Топ:** Claude Sonnet 4.5 / Opus 4, Gemini 2.5 Pro.
Эти модели реально *думают* перед ответом. Дают альтернативы, видят trade-offs, не торопятся.
GPT-5 тоже хорош, но в коде часто выбирает «модный» вариант вместо простого.

### Большой рефакторинг по нескольким файлам
**Топ:** Claude Code + Sonnet 4.5; Cursor Agent с Claude.
Длинный контекст, аккуратные diff-ы, не ломает несвязанные тесты. Gemini неплох благодаря 1M-контексту, но иногда «забывает» правки.

### Автодополнение по строке
**Топ:** GitHub Copilot, Supermaven, Codeium.
Главное — задержка < 200ms. Локально с Qwen2.5-Coder 1.5B на M-серии тоже работает шустро.

### Объяснение незнакомого кода
**Топ:** Claude Sonnet 4.5, GPT-5.
Хорошо адаптируются под уровень читателя, выделяют ключевое, дают релевантные параллели.

### Поиск багов в чужом коде
**Топ:** Claude Opus 4, GPT-5.
Find-the-bug — задача reasoning. Лёгкие модели часто говорят «всё ок» там, где не ок.

### Перевод sync → async / типизация
**Топ:** любая frontier-модель, **Qwen3-Coder** для локального запуска.
Это «механическая» работа, на ней даже опен-сорс справляется.

### SQL и оптимизация запросов
**Топ:** Claude Sonnet 4.5, DeepSeek-Coder.
DeepSeek неожиданно силён на SQL, особенно сложных JOIN-ах с оконными функциями.

### Data Science / ML / pandas-Polars
**Топ:** Claude Sonnet 4.5, GPT-5.
Знают свежие API Polars, scikit-learn 1.5+, NumPy 2.x. Локальные модели могут отставать на 6-12 месяцев.

### Безопасный код, security
**Топ:** Claude Opus 4 (более осторожен), GPT-5.
⚠️ Никакая модель не заменит human review для security-критичного кода (auth, payments, crypto).

---

## 💻 Локальные модели — что реально запустить

| Память | Модель | Качество | Скорость |
|---|---|---|---|
| **8 GB RAM** | Qwen2.5-Coder 1.5B Q4 | Базовое автодополнение | 30-60 tok/s |
| **16 GB RAM** | Qwen3-Coder 7B Q4, DeepSeek-Coder 6.7B Q4 | Близко к Copilot | 15-30 tok/s |
| **32 GB RAM** | Qwen3-Coder 14B Q4, Codestral 22B Q4 | Близко к GPT-4o базовый | 8-15 tok/s |
| **64+ GB / GPU 24GB** | Qwen3-Coder 32B Q4, DeepSeek-Coder 33B Q4 | Близко к Claude Haiku / GPT-5 mini | 10-20 tok/s |
| **Apple M2/M3 Max 64GB** | Qwen3-Coder 32B Q5, Llama 3.3 70B Q4 | Лучшее, что реально запустить дома | 15-25 tok/s |

```bash
# Установка ollama
brew install ollama   # mac
curl -fsSL https://ollama.com/install.sh | sh   # linux

# Лучшие модели для кода (2026)
ollama pull qwen3-coder:14b
ollama pull deepseek-coder-v3:16b
ollama pull codestral:22b
ollama pull qwen2.5-coder:1.5b   # для автодополнения

# Подключение к Continue.dev — см. course/stage-14-vibecoding.md, урок 14.7
```

---

## 📈 Бенчмарки, на которые имеет смысл смотреть

| Бенчмарк | Что измеряет | Где смотреть |
|---|---|---|
| **HumanEval** | Простые задачи кодинга | Papers, LiveBench, Aider leaderboard |
| **MBPP** | Базовый Python | Аналогично |
| **SWE-bench / SWE-bench Verified** | Реальные баги в GitHub-репозиториях | [swebench.com](https://www.swebench.com/) |
| **LiveCodeBench** | Не зашитые в трейн задачи | [livecodebench.github.io](https://livecodebench.github.io/) |
| **Aider Leaderboard** | Применение diff-ов к реальным проектам | [aider.chat/docs/leaderboards](https://aider.chat/docs/leaderboards/) |
| **LMArena (бывший Chatbot Arena)** | Слепое сравнение людьми | [lmarena.ai](https://lmarena.ai/) |

⚠️ Не доверяй заявленным самими моделями цифрам. Смотри **независимые лидерборды** (SWE-bench, Aider, LiveCodeBench), они ближе к реальности.

---

## 💡 Практические советы

1. **Не привязывайся к одной модели.** За 6 месяцев лидерство меняется. Держи инструменты, которые позволяют менять backend (Cursor, Continue.dev, Aider).
2. **Для критичной задачи — попроси две модели.** Если Claude и GPT согласны — скорее всего, правильно. Если расходятся — копай сам.
3. **Длинный контекст ≠ магия.** Чем больше контекста, тем больше галлюцинаций деталей. Дай минимум.
4. **Лимит подписки кончился — переключайся на open-weights.** DeepSeek Chat бесплатен с лимитами; ollama локально без лимитов вообще.
5. **Тестируй на своей задаче.** Бенчмарки не предсказывают, как модель справится с твоей конкретной кодовой базой.

---

## 📚 Источники и где следить за обновлениями

- 📊 [Aider Leaderboard](https://aider.chat/docs/leaderboards/) — самый честный для реальной разработки.
- 📊 [SWE-bench Verified](https://www.swebench.com/) — баги в реальных GitHub-репозиториях.
- 📊 [LiveCodeBench](https://livecodebench.github.io/) — без data contamination.
- 📊 [LMArena](https://lmarena.ai/) — слепые сравнения людьми.
- 📊 [Hugging Face Leaderboards](https://huggingface.co/spaces) — для open-weights моделей.
- 📕 [Ollama library](https://ollama.com/library) — все актуальные локальные модели.
- 📕 [Anthropic docs](https://docs.anthropic.com/), [OpenAI docs](https://platform.openai.com/docs).
- 💬 **Telegram:** [@ai_machinelearning_big_data](https://t.me/ai_machinelearning_big_data) — оперативный поток новостей про модели и инструменты.
- 📚 [Папка лучших AI-каналов 🎁](https://t.me/addlist/8vDUwYRGujRmZjFi).

---

## ☑ Чеклист «как выбирать»

- [ ] Определил тип задачи (архитектура / автодополнение / агент-правка / chat).
- [ ] Знаю требования к приватности (можно ли отправлять код в облако?).
- [ ] Понимаю бюджет (бесплатно / $10-20/мес / API per-token).
- [ ] Учёл скорость отклика (для autocomplete нужна < 200ms).
- [ ] Проверил на 3-5 типичных для себя задачах, не на benchmark.
- [ ] Имею fallback (вторая модель / локальная) на случай лимитов/даунтайма.

---

[⬅ Этап 14 (Вайбкодинг)](stage-14-vibecoding.md) | [📚 Оглавление](README.md) | [📝 Промпты](prompts/README.md)
