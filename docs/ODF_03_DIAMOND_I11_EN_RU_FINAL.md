# TIUMENTSEV_SINTEZ 1 — Difference Retention Lab
# ODF-03: Diamond Light Source I11 / Project M

**Study status:** Local reproducible structural/provenance test; reported PASS on 2026-10-22. Not independently audited.  
**Data DOI:** https://doi.org/10.5281/zenodo.7871450  
**Beamline:** Diamond Light Source I11, Mythen II detector.  
**Proposal:** EE15723-1.  
**Code:** `examples/run_odf03_diamond_i11.py`; existing `ODF_CORE_v0_1/src/odf_core_v0_1.py`.  
**Encoding:** UTF-8 without BOM.

## EN — Abstract

The ODF-03 test links two publicly released synchrotron powder-XRD profiles to their source workbook (`Asp` sheet) without flattening their experimental conditions into anonymous numeric arrays. The recorded condition values are `0` for `578412-mythen_summed.xye` and `0.1` for `578413-mythen_summed.xye`; the unit is not established by the inspected column header. `578401-mythen_summedSILICON640C.xye` is retained as an independently identified silicon standard, without claiming an established calibration relationship to the two Asp measurements.

This is an **audit of documented data relationships**, not a validation of new phases, a causal inference, a reconstruction of missing instrument logs, or a scientific endorsement by Diamond Light Source.

## EN — Inputs

Download directly from the data DOI (do not presume that redistribution under this repository is permitted):

| File | Size (bytes) | SHA-256 (local study baseline) |
|---|---:|---|
| `578401-mythen_summedSILICON640C.xye` | 730354 | `6D1806FC791FD162036735FBFA2679B445D25F5F5CC3A289AB346A729C16C2F8` |
| `578412-mythen_summed.xye` | 737267 | `12317867B92CE27D5A309212A8160ED543AF2BEBC7A7BB4914D96D59D6E7EF6E` |
| `578413-mythen_summed.xye` | 735346 | `EB54644F1E09363D35BDA5ECA06A1B2DAA71FEDA9AAD85FBFB9FE15A2BF3CA1D` |
| `ProjectM_DiffractionData.xlsx` | 103331 | `703E46C842BA3263180652065A3F6269B2947F85E30C6B80E546B9208A9E4695` |

The hashes are baselines recorded in this study, **not** independently cross-checked with Zenodo's published checksums.

## EN — Reproduction

Requirements: Python 3.10+ and `openpyxl` (`python -m pip install openpyxl`). The source ODF v0.1 core is required; this runner does not alter it.

```powershell
python examples/run_odf03_diamond_i11.py --data "PATH_TO_FOUR_INPUT_FILES" --core "PATH_TO_ODF_CORE_v0_1_SRC" --output "PATH_TO_NEW_OUTPUT_DIRECTORY"
```

The portable runner takes paths as arguments and does not rely on the original researcher's drive letters. Expected successful console messages: `INPUT_SHA256`, `XYE_FULL_GRIDS`, `NEGATIVE_CONTROL_INTERIOR_GRID`, `EXCEL_ASP_REFERENCES`, `NEGATIVE_CONTROL_BROKEN_FILENAME`, `ODF_CORE_ORIGIN_CHECK`, then `ODF03: PASS`. Outputs: `odf03_event.json`, `odf03_event.md`, `odf03_graph.json`, `odf03_manifest.json`.

**Reported local result:** 4/4 hash matches against study baseline; full comparison of 22,508 angle coordinates between the two Asp XYE files; 2/2 exact Excel filename matches; successful detection of an in-memory interior grid perturbation and an in-memory broken filename reference; ODF required-field `origin_check()` PASS. Negative checks are implemented in the runner, **not** in the core `origin_check()` function. The portable variant was executed successfully on the local Diamond I11 dataset on 2026-10-22 using explicit `--data`, `--core`, and `--output` paths. Cross-machine independent reproduction remains unverified.

## EN — Scope and limitations

