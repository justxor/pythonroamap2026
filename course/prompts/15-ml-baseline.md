# 🎯 Промпт: ML-baseline за 5 минут

> Цель: получить рабочий baseline бустинга по своему датасету.

## Шаблон (копируй в LLM)


```text
# Роль
Ты senior ML engineer, пишешь прод-код на Python 3.13 в стеке 2026 (polars, sklearn, lightgbm, optuna, mlflow).

# Задача
Напиши baseline-пайплайн для бинарной классификации. Датасет: <описание + путь к файлу>.

# Требования
1. Загрузка через polars.read_parquet
2. EDA: shape, dtypes, missing, target balance
3. Stratified train/test split (test_size=0.2, seed=42)
4. sklearn Pipeline: ColumnTransformer (numeric: median impute + StandardScaler, cat: OneHot) + LGBMClassifier
5. fit с early_stopping_rounds=100
6. metric: ROC-AUC на holdout
7. mlflow.log_params + mlflow.log_metric + mlflow.lightgbm.log_model

# Ограничения
- Никакого pandas, только polars (преобразовав перед sklearn в .to_pandas() точечно)
- type hints везде
- без утечек (fit_transform только на train)
- выводи AUC в stdout

# Формат ответа
Один блок кода, готовый к запуску через `uv run python train.py`. Не добавляй пояснений вне кода.
```

## Пример использования

Подставь в `<описание...>` свои данные, например:

> Датасет: Telco Customer Churn (data/telco.parquet, 7043 строк, 21 колонка, target=Churn). Числовые: tenure, MonthlyCharges, TotalCharges. Категориальные: Contract, PaymentMethod, InternetService.

## Где улучшать

- Для временных рядов → замени `StratifiedKFold` на `TimeSeriesSplit`.
- Если датасет с множеством категорий (>50) → CatBoost вместо LightGBM.
- Для мультикласса → `objective="multiclass"`, `num_class=N`, метрика macro-F1.

---

[← К каталогу промптов](README.md) · [Этап 16: ML](../stage-16-ml.md)
