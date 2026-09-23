# 10: Углубление сервисного слоя storage.py и устранение запахов кода

**What to build:**
Устранить выявленные при ревью запахи кода по Фаулеру (*Duplicated Code*, *Feature Envy*, *Primitive Obsession*, *Divergent Change*) в `server.py` в соответствии с принципами deep modules (`/codebase-design`).
1. Перенести функцию `generate_milestones_for_task` из `server.py` в `services/storage.py` (или специализированный `services/tasks.py`), инкапсулировав бизнес-правила создания контрольных точек.
2. Реализовать в `Storage` метод агрегации прогресса `get_task_progress(task_id: str) -> dict`, возвращающий `{ total, completed, percentage, earned_xp }`, устранив дублирование вычислений в строках 190-196 и 388-394 `server.py`.
3. Реализовать методы доменной агрегации данных для кабинета бизнеса и кабинета студента внутри сервисного слоя, избавив эндпоинты `server.py` от ручной переборки чужих словарей и внешних ключей.
4. Ввести Pydantic/dataclass-модель `Milestone` для структурирования этапов.

**Blocked by:** 07: Защита от сгорания XP при подтверждении этапа без команды

**Status:** open

- [ ] Написать модульные тесты в `tests/test_ui_components.py` или `tests/test_storage.py` на методы расчета прогресса и генерации этапов в `services/storage.py`.
- [ ] Перенести `generate_milestones_for_task` и агрегацию этапов в `services/storage.py`.
- [ ] Устранить дублирование подсчета прогресса в `server.py` через вызов метода хранилища.
- [ ] Очистить функции `get_business_cabinet_data` и `get_student_cabinet_data` от Feature Envy.
- [ ] Проверить, что все существующие тесты остаются зелеными (`./venv/bin/pytest tests/`).
- [ ] В коде строго 0 эмодзи.
