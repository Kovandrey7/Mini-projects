import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS client_info(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email VARCHAR(80) UNIQUE NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS client_phone(
            client_id INTEGER NOT NULL REFERENCES client_info(client_id) ON DELETE CASCADE,
            phone VARCHAR(20) NOT NULL
        );
        ''')

        conn.commit()


def delete_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE IF EXISTS client_phone;
        DROP TABLE IF EXISTS client_info;
        """)


def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        if find_client(conn, email=email):
            return "Клиент с данным email уже существует"

        cur.execute("""
            INSERT INTO client_info(first_name, last_name, email)
            VALUES
                (%s, %s, %s) RETURNING client_id;
        """, (first_name, last_name, email))

        if phone is not None:
            client_id = cur.fetchone()
            add_client_phone = add_phone(conn, client_id=client_id, phone=phone)
            if add_client_phone == "Данный номер есть в базе":
                conn.rollback()
                return "Невозможно добавить клиента"
        conn.commit()
        return "Клиент добавлен в базу"


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        if find_client(conn, phone=phone):
            return "Данный номер есть в базе"

        cur.execute("""
            SELECT * FROM client_info ci
            WHERE client_id = %s;
        """, (client_id,))

        if not cur.fetchone():
            return "Такого клиента нет в базе"

        cur.execute("""
            INSERT INTO client_phone
            VALUES
                (%s, %s);
        """, (client_id, phone))

        conn.commit()
        return "Телефон успешно добавлен"


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT first_name, last_name, email, client_id 
        FROM client_info
        WHERE client_id = %s;
        """, (client_id,))

        client_data = cur.fetchone()
        if not client_data:
            return "Такого пользователя нет"
        if first_name is None:
            first_name = client_data[0]
        if last_name is None:
            last_name = client_data[1]
        if email is None:
            email = client_data[2]

        cur.execute("""
        UPDATE client_info
        SET first_name = %s, last_name = %s, email = %s
        WHERE client_id = %s
        """, (first_name, last_name, email, client_id))

        conn.commit()
    return "Данные клиента успешно изменены"


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client_phone
            WHERE client_id = %s and phone = %s;
        """, (client_id, phone))

        conn.commit()
        return "Телефон успешно удален из базы"


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""         
            DELETE FROM client_info
            WHERE client_id = %s;         
        """, (client_id,))

        conn.commit()
        return "Клиент успешно удален из базы"

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        if first_name is None:
            first_name = '%'
        if last_name is None:
            last_name = '%'
        if email is None:
            email = '%'

        client_data = [first_name, last_name, email]
        new_str = ''

        if phone:
            new_str =' AND cp.phone = %s::text'
            client_data.append(phone)

        my_requests = f"""
                    SELECT 
                        ci.email,
                        ci.first_name,
                        ci.last_name,
                        CASE
                            WHEN ARRAY_AGG(cp.phone) = '{{Null}}' THEN '{{}}'
                            ELSE ARRAY_AGG(cp.phone)
                        END 
                    FROM client_info ci
                    LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                    WHERE first_name ILIKE %s AND last_name ILIKE %s AND email ILIKE %s{new_str}
                    GROUP BY ci.email, ci.first_name, ci.last_name
                    """
        cur.execute(
                    my_requests,
                    client_data
                )

        return cur.fetchall()


with psycopg2.connect(database="netology_db", user="postgres", password=input("Введите пароль: ")) as conn:
    delete_tables(conn)
    create_db(conn)
    print(add_client(conn, "Vasia", "Pupkin", "VP@list.ru"))
    print(add_client(conn, "Andrey", "Koval", "AK@list.ru", "+71234567890"))
    print(add_client(conn, "Andrey", "Fedorov", "AF@list.ru", "+79874562321"))
    print(add_client(conn, "Petya", "Fomin", "VP@list.ru"))
    print(add_client(conn, "Peter", "Parker", "spider-man@list.ru", "+71236548789"))
    print(add_phone(conn, 1, "+79646546362"))
    print(add_phone(conn, 2, "+71112223334"))
    print(add_phone(conn, 1, "+79646546362"))
    print(add_phone(conn, 5, "+74567891223"))
    print(change_client(conn, 1, first_name="Nika", last_name="Koval", email="NK@list.ru"))
    print(change_client(conn, 1, last_name="Petrov", email="Petrov@list.ru"))
    print(delete_phone(conn, 2,"+71234567890"))
    print(delete_client(conn, 2))
    print(find_client(conn, "Andrey"))
    print(find_client(conn, "Peter", "Parker", "spider-man@list.ru"))
    print(find_client(conn, "Andrey", "Koval", "AK@list.ru", "+71112223334"))