- An exact data reference and recorded condition difference do not establish causal response or material phase change.
- There is no established direct silicon-to-Asp calibration linkage in this study.
- Angle-grid identity does not verify instrument calibration or experimental chronology.
- The XYE files are processed profiles, not full raw detector/event histories.
- Data license and permission to redistribute original files must be checked at the source; this repository should initially publish code, manifests, audit outputs, and DOI pointers, not copies of source diffraction data.
- An external laboratory audit and operational beamline pilot remain future steps.

---

## RU — Аннотация

ODF-03 связывает два открытых дифракционных профиля, полученных на синхротроне, с исходной таблицей (`Asp`) без сведения условий эксперимента к анонимным числовым массивам. В таблице указаны значения условия `0` для `578412-mythen_summed.xye` и `0,1` для `578413-mythen_summed.xye`. Единица измерения этого параметра по просмотренному заголовку не установлена. Файл `578401-mythen_summedSILICON640C.xye` удерживается как отдельно обозначенный кремниевый стандарт; непосредственная калибровочная связь с измерениями Asp не утверждается.

Это **аудит документированных отношений происхождения данных**, а не доказательство новой фазы, причинного механизма, восстановление отсутствующего журнала установки или экспертиза Diamond Light Source.

## RU — Исходники

Четыре исходных файла перечислены в англоязычной таблице выше с точными именами, размерами и SHA-256. Скачивать по DOI https://doi.org/10.5281/zenodo.7871450. Контрольные суммы фиксируют локальный исходный набор; соответствие опубликованным контрольным суммам Zenodo отдельно не проверялось.

## RU — Воспроизведение

Нужны Python 3.10+, `openpyxl` и существующее ядро `ODF_CORE_v0_1/src/odf_core_v0_1.py`. Установка библиотеки:

```powershell
python -m pip install openpyxl
```

Команда для запуска:

```powershell
python examples/run_odf03_diamond_i11.py --data "КАТАЛОГ_ЧЕТЫРЁХ_ФАЙЛОВ" --core "КАТАЛОГ_SRC_ЯДРА_ODF" --output "НОВЫЙ_КАТАЛОГ_РЕЗУЛЬТАТОВ"
```

Ожидаемые сообщения: `INPUT_SHA256`, `XYE_FULL_GRIDS`, `NEGATIVE_CONTROL_INTERIOR_GRID`, `EXCEL_ASP_REFERENCES`, `NEGATIVE_CONTROL_BROKEN_FILENAME`, `ODF_CORE_ORIGIN_CHECK`, затем `ODF03: PASS`. Создаются `odf03_event.json`, `odf03_event.md`, `odf03_graph.json` и `odf03_manifest.json`.

**Фактически полученный результат локального прогона v1.1 (22.10.2026):** 4/4 локальных SHA-256; совпадение всех 22 508 угловых координат для пары Asp; 2/2 связей с Excel; обнаружение искусственной порчи внутренней координаты и имени файла в оперативной памяти; встроенный `origin_check()` — PASS по обязательным полям.

Отрицательные контроли проверяются **внешним runner**, а не автоматически встроенным `origin_check()`. Переносимый runner успешно выполнен на локальном наборе Diamond I11 22.10.2026 с явными параметрами `--data`, `--core`, `--output`. Независимое воспроизведение на другой машине пока не проводилось.

## RU — Границы результата

- Нельзя выводить физическую причинность или новую фазу только из различий в профилях и значениях таблицы.
- Калибровочная связь отдельного кремниевого стандарта с парой Asp не установлена.
- Совпадение угловых сеток не доказывает калибровку прибора и не восстанавливает хронологию действий оператора.
- `.xye` — обработанные профили, а не полный поток исходных событий детектора.
- До публикации самих экспериментальных файлов нужно проверить лицензию и условия перераспространения. Без этого в GitHub размещать только код, результаты аудита, манифест и DOI исходного набора.
- Независимая внешняя экспертиза и эксплуатационный пилот на линии синхротрона ещё не проведены.
