
Olá, esse é um projeto simples de carregar uma base de dados no HIVE utilizando a cloud GCP
Passo a passo a seguir:


### Pré-requisitos
1. **Google Cloud SDK e Cloud Code**: Certifique-se de que o Google Cloud SDK (`gcloud`) e Cloud Code esteja instalado e configurado no seu sistema.
2. **VS Code**: Tenha o Visual Studio Code instalado.
3. **Extensão Remote - SSH**: No VS Code, instale a extensão de SSH da google
4. **Permissões de Acesso**: Certifique-se de ter permissões adequadas para acessar o cluster GCP via SSH.
#### Etapas iniciais
1. Crie uma conta GCP
2. Crie um bucket GCP (esse será usado para fazer upload dos arquivos locais pra cloud.)
3. Crie um Cluster
  

Faça login no terminal:
```
gcloud auth login
```

Pegue o caminho do bucket no console da GCP
Comando no terminal para fazer upload dos arquivos locais no bucket GCP

```
gsutil cp caminho/dos/arquivos/locais gs://pos-graduacao/Olimpiadas/
```

No nosso exemplo o bucket tem o caminho /pos-graduacao/Olimpiadas/


Para conectar a um cluster GCP via SSH usando o VS Code, você pode seguir os passos abaixo:

### Passos para Conectar via SSH pelo VS Code

1. **Configurar o Acesso SSH ao Cluster GCP**:
   - Abra o terminal e use o comando `gcloud` para configurar o acesso SSH ao seu cluster:
     ```bash
     gcloud compute ssh <nome-da-instância> --zone=<zona-do-cluster>
     ```
   - Este comando configurará o arquivo `~/.ssh/config` com as informações necessárias para conectar à instância.

2. **Configurar o Remote - SSH no VS Code**:
   - No VS Code, pressione `Ctrl + Shift + P` (ou `Cmd + Shift + P` no Mac) para abrir a paleta de comandos.
   - Digite e selecione `Remote-SSH: Add New SSH Host`.
   - Cole a configuração SSH do seu cluster GCP que foi criada no passo anterior, ou adicione manualmente no formato:
     ```
     Host <nome-do-cluster>
         HostName <endereço-ip-ou-dns>
         User <nome-do-usuário>
         IdentityFile <caminho-para-sua-chave-privada>
     ```
   - Salve as configurações no arquivo `~/.ssh/config`.
## Conectando ao cluster
1. **Obtenha o IP do seu cluster:**
    
    - Use o comando `gcloud` para obter o IP externo do seu cluster
        
        `gcloud compute instances list --filter="name=('cluster-hadoop-m')" --format="get(networkInterfaces[0].accessConfigs[0].natIP)"`
        
    - Anote o IP externo do seu cluster.

- **Edite o arquivo de configuração SSH (`~/.ssh/config`):**
    
    - Abra o arquivo de configuração SSH em um editor de texto
        
    - Adicione a configuração manualmente. Supondo que o IP do seu cluster é `34.123.456.78`, o arquivo deve ficar assim:

        `Host cluster-hadoop   HostName 34.123.456.78   User [seu usuário GCP]   IdentityFile [caminho para sua chave SSH, geralmente ~/.ssh/google_compute_engine]   StrictHostKeyChecking no`
        
    
    Substitua `[seu usuário GCP]` pelo seu nome de usuário do GCP e `[caminho para sua chave SSH]` pelo caminho correto da sua chave SSH. O caminho padrão é geralmente `~/.ssh/google_compute_engine`.
    
    
Depois de editar o arquivo de configuração SSH, siga estes passos:

1. **Teste a conexão SSH manualmente:**
    
    - No terminal, digite:
        
        `ssh cluster-hadoop`
        
    - Isso deve se conectar ao seu cluster Hadoop.
2. **Conecte-se ao cluster pelo VS Code:**
    
    - Abra o VS Code.
    - Pressione `Ctrl+Shift+P` para abrir a paleta de comandos.
    - Digite `Remote-SSH: Connect to Host...` e selecione `cluster-hadoop`.



### **Verifique o Caminho do Bucket e dos Arquivos**

