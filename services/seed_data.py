from typing import List, Dict, Any

def get_initial_drafts() -> List[Dict[str, Any]]:
    return [
        {
            "id": "draft-001",
            "raw_text": "Нужен умный чат-бот для поддержки клиентов интернет-магазина электроники, чтобы разгрузить операторов в пиковые часы.",
            "industry": "Ритейл и e-commerce",
            "task_type": "Диалоговый AI и чат-боты",
            "created_at": "2026-09-20T10:00:00"
        },
        {
            "id": "draft-002",
            "raw_text": "Хотим предиктивную модель для оценки риска невозврата микрокредитов на основе выписок и истории транзакций.",
            "industry": "Финтех и банкинг",
            "task_type": "Data Science и предиктивная аналитика",
            "created_at": "2026-09-20T11:30:00"
        },
        {
            "id": "draft-003",
            "raw_text": "Необходим сервис для автоматической проверки студенческих эссе и выдачи развернутых рекомендаций по улучшению структуры.",
            "industry": "EdTech и образование",
            "task_type": "Диалоговый AI и чат-боты",
            "created_at": "2026-09-21T09:15:00"
        },
        {
            "id": "draft-004",
            "raw_text": "Требуется оптимизировать маршруты курьеров по городу с учетом временных окон клиентов и текущей загруженности дорог.",
            "industry": "Логистика и доставка",
            "task_type": "Автоматизация бизнес-процессов",
            "created_at": "2026-09-21T14:40:00"
        },
        {
            "id": "draft-005",
            "raw_text": "Ищем решение для интеллектуальной классификации обращений пациентов поликлиники и автоматического распределения по врачам.",
            "industry": "Здравоохранение и медицина",
            "task_type": "Автоматизация бизнес-процессов",
            "created_at": "2026-09-22T16:20:00"
        }
    ]

