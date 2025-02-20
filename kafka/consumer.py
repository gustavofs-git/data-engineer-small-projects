from confluent_kafka import Consumer, KafkaError
import json
from datetime import datetime, timedelta
from database import insert_fraudulent_transaction

# Configuração do consumidor
conf_consumer = {
    'bootstrap.servers': 'localhost:19092',
    'group.id': 'fraud-detection-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf_consumer)

# Dicionário para armazenar o histórico de transações por usuário
user_history = {}

# Função para aplicar as regras de fraude
def detect_fraud(transaction):
    user_id = transaction['user_id']
    amount = transaction['value']  # Certifique-se de que o campo está correto
    timestamp = datetime.fromtimestamp(transaction['timestamp'])
    country = transaction['country']

    if user_id not in user_history:
        user_history[user_id] = {'transactions': [], 'max_amount': 0}

    user_data = user_history[user_id]
    user_transactions = user_data['transactions']
    user_max_amount = user_data['max_amount']

    # Regra 1: Alta Frequência
    if len(user_transactions) > 0:
        last_transaction = user_transactions[-1]
        time_diff = timestamp - last_transaction['timestamp']
        if time_diff < timedelta(minutes=5) and last_transaction['amount'] != amount:
            return "Alta Frequência"

    # Regra 2: Alto Valor
    if amount > 2 * user_max_amount:
        return "Alto Valor"

    # Regra 3: Outro País
    if len(user_transactions) > 0:
        last_country = user_transactions[-1]['country']
        if country != last_country and timestamp - user_transactions[-1]['timestamp'] < timedelta(hours=2):
            return "Outro País"

    # Atualiza o histórico do usuário
    user_transactions.append({'amount': amount, 'timestamp': timestamp, 'country': country})
    if amount > user_max_amount:
        user_data['max_amount'] = amount

    return None

# Consome as mensagens do tópico 'input'
consumer.subscribe(['input'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Processa a transação
        transaction = json.loads(msg.value().decode('utf-8'))
        print(f"Transação recebida: {transaction}")  # Debug: Verifique o formato da transação
        fraud_type = detect_fraud(transaction)

        # Se for uma fraude, armazena no banco de dados
        if fraud_type:
            print(f"Fraude detectada: {fraud_type} - {transaction}")
            insert_fraudulent_transaction(transaction, fraud_type)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()