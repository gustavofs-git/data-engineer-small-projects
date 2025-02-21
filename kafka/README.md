
# Sistema de Detecção de Fraude em Tempo Real para Transações com Cartão de Crédito

#### A parte teorica e a parte pratica podem ser acessadas em: [data-engineer-small-projects/kafka at main · gustavofs-git/data-engineer-small-projects](https://github.com/gustavofs-git/data-engineer-small-projects/tree/main/kafka) devido ao pedido do moodle de enviar como pdf o conversor que eu usei tanto a imagem quanto os textos ficaram mal formatados. Voce consegue encontrar uma versao mais bem apresentada no repositorio acima.


## Parte teórica

## **1. Introdução**

O aumento das transações digitais e o uso massivo de cartões de crédito trouxeram consigo um crescimento significativo em tentativas de fraudes. Para mitigar esses riscos, é essencial contar com um sistema capaz de detectar atividades suspeitas em tempo real, garantindo a segurança das transações e a confiança dos usuários.

Este projeto propõe a criação de um **Sistema de Detecção de Fraude em Tempo Real**, utilizando tecnologias modernas como **Apache Kafka**, **Apache Flink**, **PostgreSQL** e **Machine Learning**. O sistema é projetado para analisar transações de cartão de crédito, identificar comportamentos suspeitos e fornecer respostas imediatas, além de atualizar dinamicamente as regras de detecção de fraude.

![[kafka.drawio 1.png]]
---

## **2. Objetivos**

O sistema tem como principais objetivos:

1. **Detectar fraudes em tempo real**:
    - Identificar transações suspeitas com base em regras de negócio e histórico de fraudes.
    - Utilizar Machine Learning para detectar padrões de comportamento suspeitos em transações sem histórico de fraude.
2. **Fornecer resposta imediata**:
    - Bloquear transações fraudulentas e notificar os usuários ou sistemas envolvidos.
3. **Atualizar dinamicamente as regras de detecção**:
    - Alimentar a lista de bloqueio com novos padrões de fraude identificados pelo modelo de Machine Learning.
4. **Garantir escalabilidade e disponibilidade**:
    - Suportar até 10 mil transações por segundo (TPS) e garantir 99,9% de uptime.

---

## **3. Justificativa**

A detecção de fraudes em tempo real é crítica para:

- **Reduzir perdas financeiras**: Bloquear transações fraudulentas antes que sejam concluídas.
- **Proteger a reputação da empresa**: Evitar que usuários sejam vítimas de fraudes, mantendo a confiança no sistema.
- **Atender a requisitos regulatórios**: Cumprir normas de segurança e proteção de dados.

A escolha de tecnologias como **Kafka**, **Flink** e **PostgreSQL** se deve à sua capacidade de processar grandes volumes de dados em tempo real, garantindo escalabilidade, baixa latência e alta disponibilidade.

---

## **4. Arquitetura do Sistema**

### **4.1. Diagrama de Arquitetura**

A arquitetura do sistema é composta pelos seguintes componentes:

1. **Gerador de Transações**:
    - Simula transações de cartão de crédito e as envia para o Kafka.

2. **Apache Kafka**:
    - **Tópico de Entrada**: Recebe transações do gerador.
    - **Tópico de Saída**: Envia transações fraudulentas para o módulo de resposta imediata.
    - **Tópico de Treinamento**: Envia transações não fraudulentas para o modelo de Machine Learning.

3. **Apache Flink**:
    - Processa transações em tempo real, aplica regras de negócio e consulta o PostgreSQL para verificar fraudes conhecidas.
    - Envia transações suspeitas para o **Tópico de Saída** e transações válidas para o **Tópico de Treinamento**.

4. **PostgreSQL**:
    - Armazena a lista de bloqueio (cartões, usuários e sites fraudulentos) e dados históricos de transações.
    - Fornece dados adicionais para o treinamento do modelo de Machine Learning.

5. **Modelo de Machine Learning**:
    - Consome transações do **Tópico de Treinamento** e dados históricos do PostgreSQL.
    - Treina um modelo para detectar novos padrões de fraude e atualiza a lista de bloqueio no PostgreSQL.
    
