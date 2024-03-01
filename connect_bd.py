import mysql.connector

# conecta ao servidor 
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senai"
)

# cria um cursor para executar comandos sql 
cursor = conexao.cursor()

# cria um banco de dados chamado 'pwbe' se ele ainda não existir
cursor.execute('CREATE DATABASE IF NOT EXISTS pwbe_escola')

# seleciona o banco de dados 'pwbe'
cursor.execute("USE pwbe_escola")

# cria uma tabela chamada 'tabela_pwbe' com os campos 'id' e 'nome'
cursor.execute("CREATE TABLE IF NOT EXISTS dados_login (id_professor INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), login VARCHAR(255), senha VARCHAR(255))")
# turma
cursor.execute("CREATE TABLE IF NOT EXISTS turmas (id_turma INT AUTO_INCREMENT PRIMARY KEY, descricao VARCHAR(255))")
# atividade
cursor.execute("CREATE TABLE IF NOT EXISTS atividades (id_atividade INT AUTO_INCREMENT PRIMARY KEY, descricao VARCHAR(255))")
# turmas_professor
cursor.execute("CREATE TABLE IF NOT EXISTS turmas_professor (id INT AUTO_INCREMENT PRIMARY KEY, id_professor INT, id_turma INT, FOREIGN KEY (id_professor)"
               "REFERENCES dados_login(id_professor), FOREIGN KEY(id_turma) REFERENCES turmas(id_turma))")
# atividades_turma
cursor.execute("CREATE TABLE IF NOT EXISTS atividades_turma (id INT AUTO_INCREMENT PRIMARY KEY, id_turma INT, id_atividade INT, FOREIGN KEY (id_turma)"
               "REFERENCES turmas(id_turma), FOREIGN KEY (id_atividade) REFERENCES atividades(id_atividade))")

# fecha o cursor e a conexão
cursor.close()
conexao.close()

print("Tabelas criadas com sucesso.")

# def conectar():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="senai",
#         database="pwbe"
#     )
