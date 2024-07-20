import psycopg2

# Работа с БД из python с помощью драйвера psycopg2

# Создаем подключение к бд. С помощью функции .connect(),
# данная функция принимает на вход несколько данных (ЛОГИН, ПАРОЛЬ, НАЗВАНИЕ БД к которой подключаешься)
# Выполнение данной функции вернет нам объект подключения в данном случае "conn"
# conn.close() - Команда закрытия при завершении работы.
conn = psycopg2.connect(database='netology_db', user="postgres", password="1234")
# Что бы отправлять запросы в Postgres, нам необходим объект - курсор, позволяет отправлять запросы и получать ответы обратно от БД.
# Запрашиваем у соединения новый курсор.
# Таким макаром - cur = conn.cursor()
# Так же требует, закрытия после работы т.е. cur.close()
# Или же используем контекстный менеджер with, что бы не закрывать его через команду.
with conn.cursor() as cur:
    #Создание таблицы
    # Курсор не выполняет автоматически все запросы которые пишутся в execute, он сохраняет их в памяти до объявление commit-та и только после него запросы отправляются в БД.
#     cur.execute("CREATE TABLE test (id SERIAL PRIMARY KEY);")
#     # Транзакции - это механизм, который позволяет нам выполнить либо все, либо ничего если вдруг где-то произошла ошибка.
#     # Что бы отправить все изменения в БД, необходимо на объекте соединения т.е. в with conn...  выполнить функцию commit.
#     # В этот момент все "курсоры" которые были созданы соединением будут отправлены в БД
#     conn.commit()
#     # Так же существует функция .rollback() которая в свою очередь игнорирует и не отправляет запросы в БД
#
# #СОЗДАНИЕ ТАБЛИЦ.CRUD
#
#     # Создание таблицы и удаление онных.
#     # При создании таблиц описываем точно такой же SQl - код как обычно. Не забывая при этом закомитеть создание.
#     # Так же в начале скрипта, пишется дополнительный execute для удаления таблиц. Для удобства.
#     cur.execute("""
#         DROP TABLE homework;
#         DROP TABLE course;
#             """)
#     # Удаляем сначала homework, т.к. есть зависимость от таблицы course, а затем уже и таблицу курсов.
#     cur.execute("""
#             CREATE TABLE IF NOT EXISTS course(
#                 id SERIAL PRIMARY KEY,
#                 name VARCHAR(40) UNIQUE
#             );
#             """)
#     cur.execute("""
#             CREATE TABLE IF NOT EXISTS homework(
#                 id SERIAL PRIMARY KEY,
#                 number INTEGER NOT NULL,
#                 description TEXT NOT NULL,
#                 course_id INTEGER NOT NULL REFERENCES course(id)
#             );
#             """)
#     conn.commit()
#
# # INSERT - запросы, но при таком исполнении мы не увидим результат сразу как выполним команду
#     cur.execute("""
#             INSERT INTO course(name) VALUES('Python');
#             """)
#     conn.commit()
#
# # INSERT - запросы, вариант №2 при необходимости вернуть какую-либо информацию из созданной сущности.
#     cur.execute("""
#                 INSERT INTO course(name) VALUES('Java') RETURNING id;
#                 """)
#     conn.commit()
# # Например, с помощью команды RETURNING id можно посмотреть какой id будет присвоен только-что добавленному курсу "Java"
#     print(cur.fetchone())
# # Тут же нам поможет команда .fetchone() - данный метод поможет извлечь данные которые были возвращены БД нам во время запроса т.е. команды RETURNING.
# # Но есть один момент, команда .fetchone() - принтить результат она может, но изменения в самой БД не делает.
#     cur.execute("""
#         INSERT INTO homework(number, description, course_id) VALUES(1, 'простое дз', 1);
#                 """)
# conn.commit()  # фиксируем в БД
#
# # Извлечение данных
# # Что бы извлечь данные, используем SELECT - запросы и через принт используем один из методов
# # .fetchall(Извлечь все) или .fetchone(Извлечь первую строку) .fetchmany(Извлечь N-строк)
# # .featchall() и .fetchmany() извлекают всегда список с кортежами.
#
#         # извлечение данных (R из CRUD)
#     cur.execute("""
#             SELECT * FROM course;
#                 """)
#     print('fetchall', cur.fetchall())  # извлечь все строки
#
#     cur.execute("""
#             SELECT * FROM course;
#                 """)
#     print(cur.fetchone())  # извлечь первую строку (аналог LIMIT 1)
#
#     cur.execute("""
#             SELECT * FROM course;
#                 """)
#     print(cur.fetchmany(3))  # извлечь первые N строк (аналог LIMIT N)
#
#     cur.execute("""
#             SELECT name FROM course;
#                 """)
#     print(cur.fetchall())
#
# # Так же как и в SQL доступна выборка с оператором WHERE
#
#     cur.execute("""
#             SELECT id FROM course WHERE name='Python';
#             """)
#     print(cur.fetchone())
#
# # Использовать f-строки или метод format не стоит, иначе возможна SQL-инъекция.
# # Sql- инъекция один из вариантов взлома бд посредством написания в поле для заполнения пользователем, запроса определенного вида типа ЛОГИН: 'A' ON 1=1;
#
#     cur.execute("""
#             SELECT id FROM course WHERE name='{}';
#                 """.format("Python"))  # плохо - возможна SQL инъекция
#     print(cur.fetchone())
#
# # Правильный метод будет осуществлятся через операции драйвера. .execute() позволяет подставлять определенные данные вместо %s.
# # Правильный метод для выполнения динамический запрос с подстановкой данных.
#
#     cur.execute("""
#             SELECT id FROM course WHERE name=%s;
#                 """, ("Python",))  # параметр ('Python') обязательно должен быть именно кортежем
#     print(cur.fetchone())
#
# # Пример создания функции для извлечения данных.
# # Узнаем ID - курса по его имени, для этого в функцию передаем имя курса - name.
# # А в .execute вставляем выше написанный SELECT - запрос с подстановкой имени. Вторым аргументом передаем кортеж параметров, то есть name.
#
#
#     def get_course_id(cursor, name: str) -> int:
#         cursor.execute("""
#         SELECT id FROM course WHERE name=%s;
#         """, (name,))
#         return cur.fetchone()[0] # В результате мы достаем непосредственно запись и нулевой элемент [0] т.к. возвращается всегда кортеж объектов.
#
# # использование функции будет выглядеть след. образом все как и с обычной функцией суем в переменную, а затем принтим или передаем ее куда-либо.
#     python_id = get_course_id(cur, 'Python')
#     print('python_id', python_id)
#
# # Вставка данных в homework
#     cur.execute("""
#         INSERT INTO homework(number, description, course_id) VALUES(%s, %s, %s);
#         """, (2, "задание посложнее", python_id))
#     conn.commit()  # фиксируем в БД
#
# # Если поставить звездочку после Select - запроса, то .fetchall() - вернет список всех кортежей со всеми столбиками
#     cur.execute("""
#         SELECT * FROM homework;
#         """)
#     print(cur.fetchall())
#
#         # обновление данных (U из CRUD)
#     cur.execute("""
#         UPDATE course SET name=%s WHERE id=%s;
#         """, ('Python Advanced', python_id))
#     cur.execute("""
#         SELECT * FROM course;
#         """)
#     print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения
#
#         # удаление данных (D из CRUD)
#     cur.execute("""
#         DELETE FROM homework WHERE id=%s;
#         """, (1,))
#     cur.execute("""
#         SELECT * FROM homework;
#         """)
#     print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения.

    conn.close()


