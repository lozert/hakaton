import json
import base64
from openai import OpenAI
from user_data import data_prompt_file_path, data_model_name, data_base_url
import json


import re
from database import SelectData, keyword_similarity



def save_json(output, name="output"):
    with open(f'{name}.json', 'w', encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False)

def load_prompt_from_json(prompt_file_path):
    with open(prompt_file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_response(base_url, messages, model, top_p=0.8, temperature=0.5):
    client = OpenAI(
        base_url=base_url,
        api_key="token-abc123"
    )
    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
        top_p=top_p,
        stream=True,
        stream_options={"include_usage": True}
    )
    return completion

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
    

def send_message(prompt_data, base_url, model_name, system = False, expend_text=False):
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

    

    # Отправляем запрос к модели
    completion = get_response(base_url=base_url, messages=messages, model=model_name)
    string = ""
    for chunk in completion:
        jtemp = json.loads(chunk.model_dump_json())
        if len(jtemp["choices"]) > 0:
            string += str(jtemp["choices"][0]["delta"]["content"])
    
    return string


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
    base_url = data_base_url
    model_name = data_model_name
   
    # # Загружаем промпт из JSON
    prompt_data = load_prompt_from_json(prompt_file_path)
    
# # Отправка сообщения
    response = send_message(prompt_data, base_url, model_name, system=True)

    title, keywords = extract_title_and_keywords(response)
    try:
        
        print(f"Title {title}")
        db_keywords = SelectData.select_keywordsData(title)

        print(f"Keywords: {keywords}\n")
        print(f"db_keywords: {db_keywords}\n")
        similarity = keyword_similarity.get_similarity(keywords, db_keywords)

        
        text_data = SelectData.select_textData(similarity[0][1])
        outputLLM = send_message(prompt_data, base_url, model_name, expend_text=text_data[0][0])

        output = {
            "role": "user",
            "text": str(outputLLM)
        }

        save_json(output)
    except:
        
        outputLLM = send_message(prompt_data, base_url, model_name)
        output = { 
            "role": "user",
            "text": f"{outputLLM}"
        }
        save_json(output)
    


if __name__ == "__main__":
    main()

    
    