def get_initial_tasks() -> List[Dict[str, Any]]:
    return [
        {
            "id": "task-001",
            "title": "Интеллектуальный ассистент клиентской поддержки интернет-магазина",
            "industry": "Ритейл и e-commerce",
            "task_type": "Диалоговый AI и чат-боты",
            "context_need": "Интернет-магазин электроники получает более 1200 однотипных обращений в день о статусе заказов, возвратах и характеристиках товаров. Операторы перегружены, время первого ответа выросло до 28 минут.",
            "data_materials": "Выгрузка 25 000 обезличенных диалогов в формате JSONL, база знаний FAQ из 450 статей, каталог товаров с характеристиками в формате CSV.",
            "expected_result": "Работающий микросервис чат-бота с интеграцией в Telegram и веб-виджет, классификатором интентов и возможностью перевода сложного диалога на оператора.",
            "success_criteria": "Автоматическое разрешение не менее 65% типовых обращений без участия человека; точность классификации интентов не ниже 88%; среднее время ответа до 2 секунд.",
            "constraints": "Срок разработки 4 недели; язык Python (FastAPI); упаковка в Docker-контейнер; соответствие 152-ФЗ по персональным данным.",
            "target_users": "Покупатели интернет-магазина и дежурные специалисты первой линии технической поддержки.",
            "business_contact": "CTO Алексей Смирнов (alexey@retail-tech.kz, Telegram: @alex_retail), еженедельные онлайн-синки по вторникам в 15:00.",
            "rating": 95,
            "readiness_level": "Приоритетная",
            "rating_breakdown": {
                "context_need": 20,
                "data_materials": 20,
                "expected_result": 15,
                "success_criteria": 15,
                "constraints": 10,
                "target_users": 10,
                "business_contact": 10
            },
            "missing_fields": [],
            "published": True,
            "created_at": "2026-09-20T12:00:00",
            "updated_at": "2026-09-20T12:00:00"
        },
        {
            "id": "task-002",
            "title": "Предиктивная модель кредитного скоринга малого бизнеса",
            "industry": "Финтех и банкинг",
            "task_type": "Data Science и предиктивная аналитика",
            "context_need": "Финтех-компания выдает оборотные кредиты малому бизнесу. Текущая ручная андеррайтинговая проверка занимает до 3 дней, что приводит к отказу клиентов в пользу конкурентов.",
            "data_materials": "Агрегированные данные 10 000 кредитных историй за 3 года, транзакционная активность и финансовая отчетность компаний в Parquet.",
            "expected_result": "Модель бинарной классификации дефолта с API для расчета кредитного рейтинга заемщика в режиме реального времени.",
            "success_criteria": "Метрика ROC-AUC не ниже 0.78 на тестовой выборке; время ответа API скоринга до 800 мс.",
            "constraints": "Стек Python (CatBoost / LightGBM, FastAPI); воспроизводимый пайплайн обучения с DVC; срок 4 недели.",
            "target_users": "Риск-менеджеры, кредитные аналитики и клиенты сервиса через моментальную форму.",
            "business_contact": "Руководитель аналитики Данияр Алиев (daniyar@finscore.kz, Telegram: @daniyar_fin), встречи раз в неделю.",
            "rating": 85,
            "readiness_level": "Готовая",
            "rating_breakdown": {
                "context_need": 20,
                "data_materials": 20,
                "expected_result": 15,
                "success_criteria": 15,
                "constraints": 10,
                "target_users": 10,
                "business_contact": 10
            },
            "missing_fields": [],
            "published": True,
            "created_at": "2026-09-20T14:30:00",
            "updated_at": "2026-09-20T14:30:00"
        },
        {
            "id": "task-003",
            "title": "Сервис автоматической аналитики вовлеченности студентов",
            "industry": "EdTech и образование",
            "task_type": "Data Science и предиктивная аналитика",
            "context_need": "Онлайн-академия обучает более 3000 студентов. Около 30% бросают обучение на 3-4 неделе из-за потери мотивации, но кураторы узнают об этом слишком поздно.",
            "data_materials": "Логи активности студентов в LMS за 6 потоков (просмотры лекций, сдача домашних заданий, паузы).",
            "expected_result": "Дашборд для кураторов с индикатором риска оттока студента и рекомендациями по персонализированному контакту.",
            "success_criteria": "Заблаговременное выявление признаков оттока не менее чем за 5 дней до прекращения активности.",
            "constraints": "Разработка на Python/Streamlit или React; срок 3 недели.",
            "target_users": "Кураторы учебных групп и методисты курсов.",
            "business_contact": "Лид продукта Асель Мусина (asel@edutrack.kz), консультации в Telegram.",
            "rating": 65,
            "readiness_level": "Рабочая",
            "rating_breakdown": {
                "context_need": 20,
                "data_materials": 10,
                "expected_result": 15,
                "success_criteria": 8,
                "constraints": 5,
                "target_users": 5,
                "business_contact": 5
            },
            "missing_fields": ["data_materials", "success_criteria", "constraints", "target_users", "business_contact"],
            "published": True,
            "created_at": "2026-09-21T10:00:00",
            "updated_at": "2026-09-21T10:00:00"
        },
        {
            "id": "task-004",
            "title": "Оптимизация маршрутов экспресс-доставки последней мили",
            "industry": "Логистика и доставка",
            "task_type": "Автоматизация бизнес-процессов",
            "context_need": "Служба доставки сталкивается с опозданиями курьеров в часы пик из-за ручного распределения заказов диспетчерами.",
            "data_materials": "Исторические GPS-треки курьеров за месяц и адреса доставок в CSV.",
            "expected_result": "Алгоритм построения динамических маршрутов с минимизацией совокупного пробега.",
            "success_criteria": "Сокращение среднего опоздания курьеров на 25%.",
            "constraints": "Реализация на Python или Go; срок 4 недели.",
            "target_users": "Диспетчеры логистического хаба и пешие/автокурьеры.",
            "business_contact": "Диспетчерский отдел (logistics@speedy.kz).",
            "rating": 55,
            "readiness_level": "Рабочая",
            "rating_breakdown": {
                "context_need": 20,
                "data_materials": 10,
                "expected_result": 15,
                "success_criteria": 8,
                "constraints": 5,
                "target_users": 5,
                "business_contact": 5
            },
            "missing_fields": ["data_materials", "success_criteria", "constraints", "target_users", "business_contact"],
            "published": True,
            "created_at": "2026-09-21T15:00:00",
            "updated_at": "2026-09-21T15:00:00"
        },
        {
            "id": "task-005",
            "title": "Автоматическая маршрутизация пациентов поликлиники",
            "industry": "Здравоохранение и медицина",
            "task_type": "Автоматизация бизнес-процессов",
            "context_need": "В регистратуре скапливаются очереди из-за долгого опроса симптомов и выбора нужного специалиста.",
            "data_materials": "Примеры 200 типовых текстовых жалоб пациентов.",
            "expected_result": "Прототип опросника в терминале самозаписи.",
            "success_criteria": "Ускорение записи.",
            "constraints": "Срок 2 недели.",
            "target_users": "Пациенты.",
            "business_contact": "Регистратура поликлиники.",
            "rating": 30,
            "readiness_level": "Черновик",
            "rating_breakdown": {
                "context_need": 10,
                "data_materials": 5,
                "expected_result": 8,
                "success_criteria": 4,
                "constraints": 3,
                "target_users": 3,
                "business_contact": 3
            },
            "missing_fields": ["context_need", "data_materials", "expected_result", "success_criteria", "constraints", "target_users", "business_contact"],
            "published": True,
            "created_at": "2026-09-22T17:00:00",
            "updated_at": "2026-09-22T17:00:00"
        }
    ]

