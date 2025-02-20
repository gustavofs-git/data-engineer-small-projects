import psycopg2
from psycopg2 import sql

# Configuração do PostgreSQL
def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="fraud_detection",
            user="admin",
            password="admin",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

# Cria a tabela de transações suspeitas
def create_table():
    conn = get_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            # Tabela de transações suspeitas
            cur.execute("""
                CREATE TABLE IF NOT EXISTS fraudulent_transactions (
                    id SERIAL PRIMARY KEY,
                    user_id INT,
                    transaction_id INT,
                    amount FLOAT,
                    timestamp BIGINT,
                    country VARCHAR(50),
                    fraud_type VARCHAR(50),
                    site_id INT
                )
            """)
        conn.commit()
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        conn.close()

# Insere uma transação suspeita no banco de dados
def insert_fraudulent_transaction(transaction, fraud_type):
    conn = get_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO fraudulent_transactions (user_id, transaction_id, amount, timestamp, country, fraud_type, site_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                transaction['user_id'],
                transaction['transaction_id'],
                transaction['value'],
                transaction['timestamp'],
                transaction['country'],
                fraud_type,
                transaction['site_id']
            ))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir transação suspeita: {e}")
    finally:
        conn.close()