6. **Módulo de Resposta Imediata**:
    - Consome transações fraudulentas do **Tópico de Saída** e toma ações como bloquear a transação e notificar o usuário.
    
7. **Monitoramento**:
    - Coleta métricas de desempenho e saúde do sistema, como latência, taxa de processamento e disponibilidade.


### **4.2. Fluxo de Dados**

1. **Transações** são geradas e enviadas para o **Tópico de Entrada** do Kafka.
2. O **Apache Flink** consome as transações, aplica regras de negócio e consulta o **PostgreSQL** para verificar fraudes conhecidas.
3. Transações suspeitas são enviadas para o **Tópico de Saída**, enquanto transações válidas vão para o **Tópico de Treinamento**.
4. O **Modelo de Machine Learning** consome transações do **Tópico de Treinamento** e dados históricos do PostgreSQL para treinar e atualizar a lista de bloqueio.
5. O **Módulo de Resposta Imediata** bloqueia transações fraudulentas e notifica os usuários.
6. O sistema é monitorado em tempo real pelo **Prometheus**, que coleta métricas e envia alertas em caso de problemas.

---

## **5. Tecnologias Utilizadas**

### **5.1. Apache Kafka**

- **Função**: Atua como o barramento de mensagens central, garantindo a ingestão e distribuição de transações em tempo real.
- **Benefícios**: Alta escalabilidade, baixa latência e tolerância a falhas.
### **5.2. Apache Flink**

- **Função**: Processa transações em tempo real, aplica regras de negócio e integra-se ao PostgreSQL para consultas de fraudes conhecidas.
- **Benefícios**: Processamento de streams com baixa latência e suporte a stateful computations.

### **5.3. PostgreSQL**

- **Função**: Armazena a lista de bloqueio, dados históricos de transações e metadados de usuários e estabelecimentos.
- **Benefícios**: Confiabilidade, suporte a consultas complexas e integração com ferramentas de análise.

### **5.4. Machine Learning**

- **Função**: Detecta novos padrões de fraude em transações sem histórico suspeito.
- **Benefícios**: Aprendizado contínuo com novos dados, melhorando a precisão da detecção ao longo do tempo.

### **5.5. Prometheus**

- **Função**: Coleta métricas de desempenho e saúde do sistema em tempo real.
- **Benefícios**: Integração com Grafana para visualização de dashboards e alertas proativos.

---

## **6. Casos de Uso**

### **6.1. Transação Fraudulenta Conhecida**

1. Uma transação é enviada para o Kafka.
2. O Flink consulta o PostgreSQL e identifica que o cartão ou usuário está na lista de bloqueio.
3. A transação é enviada para o **Tópico de Saída**.
4. O **Módulo de Resposta Imediata** bloqueia a transação e notifica o usuário.

### **6.2. Transação Suspeita (Detectada por ML)**

1. Uma transação é enviada para o Kafka.
2. O Flink não encontra correspondência na lista de bloqueio e a envia para o **Tópico de Treinamento**.
3. O **Modelo de Machine Learning** identifica um padrão suspeito e atualiza a lista de bloqueio no PostgreSQL.
4. Transações futuras com padrões semelhantes serão bloqueadas automaticamente.

### **6.3. Transação Válida**

1. Uma transação é enviada para o Kafka.
2. O Flink verifica que a transação é válida e a envia para o **Tópico de Treinamento**.
3. O **Modelo de Machine Learning** utiliza a transação para treinamento, melhorando sua precisão.

---

## **7. Pontos Únicos de Falha (SPOFs) e Mitigações**

### **7.1. Kafka**
- **Risco de SPOF**: Falha de um broker pode parar o sistema.
- **Mitigação**: Configurar um cluster Kafka com múltiplos brokers e réplicas de tópicos.

### **7.2. Flink**
- **Risco de SPOF**: Falha do JobManager pode interromper o processamento.
- **Mitigação**: Configurar o Flink em modo alta disponibilidade (HA) com múltiplos JobManagers.

### **7.3. PostgreSQL**
- **Risco de SPOF**: Falha do banco de dados pode parar o sistema.
- **Mitigação**: Configurar um cluster PostgreSQL com replicação síncrona ou usar um banco de dados gerenciado em nuvem.

