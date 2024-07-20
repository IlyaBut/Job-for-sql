import psycopg2
from pprint import pprint

# Функция, создающая структуру БД (таблицы).
def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(60),
        lastname VARCHAR(60),
        email VARCHAR(60)
        );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonenumbers(
        number VARCHAR(11) PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id)
        );
    """)
    return

# Удаление таблиц
def delete_db(cur):
    cur.execute("""
        DROP TABLE clients, phonenumbers CASCADE;
        """)

# Функция, позволяющая добавить телефон для существующего клиента.
def insert_tel(cur, client_id, tel):
    cur.execute("""
        INSERT INTO phonenumbers(number, client_id)
        VALUES (%s, %s)
        """, (tel, client_id))
    return client_id

# Функция, позволяющая добавить нового клиента.
def insert_client(cur, name=None, surname=None, email=None, tel=None):
    cur.execute("""
        INSERT INTO clients(name, lastname, email)
        VALUES (%s, %s, %s)
        """, (name, surname, email))
    cur.execute("""
        SELECT id from clients
        ORDER BY id DESC
        LIMIT 1
        """)
    id = cur.fetchone()[0]
    if tel is None:
        return id
    else:
        insert_tel(cur, id, tel)
        return id

# Функция, позволяющая изменить данные о клиенте.
def update_client(cur, id, name=None, surname=None, email=None):
    cur.execute("""
        SELECT * from clients
        WHERE id = %s
        """, (id, ))
    info = cur.fetchone()
    if name is None:
        name = info[1]
    if surname is None:
        surname = info[2]
    if email is None:
        email = info[3]
    cur.execute("""
        UPDATE clients
        SET name = %s, lastname = %s, email =%s 
        where id = %s
        """, (name, surname, email, id))
    return id

# Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(cur, number):
    cur.execute("""
        DELETE FROM phonenumbers 
        WHERE number = %s
        """, (number, ))
    return number

# Функция, позволяющая удалить существующего клиента.
def delete_client(cur, id):
    cur.execute("""
        DELETE FROM phonenumbers
        WHERE client_id = %s
        """, (id, ))
    cur.execute("""
        DELETE FROM clients 
        WHERE id = %s
       """, (id,))
    return id

# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(cur, name=None, surname=None, email=None, tel=None):
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if surname is None:
        surname = '%'
    else:
        surname = '%' + surname + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if tel is None:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s
            """, (name, surname, email))
    else:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s AND p.number like %s
            """, (name, surname, email, tel))
    return cur.fetchall()


if __name__ == '__main__':
    with psycopg2.connect(database="netology_db", user="postgres",
                          password="1234") as conn:
        with conn.cursor() as curs:
            # Удаление таблиц перед запуском
            delete_db(curs)
            # 1. Cоздание таблиц
            create_db(curs)
            print("БД создана")
            # 2. Добавляем 5 клиентов
            print("Добавлен клиент id: ",
                  insert_client(curs, "Вадик", "Пупыров", "Focus@gmail.com"))
            print("Добавлен клиент id: ",
                  insert_client(curs, "Кира", "Йошикагевич",
                                "Gher@gmail.com", 79995554591))
            print("Добавлен клиент id: ",
                  insert_client(curs, "Икс", "Столов",
                                "Ham123@gmail.com", 79086661234))
            print("Добавлен клиент id: ",
                  insert_client(curs, "Joi", "Бидуинов",
                                "stasfg@gmail.com", 72228883477))
            print("Добавлена клиент id: ",
                  insert_client(curs, "Бони", "Клайдов",
                                "klfhce12@gmail.com"))
            print("Данные в таблицах")
            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER by c.id
                """)
            pprint(curs.fetchall())
            # 3. Добавляем клиенту номер телефона(одному первый, одному второй)
            print("Телефон добавлен клиенту id: ",
                  insert_tel(curs, 1, 79001208473))
            print("Телефон добавлен клиенту id: ",
                  insert_tel(curs, 5, 78889994567))

            print("Данные в таблицах")
            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER by c.id
                """)
            pprint(curs.fetchall())
            # 4. Изменим данные клиента
            print("Изменены данные клиента id: ",
                  update_client(curs, 1, "Парело", None, 'HHHHiiii@gmail.com'))
            # 5. Удаляем клиенту номер телефона
            print("Телефон удалён c номером: ",
                  delete_phone(curs, '79995554591'))
            print("Данные в таблицах")
            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER by c.id
                """)
            pprint(curs.fetchall())
            # 6. Удалим клиента номер 2
            print("Клиент удалён с id: ",
                  delete_client(curs, 2))
            curs.execute("""
                            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                            LEFT JOIN phonenumbers p ON c.id = p.client_id
                            ORDER by c.id
                            """)
            pprint(curs.fetchall())
            # 7. Найдём клиента
            print('Найденный клиент по имени:')
            pprint(find_client(curs, 'Бони'))

            print('Найденный клиент по email:')
            pprint(find_client(curs, None, None, 'stasfg@gmail.com'))

            print('Найденный клиент по имени, фамилии и email:')
            pprint(find_client(curs, 'Joi', 'Бидуинов',
                               'stasfg@gmail.com'))

            print('Найденный клиент по имени, фамилии, телефону и email:')
            pprint(find_client(curs, 'Вадик', 'Пупыров',
                               'Focus@gmail.com', '79001208473'))

            print('Найденный клиент по имени, фамилии, телефону:')
            pprint(find_client(curs, None, None, None, '79086661234'))