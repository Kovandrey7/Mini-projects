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
            client_id INTEGER NOT NULL REFERENCES client_info(client_id),
            phone VARCHAR(20) UNIQUE NOT NULL
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

        conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        if first_name is not None and last_name is None and email is None and phone is None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.first_name = %s
                ORDER BY ci.client_id ASC;
            """, (first_name,))

        elif first_name is None and last_name is not None and email is None and phone is None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.last_name = %s
                ORDER BY ci.client_id ASC;
            """, (last_name,))

        elif first_name is None and last_name is None and email is not None and phone is None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.email = %s
                ORDER BY ci.client_id ASC;
            """, (email,))

        elif first_name is None and last_name is None and email is None and phone is not None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE cp.phone = %s
                ORDER BY ci.client_id ASC;
            """, (phone,))

        elif first_name is not None and last_name is not None and email is None and phone is None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.first_name = %s and ci.last_name = %s
                ORDER BY ci.client_id ASC;
            """, (first_name, last_name))

        elif first_name is not None and last_name is None and email is not None and phone is None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.first_name = %s and ci.email = %s
                ORDER BY ci.client_id ASC;
            """, (first_name, email))

        elif first_name is not None and last_name is None and email is None and phone is not None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.first_name = %s and cp.phone = %s
                ORDER BY ci.client_id ASC;
            """, (first_name, phone))

        elif first_name is None and last_name is not None and email is not None and phone is None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.last_name = %s and ci.email = %s
                ORDER BY ci.client_id ASC;
            """, (last_name, email))

        elif first_name is None and last_name is not None and email is None and phone is not None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.last_name = %s and cp.phone = %s
                ORDER BY ci.client_id ASC;
            """, (last_name, phone))

        elif first_name is None and last_name is None and email is not None and phone is not None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.email = %s and cp.phone = %s
                ORDER BY ci.client_id ASC;
            """, (email, phone))

        elif first_name is not None and last_name is not None and email is not None and phone is None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.first_name = %s and ci.last_name = %s and ci.email = %s
                ORDER BY ci.client_id ASC;
            """, (first_name, last_name, email))

        elif first_name is not None and last_name is not None and email is None and phone is not None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.first_name = %s and ci.last_name = %s and cp.phone = %s
                ORDER BY ci.client_id ASC;
            """, (first_name, last_name, phone))

        elif first_name is not None and last_name is None and email is not None and phone is not None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.first_name = %s and ci.email = %s and cp.phone = %s
                ORDER BY ci.client_id ASC;
            """, (first_name, email, phone))

        elif first_name is None and last_name is not None and email is not None and phone is not None:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.last_name = %s and ci.email = %s and cp.phone = %s
                ORDER BY ci.client_id ASC;
            """, (last_name, email, phone))

        else:
            cur.execute("""
                SELECT ci.client_id, ci.first_name, ci.last_name, ci.email, cp.phone 
                FROM client_info ci
                LEFT JOIN client_phone cp ON cp.client_id = ci.client_id
                WHERE ci.first_name = %s and ci.last_name = %s and ci.email = %s and cp.phone = %s
                ORDER BY ci.client_id ASC;
            """, (first_name ,last_name, email, phone))

        print(cur.fetchall())


with psycopg2.connect(database="netology_db", user="postgres", password=input("Введите пароль: ")) as conn:
    # delete_tables(conn)
    create_db(conn)
    add_client(conn, "Vasia", "Pupkin", "VP@list.ru")
    add_client(conn, "Andrey", "Koval", "AK@list.ru", "+71234567890")
    add_client(conn, "Andrey", "Fedorov", "AF@list.ru", "+79874562321")
    add_client(conn, "Peter", "Parker", "spider-man@list.ru", "+71236548789")
    add_phone(conn, 1, "+79646546362")
    add_phone(conn, 2, "+71112223334")
    change_client(conn, 1, first_name="Nika", last_name="Koval", email="NK@list.ru")
    change_client(conn, 1, last_name="Petrov", email="Petrov@list.ru")
    # delete_phone(conn, 2,"+71234567890")
    # delete_client(conn, 2)
    find_client(conn, "Andrey")
    find_client(conn, "Peter", "Parker", "spider-man@list.ru")
    find_client(conn, "Andrey", "Koval", "AK@list.ru", "+71112223334")
