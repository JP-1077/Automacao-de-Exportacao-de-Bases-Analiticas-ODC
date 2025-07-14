# ================================================================================
"""
Projeto: Exportação de Bases Analíticas do ODC - GOV e PROCON
Data da Criação: 03/07/2025
Desenvolvedor: João Pedro
Finalidade: 
    - Extrair dados das tabelas de tb_odc_gov e tb_odc_proconbrasil 
    - Exportar os dados em formato CSV
    - Salvar os dados em um diretório do OneDrive

"""
# ================================================================================


# Importação das bibliotecas necessárias para realizar a criação da aplicação.
import pandas as pd # Manipulação de dados em Data Frames
import pyodbc       # Conexão com Banco de dados SQL Server
import os           # Interação com o sistema operacional 
from datetime import datetime

# Dados que fazem referência ao banco de dados SQL Server
dados_conexao_banco = (
    'Driver={SQL Server};'      # Drive de conexão
    'Server=Snepdb56c01;'       # Nome do servidor
    'Database=BDS;'             # Nome do banco de dados
    'Trusted_Connection=yes;'   # Autenticação integrada do Windows
)

# Identifica qual é o usuário que está logado no sistema

user = os.path.basename(os.environ['USERPROFILE'])
print(f'Usuário: + {user} + Conectado')

# Conexão com banco de dados
try:
    conexao = pyodbc.connect(dados_conexao_banco)
    cursor = conexao.cursor()
    print('Conexão Bem Sucessida com Banco de Dados BDS')
except Exception as e:
    print(f'Erro ao conectar ao banco de dados: {e}')


# Código SQL para extração da base GOV
base_gov = """
SELECT 
    protocolo,
    [Mês Abertura],
    [Tempo Resposta],
    [Grupo Problema],
    NOME_COMPLETO,
    LOGIN_REDE,
    data_turbina,
    nota,
    [Avaliação Reclamação],
    Situação,
    data_tratativa,
    Aging_tratativa,
    modalidade,
    REINC_60D,
    cpf_consumidor,
    UF,
    infraco,
    service_id,
    tecnologia,
    plano,
    problema 
FROM 
    tb_odc_gov
"""

# Código SQL para extração da base Procon
base_procon = "SELECT * FROM tb_odc_proconbrasil"

# Realiza leitura dos códigos SQL e carrega os dados em DataFrames do Pandas
df_gov = pd.read_sql(base_gov, conexao)
df_procon = pd.read_sql(base_procon, conexao)

# Definição do caminho para exportação no OneDrive
onedrive_path = r"C:\Users\{}\TIM\OneDrive - MIS_TIM\0001 - ATENDIMENTO\0006 - Bases_Analitica_ODC".format(user)

# Exportação dos DataFrames para arquivos CSV no diretório especificado
df_gov.to_csv(os.path.join(onedrive_path, 'Base_GOV.csv'), index=False, sep=';')
df_procon.to_csv(os.path.join(onedrive_path, 'Base_Procon.csv'), index=False, sep=';')


# Definindo a instrução SQL para inserir um log na tabela de monitoramento de processos (TB_PROCS_LOG)
log_processo = """
	insert into TB_PROCS_LOG
	values(
		'ETL_EXPORT_BASE_ANALITICA_ODC', --processo
		?, --horario start
		cast(getdate() as datetime), -- horario end
		'OK', --status
		NULL)
"""

# Captura o horário exato de início do processo em Python, que será utilizado no log
horario_start = datetime.now()

# Executa a instrução SQL usando um cursor, passando o horário de início como parâmetro
cursor.execute(log_processo, horario_start)

# Commita a transação no banco de dados para garantir que o log seja salvo
conexao.commit()

# Imprime mensagens informativas no console, para identificarmos se a exportação e o processo como um todo foi finalizado com sucesso
print("Exportação concluída com sucesso")
print ("Processo Finalizado e Log Inserido na tabela")