import pytest
from services.ai_generator import AIGenerator

def test_local_fallback_next_question():
    generator = AIGenerator(api_key="")  # Force local fallback
    q_data = generator.generate_next_question(
        draft_text="Нужен умный чат-бот для поддержки клиентов интернет-магазина",
        industry="Ритейл и e-commerce",
        task_type="Диалоговый AI и чат-боты",
        qa_history=[]
    )
    assert "question" in q_data
    assert "field_target" in q_data
    assert "quick_reply_for_jury" in q_data
    assert len(q_data["question"]) > 10
    assert len(q_data["quick_reply_for_jury"]) > 10

def test_local_fallback_card_synthesis():
    generator = AIGenerator(api_key="")
    qa_history = [
        {
            "field_target": "data_materials",
            "question": "Какие данные вы передадите?",
            "answer": "Выгрузка 25 000 диалогов в JSONL"
        },
        {
            "field_target": "success_criteria",
            "question": "Критерии успеха?",
            "answer": "Точность классификации от 88%"
        },
        {
            "field_target": "constraints",
            "question": "Ограничения?",
            "answer": "Python FastAPI, Docker, 4 недели"
        }
    ]
    card = generator.synthesize_task_card(
        draft_text="Чат-бот для интернет-магазина",
        industry="Ритейл и e-commerce",
        task_type="Диалоговый AI и чат-боты",
        qa_history=qa_history
    )
    assert "title" in card
    assert "data_materials" in card
    assert "25 000" in card["data_materials"]
    assert "88%" in card["success_criteria"]
    assert "FastAPI" in card["constraints"]
