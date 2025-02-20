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
        
        bash
        
        Copy
        
        git clone https://github.com/seu-usuario/seu-repositorio.git
        cd seu-repositorio
        
2. **Subir os Contêineres com Docker Compose**:
    
    - Execute o comando abaixo para subir os contêineres do Kafka e PostgreSQL:
        
        bash
        
        Copy
        
        docker-compose up -d
        
3. **Crie os Tópicos no Kafka**:
    
    - Acesse o contêiner do Kafka:
        
        bash
        
        Copy
        
        docker exec -it kafka1 /bin/bash
        
    - Crie os tópicos `input`, `output` e `training`:
        
        bash
        
        Copy
        
        /opt/kafka/bin/kafka-topics.sh --create --topic input --bootstrap-server kafka1:9092 --partitions 3 --replication-factor 3
        /opt/kafka/bin/kafka-topics.sh --create --topic output --bootstrap-server kafka1:9092 --partitions 3 --replication-factor 3
        /opt/kafka/bin/kafka-topics.sh --create --topic training --bootstrap-server kafka1:9092 --partitions 3 --replication-factor 3
        
4. **Verifique os Tópicos**:
    
    - Liste os tópicos criados:
        
        bash
        
        Copy
        
        /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server kafka1:9092
        

---

### **3. Executando o Sistema**

1. **Gere Transações com o Produtor**:
    
    - Execute o script `producer.py` para gerar transações e enviá-las para o tópico `input`:
        
        bash
        
        Copy
        
        python producer.py
        
2. **Processe Transações com o Consumidor**:
    
    - Execute o script `consumer.py` para consumir transações do tópico `input`, detectar fraudes e armazenar as transações suspeitas no PostgreSQL:
        
        bash
        
        Copy
        
        python consumer.py
        
3. **Verifique as Transações Suspeitas**:
    
    - Acesse o banco de dados PostgreSQL para verificar as transações suspeitas armazenadas:
        
        bash
        
        Copy
        
        docker exec -it postgres psql -U admin -d fraud_detection
        
    - Consulte a tabela `fraudulent_transactions`:
        
        sql
        
        Copy
        
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