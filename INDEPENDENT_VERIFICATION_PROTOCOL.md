# TIUMENTSEV_SINTEZ 1 — Difference Retention Lab
# INDEPENDENT VERIFICATION PROTOCOL

**Version:** 1.0 (proposed public research protocol)  
**Date:** 2026-10-24  
**Status:** Open invitation to independent replication; not a certification of ODF advantage  
**Repository:** https://github.com/andy6011960/difference-retention-lab  
**License:** Consult the repository's LICENSE file (reported as Apache-2.0); this protocol does not alter software-license permissions.  
**Scope:** Scientific data/process provenance, retention of differences, experimental replay, and cross-system attribution.  

## 1. Purpose

Difference Retention Lab (DRL) invites synchrotron facilities, beamline scientists, data-stewardship groups, and independent researchers to test whether an Origin/Difference/Formation (ODF) representation provides **measurable, reproducible benefits** over competent conventional approaches to scientific event logging, provenance storage, and replay.

The research question is **not** whether ODF can store files or event sequences. Ordinary databases and provenance logs already do that. The question is whether a particular ODF representation improves the preservation and reconstruction of *why* a measurement or intervention occurred, which distinctions were operational at that time, how decisions depended on preceding observations, and what remains unresolved — under an equivalent evidence and indexing contract.

Independent results, including failures and null results, are welcome. Participation and feedback are voluntary. No private beamline data must be disclosed to the project maintainers.

## 2. Evidence status and boundaries

Existing internal exploratory exercises have demonstrated selected operations such as graph/trace ingestion, round-trip reconstruction, and externally audited attribution. They **have not established general superiority** over indexed event logs, hash-linked adjacency stores, or databases with equivalent provenance guarantees. Synthetic branching, merging, or newly marked entities are not evidence of scientific emergence. An ODF `PASS` for a structural check does not establish truth, scientific novelty, research efficiency, or accuracy of an attributed statement.

This protocol is a **proposed external evaluation design**, not a claim that all described experiments, adapters, or commands are already implemented in this repository. Use the scripts and documentation actually present at the commit under test; record missing functions as **NOT AVAILABLE / NOT TESTED**, rather than substituting undocumented behavior.

## 3. Participation and independent operation

Researchers may clone, inspect, adapt, execute, and assess the published materials under the applicable repository license. Collaboration, reporting, and acknowledgment beyond applicable legal and scholarly obligations are **not conditions of running the code**.

Possible modes:

- **Independent:** execute and retain all results locally; publication or sharing is optional.
- **Voluntary report:** share a sanitized test manifest, metrics, and redacted failure traces using a GitHub Issue, Discussion (if enabled), or the contact channel listed in the repository.
- **Joint study:** agree separately, in writing, on scope, access, confidentiality, authorship, and publication before exchanging nonpublic data.

Do not submit confidential raw scans, personal data, credentials, proprietary sample descriptions, access tokens, or export-controlled details to public issues. A reproducible synthetic/minimized example is preferred when safe.

## 4. Before testing: freeze the experiment

Record **before looking at outcome metrics**:

1. Repository URL, exact commit SHA, branch/tag, modified files, and diff or patch hash.
2. Experiment identifier; UTC timestamps; host, CPU, RAM, OS, Python/runtime and dependency versions.
3. Dataset identifier, licensing/access level, checksum of each input, units, and data schema.
4. Whether datasets are real, simulated, transformed from real observations, or mixed; distinguish each segment.
5. Exact research question, primary outcome, secondary outcomes, predefined success criterion, and exclusions.
6. All procedures for ODF and comparators, including schema, indexes, caching, compression, batching, and concurrency.
7. Human involvement, intervention logs, prompt/version/provider information for any LLM-assisted stage, and known randomness sources.
8. Planned sample size, repetitions, and method for computing intervals or uncertainty.

Never publish a checksum in place of a full description of what the checksum covers. A dataset hash proves byte identity relative to the supplied artifact; it does not prove data quality or provenance by itself.

## 5. Experimental tracks

### Track A — Structural integrity and faithful replay

**Input:** a sequence of observations, configuration changes, scientific decisions, corrections, and intentionally unresolved interpretations. Include at least one branch, one revision/supersession, and one interrupted operation when available.  
**Task:** ingest and reconstruct an event, its preceding conditions, affected entities, stated rationale, sources, and unresolved alternatives.  
**Check:** compare reconstructed records with independently retained ground truth. Report missing, added, reordered, and misattributed relationships separately. Evaluate exact-text reconstruction only when text preservation was explicitly part of the contract.

### Track B — Beamline experimental decision context

