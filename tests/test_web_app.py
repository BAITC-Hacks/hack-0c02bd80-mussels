import re
from pathlib import Path
import pytest
from starlette.testclient import TestClient

# Import will fail during initial red phase if server.py is not yet created
try:
    from server import app
except ImportError:
    app = None


@pytest.fixture
def client():
    assert app is not None, "server.app must be defined"
    return TestClient(app)


def test_index_page_status_and_content(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    content = response.text
    assert "AI Sana" in content
    assert "Конструктор" in content
    assert "Каталог" in content
    assert "Кабинет студента" in content
    assert "Кабинет бизнеса" in content
    assert "Демо жюри" in content
    assert "OpenAI API" in content or "Локальный движок" in content
    assert "/api/reset-data" in content or "Сброс данных" in content


def test_nav_routes(client):
    for route in ["/catalog", "/student", "/business", "/jury-demo"]:
        response = client.get(route)
        assert response.status_code == 200
        assert "AI Sana" in response.text


def test_reset_data_endpoint(client):
    response = client.post("/api/reset-data")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"


def test_no_emojis_in_web_code():
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
        "\U0001FA00-\U0001FA6F"  # symbols and pictographs extended-a
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
        "\U00002600-\U000026FF"  # misc symbols
        "]+",
        flags=re.UNICODE,
    )

    base_dir = Path(__file__).resolve().parent.parent
    files_to_check = [base_dir / "server.py", Path(__file__)]
    templates_dir = base_dir / "templates"
    if templates_dir.exists():
        files_to_check.extend(templates_dir.rglob("*.html"))

    for file_path in files_to_check:
        if file_path.exists():
            text = file_path.read_text(encoding="utf-8")
            matches = emoji_pattern.findall(text)
            assert not matches, f"Emoji found in {file_path}: {matches}"
