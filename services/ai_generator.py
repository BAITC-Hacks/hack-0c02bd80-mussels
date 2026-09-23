import json
import logging
from typing import Dict, Any, List, Optional
from config import OPENAI_API_KEY, OPENAI_MODEL, SCORING_WEIGHTS

logger = logging.getLogger(__name__)

class AIGenerator:
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = OPENAI_MODEL):
        self.api_key = api_key or ""
        self.model = model
        self.client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI client: {e}")
                self.client = None

    def generate_next_question(
        self,
        draft_text: str,
        industry: str,
        task_type: str,
        qa_history: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Generates the next relevant clarification question targeting an uncovered block.
        Returns: {
            "question": "...",
            "field_target": "data_materials",
            "quick_reply_for_jury": "..."
        }
        """
        # Determine which fields have not been answered yet
        answered_targets = [qa.get("field_target") for qa in qa_history if qa.get("field_target")]
        
        # Priority order of fields to clarify
        candidate_fields = [
            "data_materials",
            "success_criteria",
            "constraints",
            "expected_result",
            "target_users",
            "business_contact"
        ]
        
        target_field = None
        for cf in candidate_fields:
            if cf not in answered_targets:
                target_field = cf
                break
        if not target_field:
            target_field = "constraints"

        # Try OpenAI if available
        if self.client:
            try:
                prompt = f"""Ты — бизнес-аналитик платформы хакатона. Представитель бизнеса описывает задачу.
Отрасль: {industry}
Направление: {task_type}
Исходный черновик: {draft_text}

История предыдущих вопросов и ответов:
{json.dumps(qa_history, ensure_ascii=False, indent=2)}

Сейчас нужно задать 1 конкретный, профессиональный вопрос для уточнения блока '{SCORING_WEIGHTS[target_field]['title']}'.
Также придумай реалистичный, готовый 'быстрый ответ' (quick_reply_for_jury), который спикер на защите может подставить в 1 клик.

Верни строго JSON следующего формата:
{{
  "question": "Текст вопроса",
  "field_target": "{target_field}",
  "quick_reply_for_jury": "Реалистичный ответ с конкретными цифрами и фактами"
}}
"""
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Ты экспертный аналитик ИТ-проектов. Отвечай только валидным JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3,
                    timeout=10.0
                )
                content = response.choices[0].message.content
                data = json.loads(content)
                if data.get("question") and data.get("quick_reply_for_jury"):
                    data["field_target"] = target_field
                    return data
            except Exception as e:
                logger.warning(f"OpenAI next question failed, using local fallback: {e}")

        # Local fallback
        return self._local_fallback_question(target_field, industry, task_type, draft_text)

    def _local_fallback_question(
        self,
        target_field: str,
        industry: str,
        task_type: str,
        draft_text: str
    ) -> Dict[str, str]:
        templates = {
            "data_materials": {
                "question": "Какие конкретно исходные данные, примеры диалогов, документы или базы знаний вы готовы передать команде?",
                "quick_reply_for_jury": "Выгрузка 25 000 обезличенных диалогов в JSONL, база FAQ из 450 статей и каталог товаров в CSV."
            },
            "success_criteria": {
                "question": "По каким измеримым метрикам и критериям вы будете оценивать успешность решения и принимать работу?",
                "quick_reply_for_jury": "Автоматическое разрешение не менее 65% типовых обращений, точность классификации от 88%, время ответа до 2 сек."
            },
            "constraints": {
                "question": "Каковы жесткие ограничения по срокам, технологическому стеку, безопасности данных или интеграциям?",
                "quick_reply_for_jury": "Срок разработки 4 недели, стек Python/FastAPI, упаковка в Docker, соблюдение требований безопасности данных."
            },
            "expected_result": {
                "question": "Что именно должно стать финальным результатом работы команды (веб-сервис, бот, API, дашборд)?",
                "quick_reply_for_jury": "Работающий микросервис с Telegram-ботом, веб-виджетом и панелью передачи диалога живому оператору."
            },
            "target_users": {
                "question": "Кто является конечной аудиторией этого решения и кто будет взаимодействовать с системой ежедневно?",
                "quick_reply_for_jury": "Конечные покупатели интернет-магазина и дежурные операторы первой линии клиентской поддержки."
            },
            "business_contact": {
                "question": "Кто из представителей вашей компании будет вести проект и в каком формате планируются консультации?",
                "quick_reply_for_jury": "CTO Алексей Смирнов (alexey@retail.kz, @alex_retail), еженедельные онлайн-синки по вторникам."
            }
        }
        res = templates.get(target_field, templates["data_materials"])
        return {
            "question": res["question"],
            "field_target": target_field,
            "quick_reply_for_jury": res["quick_reply_for_jury"]
        }

    def synthesize_task_card(
        self,
        draft_text: str,
        industry: str,
        task_type: str,
        qa_history: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Synthesizes all 7 structured fields of the task card from the draft and QA history.
        """
        if self.client:
            try:
                prompt = f"""Сформируй карточку бизнес-задачи на основе черновика и ответов представителя бизнеса.
Отрасль: {industry}
Направление: {task_type}
Исходный черновик: {draft_text}

Ответы на уточняющие вопросы:
{json.dumps(qa_history, ensure_ascii=False, indent=2)}

Требования:
1. Не выдумывай факты, которых нет в черновике или ответах. Если что-то не указано, оставь формулировку минимальной или пустой.
2. Сформируй емкий профессиональный заголовок title.
3. Заполни поля: context_need, data_materials, expected_result, success_criteria, constraints, target_users, business_contact.

Верни строго JSON вида:
{{
  "title": "Название задачи",
  "context_need": "...",
  "data_materials": "...",
  "expected_result": "...",
  "success_criteria": "...",
  "constraints": "...",
  "target_users": "...",
  "business_contact": "..."
}}
"""
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Ты экспертный аналитик ТЗ. Отвечай только валидным JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    timeout=12.0
                )
                content = response.choices[0].message.content
                data = json.loads(content)
                data["industry"] = industry
                data["task_type"] = task_type
                return data
            except Exception as e:
                logger.warning(f"OpenAI card synthesis failed, using local fallback: {e}")

        # Local fallback synthesis
        return self._local_fallback_synthesis(draft_text, industry, task_type, qa_history)

    def _local_fallback_synthesis(
        self,
        draft_text: str,
        industry: str,
        task_type: str,
        qa_history: List[Dict[str, str]]
    ) -> Dict[str, str]:
        answers_by_field = {qa.get("field_target", ""): qa.get("answer", "") for qa in qa_history}

        title = f"{task_type}: {draft_text[:50]}..." if len(draft_text) > 50 else f"{task_type}: {draft_text}"
        if "бот" in draft_text.lower():
            title = "Интеллектуальный ассистент клиентской поддержки интернет-магазина"
        elif "скоринг" in draft_text.lower() or "кредит" in draft_text.lower():
            title = "Предиктивная модель кредитного скоринга малого бизнеса"

        return {
            "title": title,
            "industry": industry,
            "task_type": task_type,
            "context_need": draft_text + (" " + answers_by_field.get("context_need", "")).strip(),
            "data_materials": answers_by_field.get("data_materials", "Предоставляются исторические данные по запросу."),
            "expected_result": answers_by_field.get("expected_result", "Работающий программный прототип с документацией."),
            "success_criteria": answers_by_field.get("success_criteria", "Соответствие функциональным требованиям и прохождение тестов."),
            "constraints": answers_by_field.get("constraints", "Срок реализации 4 недели, стандартный стек технологий."),
            "target_users": answers_by_field.get("target_users", "Конечные клиенты и сотрудники компании."),
            "business_contact": answers_by_field.get("business_contact", "Координатор проекта от бизнеса.")
        }