**Input:** authorized beamline or laboratory history, such as instrument setup, acquisition metadata, calibration events, scan triggers, sample/environment states, quality flags, and operator/scientist decisions.  
**Task:** recover why a particular acquisition was initiated or changed, and what observations justified or contradicted the decision.  
**Check:** independent reviewers assess answer correctness and evidence traceability against source logs. Report **UNKNOWN** where the rationale was never recorded; neither ODF nor comparators should manufacture it.

### Track C — Long-horizon reconstruction and transfer

**Input:** time-separated experiment sessions, changed personnel or environment, and a deliberately interrupted analysis.  
**Task:** resume work using a retained record only; recover the last justified state, open tensions, and provenance of new actions.  
**Check:** compare error rate, omitted constraints, reconstruction time, and subjective review workload on the same test items. Separate machine-only replay from LLM-assisted reconstruction.

### Track D — Attribution and multi-agent research traces (optional)

**Input:** immutable speaker/action logs and a derived narrative that includes at least one *known* incorrect role attribution, plus controls with correct attribution and missing evidence.  
**Task:** preserve the narrative exactly, then determine whether a separate provenance-audit procedure identifies statements whose claimed speaker lacks corresponding recorded acts.  
**Check:** report false positives/negatives and the distinctions **confirmed**, **contradicted**, **unsupported by available records**, and **not assessable**. Do not equate absence of evidence with proof of falsehood, nor source verification with scientific truth. Report native ODF-Core checks separately from external validators.

### Track E — Cost and scaling

**Input:** progressively larger realistic histories with fixed schema complexity, plus an explicitly described synthetic stress set if desired.  
**Task:** ingest, query, replay, traverse branches/merges, and verify origins.  
**Check:** cold/warm latency, CPU time, peak memory, storage size, query completeness, indexing time, and failure rate. Distinguish transfer cost from provenance-query performance. Report correctness before speed.

## 6. Fair comparators

At minimum, evaluate ODF against one **competent, indexed, provenance-preserving baseline**, not merely a plain text file. Depending on the track, suitable baselines include:

- an indexed event log with immutable event identifiers and source links;
- a relational store (e.g., SQLite) with equivalent schemas and indexes;
- a hash-linked or content-addressed graph/adjacency representation with equivalent version history.

Hold the **information contract** constant: both sides must preserve all information needed for the target query. Record when ODF and the comparator use different indexing, compression, caching, precomputation, or deduplication. An advantage arising solely from a richer input record is not evidence of a superior representation.

## 7. Measures and reporting

For every track, report numerator/denominator and the precise denominator definition, not just `PASS`:

| Dimension | Suggested measure | Interpretation limit |
|---|---|---|
| Retention | Required fields and relations recovered / required fields and relations | Depends on documented ground truth |
| Provenance | Correct source/actor/transition links / evaluated links | Does not prove content is true |
| Unresolved distinctions | Open questions retained without being silently marked solved | Requires prespecified adjudication |
| Replay | Correctly reconstructed steps / tested steps | A faithful replay may reproduce an error |
| Detection | Precision/recall of explicit attribution audit | Must distinguish native checks from external audit |
| Efficiency | Median and tail latency, memory, storage, CPU | Equivalent workloads and hardware required |
| Human effort | Review/correction time and error count | Blind or randomized assessment preferred |

Use multiple runs, report spread or confidence intervals where meaningful, and preserve failures. For LLM-enabled comparisons, hold source evidence and task wording constant, randomize ordering when practical, and record model/provider/version, sampling settings, tool access, and retries. A single generative response cannot establish an ODF-specific improvement.

## 8. Minimum reproducible submission

A voluntary report should contain:

```text
verification_report/
  README.md                 # objective, conclusions, limitations
  manifest.json             # hashes, versions, environment, track, settings
  methods.md                # exact commands or reproducible procedure
  results.csv               # per-trial metrics, including unsuccessful trials
  evidence_map.csv          # claimed result -> source-event IDs / file refs
  failures.md               # null results, exclusions, protocol deviations
  synthetic_example/        # optional sanitized input and expected outputs
```

The file names above define a **suggested reporting package**, not guaranteed files or implemented commands in the repository. Where release instructions are absent, quote the actual steps taken and open an issue describing the missing entry point. Do not fill gaps by guessing API names.

Suggested `manifest.json` fields:

