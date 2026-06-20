# ==================================================================================================

# README_EXPERIMENT_RUNNER

#

# Difference Retention Laboratory

#

# Experiment Runner Architecture

#

# ==================================================================================================

Version: 1.0

Status: CANONICAL

Date: 2026-06-20

Author: Difference Retention Laboratory

---

# ENGLISH VERSION

---

## Purpose

Experiment Runner is the first executable laboratory layer.

Its purpose is not to analyse experiments.

Its purpose is to execute experiments while preserving the complete evidential chain.

---

## Ontological Principle

Experiment Runner executes.

It does not interpret.

It does not evaluate physical correctness.

It does not infer scientific conclusions.

It records the existence of an experimental run.

---

## Position inside the Architecture

```text
Evidence Adapter

        │

        ▼

Experiment Runner

        │

        ▼

Experiment Run Record

        │

        ▼

Retention Analysis
```

---

## Responsibilities

Experiment Runner shall:

• receive validated Evidence State streams;

• verify architectural invariants;

• register the execution of an experiment;

• preserve provenance;

• preserve Evidence identifiers;

• preserve state ordering;

• produce an immutable Experiment Run Record.

---

## Non-Responsibilities

Experiment Runner shall never:

• calculate physical models;

• estimate parameters;

• smooth signals;

• classify origin;

• modify Evidence;

• modify State streams;

• perform scientific interpretation;

• make decisions.

---

## Inputs

Validated State Streams.

Current implementation:

RC_EVIDENCE_STATE_STREAM.

Future implementations may include:

Carbon State Streams

Electrolyte State Streams

Biological State Streams

---

## Outputs

Experiment Run Record.

The record documents:

• executed environment;

• participating states;

• Evidence statistics;

• provenance preservation;

• execution status.

---

## Internal Invariants

The following invariants shall always hold.

Evidence remains unchanged.

Provenance remains preserved.

Experiment Runner performs no interpretation.

State ordering is preserved.

Every run remains reproducible.

---

## Interaction with Other Components

Experiment Runner accepts only validated Adapter outputs.

It communicates with later analytical layers only through Experiment Run Records.

---

## Scientific Meaning

Experiment Runner separates experimentation from interpretation.

This distinction allows laboratory execution to remain reproducible independently of future scientific models.

---

## Future Evolution

Future versions may support:

• multiple simultaneous environments;

• synchronized experiments;

• distributed execution;

• replay;

• parameter sweeps;

• experimental scheduling;

• automatic laboratory journals.

---

## Architectural Verdict

Experiment Runner is the execution boundary of Difference Retention Laboratory.

It transforms validated experimental states into reproducible laboratory experiments without performing scientific interpretation.

---

# ==================================================================================================

# РУССКАЯ ВЕРСИЯ

# ==================================================================================================

## Назначение

Experiment Runner является первым исполнительным уровнем лаборатории.

Его задача состоит не в анализе эксперимента.

Его задача — выполнить эксперимент, сохранив всю цепочку происхождения данных.

---

## Онтологический принцип

Experiment Runner запускает эксперимент.

Он не интерпретирует.

Он не оценивает физическую корректность.

Он не делает научных выводов.

Он фиксирует факт выполнения лабораторного эксперимента.

---

## Положение в архитектуре

```text
Evidence Adapter

        │

        ▼

Experiment Runner

        │

        ▼

Experiment Run Record

        │

        ▼

Retention Analysis
```

---

## Ответственность

Experiment Runner обязан:

• принимать только валидированные потоки состояний;

• проверять архитектурные инварианты;

• регистрировать запуск эксперимента;

• сохранять происхождение данных;

• сохранять идентификаторы Evidence;

• сохранять порядок состояний;

• формировать неизменяемую запись эксперимента.

---

## Что компонент НЕ делает

Experiment Runner никогда не имеет права:

• вычислять физические модели;

• оценивать параметры среды;

• сглаживать сигналы;

• классифицировать происхождение;

• изменять Evidence;

• изменять State Stream;

• выполнять научную интерпретацию;

• принимать решения.

---

## Входы

Валидированные потоки состояний.

Текущая реализация:

RC_EVIDENCE_STATE_STREAM.

В дальнейшем:

Carbon State Stream

Electrolyte State Stream

Biological State Stream

---

## Выходы

Experiment Run Record.

Запись эксперимента содержит:

• исследуемую среду;

• список состояний;

• статистику Evidence;

• информацию о сохранении происхождения;

• статус выполнения эксперимента.

---

## Внутренние инварианты

Должны сохраняться всегда.

Evidence остаётся неизменным.

Происхождение сохраняется.

Experiment Runner не выполняет интерпретацию.

Порядок состояний сохраняется.

Любой запуск воспроизводим.

---

## Взаимодействие с другими компонентами

Experiment Runner принимает только валидированные результаты Adapter.

Дальнейшие уровни лаборатории получают исключительно Experiment Run Record.

---

## Научный смысл

Experiment Runner вводит принципиальное разделение между выполнением эксперимента и его научной интерпретацией.

Благодаря этому эксперимент становится воспроизводимым независимо от будущих физических моделей.

---

## Перспективы развития

В дальнейшем Experiment Runner может поддерживать:

• одновременный запуск нескольких сред;

• синхронизированные эксперименты;

• распределённое выполнение;

• воспроизведение экспериментов;

• серии параметрических прогонов;

• расписание лабораторных запусков;

• автоматическое ведение лабораторного журнала.

---

## Архитектурный вывод

Experiment Runner является исполнительной границей Difference Retention Laboratory.

Он превращает проверенный поток экспериментальных состояний в воспроизводимую запись лабораторного эксперимента, не вмешиваясь в научную интерпретацию результатов.

# END OF DOCUMENT
