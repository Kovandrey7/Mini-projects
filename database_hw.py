import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        DROP TABLE client_phone;
        DROP TABLE client_info;
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS client_info(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email VARCHAR(80) UNIQUE NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS client_phone(
            client_id INTEGER NOT NULL REFERENCES client_info(client_id),
            phone VARCHAR(20) UNIQUE NOT NULL
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
                INSERT INTO client_info(first_name, last_name, email)
                VALUES
                    (%s, %s, %s) RETURNING client_id, first_name, last_name;
                """, (first_name, last_name, email))

            print(cur.fetchone())

            cur.execute("""
                SELECT client_id FROM client_info
                WHERE email = %s;
            """, (email,))
            client_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO client_phone(client_id, phone)
                VALUES
                    (%s, %s) RETURNING client_id, phone;
            """, (client_id, phone))

            print(cur.fetchone())


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client_phone
            VALUES
                (%s, %s) RETURNING client_id, phone;
        """, (client_id, phone))

        print(cur.fetchone())


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

        conn.commit()


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client_phone
            WHERE client_id = %s and phone = %s;
        """, (client_id, phone))

        conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client_phone
            WHERE client_id = %s;
            
            DELETE FROM client_info
            WHERE client_id = %s;         
        """, (client_id, client_id))


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
    delete_phone(conn, 2,"+71234567890")
    delete_client(conn, 2)