def get_initial_teams() -> List[Dict[str, Any]]:
    return [
        {
            "id": "team-001",
            "name": "NeuralMinds",
            "industry_interests": ["Ритейл и e-commerce", "EdTech и образование"],
            "task_type_interests": ["Диалоговый AI и чат-боты", "Веб-платформы и клиентские сервисы"],
            "skills": ["Python", "FastAPI", "NLP", "LLM", "Docker", "PostgreSQL"],
            "preferred_readiness": "Любая",
            "progress_points": 125,
            "completed_milestones": ["ms-001", "ms-002"]
        },
        {
            "id": "team-002",
            "name": "DataCrafters",
            "industry_interests": ["Финтех и банкинг", "Ритейл и e-commerce"],
            "task_type_interests": ["Data Science и предиктивная аналитика", "Автоматизация бизнес-процессов"],
            "skills": ["Python", "CatBoost", "PyTorch", "SQL", "Pandas", "Scikit-Learn"],
            "preferred_readiness": "Готовая",
            "progress_points": 95,
            "completed_milestones": ["ms-003"]
        },
        {
            "id": "team-003",
            "name": "EdTech Innovators",
            "industry_interests": ["EdTech и образование", "Здравоохранение и медицина"],
            "task_type_interests": ["Веб-платформы и клиентские сервисы", "Диалоговый AI и чат-боты"],
            "skills": ["TypeScript", "React", "Python", "Django", "TailwindCSS"],
            "preferred_readiness": "Рабочая",
            "progress_points": 70,
            "completed_milestones": ["ms-004"]
        },
        {
            "id": "team-004",
            "name": "RouteMasters",
            "industry_interests": ["Логистика и доставка", "Ритейл и e-commerce"],
            "task_type_interests": ["Автоматизация бизнес-процессов", "Data Science и предиктивная аналитика"],
            "skills": ["Go", "Python", "Оптимизация графов", "PostGIS", "Docker"],
            "preferred_readiness": "Любая",
            "progress_points": 60,
            "completed_milestones": ["ms-005"]
        },
        {
            "id": "team-005",
            "name": "MedAI Squad",
            "industry_interests": ["Здравоохранение и медицина", "Финтех и банкинг"],
            "task_type_interests": ["Компьютерное зрение и мультимедиа", "Data Science и предиктивная аналитика"],
            "skills": ["Python", "PyTorch", "OpenCV", "FastAPI", "MLOps"],
            "preferred_readiness": "Приоритетная",
            "progress_points": 40,
            "completed_milestones": []
        }
    ]

