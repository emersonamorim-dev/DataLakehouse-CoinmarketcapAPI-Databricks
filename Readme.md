# Data Lakehouse Coinmarketcap - Databricks

Codificação em Python com Framework Streamlit e Flask este aplicação completa de Data Lakehouse usando a API da Coinmarketcap usando o  Databricks extrair os dados. Essa aplicação foi projetado para processar e visualizar dados em uma arquitetura Data Lakehouse multicamadas usando Streamlit para Dashboard, MongoDB como banco de dados e um pipeline estruturado para processos ETL (Extrair, Transformar, Carregar).

## Estrutura de diretório

Aqui está uma visão geral da estrutura de diretórios:

- `airflow/` - Contém DAGs Apache Airflow para gerenciamento de fluxo de trabalho.
- `dashboard/` - Arquivos do painel Streamlit.
- `dados/`
   - `bronze/` - Dados brutos ingeridos no data lake.
   - `silver/` - Dados intermediários processados.
   - `gold/` - Dados finais processados prontos para análise.
- `databricks/`
   - `jobs/` - Configurações de trabalho para Databricks.
   - `notebooks/` - Notebooks Databricks para processamento de dados.
- `datalake/` - Contém camadas de dados estruturados correspondentes a bronze, prata e ouro.
- `docker/` - Arquivos Docker para conteinerização.
- `env/` - Arquivos de ambiente para configuração.
- `jupyter/notebook/` - Notebooks Jupyter para processamento e exploração de dados.
- `kubernetes/` - Arquivos de configuração do Kubernetes.
- `logs/` - Logs do aplicativo e serviços.
- `pipeline/`
   - `agregado/` - Scripts de agregação.
   - `extract/` - Scripts de extração de dados.
   - `transform/` - Scripts de transformação de dados.
- `powerbi/` - Arquivos do painel do Power BI.


### Tecnologias Utilizadas 🛠️

