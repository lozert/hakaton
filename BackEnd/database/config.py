import psycopg2

# Здесь вводить свои данные для подключения к базе данных
db_params = {
    'dbname': 'Agrotech',  # Имя базы данных
    'user': 'postgres',        # Имя пользователя
    'password': 'dlikaros',    # Пароль
    'host': 'localhost',            # Хост (обычно localhost)
    'port': '5432'                  # Порт PostgreSQL (по умолчанию 5432)
}


# Подключение к базе данных
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()
print("Соединение с базой данных установлено.")