```json
{
  "protocol_version": "1.0",
  "experiment_id": "facility-local-example",
  "repository": "https://github.com/andy6011960/difference-retention-lab",
  "commit_sha": "REPLACE_WITH_REAL_SHA",
  "track": "A",
  "dataset_kind": "real|synthetic|mixed",
  "input_checksums": [],
  "comparator": "describe_actual_baseline",
  "information_contract": "describe_equal_requirements",
  "environment": {},
  "outcome_status": "PASS|FAIL|INCONCLUSIVE|NOT_TESTED",
  "limitations": []
}
```

## 9. Scientific interpretation and claim discipline

- **Verified functionality:** repeatably observed in an identified version and test setting.
- **Candidate advantage:** better result in a documented setting with equivalent controls; requires replication.
- **Open identification bridge:** a proposed link between ODF representation and a broader scientific or mathematical interpretation, not established correspondence.
- **Not tested:** no execution or inadequate independent evidence.
- **Negative/null result:** a valuable outcome; preserve and publish when possible.

Distinguish preservation of statements from warranted scientific conclusions. A stored citation, declared author, or generated narrative is evidence that a claim was recorded, **not** that its content or attribution has been verified. Emergence or a new scientific discovery requires independent criteria beyond adding a graph node or labeling a transition.

## 10. Research ethics and data governance

Comply with facility rules, applicable laws, data-use agreements, authorship policies, and security requirements. Do not make public uploads of sensitive research or user records. Document anonymization limits; pseudonymized event IDs may still be linkable to individuals. Keep any optional LLM service out of restricted data paths unless the facility has explicitly authorized such processing. Prefer local, verifiable comparison where needed.

Apache-2.0, if applicable to the tested files, permits extensive independent use subject to license conditions; this research invitation does not add mandatory telemetry, reporting, contact, joint-publication, or contribution requirements. Voluntary cooperation is separate from license compliance. Discuss academic credit, shared authorship, confidentiality, and intellectual-property allocations in advance for joint projects.

## 11. Invitation

We welcome critical replication, failed tests, cases where conventional approaches outperform ODF, and proposals for better controls. The immediate objective is to determine **where ODF is genuinely useful, where it is equivalent, and where it fails**. A reproducible negative result is as important as a positive one.

---

# TIUMENTSEV_SINTEZ 1 — Лаборатория удержания различий
# ПРОТОКОЛ НЕЗАВИСИМОЙ ВЕРИФИКАЦИИ

**Версия:** 1.0 (проект открытого исследовательского протокола)  
**Дата:** 24.10.2026  
**Статус:** приглашение к независимым испытаниям; не свидетельство преимущества ODF  
**Репозиторий:** https://github.com/andy6011960/difference-retention-lab  
**Лицензия:** точные условия — в LICENSE репозитория (пользователь указал Apache-2.0); этот протокол не изменяет лицензию программы.  
**Предмет:** научные данные и происхождение процессов, удержание различий, восстановление экспериментов, атрибуция в ассамбляжах.  

## 1. Назначение

Difference Retention Lab (DRL) предлагает синхротронным центрам, исследователям экспериментальных станций, специалистам по научным данным и независимым лабораториям проверить, даёт ли представление Origin/Difference/Formation (ODF) **воспроизводимые измеримые преимущества** по сравнению с корректными классическими средствами журналирования, хранения provenance и восстановления эксперимента.

Проверяется **не** возможность сохранить файл или последовательность событий — это давно решается существующими системами. Проверяется возможность удержать и восстановить *почему* измерение было проведено в конкретный момент, какие различения определяли выбор действия, какие наблюдения ему предшествовали, что осталось неразрешённым и как исследование продолжалось; причём контрольные системы должны получать равнозначные сведения и индексы.

Приветствуются отрицательные результаты и отсутствие преимуществ. Передача отчётов добровольна. Лаборатории не обязаны раскрывать исходные конфиденциальные данные.

## 2. Текущий статус доказательств

Внутренние исследовательские прогоны показали некоторые возможности передачи графов и следов, точного восстановления записей и выявления ошибки атрибуции **внешним** аудитом. Однако они **не доказали общего преимущества** ODF перед индексированными журналами событий, хеш-связанными графами и базами данных с равными требованиями к provenance. Синтетическая ветвь или маркировка «новой целостности» не свидетельствует о научной эмерджентности. Структурное `PASS` не подтверждает научную истинность, новизну, корректность авторства или экономию ресурсов.

Этот документ — **протокол будущего внешнего испытания**, а не утверждение, что все перечисленные адаптеры, тесты и команды уже реализованы в репозитории. Использовать фактически опубликованные на проверяемом коммите инструкции. Отсутствующую функцию отмечать **NOT AVAILABLE / NOT TESTED**, не подменяя догадкой.

## 3. Форматы участия