Certifique-se de que o caminho do bucket e dos arquivos está correto. No seu caso, verifique se o caminho `gs://pos-graduacao/Olimpiadas/ realmente existe e contém arquivos.

Para listar o conteúdo do bucket, use o seguinte comando:
```sh
gsutil ls gs://pos-graduacao/Olimpiadas/
```
Isso mostrará todos os diretórios e arquivos disponíveis no bucket.

```
gs://pos-graduacao/Olimpiadas/olympic_athletes.csv 
gs://pos-graduacao/Olimpiadas/olympic_hosts.csv 
gs://pos-graduacao/Olimpiadas/olympic_medals.csv 
gs://pos-graduacao/Olimpiadas/olympic_results.csv
```

Digite o comando `hive

Ótimo! Agora que você está no prompt do Hive (`hive>`), você pode executar diretamente os comandos SQL necessários para criar as tabelas. Aqui estão os comandos novamente para você executar um por um:

### Comandos SQL para criação das Tabelas


1. **Criação do Database e Uso do Database**:
   ```sql
   CREATE DATABASE IF NOT EXISTS olympics;
   USE olympics;
   ```

2. **Criação da Tabela `olympic_athletes`**:
   ```sql
   CREATE TABLE IF NOT EXISTS olympic_athletes (
     athlete_url STRING,
     athlete_full_name STRING,
     games_participations INT,
     first_game STRING,
     athlete_year_birth INT,
     athlete_medals INT,
     bio STRING
   )
   ROW FORMAT DELIMITED
   FIELDS TERMINATED BY ','
   STORED AS TEXTFILE;
   ```

3. **Criação da Tabela `olympic_medals`**:
   ```sql
   CREATE TABLE IF NOT EXISTS olympic_medals (
     discipline_title STRING,
     slug_game STRING,
     event_title STRING,
     event_gender STRING,
     medal_type STRING,
     participant_type STRING,
     participant_title STRING,
     athlete_url STRING,
     athlete_full_name STRING,
     country_name STRING,
     country_code STRING,
     country_3_letter_code STRING
   )
   ROW FORMAT DELIMITED
   FIELDS TERMINATED BY ','
   STORED AS TEXTFILE;
   ```

4. **Criação da Tabela `olympic_hosts`**:
   ```sql
   CREATE TABLE IF NOT EXISTS olympic_hosts (
     game_slug STRING,
     game_end_date STRING,
     game_start_date STRING,
     game_location STRING,
     game_name STRING,
     game_season STRING,
     game_year INT
   )
   ROW FORMAT DELIMITED
   FIELDS TERMINATED BY ','
   STORED AS TEXTFILE;
   ```

5. **Criação da Tabela `olympic_result`**:
   ```sql
   CREATE TABLE IF NOT EXISTS olympic_result (
     discipline_title STRING,
     event_title STRING,
     slug_game STRING,
     participant_type STRING,
     medal_type STRING,
     athletes STRING,
     rank_equal INT,
     rank_position INT,
     country_name STRING,
     country_code STRING,
     country_3_letter_code STRING,
     athlete_url STRING,
     athlete_full_name STRING,
     value_unit STRING,
     value_type STRING
   )
   ROW FORMAT DELIMITED
   FIELDS TERMINATED BY ','
   STORED AS TEXTFILE;
   ```

### Passos:

1. **Digite cada comando no prompt do Hive** e pressione `Enter`. Por exemplo:
   ```sql
   hive> CREATE DATABASE IF NOT EXISTS olympics;
   hive> USE olympics;
   hive> CREATE TABLE IF NOT EXISTS olympic_athletes (
     athlete_url STRING,
     athlete_full_name STRING,
     games_participations INT,
     first_game STRING,
     athlete_year_birth INT,
     athlete_medals INT,
     bio STRING
   )
   ROW FORMAT DELIMITED
   FIELDS TERMINATED BY ','
   STORED AS TEXTFILE;
   ```
   Repita isso para cada tabela.

2. **Verifique se as tabelas foram criadas corretamente**:
   ```sql
   hive> SHOW TABLES;
   ```

Isso deve listar todas as tabelas que você criou no database `olympics`.

# Importando arquivos
### 1. **Copiar os Arquivos do GCS para o Diretório Temporário no Cluster**

