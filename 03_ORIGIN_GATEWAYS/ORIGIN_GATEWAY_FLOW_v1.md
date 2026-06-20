# ORIGIN_GATEWAY_FLOW_v1

## Канонический поток

RAW DATA
↓
Origin Gateway
↓
ODF-labeled observation stream
↓
Environment Adapter
↓
Experiment Runner
↓
Environment
↓
Retention / Memory / Topology / Observer / Journal

## Главный инвариант

До прохождения через Origin Gateway данные не считаются лабораторными данными.

Они являются только внешним сырьём.

## Запрет

Environment Adapter не имеет права принимать raw data напрямую.

Любой Adapter обязан получать только поток с метками происхождения.