![Apache Airflow](https://img.shields.io/badge/-Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Databricks](https://img.shields.io/badge/-Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Jupyter](https://img.shields.io/badge/-Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Kubernetes](https://img.shields.io/badge/-Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PowerBI](https://img.shields.io/badge/-PowerBI-F2C811?style=for-the-badge&logo=power-bi&logoColor=black)
![MongoDB](https://img.shields.io/badge/-MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## Começando

### Instalação

É necessário alterar os caminhos em main.py
```
/home/your-user/seu-diretorio/data-lakehouse-coinmarketcap/datalake/bronze/bronze.json
```

Em aggregate do arquivo gold.py
```
/home/your-user/seu-diretorio/data-lakehouse-coinmarketcap/datalake/gold/gold.json
```

1. Clone o repositório em sua máquina local.
2. Navegue até o diretório e crie um ambiente virtual:

- Rode os seguintes comandos:

```
python -m venv venv
```
```
source venv/bin/activate
```

3. Instale os pacotes Python necessários:

```
pip install -r requirements.txt
```

4. Inicie o serviço MongoDB em sua máquina ou use o Docker para executar um contêiner MongoDB.

### Executando o aplicativo

1. É necessário iniciar sua instância do MongoDB se ainda não estiver em execução para rodar aplicação:
Adicione o repositório oficial do MongoDB: Primeiro, você precisa adicionar a chave GPG do repositório oficial do MongoDB e adicionar o repositório aos seus repositórios APT. Execute os seguintes comandos no terminal:

```
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
```

```
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
```

```
sudo apt update
```

```
sudo apt install -y mongodb-org
```

```
sudo systemctl start mongod
```

```
sudo systemctl status mongod
```

O MongoDB deve aparecer em verde com seguinte mensagem:
Active: active (running)

- Agora abra outra Aba do Termonal é necesssário criar o Banco de dados no Terminal e criar a Collection:

```
mongo
```

Criar um banco de dados: No shell do MongoDB, para criar um novo banco de dados, você pode simplesmente especificar o nome do banco de dados da seguinte maneira:

```
use coinDB
```

Criar uma coleção: Após selecionar um banco de dados, você pode criar uma coleção dentro desse banco de dados usando o seguinte comando:

```
db.createCollection("coinMarket")
```

Depois de executar esses comandos, você terá criado um banco de dados e uma coleção dentro desse banco de dados. Você pode verificar se eles foram criados corretamente usando comandos como show dbs para listar os bancos de dados e show collections para listar as coleções dentro de um banco de dados específico.

listar os bancos de dados:

```
show dbs
```

listar as coleções

```
show collections
```

2. Para executar o Dashbord no Streamlit, navegue até o diretório `dashboard/` configure o Banco de dados criado
no terminal e a collection para depois ir executar os comandos para rodar Dashboard

```
streamlit run dashboard.py
```

```
streamlit run app.py
```
3. Acesse o Dashbord do Streamlit em seu navegador em `localhost:8501`.


4. Para rodar o Apache Airflow dentro de uma aplicação abra uma nova aba no Terminal no diretório da aplicação:
A estrutura de diretórios na imagem indica que há um ambiente virtual do Python configurado (airflow_venv), diretórios para DAGs (dags), plugins personalizados (plugins), scripts (scripts) e um banco de dados SQLite (sqlite).


1. Ativar o Ambiente Virtual
Primeiro, você deve ativar o ambiente virtual que contém o Apache Airflow e suas dependências. Abra um terminal e navegue até o diretório que contém o airflow_venv e execute o seguinte comando:

```
python -m venv venv
```

```
source venv/bin/activate
```

2. Inicializar o Banco de Dados do Airflow
Antes de executar o Airflow pela primeira vez, é necessário inicializar seu banco de dados. Com a estrutura de diretórios fornecida, parece que você está usando um banco de dados SQLite. O comando de inicialização é:

```
airflow db init
```

3. Criar um Usuário (Se Necessário)
Para acessar a interface do usuário (UI) do Airflow, você precisa criar um usuário. Você pode fazer isso com o seguinte comando:

```
airflow users create \
    --username your_username \
    --firstname Your_Firstname \
    --lastname Your_Lastname \
    --role Admin \
    --email your_email@example.com
```

4. Iniciar o Scheduler do Airflow
O Scheduler do Airflow é o componente que orquestra a execução das DAGs. Para iniciá-lo, execute:

```
airflow scheduler
```

5. Iniciar a Webserver do Airflow
Em um novo terminal (certificando-se de que o ambiente virtual esteja ativado), inicie a webserver do Airflow com:

```
airflow webserver --port 8088
```

Isso iniciará a interface web do Airflow na porta 8080, e você poderá acessá-la através de um navegador de internet navegando até http://localhost:8088.

6. Testar e Ativar as DAGs
Com a interface web do Airflow funcionando, você pode testar e ativar suas DAGs:

Testar uma DAG: No terminal, você pode testar uma tarefa individual usando o comando airflow tasks test, por exemplo:

```
airflow tasks test your_dag_id your_task_id your_execution_date
```

Ativar/Desativar uma DAG: Na interface web, clique na DAG que deseja ativar e alterne o interruptor para o estado 'ON'.


7. O código acima assume que você tem um MongoDB rodando localmente e contém código para puxar dados dele. Ajuste a string de conexão e os nomes do banco de dados e da coleção conforme necessário.
Plotly Express:

Estamos usando Plotly Express para criar um gráfico de linha simples. Você pode ajustar isso conforme necessário para se adequar aos seus dados e requisitos.
Layout Dash:

O layout do Dash é definido usando uma combinação de componentes HTML e core. Você pode expandir isso para incluir mais gráficos, tabelas, filtros e outros elementos conforme necessário.
Execução:

Execute o aplicativo usando python app.py, e ele será hospedado localmente. Você pode acessá-lo em http://127.0.0.1:8050 no seu navegador web.
Personalização:

Este é um exemplo básico. O Dash é altamente personalizável, e você pode adicionar muitos outros elementos, estilos e interatividades ao seu dashboard.
Dados:

Certifique-se de que seus dados estão estruturados e limpos para serem visualizados. Você pode precisar ajustar o código de acordo com a estrutura específica dos seus dados.
Componentes:

Explore os componentes do Dash e do Plotly para adicionar funcionalidades como dropdowns, sliders, tabelas e outros elementos interativos ao seu dashboard.

### Processamento de dados

1. Use os notebooks Jupyter fornecidos em `jupyter/notebook/` para executar tarefas ETL:
- `etl_bronze.ipynb`: para processar dados brutos para a camada bronze.
- `etl_silver.ipynb`: para refinar dados de bronze para a camada de prata.
- `etl_gold.ipynb`: para processamento final para obtenção de dados da camada de ouro.

2. Agende e monitore fluxos de trabalho ETL usando Apache Airflow localizado no diretório `airflow/`.

### Implantação via Containers

- Para implantação no Kubernetes, consulte as configurações no diretório `kubernetes/`.
- Use os arquivos do diretório `docker/` para construir e executar contêineres para configuração de ambiente isolado.


### Conclusão
Este sistema completo de Data Lakehouse da CoinMarketCap o projeto foi uma iniciativa ambiciosa que visou capitalizar a riqueza de dados do mercado de criptomoedas para fornecer insights aprofundados e aprimorar a tomada de decisão no ambiente financeiro dinâmico de hoje. Utilizando a robusta plataforma do Databricks, conseguimos consolidar, processar e analisar grandes volumes de dados relacionados a preços de ativos, volumes de transação, e mudanças de mercado em tempo real.

O Databricks serviu como o núcleo de processamento e análise, permitindo-nos executar transformações complexas de dados e algoritmos de aprendizado de máquina em um ambiente unificado. O uso de notebooks interativos facilitou a colaboração entre analistas de dados, engenheiros de dados e cientistas de dados, enquanto a infraestrutura gerenciada simplificou o provisionamento e a manutenção de recursos computacionais.

Por meio de nosso Data Lakehouse, estabelecemos camadas de dados categorizadas como bronze, prata e ouro, que representam respectivamente os dados brutos, processados e prontos para análise. Esta abordagem estratificada assegurou que os dados fossem refinados de maneira sistemática, maximizando a confiabilidade e a utilidade das informações geradas.

Os dashboards interativos criados com Streamlit proporcionaram uma interface intuitiva para a exploração de dados, permitindo aos usuários finais acessar relatórios customizados e realizar análises ad-hoc com facilidade. Além disso, a integração com MongoDB ofereceu uma solução ágil para armazenar e recuperar dados operacionais.

Através desta solução de Data Lakehouse, entregamos uma plataforma que não só suporta o crescimento contínuo do volume e da variedade de dados do CoinMarketCap mas também introduz a escalabilidade necessária para futuras expansões. As potenciais áreas de crescimento incluem a incorporação de novas fontes de dados, o aprimoramento de modelos de previsão de preços com técnicas avançadas de machine learning e a expansão para suportar outras classes de ativos além das criptomoedas.

Em resumo, o projeto Data Lakehouse CoinMarketCap com Databricks foi uma jornada transformadora que fortaleceu nossa capacidade analítica e ofereceu uma visão valiosa sobre o mercado de criptomoedas. Continuaremos a evoluir nossa plataforma para manter a relevância e o valor em um mercado que está sempre mudando.



### Desenvolvido por:
Emerson Amorim [@emerson-amorim-dev](https://www.linkedin.com/in/emerson-amorim-dev/)





