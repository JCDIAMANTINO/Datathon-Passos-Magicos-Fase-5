# 📊 Datathon Passos Mágicos — Previsão de Risco de Defasagem

## 🧠 Descrição do Projeto

Este projeto foi desenvolvido como parte da **Fase Final (Datathon) da ONG Passos Mágicos** e tem como objetivo aplicar técnicas de **Machine Learning** para análise e predição do **risco de defasagem pedagógica**, utilizando dados relacionados a características demográficas, desempenho acadêmico e avaliações psicopedagógicas dos alunos.

Além da modelagem preditiva, o projeto também contempla a criação de um **dashboard interativo**, construído com a biblioteca Plotly, permitindo a visualização aprofundada de insights relevantes sobre os dados históricos e a realização de previsões em tempo real a partir do modelo treinado.

## 🎯 Objetivos

* Explorar e analisar dados relacionados à jornada educacional dos alunos (Fases e Pedras).
* Desenvolver um modelo de Machine Learning para classificação do risco de queda de desempenho.
* Fornecer respostas claras a 12 perguntas estratégicas de negócio por meio de visualizações interativas.
* Disponibilizar uma aplicação web intuitiva como ferramenta de suporte à decisão para a equipe pedagógica.
* Consolidar o impacto social da ONG por meio da ciência de dados.

## 🗂 Estrutura do Projeto

```text
Datathon-Passos-Magicos-Fase-5/
├── pede_completo.csv               # Conjunto de dados tratado e utilizado
├── modelo_passos_magicos.pkl       # Modelo de Machine Learning treinado e serializado
├── app.py                          # Aplicação principal (Dashboard Analytics e Previsão)
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação do projeto
└── .gitignore                      # Arquivos e pastas ignorados pelo Git
```

## 📊 Conjunto de Dados

O conjunto de dados contém informações demográficas, acadêmicas e comportamentais dos alunos, incluindo:
* **Perfil:** Idade, Ano de Ingresso e Instituição de Ensino (Pública/Privada).
* **Posicionamento:** Fase Ideal (baseada na série escolar), Fase Atual no programa e Nível de Defasagem.
* **Indicadores Passos Mágicos:**
  * Desempenho Acadêmico (IDA)
  * Engajamento (IEG)
  * Autoavaliação (IAA)
  * Saúde Psicológica (IPS)
  * Avaliação Psicopedagógica (IPP)
  * Ponto de Virada (IPV)
  * Adequação de Nível (IAN)

As classes de saída do nosso modelo representam o status do aluno:
* **0:** Aluno Estável (Fora de risco)
* **1:** Alto Risco de Queda de Desempenho / Defasagem

## 💡 Modelagem e Machine Learning

O projeto utiliza algoritmos de Machine Learning (via `scikit-learn`) para resolver um problema de **classificação binária**, abrangendo as seguintes etapas:
* Pré-processamento e limpeza dos dados históricos (2022 a 2024).
* Análise Exploratória de Dados (EDA) para identificar fatores de influência (como a forte correlação do IDA com o Ponto de Virada).
* Treinamento do modelo classificador.
* Salvamento do modelo treinado (`.pkl` via `joblib`) para consumo rápido em ambiente de produção.

## 📈 Painel e Aplicativo

O aplicativo web, desenvolvido em **Streamlit**, atua em duas frentes:
1. **Business Intelligence (Analytics):** Visualização interativa dos dados utilizando `Plotly Express`, permitindo investigar zonas de alerta, efetividade da jornada das "Pedras" e comparar perfis de alunos com alta granularidade e interatividade.
2. **Simulador Preditivo:** Uma interface onde o pedagogo insere as notas atuais do aluno e o modelo cruza essas informações com o histórico da ONG, gerando um "Raio-X" imediato com a probabilidade de risco, elencando focos críticos para intervenção e pontos fortes para apoio.

Link da Aplicação em Produção: *[https://dashboard-ped-magicos-risco-defasagem-jcd.streamlit.app/]*

## 🚀 Como Executar o Projeto

**1️⃣ Clonar o Repositório**
```bash
git clone https://github.com/JCDIAMANTINO/Datathon-Passos-Magicos-Fase-5.git
cd Datathon-Passos-Magicos-Fase-5
```

**2️⃣ Criar Ambiente Virtual (Recomendado)**
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

**3️⃣ Instalar Dependências**
```bash
pip install -r requirements.txt
```

**4️⃣ Executar a Aplicação (Dashboard e Modelo)**
```bash
streamlit run app.py
```
**5️⃣ Executar os Notebooks**
```bash
jupyter Notebook_01_tratamento_dos_dados.ipynb
```
e/ou
```bash
jupyter Notebook_02_analise_explorat.ipynb
```
e/ou
```bash
jupyter Notebook_03_machine_learning.ipynb
```

## 🧪 Resultados

O modelo treinado e o dashboard interativo demonstram excelente capacidade de extração de valor dos dados educacionais, permitindo:
* Identificação clara das **Zonas de Alerta** (Fases 2 e 3 concentram o maior risco histórico).
* Apoio direto à análise de risco individual, transformando a postura da Associacao de reativa para **preditiva**.
* Visualização clara e interativa que democratiza o acesso aos dados para professores e psicopedagogos, sem necessidade de conhecimento em programação.
