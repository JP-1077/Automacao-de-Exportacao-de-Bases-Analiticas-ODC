# Automacao de Exportacao de Bases Analiticas

## Objetivo 🎯
Automatizar a extração de dados de duas tabelas analiticas presentes em um banco de dados SQL Server, exportando os dados em formato CSV para um diretório do OneDrive.

## Tecnologia e Ferramentas 🛠
* Linguagem: Python
* Bibliotecas:
  * pandas (manipulação de dados)
  * pyodbc (conexão com SQL Server)
  * os (interação com sistema operacional)
  * datetime (registro de tempo)
* Banco de Dados: SQL Server

## System Design ✍🏼

![Pipeline](Pipeline(4).png)

1. Conexão com banco de dados: SQL Server via pyodbc
  
2. Extração de dados:
    * SELECT específico para tb_odc_gov
    * SELECT * para tb_odc_proconbrasil
      
3. Exportação: Criação de arquivos Base_GOV.csv e Base_Procon.csv no diretório do OneDrive
   
4. Log de execução: Inserção de registro na tabela TB_PROCS_LOG com horário de início e status

## Detalhes Técnicos ⚙

### Fonte de Dados

* Banco de Dados SQL Server

### Transformações

* Nenhuma transformação direta nos dados.
* Exportação direta dos DataFrames para CSV com separador ;.

### Base Final

* Base_GOV.csv
* Base_Procon.csv

## Monitoramento ✅

Nome do Processo: ETL_EXPORT_BASE_ANALITICA_ODC

Horario de Execução: 15:00