Код допускается применять самостоятельно в пределах лицензии. Сообщение результатов и совместное авторство **не являются обязательным условием** использования.

- **Независимо:** запускать и хранить результаты у себя; отчёт по желанию.
- **Добровольный отчёт:** предоставить обезличенные метрики, описание прогона и безопасно сокращённые примеры через GitHub Issues, Discussions (если доступны) или контактный канал репозитория.
- **Совместный пилот:** заранее письменно согласовать доступ к данным, конфиденциальность, объём работ, авторство, публикацию и права на результаты.

Нельзя выкладывать в открытые Issues секретные данные, токены, персональные сведения, закрытые данные установок и образцов. При возможности использовать небольшой обезличенный воспроизводимый пример.

## 4. Предварительная фиксация эксперимента

**До просмотра результатов** зарегистрировать:

1. URL репозитория, точный SHA коммита, ветку/релиз, модификации и их контрольные суммы.
2. ID эксперимента, временные метки UTC, ОС, процессор, ОЗУ, версии Python и библиотек.
3. Идентификатор набора данных, права доступа, хеши входных файлов, единицы измерения и схему.
4. Происхождение данных: реальные, синтетические, преобразованные реальные либо смешанные; смешанные фрагменты пометить отдельно.
5. Проверяемую гипотезу, первичную метрику, вспомогательные метрики, порог успешности и исключения.
6. Настройки ODF и контролей: схема, индексы, кеши, сжатие, пакеты, параллелизм.
7. Вмешательства человека и журналы решений; для LLM — провайдера, модель, настройки и рандомизацию.
8. Число повторов и метод оценки разброса/неопределённости.

Хеш подтверждает тождество байтов указанного файла; сам по себе он не подтверждает научную корректность содержания или происхождения.

## 5. Исследовательские направления

### A — Целостность структуры и точное восстановление

**Вход:** наблюдения, изменения условий, решения, исправления и неразрешённые интерпретации. Желательно включить ветвление, пересмотр/замещение и прерванный этап.  
**Задача:** восстановить событие, исходные условия, затронутые сущности, основание решения, источники и альтернативы.  
**Проверка:** сравнить с независимо удерживаемым эталоном. По отдельности учитывать утраченные, добавленные, переставленные и ошибочно атрибутированные отношения. Побайтовое/текстовое совпадение проверять только там, где оно предусмотрено договором сохранения.

### B — Контекст решений на синхротронной станции

**Вход:** разрешённая история установки: конфигурация, метаданные измерения, калибровка, триггеры сканов, состояния образца и среды, метки качества и решения оператора.  
**Задача:** восстановить, почему конкретный сбор данных был начат, изменён либо остановлен и какие наблюдения подтверждали или оспаривали решение.  
**Проверка:** независимая оценка правильности и прослеживаемости ответа по исходным журналам. Если причина не записывалась, ответ **UNKNOWN**: ни ODF, ни сравниваемая система не вправе её выдумывать.

### C — Долгосрочное восстановление и перенос работы

**Вход:** разнесённые во времени сессии, смена персонала/условий, намеренно прерванный анализ.  
**Задача:** возобновить исследование только по сохранённой записи; определить последний обоснованный шаг, открытые напряжения, происхождение новых действий.  
**Проверка:** потери ограничений, ошибки, время восстановления и трудозатраты проверки на одинаковых задачах. Машинное восстановление и генеративный анализ оценивать раздельно.

### D — Атрибуция и следы взаимодействия когнитивных контуров (дополнительно)

**Вход:** неизменяемый журнал реальных реплик/действий и производное изложение с заранее известной ошибочной атрибуцией роли, плюс корректные и неопределённые контрольные случаи.  
**Задача:** точно сохранить изложение и отдельно проверить, существует ли зарегистрированный акт указанного участника.  
**Проверка:** ложные срабатывания и пропуски; различать **подтверждено**, **опровергнуто**, **не подтверждено доступным журналом**, **не поддаётся оценке**. Отсутствие свидетельства — не доказательство ложности; подтверждение автора — не доказательство истинности утверждения. Проверку ядра ODF и результат внешнего аудитора приводить отдельно.

### E — Ресурсы и масштабирование

**Вход:** растущие объёмы реалистичных историй; отдельно — документированный синтетический стресс-набор.  
**Задача:** загрузка, запросы, восстановление, обход ветвей/слияний, проверка происхождения.  
**Проверка:** холодная/тёплая задержка, время CPU, пик памяти, размер хранилища, полнота ответов, индексация, ошибки. Стоимость передачи данных и запросов provenance измерять отдельно. Корректность первична по отношению к скорости.

