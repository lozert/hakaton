import json
import requests
from user_data import data_prompt_file_path,token, data_base_url
import json


import re
from database import SelectData, keyword_similarity


def save_json(output, name="output"):
    with open(f'{name}.json', 'w', encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False)

def load_prompt_from_json(prompt_file_path):
    with open(prompt_file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_response_from_huggingface(base_url, messages):
    # Используем Hugging Face Inference API для получения ответа от модели
    
    
    headers = {
        'Authorization': f"Bearer {token}"  # Ваш Hugging Face токен
    }

    data = {
        "inputs": " ".join([message["content"][0]["text"] for message in messages])  # Собираем все текстовые сообщения
    }

    response = requests.post(base_url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")


def get_system_prompt():
    messages = []
    title = "Ключевые вслова: " + str(SelectData.select_title_type())

    prompt = load_prompt_from_json("system_prompt.json")
  
    for entry in prompt:
        role = entry["role"]
        text = entry["text"]

        content = [{"type": "text", "text": text + " " + title}]
        messages.append({
            "role": role,
            "content": content
        })
    return messages
    

def send_message(prompt_data, base_url,  system=False, expend_text=False):
    messages = []

    # Обработка каждого элемента в `prompt_data`
    for entry in prompt_data:
        role = entry["role"]
        text = entry["text"]

        if expend_text:
            content = [{"type": "text", "text": str(expend_text) + "\n" + text}]
        else:
            content = [{"type": "text", "text": text}]

        # Добавляем сообщение с ролью и контентом
        messages.append({
            "role": role,
            "content": content
        })

    if system:
        system_prompt = get_system_prompt()
        messages.append(system_prompt[0])

    # Отправляем запрос к Hugging Face
   
    response = get_response_from_huggingface(base_url, messages)

    # Возвращаем текст ответа от Hugging Face модели

    return response[0]['generated_text']


def extract_title_and_keywords(data_str):
    # Извлекаем title и keywords
    title_match = re.search(r"title:\s*([^,\n]+)", data_str)
    keywords_match = re.search(r"keywords:\s*\[(.*?)\]", data_str)

    if title_match and keywords_match:
        title = title_match.group(1)
        keywords = [kw.strip() for kw in keywords_match.group(1).split(',')]
        
    return title, keywords


def main():
    prompt_file_path = data_prompt_file_path
    base_url = data_base_url  # Этот base_url указывает на сервер Hugging Face

   
    # Загружаем промпт из JSON
    prompt_data = load_prompt_from_json(prompt_file_path)
    
    # Отправка сообщения
    response = send_message(prompt_data, base_url, system=True)

    title, keywords = extract_title_and_keywords(response)
    try:
        print(f"Title {title}")
        print(f"Keywords: {keywords}\n")
        db_keywords = SelectData.select_keywordsData(title)

        
        print(f"db_keywords: {db_keywords}\n")
        similarity = keyword_similarity.get_similarity(keywords, db_keywords)

        text_data = SelectData.select_textData(similarity[0][1])
        outputLLM = send_message(prompt_data, base_url,  expend_text=text_data[0][0])

        output = {
            "role": "user",
            "text": str(outputLLM)
        }

        save_json(output)
    except Exception as e:
        print(f"Error: {str(e)}")
        outputLLM = send_message(prompt_data, base_url)
        output = { 
            "role": "user",
            "text": f"{outputLLM}"
        }
        save_json(output)


if __name__ == "__main__":
    main()