### **7.4. Machine Learning Model**
- **Risco de SPOF**: Falha do serviço de inferência pode impedir a detecção de fraudes.
- **Mitigação**: Hospedar o modelo em Kubernetes com múltiplas réplicas e implementar fallback para regras de negócio.

### **7.5. Módulo de Resposta Imediata**
- **Risco de SPOF**: Falha do módulo pode impedir o bloqueio de transações fraudulentas.
- **Mitigação**: Implementar múltiplas instâncias com balanceamento de carga e usar filas para garantir processamento.

### **7.6. Prometheus**
- **Risco de SPOF**: Falha do sistema de monitoramento pode impedir a detecção de problemas.
- **Mitigação**: Configurar o Prometheus em modo alta disponibilidade (HA) ou usar um serviço gerenciado como Datadog.

---

## Parte pratica
# Sistema de Detecção de Fraudes em Tempo Real com Kafka e PostgreSQL

Este projeto implementa um sistema de detecção de fraudes em tempo real usando Apache Kafka para processamento de transações financeiras e PostgreSQL para armazenamento de transações suspeitas. O sistema consome transações de um tópico Kafka, aplica regras de detecção de fraudes e armazena as transações suspeitas em um banco de dados PostgreSQL.

---

## **Tecnologias Utilizadas**

- **Apache Kafka**: Para processamento de transações em tempo real.
    
- **PostgreSQL**: Para armazenamento de transações suspeitas.
    
- **Docker**: Para orquestração de contêineres (Kafka e PostgreSQL).
    
- **Python**: Para implementação do produtor e consumidor Kafka.
    

---

## **Passo a Passo**

### **1. Pré-requisitos**