Use `gsutil` para copiar os arquivos para um diretório temporário no seu cluster Hadoop. No terminal do cluster, execute:

```sh
# Criar diretórios temporários para os arquivos
mkdir -p /tmp/olympics

# Copiar os arquivos do GCS para o diretório temporário
gsutil cp gs://pos-graduacao/Olimpiadas/olympic_athletes.csv /tmp/olympics/
gsutil cp gs://pos-graduacao/Olimpiadas/olympic_hosts.csv /tmp/olympics/
gsutil cp gs://pos-graduacao/Olimpiadas/olympic_medals.csv /tmp/olympics/
gsutil cp gs://pos-graduacao/Olimpiadas/olympic_results.csv /tmp/olympics/
```

### 2. **Mover os Arquivos para o HDFS**

Depois de copiar os arquivos para o diretório temporário, mova-os para o HDFS. Execute os seguintes comandos:

```sh
# Criar diretórios no HDFS
hdfs dfs -mkdir -p /user/hive/warehouse/olympics/athletes
hdfs dfs -mkdir -p /user/hive/warehouse/olympics/hosts
hdfs dfs -mkdir -p /user/hive/warehouse/olympics/medals
hdfs dfs -mkdir -p /user/hive/warehouse/olympics/results

# Mover os arquivos para o HDFS
hdfs dfs -put /tmp/olympics/olympic_athletes.csv /user/hive/warehouse/olympics/athletes/
hdfs dfs -put /tmp/olympics/olympic_hosts.csv /user/hive/warehouse/olympics/hosts/
hdfs dfs -put /tmp/olympics/olympic_medals.csv /user/hive/warehouse/olympics/medals/
hdfs dfs -put /tmp/olympics/olympic_results.csv /user/hive/warehouse/olympics/results/
```

### 3. **Carregar os Dados nas Tabelas do Hive**

Agora que os arquivos estão no HDFS, você pode carregar os dados nas tabelas do Hive. No prompt do Hive (`hive>`), execute os seguintes comandos:

```sql
-- Usar o database olympics
USE olympics;

-- Carregar dados na tabela olympic_athletes
LOAD DATA INPATH '/user/hive/warehouse/olympics/athletes/olympic_athletes.csv' INTO TABLE olympic_athletes;

-- Carregar dados na tabela olympic_medals
LOAD DATA INPATH '/user/hive/warehouse/olympics/medals/olympic_medals.csv' INTO TABLE olympic_medals;

-- Carregar dados na tabela olympic_hosts
LOAD DATA INPATH '/user/hive/warehouse/olympics/hosts/olympic_hosts.csv' INTO TABLE olympic_hosts;

-- Carregar dados na tabela olympic_result
LOAD DATA INPATH '/user/hive/warehouse/olympics/results/olympic_results.csv' INTO TABLE olympic_result;
```

### Resumo dos Passos

1. **Copiar os arquivos do GCS para o diretório temporário no cluster**.
2. **Mover os arquivos para o HDFS**.
3. **Carregar os dados nas tabelas do Hive**.

Esses passos devem garantir que seus dados estejam carregados corretamente no Hive. Se encontrar algum erro, verifique os caminhos e permissões para garantir que tudo esteja configurado corretamente.

Claro! Vou ajustar as consultas conforme suas novas instruções:

# Consultas SQL para analises
### 1. Pergunta: **Quais são os 3 países que ganharam mais medalhas em cada evento dos Jogos Olímpicos desde o início?**

#### Consulta SQL:
```sql
WITH ranked_medals AS (
    SELECT h.game_year, h.game_location, m.event_title, m.country_name, COUNT(*) AS total_medals,
           RANK() OVER (PARTITION BY h.game_year, h.game_location, m.event_title ORDER BY COUNT(*) DESC) AS rnk
    FROM olympic_medals m
    JOIN olympic_hosts h ON m.slug_game = h.game_slug
    GROUP BY h.game_year, h.game_location, m.event_title, m.country_name
)
SELECT game_year, game_location, event_title, country_name, total_medals
FROM ranked_medals
WHERE rnk <= 3
ORDER BY game_year, game_location, event_title, rnk;
```

