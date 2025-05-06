import requests

def fetch_messages(chat_id: str, days: int = 30):
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/Mikhail802/pinecone/refs/heads/main/messages_%D0%93%D0%A1%D0%9F-2%20%D0%9F%D0%B5%D1%80%D0%B5%D0%B2%D0%B0%D1%85%D1%82%D0%B0%20%D0%9E%D1%82%D0%B4%D0%B5%D0%BB_7d.json"
        )
        response.raise_for_status()
        return response.json()  # просто возвращаем список
    except Exception as e:
        print("❌ Ошибка запроса get_messages:", e)
        return []



def format_messages(messages):
    formatted = []
    for msg in messages:
        actor = msg.get("actor") or msg.get("from", "Неизвестный")
        date = msg.get("date", "Без даты")

        # 🧠 Получаем основной текст
        text = msg.get("message") or msg.get("text", "")

        # Если text пустой, но есть text_entities — собираем оттуда
        if not text and "text_entities" in msg:
            try:
                parts = []
                for part in msg["text_entities"]:
                    if isinstance(part, dict) and part.get("type") == "plain":
                        parts.append(part.get("text", ""))
                text = "".join(parts).strip()
            except Exception as e:
                print("❌ Ошибка обработки text_entities:", e)
                text = ""

        # Объединяем результат
        if isinstance(text, list):
            text = ''.join(part.get("text", "") if isinstance(part, dict) else part for part in text)

        formatted.append(f"Дата: {date}\nАвтор: {actor}\nСообщение: {text}")
    return formatted


def split_messages(formatted_messages, max_chars=1000):
    blocks = []
    current_block = ""
    for msg in formatted_messages:
        if len(current_block) + len(msg) < max_chars:
            current_block += "\n" + msg
        else:
            blocks.append(current_block.strip())
            current_block = msg
    if current_block:
        blocks.append(current_block.strip())
    return blocks
