from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_similarity(query_keywords, database_keywords):
    # Проверка на пустые данные базы данных
    if not database_keywords:
        return []

    vectorizer = TfidfVectorizer()

    # Преобразуем ключевые слова в строки (из списка в строку)
    query_str = ' '.join(query_keywords)
    db_strs = [' '.join(keywords) for keywords in database_keywords]
    
    # Создаем TF-IDF матрицу
    tfidf_matrix = vectorizer.fit_transform([query_str] + db_strs)
    
    # Вычисляем косинусное сходство между вопросом и каждой строкой
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Формируем список кортежей (сходство, ключевые слова)
    similarity_results = [(similarity_scores[i], database_keywords[i]) for i in range(len(similarity_scores))]
    
    # Сортируем результаты по убыванию схожести
    sorted_similarity_results = sorted(similarity_results, key=lambda x: x[0], reverse=True)
    
    return sorted_similarity_results


if __name__ == "__main__":
    # Пример использования
    query_keywords = ["gfgf", 'fdfdf', 'сельскохозяйственные культуры', 'агроклимат']
    db_keywords = [
        ['климатические факторы', 'рост растений', 'агроклиматические условия'],
        ['почвенные условия', 'сельское хозяйство', 'развитие растений'],
        ['сельскохозяйственные культуры', 'климат', 'засуха']
    ]

    similarity_results = get_similarity(query_keywords, db_keywords)

    # Выводим отсортированные результаты
    for score, keywords in similarity_results:
        print(f"Схожесть: {score:.4f}, Ключевые слова: {keywords}")
