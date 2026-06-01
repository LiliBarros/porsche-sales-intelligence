Porsche Sales Intelligence

Projeto de Conclusão de Curso • Engenharia de Dados & Business Intelligence

Este repositório contém o projeto de aplicação prática desenvolvido para a conclusão do curso de especialização em Tecnologia e Análise de Dados. O ecossistema demonstra a implementação de um pipeline de dados completo de ponta a ponta (end-to-end), englobando a ingestão, higienização, normalização regulatória de dados brutos (ETL) e a entrega de valor analítico através de um Painel de Business Intelligence (BI) interativo e responsivo.

O objetivo deste trabalho académico é demonstrar a viabilidade de pipelines leves e funcionais, aliando o poder analítico do Python no tratamento de dados ao dinamismo de aplicações web estáticas para a tomada de decisões estratégicas.

🏛️ Objetivos de Aprendizagem e Metodologia

O desenvolvimento deste projeto guiou-se pela aplicação prática de conceitos teóricos fundamentais em ciência de dados:

Garantia de Qualidade de Dados (Data Quality): Implementação de regras de validação estritas para mitigar a propagação de informação ruidosa ou inconsistente.

Normalização Algorítmica (ETL): Desenvolvimento de scripts capazes de converter formatos ambíguos (linguagem natural, unidades de medida distintas e formatos de data despadronizados) em esquemas canónicos reutilizáveis.

Comunicação de Dados (Data Storytelling): Desenho de uma interface de utilizador (UI) premium e minimalista, inspirada no portal oficial da Porsche, facilitando a interpretação imediata de métricas de desempenho.

📂 Arquitetura e Fluxo do Projeto

O projeto está estruturado de forma modular para refletir claramente as etapas do fluxo de processamento de dados:

├── porsche_database.xlsx            # Extração (E): Base de dados comercial bruta (dados ruidosos)
├── schema.md                        # Dicionário de Dados: Regras e especificações canónicas
├── higienizador.py                  # Transformação (T): Pipeline de ETL desenvolvido em Python
├── porsche_database_sanitized.xlsx  # Carga (L): Base de dados final estruturada e higienizada
└── index.html                       # Aplicação Final: Dashboard analítico para consumo de BI


1. Fase de Transformação (Engine de ETL com Python)

O ficheiro higienizador.py serve como o motor de ETL do projeto. Construído com a biblioteca Pandas, o script resolve problemas típicos de bases de dados reais utilizando técnicas de correspondência fonética e expressões regulares (RegEx):

Tratamento Temporal: Converte múltiplos formatos de data textuais e numéricos para a norma ISO YYYY-MM-DD. Datas impossíveis no calendário (ex: 30 de fevereiro) são marcadas como INVALID.

Processamento de Linguagem Natural (NLP): Conversão de valores expressos por extenso (ex: "twenty twenty four") para inteiros válidos através da biblioteca word2number.

Compatibilidade Métrico-Imperial: Conversão matemática e arredondamento automático de quilómetros para milhas (1 km = 0.621371 mi) detetados de forma dinâmica na base de dados.

Geolocalização: Normalização dos estados norte-americanos para o padrão de duas letras do serviço postal USPS (ex: California -> CA).

2. Fase de Apresentação (Análise de Business Intelligence)

O painel index.html consome as variáveis tratadas para responder a problemas de gestão de portfólio e performance regional.

📊 Problemas de Negócio Resolvidos pelo Painel

Para demonstrar a aplicabilidade prática do modelo de dados, o dashboard foi desenhado para responder de forma visual e interativa a três grandes eixos de análise de mercado:

📈 1. Distribuição de Portfólio por Praça Comercial

Abordagem Analítica: Análise de penetração regional para responder a quais os principais modelos vendidos por cidade e por estado.

Mecanismo: Gráfico de barras interativo em Canvas (Chart.js) que permite ao utilizador clicar em qualquer região ou modelo para auto-filtrar todos os indicadores e tabelas associadas.

⏱️ 2. Ciclo de Vida do Produto e Preferência Temporal

Abordagem Analítica: Avaliação de tendências de saída com base no Model Year num determinado intervalo de tempo personalizável.

Mecanismo: Filtros dinâmicos que calculam a curva de consumo cronológica, permitindo identificar se a procura se concentra nos modelos novos ou clássicos.

📍 3. Densidade de Vendas e Desempenho por Estado (State)

Abordagem Analítica: Mapeamento de receitas brutas e volume de transações agrupados geograficamente por Estado.

Mecanismo: Um painel analítico lateral computa os dados dinamicamente, destacando qual o Estado líder em volume de unidades, o líder em faturação bruta acumulada e o modelo de maior liquidez associado.

🛠️ Tecnologias e Ferramentas Aplicadas

Engenharia de Dados (ETL): Python 3, Pandas, OpenPyXL, Word2Number, Regular Expressions (RegEx).

Interface de Utilizador (UI/UX): HTML5, Tailwind CSS, Componentes Responsivos, Lucide Icons.

Visualização de Dados: Chart.js (Renderização nativa em elemento Canvas).

🚀 Como Executar e Validar o Projeto

Pré-requisitos (Camada Python)

Para reproduzir a higienização dos dados locais:

Certifique-se de que possui o Python instalado na sua máquina.

Instale as bibliotecas necessárias:

pip install pandas openpyxl word2number


Execute o pipeline:

python higienizador.py


Execução do Painel de BI

Não é necessário configurar servidores Web complexos ou ligar bases de dados pesadas para validar esta entrega académica.

Basta abrir o ficheiro index.html em qualquer navegador moderno.

O painel carrega autonomamente a base tratada para demonstrar as interações dinâmicas.

Trabalho académico desenvolvido com fins exclusivamente didáticos para consolidação de competências em Engenharia de Dados e Análise Visual.