#### Resposta:
Esta consulta retorna os 3 países que ganharam mais medalhas em cada evento dos Jogos Olímpicos, listados por ano e local dos Jogos.

---

### 2. Pergunta: **Qual é a média de medalhas ganhas pelos atletas de cada país em todas as edições dos Jogos Olímpicos, agrupadas pelo ano dos Jogos e país anfitrião?**

#### Consulta SQL:
```sql
SELECT h.game_year, h.game_location, m.country_name, AVG(m.medal_count) AS avg_medals
FROM (
    SELECT h.game_year, h.game_location, m.country_name, COUNT(*) AS medal_count
    FROM olympic_medals m
    JOIN olympic_hosts h ON m.slug_game = h.game_slug
    GROUP BY h.game_year, h.game_location, m.country_name, m.slug_game
) m
GROUP BY h.game_year, h.game_location, m.country_name
ORDER BY h.game_year, avg_medals DESC;
```

#### Resposta:
Esta consulta calcula a média de medalhas ganhas por atletas de cada país em cada ano dos Jogos Olímpicos, agrupada pelo ano dos Jogos e país anfitrião.

---

### 3. Pergunta: **Qual o desempenho médio dos países anfitriões em termos de medalhas ganhas, e como isso varia ao longo dos anos?**

#### Consulta SQL:
```sql
SELECT h.game_year, h.game_location, AVG(m.total_medals) AS avg_medals
FROM (
    SELECT h.game_year, h.game_location, m.country_name, COUNT(*) AS total_medals
    FROM olympic_medals m
    JOIN olympic_hosts h ON m.slug_game = h.game_slug
    GROUP BY h.game_year, h.game_location, m.country_name
) m
GROUP BY h.game_year, h.game_location
ORDER BY h.game_year;
```

#### Resposta:
Esta consulta calcula a média de medalhas ganhas pelos países anfitriões ao longo dos anos, mostrando como o desempenho dos anfitriões varia ao longo do tempo.

---

### 4. Pergunta: **Quais são as médias de medalhas por evento de cada país desde o início dos Jogos Olímpicos, agrupadas por ano da edição dos Jogos?**

#### Consulta SQL:
```sql
SELECT h.game_year, r.event_title, m.country_name, AVG(m.total_medals) AS avg_medals
FROM (
    SELECT h.game_year, r.event_title, m.country_name, COUNT(*) AS total_medals
    FROM olympic_result r
    JOIN olympic_medals m ON r.athlete_url = m.athlete_url
    JOIN olympic_hosts h ON r.slug_game = h.game_slug
    GROUP BY h.game_year, r.event_title, m.country_name
) m
GROUP BY h.game_year, r.event_title, m.country_name
ORDER BY h.game_year, avg_medals DESC;
```

#### Resposta:
Essa consulta fornece as médias de medalhas conquistadas por evento para cada país, agrupadas pelo ano da edição dos Jogos Olímpicos, mostrando como as médias variam por ano e evento.

---

### 5. Pergunta: **Como o número de medalhas conquistadas por atletas varia com a idade durante os Jogos Olímpicos, agrupado por faixa etária?**

#### Consulta SQL:
```sql
SELECT h.game_year, CONCAT(FLOOR((h.game_year - a.athlete_year_birth) / 5) * 5, '-', FLOOR((h.game_year - a.athlete_year_birth) / 5) * 5 + 4) AS age_group, COUNT(*) AS medals_count FROM olympic_athletes a JOIN olympic_medals m ON a.athlete_url = m.athlete_url JOIN olympic_hosts h ON m.slug_game = h.game_slug GROUP BY h.game_year, age_group ORDER BY h.game_year, age_group;
```

#### Resposta:

Essa consulta calcula o número total de medalhas conquistadas por atletas, agrupado por faixa etária (por exemplo, 20-24 anos, 25-29 anos), considerando a diferença entre o ano dos Jogos Olímpicos e o ano de nascimento dos atletas, e organiza os resultados por ano dos Jogos e faixa etária.

---
# Pontos de melhoria
Buscar uma database que possua a renda per capita dos paises poderia dar um insight profundo entre o investimento no esporte e a quantidade de medalhas.