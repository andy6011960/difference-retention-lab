# ARCHITECTURE_DOCUMENT_TEMPLATE.md

# ==================================================================================================

# DOCUMENT TITLE

# ==================================================================================================

Version: X.X

Status: Draft / Stable / Release

Date: YYYY-MM-DD

Author: Difference Retention Laboratory

---

# ENGLISH VERSION

---

## Purpose

Describe the purpose of the architectural component.

Answer the question:

Why does this component exist?

---

## Ontological Principle

Describe the ontological role.

Explain:

What is this object?

What is it not?

What distinguishes it from neighbouring components?

---

## Position inside the Architecture

Illustrate the architectural position.

Example:

```text
Higher Layer
      │
      ▼
Current Component
      │
      ▼
Lower Layer
```

---

## Responsibilities

List the responsibilities of the component.

Describe what the component must always perform.

---

## Non-Responsibilities

Describe what the component must never perform.

Architectural boundaries are often more important than functionality.

---

## Inputs

Describe all accepted inputs.

---

## Outputs

Describe all produced outputs.

---

## Internal Invariants

List the invariants that must always remain true.

These invariants define architectural correctness.

---

## Interaction with Other Components

Describe interaction with neighbouring modules.

Specify communication only through public interfaces.

---

## Scientific Meaning

Describe why this architectural object is scientifically meaningful.

Explain its role in the ontology.

---

## Future Evolution

Describe expected future extensions.

Do not describe implementation.

Describe architectural growth.

---

## Architectural Verdict

Summarize the architectural role in one or two sentences.

This section should answer:

Why is this component indispensable?

---

# ==================================================================================================

# РУССКАЯ ВЕРСИЯ

# ==================================================================================================

---

## Назначение

Опишите назначение архитектурного компонента.

Ответьте на вопрос:

Для чего существует данный компонент?

---

## Онтологический принцип

Опишите онтологическую роль.

Ответьте:

Что представляет собой данный объект?

Чем он не является?

Чем он отличается от соседних компонентов?

---

## Положение в архитектуре

Покажите положение компонента.

Например:

```text
Верхний уровень
      │
      ▼
Текущий компонент
      │
      ▼
Нижний уровень
```

---

## Ответственность

Перечислите обязанности компонента.

Что он обязан выполнять всегда?

---

## Что компонент НЕ делает

Перечислите архитектурные ограничения.

Чем компонент принципиально не занимается?

---

## Входы

Опишите принимаемые данные.

---

## Выходы

Опишите результаты работы.

---

## Внутренние инварианты

Перечислите свойства, которые всегда должны сохраняться.

Именно они определяют корректность архитектуры.

---

## Взаимодействие с другими компонентами

Опишите взаимодействие через публичные интерфейсы.

Не описывайте внутреннюю реализацию соседних модулей.

---

## Научный смысл

Объясните научную роль компонента.

Почему он необходим с точки зрения онтологии Difference Retention Laboratory?

---

## Перспективы развития

Опишите возможное развитие архитектуры.

Не описывайте программную реализацию.

Опишите направление эволюции.

---

## Архитектурный вывод

В одном-двух абзацах сформулируйте итог.

Ответьте на вопрос:

Почему без данного компонента архитектура была бы неполной?

---

# END OF TEMPLATE
