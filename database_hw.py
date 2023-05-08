import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        DROP TABLE client_info;
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS client_info(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email VARCHAR(80) UNIQUE NOT NULL,
            phone VARCHAR(20)[] UNIQUE
        );
        ''')

        conn.commit()


def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:

        if phone is None:
            cur.execute("""
                INSERT INTO client_info(first_name, last_name, email)
                VALUES
                    (%s, %s, %s) RETURNING client_id, first_name, last_name;
                """, (first_name, last_name, email))

            print(cur.fetchone())


        else:
            cur.execute("""
                INSERT INTO client_info(first_name, last_name, email, phone)
                VALUES
                    (%s, %s, %s, ARRAY [%s]) RETURNING client_id, first_name, last_name;
                """, (first_name, last_name, email, phone))

            print(cur.fetchone())


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT count(phone) FROM client_info
        WHERE client_id = %s;
        ''', (client_id,))
        count_number = cur.fetchone()[0]

        if count_number == 0:
            cur.execute("""
            UPDATE client_info 
            SET phone = ARRAY [%s]
            WHERE client_id = %s;
            """, (phone, client_id))

        else:
            cur.execute("""
            UPDATE client_info
            SET phone[%s] = %s
            WHERE client_id = %s;
            """, (count_number + 1, phone, client_id))


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        if first_name is not None and last_name is not None and email is None:
            cur.execute('''
            UPDATE client_info
            SET first_name = %s, last_name = %s
            WHERE client_id = %s;
            ''', (first_name, last_name, client_id))
        elif first_name is not None and last_name is None and email is None:
            cur.execute('''
            UPDATE client_info
            SET first_name = %s
            WHERE client_id = %s;
            ''', (first_name, client_id))
        elif first_name is None and last_name is not None and email is None:
            cur.execute('''
            UPDATE client_info
            SET last_name = %s
            WHERE client_id = %s;
            ''', (last_name, client_id))
        elif first_name is None and last_name is None and email is not None:
            cur.execute('''
            UPDATE client_info
            SET email = %s
            WHERE client_id = %s;
            ''', (email, client_id))
        elif first_name is not None and last_name is None and email is not None:
            cur.execute('''
            UPDATE client_info
            SET first_name = %s, email = %s
            WHERE client_id = %s;
            ''', (first_name, email, client_id))
        elif first_name is None and last_name is not None and email is not None:
            cur.execute('''
            UPDATE client_info
            SET last_name = %s, email = %s
            WHERE client_id = %s;
            ''', (last_name, email, client_id))
        else:
            cur.execute('''
            UPDATE client_info
            SET first_name = %s, last_name = %s, email = %s
            WHERE client_id = %s;
            ''', (first_name, last_name, email, client_id))


def delete_phone(conn, client_id, phone):
    pass


def delete_client(conn, client_id):
    pass


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass


with psycopg2.connect(database="netology_db", user="postgres", password=input("Введите пароль: ")) as conn:
    create_db(conn)
    add_client(conn, "Vasia", "Pupkin", "VP@list.ru")
    add_client(conn, "Andrey", "Koval", "AK@list.ru", "+71234567890")
    add_phone(conn, 1, "+79646546362")
    add_phone(conn, 2, "+71112223334")
    change_client(conn, 1, first_name="Nika", last_name="Koval", email="NK@list.ru")
    change_client(conn, 1, last_name="Petrov", email="Petrov@list.ru")