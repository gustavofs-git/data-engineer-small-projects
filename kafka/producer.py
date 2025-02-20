from confluent_kafka import Producer
import json
from gen_transaction import TransactionGenerator

# Configuração do produtor Kafka
conf = {
    'bootstrap.servers': 'localhost:19092',
    'client.id': 'python-producer'
}

producer = Producer(conf)

# Função para enviar mensagens
def send_message(topic, message):
    producer.produce(topic, value=json.dumps(message))
    producer.flush()

# Gera transações e envia para o Kafka
transaction_generator = TransactionGenerator(trans_per_sec=10)
for tx in transaction_generator.generate_transactions():
    tx_dict = {
        'timestamp': tx.timestamp,
        'transaction_id': tx.transaction_id,
        'user_id': tx.user_id,
        'card_id': tx.card_id,
        'site_id': tx.site_id,
        'value': tx.value,
        'location_id': tx.location_id,
        'country': tx.country
    }
    send_message('input', tx_dict)
    print(f"Enviado: {tx_dict}")