
# Sistema de Detecção de Fraude em Tempo Real para Transações com Cartão de Crédito
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