1. **Instale o Docker**:
    
    - Baixe e instale o Docker Desktop: [Docker Installation Guide](https://docs.docker.com/get-docker/).
        
2. **Instale o Docker Compose**:
    
    - O Docker Compose já vem incluído no Docker Desktop. Se necessário, siga o guia de instalação: [Docker Compose Installation Guide](https://docs.docker.com/compose/install/).
        
3. **Instale o Python**:
    
    - Baixe e instale o Python 3.x: [Python Installation Guide](https://www.python.org/downloads/).
        
4. **Instale as Dependências do Python**:
    
    - No terminal, execute:
        
        bash
        
        Copy
        
        pip install confluent-kafka psycopg2
        

---

### **2. Configuração do Ambiente**

1. **Clone o Repositório**:
    
    - Clone este repositório para o seu ambiente local:
        
2. **Subir os Contêineres com Docker Compose**:
    
    - Execute o comando abaixo para subir os contêineres do Kafka e PostgreSQL:

        docker-compose up -d
        
3. **Crie os Tópicos no Kafka**:
    
    - Acesse o contêiner do Kafka:
        
        docker exec -it kafka1 /bin/bash
        
    - Crie os tópicos `input`, `output` e `training`:
        
        /opt/kafka/bin/kafka-topics.sh --create --topic input --bootstrap-server kafka1:9092 --partitions 3 --replication-factor 3
        /opt/kafka/bin/kafka-topics.sh --create --topic output --bootstrap-server kafka1:9092 --partitions 3 --replication-factor 3
        /opt/kafka/bin/kafka-topics.sh --create --topic training --bootstrap-server kafka1:9092 --partitions 3 --replication-factor 3
        
4. **Verifique os Tópicos**:
    
    - Liste os tópicos criados:
        
        /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server kafka1:9092
        

---

### **3. Executando o Sistema**

1. **Gere Transações com o Produtor**:
    
    - Execute o script `producer.py` para gerar transações e enviá-las para o tópico `input`:

        python producer.py
        
2. **Processe Transações com o Consumidor**:
    
    - Execute o script `consumer.py` para consumir transações do tópico `input`, detectar fraudes e armazenar as transações suspeitas no PostgreSQL:
        
        python consumer.py
        
3. **Verifique as Transações Suspeitas**:
    
    - Acesse o banco de dados PostgreSQL para verificar as transações suspeitas armazenadas:
        
        docker exec -it postgres psql -U admin -d fraud_detection
        
    - Consulte a tabela `fraudulent_transactions`:
        
        SELECT * FROM fraudulent_transactions;

---

### **4. Estrutura do Projeto**

- **`docker-compose.yml`**:
    
    - Configuração dos contêineres Kafka e PostgreSQL.
        
- **`producer.py`**:
    
    - Gera transações financeiras e as envia para o tópico `input` no Kafka.
        
- **`consumer.py`**:
    
    - Consome transações do tópico `input`, aplica regras de detecção de fraudes e armazena transações suspeitas no PostgreSQL.
        
- **`database.py`**:
    
    - Gerencia a conexão com o PostgreSQL e a inserção de transações suspeitas.
        
- **`gen_transaction.py`**:
    
    - Gera transações financeiras válidas e fraudulentas.


### **5. Codes**

docker-compose.yaml:
```
services:

  kafka1:

    image: apache/kafka:latest

    hostname: kafka1

    container_name: kafka1

    ports:

      - "19092:9092"

    networks:

      my_network:

        ipv4_address: 172.20.0.101

    environment:

      KAFKA_NODE_ID: 1

      KAFKA_PROCESS_ROLES: broker,controller

      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093

      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT

      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:19092

      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT

      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER

      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka1:9093,2@kafka2:9093,3@kafka3:9093

      CLUSTER_ID: 'fEhAzqLPS8aklU4iXPqqbA'

      KAFKA_LOG_DIRS: /tmp/kafka/data

    volumes:

      - ./kafka-data1:/tmp/kafka/data

  

  kafka2:

    image: apache/kafka:latest

    hostname: kafka2

    container_name: kafka2

    ports:

      - "29092:9092"

    networks:

      my_network:

        ipv4_address: 172.20.0.102

    environment:

      KAFKA_NODE_ID: 2

      KAFKA_PROCESS_ROLES: broker,controller

      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093

      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT

      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:29092

      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT

      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER

      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka1:9093,2@kafka2:9093,3@kafka3:9093

      CLUSTER_ID: 'fEhAzqLPS8aklU4iXPqqbA'

      KAFKA_LOG_DIRS: /tmp/kafka/data

    volumes:

      - ./kafka-data2:/tmp/kafka/data

  

  kafka3:

    image: apache/kafka:latest

    hostname: kafka3

    container_name: kafka3

    ports:

      - "39092:9092"

    networks:

      my_network:

        ipv4_address: 172.20.0.103

    environment:

      KAFKA_NODE_ID: 3

      KAFKA_PROCESS_ROLES: broker,controller

      KAFKA_LISTENERS: PLAINTEXT://:9092,CONTROLLER://:9093

      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT

      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:39092

      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT

      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER

      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka1:9093,2@kafka2:9093,3@kafka3:9093

      CLUSTER_ID: 'fEhAzqLPS8aklU4iXPqqbA'

      KAFKA_LOG_DIRS: /tmp/kafka/data

    volumes:

      - ./kafka-data3:/tmp/kafka/data

  

  postgres:

    image: postgres:latest

    container_name: postgres

    environment:

      POSTGRES_USER: admin

      POSTGRES_PASSWORD: admin

      POSTGRES_DB: fraud_detection

    ports:

      - "5432:5432"

    volumes:

      - ./postgres-data:/var/lib/postgresql/data

    networks:

      my_network:

        ipv4_address: 172.20.0.104

  

networks:

  my_network:

    name: kafka-network

    ipam:

      config:

        - subnet: 172.20.0.0/16

          gateway: 172.20.0.1



```

producer.py

```
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
```

consumer.py
```

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

    amount = transaction['value']  # Certifique-se de que o campo está correto

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

        print(f"Transação recebida: {transaction}")  # Debug: Verifique o formato da transação

        fraud_type = detect_fraud(transaction)

  

        # Se for uma fraude, armazena no banco de dados

        if fraud_type:

            print(f"Fraude detectada: {fraud_type} - {transaction}")

            insert_fraudulent_transaction(transaction, fraud_type)

  

except KeyboardInterrupt:

    pass

finally:

    consumer.close()
```


database.py

```
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
```