def get_initial_proposals() -> List[Dict[str, Any]]:
    return [
        {
            "id": "prop-001",
            "task_id": "task-001",
            "team_id": "team-001",
            "team_name": "NeuralMinds",
            "solution_idea": "Разработка гибридного RAG-бота на базе FastAPI и векторной базы Qdrant с классификацией интентов и бесшовным переводом на оператора.",
            "plan": "1 неделя: парсинг FAQ и векторизация. 2 неделя: интеграция Telegram бота и API интернет-магазина. 3 неделя: веб-виджет и тестирование сценариев возврата. 4 неделя: контейнеризация и нагрузочное тестирование.",
            "timeline": "4 недели",
            "prototype_url": "https://github.com/neuralminds/support-ai-prototype",
            "status": "accepted",
            "submitted_at": "2026-09-20T16:00:00",
            "review_comment": "Сильный план реализации и релевантный стек. Команда выбрана для дальнейшей работы."
        },
        {
            "id": "prop-002",
            "task_id": "task-001",
            "team_id": "team-003",
            "team_name": "EdTech Innovators",
            "solution_idea": "Создание веб-чата на React с бэкендом на Django и интеграцией открытых LLM для ответов на частые вопросы.",
            "plan": "2 недели дизайн и верстка интерфейса, 2 недели настройка prompt engineering и тестирование.",
            "timeline": "4 недели",
            "prototype_url": "https://github.com/edtech-innovators/chat-client",
            "status": "pending",
            "submitted_at": "2026-09-21T11:00:00",
            "review_comment": ""
        },
        {
            "id": "prop-003",
            "task_id": "task-002",
            "team_id": "team-002",
            "team_name": "DataCrafters",
            "solution_idea": "Построение ансамбля CatBoost с генерацией признаков кредитного поведения и интерпретацией через SHAP-значения для кредитных аналитиков.",
            "plan": "1 неделя EDA и предобработка Parquet данных. 2 неделя обучение моделей и тюнинг гиперпараметров. 3 неделя FastAPI сервис. 4 неделя валидация.",
            "timeline": "4 недели",
            "prototype_url": "https://github.com/datacrafters/scoring-pipeline",
            "status": "accepted",
            "submitted_at": "2026-09-21T12:30:00",
            "review_comment": "Отличная проработка метрик качества и учет интерпретируемости модели."
        },
        {
            "id": "prop-004",
            "task_id": "task-003",
            "team_id": "team-003",
            "team_name": "EdTech Innovators",
            "solution_idea": "Дашборд на Streamlit с визуализацией динамики активности студентов и алертами в Telegram кураторам.",
            "plan": "1 неделя анализ логов LMS, 2 неделя разработка дашборда и интеграция уведомлений.",
            "timeline": "3 недели",
            "prototype_url": "https://github.com/edtech-innovators/student-retention-dashboard",
            "status": "pending",
            "submitted_at": "2026-09-22T09:45:00",
            "review_comment": ""
        },
        {
            "id": "prop-005",
            "task_id": "task-004",
            "team_id": "team-004",
            "team_name": "RouteMasters",
            "solution_idea": "Реализация эвристического VRP-алгоритма на Python/Go с учетом дорожной обстановки и минимизацией совокупного времени в пути.",
            "plan": "1 неделя обработка GPS треков, 2 неделя алгоритм оптимизации маршрутов, 3-4 неделя API диспетчера.",
            "timeline": "4 недели",
            "prototype_url": "https://github.com/routemasters/delivery-optimizer",
            "status": "pending",
            "submitted_at": "2026-09-22T14:10:00",
            "review_comment": ""
        }
    ]

def get_initial_milestones() -> List[Dict[str, Any]]:
    return [
        {
            "id": "ms-001",
            "task_id": "task-001",
            "team_id": "team-001",
            "title": "Этап 1: Архитектура микросервиса и схема интеграции с базой FAQ",
            "points": 25,
            "status": "completed",
            "completed_at": "2026-09-21T18:00:00"
        },
        {
            "id": "ms-002",
            "task_id": "task-001",
            "team_id": "team-001",
            "title": "Этап 2: Прототип чат-бота в Telegram с классификацией интентов",
            "points": 35,
            "status": "completed",
            "completed_at": "2026-09-22T15:00:00"
        },
        {
            "id": "ms-003",
            "task_id": "task-002",
            "team_id": "team-002",
            "title": "Этап 1: Предобработка кредитных историй и baseline модель CatBoost",
            "points": 30,
            "status": "completed",
            "completed_at": "2026-09-22T12:00:00"
        },
        {
            "id": "ms-004",
            "task_id": "task-003",
            "team_id": "team-003",
            "title": "Этап 1: Анализ признаков оттока студентов по логам LMS",
            "points": 25,
            "status": "completed",
            "completed_at": "2026-09-22T17:30:00"
        },
        {
            "id": "ms-005",
            "task_id": "task-004",
            "team_id": "team-004",
            "title": "Этап 1: Математическая постановка задачи VRP и валидация GPS-графа",
            "points": 25,
            "status": "completed",
            "completed_at": "2026-09-22T19:00:00"
        },
        {
            "id": "ms-006",
            "task_id": "task-001",
            "team_id": "team-001",
            "title": "Этап 3: Финальный деплой веб-виджета и нагрузочное тестирование",
            "points": 40,
            "status": "in_progress",
            "completed_at": None
        }
    ]
