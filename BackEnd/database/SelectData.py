from database.config import cursor, conn

def select_title_type():
    # Ваш SELECT-запрос
    select_query = "SELECT title FROM title_type"

    # Выполнение запроса
    cursor.execute(select_query)
    rows = cursor.fetchall()

    # Извлечение строк из кортежей
    titles = [row[0] for row in rows]
    titles.append("Ничего")
    return titles

def select_keywordsData(title_text):
    # Запрос для получения всех title и keywords по тексту title
    query = """
        SELECT t.title, d.keywords
        FROM data d
        JOIN title_type t ON d.title = t.id
        WHERE t.title = %s;
    """
    
    # Выполнение запроса
    cursor.execute(query, (title_text,))
    
    # Получение всех результатов
    results = cursor.fetchall()
    
    
    
    if results:
        # Для каждого результата выводим title и keywords
        data = []
        for result in results:
            keywords = result[1]
            data.append(keywords)
        return data
    else:
        return None
    

def select_textData(keywords):
    query = """
        SELECT text
        FROM data
        WHERE keywords && %s;
    """
    
    # Преобразуем список ключевых слов в массив для SQL
    keywords_array = '{' + ','.join(keywords) + '}'
    
    # Выполнение запроса
    cursor.execute(query, (keywords_array,))
    
    # Получение результатов
    result = cursor.fetchall()
    
    return result