from config import cursor, conn
import json

def insert_title_type(id: int, title: str):
    insert_query = "INSERT INTO title_type (id, title) VALUES (%s, %s);"

    cursor.execute(insert_query, (id, title))
    conn.commit()

def insert_data(id: int, title: int, text: str, keywords: list):
    insert_query = "INSERT INTO data (id, title, text, keywords) VALUES (%s, %s, %s, %s);"

    cursor.execute(insert_query, (id, title, text, keywords))
    conn.commit()

def title_type_data():
    with open("title_type.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    id = 1
    for data_item in data:
        title = data_item["title"]

        insert_title_type(id, title)
        id +=1
    
def data_data():
    
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    id = 1
    for data_item in data:
        title = data_item["title"]
        text = data_item["text"]
        keywords = data_item["keywords"]
        
        insert_data(id, title, text, keywords)
        id +=1
    
if __name__ == "__main__":
    title_type_data()
    data_data()