## 6. Равноправные контрольные решения

Минимально нужен хотя бы один **полноценный индексированный контроль с сохранением provenance**, а не просто текстовый файл. Возможные варианты:

- индексированный журнал событий с неизменяемыми ID и ссылками на источники;
- реляционная база (например, SQLite) с эквивалентной схемой и индексами;
- хеш-связанный/content-addressed граф с равноценным версионированием.

Для ODF и контрольной системы требуется **один информационный контракт**: обе получают все данные для целевых запросов. Если меняются индексы, сжатие, предварительные вычисления, кеширование либо дедупликация, это явно отмечается. Выигрыш от более богатого входного набора не доказывает преимущество способа представления.

## 7. Метрики и интерпретация

В каждом случае публиковать числитель и знаменатель, а не только `PASS`:

| Характеристика | Метрика | Ограничение |
|---|---|---|
| Удержание | Восстановленные обязательные поля и связи / эталонные | Нужен независимый эталон |
| Provenance | Верные ссылки на источник, актора и переход / проверенные ссылки | Не подтверждает истинность содержания |
| Открытые различения | Сохранённые неразрешённые вопросы, не объявленные разрешёнными | Требуется независимый критерий |
| Replay | Корректно восстановленные шаги / проверенные шаги | Можно точно восстановить ошибку |
| Атрибуция | Precision/recall явно указанного аудитора | Не смешивать проверки ядра и внешнего кода |
| Ресурсы | Медиана и хвост задержек, память, объём, CPU | Равные данные и оборудование |
| Человеческий труд | Время и количество исправлений | Желательна слепая/рандомизированная оценка |

Проводить повторные прогоны, сообщать разброс и интервалы неопределённости. Для LLM обеспечить одинаковые первичные свидетельства и формулировки задач; фиксировать модель, провайдера, настройки генерации, доступ к инструментам и повторы. Единичный ответ LLM не доказывает улучшения именно благодаря ODF.

## 8. Минимальный отчёт

Предлагаемая структура добровольного пакета:

```text
verification_report/
  README.md                 # задача, выводы и ограничения
  manifest.json             # версии, хеши, параметры
  methods.md                # реальные команды и процедура
  results.csv               # все повторы, включая неудачные
  evidence_map.csv          # утверждения -> ID исходных событий
  failures.md               # отрицательные результаты и отклонения
  synthetic_example/        # необязательный безопасный пример
```

Имена выше — **предложенный формат отчётности**, а не заявка на наличие таких файлов и команд в коде репозитория. Если опубликованный интерфейс отсутствует, так и указывать. Не придумывать API или CLI.

Образец `manifest.json` приведён в английском разделе; значения `REPLACE_WITH_REAL_SHA` и другие шаблоны должны быть заменены реальными данными, а не публиковаться как результат измерения.

## 9. Дисциплина выводов

- **Проверенная функция:** многократно воспроизведённый результат конкретной версии и условий.
- **Кандидат на преимущество:** выигрыш над равноправным контролем, требующий дальнейшей репликации.
- **Открытый мост идентификации:** предполагаемая связь онтологического представления и внешнего научного аппарата, пока не доказанная.
- **Не проверено:** нет исполнения или независимых свидетельств.
- **Нулевой/отрицательный результат:** полноценный научный результат, подлежащий сохранению.

Хранение утверждения не равно подтверждению его истинности. Указанное авторство и сохранённый ответ генеративной модели ещё не свидетельствуют о фактической позиции человека. Возникновение новой научной целостности требует самостоятельных критериев; новый узел или маркер графа этого не устанавливает.

## 10. Этика и управление данными

Соблюдать правила учреждения, закон, ограничения использования данных, требования безопасности и научного авторства. Не загружать конфиденциальные исследования, личные данные и ключи доступа в публичные сервисы. Учитывать, что псевдонимизация не всегда исключает повторную идентификацию людей. Не отправлять ограниченные данные внешней LLM без явно разрешённой процедуры.

Если к проверяемому коду применяется Apache-2.0, лицензия допускает широкое самостоятельное использование при соблюдении её условий. Этот протокол **не вводит** обязательную телеметрию, отчётность, контакт, совместное авторство или передачу изменений. Договорённости о совместном пилоте оформляются отдельно.

## 11. Приглашение

Мы приветствуем независимые воспроизведения, неудачи, случаи преимущества классического контроля и предложения более строгих экспериментов. Непосредственная цель — установить, **где ODF действительно полезен, где эквивалентен известным средствам, а где недостаточен**. Отрицательный воспроизводимый результат не менее ценен, чем положительный.
