#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo "AI Sana - Автономное веб-приложение (FastAPI)"
echo "Чистая белая архитектура (Clean Tech White)"
echo "=================================================="

# Проверка наличия виртуального окружения
if [ ! -d "$DIR/venv" ]; then
    echo "[ОШИБКА] Виртуальное окружение не найдено в $DIR/venv"
    echo "Пожалуйста, создайте окружение и установите зависимости:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

UVICORN_BIN="$DIR/venv/bin/uvicorn"
if [ ! -f "$UVICORN_BIN" ]; then
    echo "[ОШИБКА] uvicorn не найден в $DIR/venv/bin/uvicorn"
    echo "Пожалуйста, выполните: ./venv/bin/pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "Сервер запускается:"
echo "  - Главная страница:    http://localhost:8000"
echo "  - Конструктор:         http://localhost:8000/constructor"
echo "  - Каталог задач:       http://localhost:8000/catalog"
echo "  - Кабинет студента:    http://localhost:8000/student"
echo "  - Кабинет бизнеса:     http://localhost:8000/business"
echo "  - Экспресс-демо жюри:  http://localhost:8000/jury-demo"
echo ""
echo "Для остановки сервера нажмите Ctrl+C"
echo "--------------------------------------------------"

exec "$UVICORN_BIN" server:app --host 0.0.0.0 --port 8000 --reload
