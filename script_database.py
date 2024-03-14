# importações
from flask import Flask, request
import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs, urlparse
import hashlib
from database import conectar  # importa a função conectar no Banco de dados 

conexao = conectar()

class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            # tenta abrir um arquivo
            f = open(os.path.join(path, 'index.html'), 'r')
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileNotFoundError:
            pass

        return super().list_directory(path)

    def do_GET(self):
        if self.path == '/login':
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header('Content type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, 'File Not Found')

        elif self.path == '/login_failed':
            # senha incorreta
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # le o html
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()

            # adiciona mensagem de erro
            mensagem = 'Login e/ou senha incorreto. Tente novamente.'
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
            # # envia pro cliente
            self.wfile.write(content.encode('utf-8'))
            # self.wfile.write("Senha incorreta".encode('utf-8'))

        elif self.path.startswith('/cadastro'):
            # extraindo parâmetros da URL
            query_params = parse_qs(urlparse(self.path).query)
            login = query_params.get('login', [' '])[0]
            senha = query_params.get('password', [' '])[0]

            # msg boas vindas
            welcome_message = f"Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui, bora fazer o cadastro?"

            # responde com a page de cadastro
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # le o conteudo da page cadastro
            with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r', encoding='utf-8') as cadastro_file:
                content = cadastro_file.read()

            # substitui os marcadores de posição pelos valores correspondentes
            content = content.replace('{login}', login)
            content = content.replace('{senha}', senha)
            content = content.replace('{welcome_message}', welcome_message)

            # envia para o cliente
            self.wfile.write(content.encode('utf-8'))

            # evita a execução do resto
            return
        
        elif self.path.startswith('/turmas'):
            query_params = parse_qs(urlparse(self.path).query)
            code = query_params.get('code', [' '])[0]
            descricao = query_params.get('descricao', [' '])[0]

            # msg boas vindas
            message = f"Olá, vamos cadastrar sua turma nova!"

            # responde com a page de cadastro
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # le o conteudo da page cadastro
            with open(os.path.join(os.getcwd(), 'turmas.html'), 'r', encoding='utf-8') as turmas_file:
                content = turmas_file.read()

            # substitui os marcadores de posição pelos valores correspondentes
            content = content.replace('{code}', code)
            content = content.replace('{descricao}', descricao)
            content = content.replace('{message}', message)

            # envia para o cliente
            self.wfile.write(content.encode('utf-8'))

            # evita a execução do resto
            return
        
        elif self.path.startswith('/atividades'):
            query_params = parse_qs(urlparse(self.path).query)
            codigo = query_params.get('codigo', [' '])[0]
            descricao = query_params.get('descricao', [' '])[0]

            # msg boas vindas
            message = f"Olá, vamos cadastrar sua atividade nova!"

            # responde com a page de cadastro
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # le o conteudo da page cadastro
            with open(os.path.join(os.getcwd(), 'atividades.html'), 'r', encoding='utf-8') as atividades_file:
                content = atividades_file.read()

            # substitui os marcadores de posição pelos valores correspondentes
            content = content.replace('{codigo}', codigo)
            content = content.replace('{descricao}', descricao)
            content = content.replace('{message}', message)

            # envia para o cliente
            self.wfile.write(content.encode('utf-8'))

            # evita a execução do resto
            return
        
        ##################################
        elif self.path.startswith('/login_turma'):
            query_params = parse_qs(urlparse(self.path).query)
            email = query_params.get('email', [' '])[0]
            descricao = query_params.get('descricao', [' '])[0]

            # msg boas vindas
            message = f"Escolha seu usuário e sua respectiva turma:"

            # responde com a page de cadastro
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # le o conteudo da page cadastro
            with open(os.path.join(os.getcwd(), 'login_turma.html'), 'r', encoding='utf-8') as login_turma_file:
                content = login_turma_file.read()

            # substitui os marcadores de posição pelos valores correspondentes
            content = content.replace('{email}', email)
            content = content.replace('{descricao}', descricao)
            content = content.replace('{message}', message)

            # envia para o cliente
            self.wfile.write(content.encode('utf-8'))

            # evita a execução do resto
            return
        
        elif self.path.startswith('/turma_atividade'):
            query_params = parse_qs(urlparse(self.path).query)
            code = query_params.get('code', [' '])[0]
            codigo = query_params.get('codigo', [' '])[0]

            # msg boas vindas
            message = f"Escolha sua turma e sua respectiva atividade:"

            # responde com a page de cadastro
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # le o conteudo da page cadastro
            with open(os.path.join(os.getcwd(), 'turma_atividade.html'), 'r', encoding='utf-8') as turma_atividade_file:
                content = turma_atividade_file.read()

            # substitui os marcadores de posição pelos valores correspondentes
            content = content.replace('{code}', code)
            content = content.replace('{codigo}', codigo)
            content = content.replace('{message}', message)

            # envia para o cliente
            self.wfile.write(content.encode('utf-8'))

            # evita a execução do resto
            return
        ############################################

        else:
            # se não achar a rota "/login", continua o comportamento padrão
            super().do_GET()

    def usuario_existente(self, login, senha):
        # verifica a existência do login
        cursor = conexao.cursor()
        cursor.execute("SELECT senha FROM dados_login WHERE login = %s", (login,))
        resultado = cursor.fetchone()
        cursor.close()

        if resultado:
            senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
            return senha_hash == resultado[0]
        
        return False
    
    def turma_existente(self, descricao):
        # Verifica a existência da turma
        cursor = conexao.cursor()
        cursor.execute("SELECT descricao FROM turmas WHERE descricao = %s", (descricao,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado is not None
    
    def atividade_existente(self, descricao):
        # Verifica a existência da atividade
        cursor = conexao.cursor()
        cursor.execute("SELECT descricao FROM atividades WHERE descricao = %s", (descricao,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado is not None
    
    def login_turma_existente(self, login, descricao):
        # Verifica se o login existe no arquivo de turmas
        cursor = conexao.cursor()
        cursor.execute("SELECT login FROM dados_login WHERE login = %s", (login,))
        resultado_login = cursor.fetchone()
        cursor.close()

        if resultado_login:
            # Verifica se a turma existe no arquivo de turmas
            cursor = conexao.cursor()
            cursor.execute("SELECT descricao FROM turmas WHERE descricao = %s", (descricao,))
            resultado_turma = cursor.fetchone()
            cursor.close()
            return resultado_turma is not None
        else:
            return False

    def turma_atividade_existente(self, login, turma):
# Verifica se a login existe no arquivo de turmas
        with open("dados_turmas.txt", "r", encoding="utf-8") as login_file:
            for line in login_file:
                stored_login = line.strip().split(';')[0]  
                if login == stored_login:
                    break
            else:
                return False
        
        # Verifica se a turma existe no arquivo de turmas
        with open("dados_atividades.txt", "r", encoding="utf-8") as turma_file:
            for line in turma_file:
                stored_turma = line.strip().split(';')[0]
                if turma == stored_turma:
                    return True
        return False

    def adicionar_usuario(self, login, senha, nome):
        cursor = conexao.cursor()
        senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO dados_login (login, senha, nome) VALUES (%s, %s, %s)", (login, senha_hash, nome))
        conexao.commit()
        cursor.close()

    def adicionar_turma(self, descricao):
        # Adiciona uma nova turma ao banco de dados
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO turmas (descricao) VALUES (%s);", (descricao,))
        conexao.commit()
        cursor.close()

    def adicionar_atividade(self, descricao):
        # Adiciona uma nova atividade ao banco de dados
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO atividades (descricao) VALUES (%s)", (descricao,))
        conexao.commit()
        cursor.close()

    def remover_ultima_linha(self, arquivo):
        print("Vou excluir a última linha.")
        with open(arquivo, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(arquivo, 'w', encoding='utf-8') as file:
            file.writelines(lines[:-1])

############################################################
    def carregar_turmas_professor(self, login):
        # carrega turmas do professor
        cursor = conexao.cursor()
        cursor.execute("SELECT id_professor, nome FROM dados_login WHERE login = %s", (login,))
        resultado = cursor.fetchone()
        cursor.close()

        # resultado[0] trás o id_professor e o resultado[1] trás o nome do professor
        id_professor = resultado[0]

        # obter turmas do professor
        cursor = conexao.cursor()
        cursor.execute("SELECT turmas.id_turma, turmas.descricao FROM turmas_professor INNER JOIN turmas ON turmas_professor.id_turma = turmas.id_turma WHERE turmas_professor.id_professor = %s", (id_professor,))
        turmas = cursor.fetchall()
        cursor.close()

        # linhas da tabela 
        linhas_tabela = ""
        for turma in turmas:
            id_turma = turma[0]
            descricao_turma = turma[1]
            link_atividade = "<a href='/atividade_turma?id={}'><i class='fas fa-pencil-alt'></i></a>".format(id_turma)
            linha = "<tr><td style='text-align:center'>{}</td><td>{}</td><td style='text-align:center'>{}</td></tr>".format(id_turma, descricao_turma, link_atividade)
            linhas_tabela += linha
        
        # turmas do banco de dados
        cursor = conexao.cursor()
        cursor.execute("SELECT id_turma, descricao FROM turmas")
        turmas = cursor.fetchall()
        cursor.close()

        # caixa de seleção 
        opcoes_caixa_selecao = ""
        for turma in turmas:
            opcoes_caixa_selecao += "<option value='{}'>{}</option>".format(turma[0], turma[1])

        with open(os.path.join(os.getcwd(), 'turma_professor.html'), 'r', encoding='utf-8') as cad_turma_file:
            content = cad_turma_file.read()

            content = content.replace('{nome_professor}', resultado[1])
            content = content.replace('{id_professor}', str(id_professor))
            content = content.replace('{login}', str(login))

            # substituindo o marcados da posição pelas linhas da tabela
            content = content.replace('<!-- Tabela com linhas zebradas -->', linhas_tabela)
            # substitui o marcador de posição pelas opções na caixa de seleção.
            content = content.replace('<!-- Opções da caixa de seleção serão inseridas aqui -->', opcoes_caixa_selecao)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(content.encode('utf-8'))
        # fim
############################################################

    def do_POST(self):
        # verifica se a rota é "/enviar_login"
        if self.path == "/enviar_login":
            # obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            # le o corpo da aquisição
            body = self.rfile.read(content_length).decode('utf-8')
            # parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            # exibe os dados no terminal
            print("Dados do formulário:")
            print("Email:", form_data.get('email', [''])[0])
            print("Senha:", form_data.get('password', [''])[0])

            # verifica existência
            login = form_data.get('email', [''])[0]
            senha = form_data.get('password', [''])[0]

            if self.usuario_existente(login, senha):
                # self.send_response(200)
                # self.send_header('Content-type', 'text/html; charset=utf-8')
                # self.end_headers()
                # mensagem = f'Usuário {login} logado com sucesso!'
                # self.wfile.write(mensagem.encode('utf-8'))
                # SUBSTITUIR POR UMA PÁGINA HTML
                self.carregar_turmas_professor(login)
              
            else:
                # verifica se o usuário já está cadastrado, caso não esteja foi caso de login errado
                cursor = conexao.cursor()
                cursor.execute("SELECT login FROM dados_login WHERE login = %s", (login,))
                resultado = cursor.fetchone()

                if resultado:
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    cursor.close()
                    return
                else:
                    self.send_response(302)
                    self.send_header('Location', f'/cadastro?login={login}&senha={senha}')
                    self.end_headers()
                    cursor.close()
                    return

        elif self.path.startswith('/confirmar_cadastro'):
            # obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            # le o corpo
            body = self.rfile.read(content_length).decode('utf-8')
            # parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            # query_params = parse_qs(urlparse(self.path).query)
            login = form_data.get('login', [''])[0]
            senha = form_data.get('password', [''])[0]
            nome = form_data.get('nome', [''])[0]

            self.adicionar_usuario(login, senha, nome)

            with open(os.path.join(os.getcwd(), 'msg_sucesso.html'), 'rb') as file:
                content = file.read().decode('utf-8')

            content = content.replace('{login}', login)
            content = content.replace('{nome}', nome)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Registro recebido com sucesso!".encode('utf-8'))

        elif self.path.startswith('/cad_turma'):
            # Obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo
            body = self.rfile.read(content_length).decode('utf-8')
            # Analisa os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            # Extrai os dados do formulário
            code = form_data.get('code', [''])[0]
            descricao = form_data.get('descricao', [''])[0]

            # Verifica a existência da turma
            if self.turma_existente(descricao):
                # Turma já existe, não é necessário fazer nada
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Turma já existe!".encode('utf-8'))
            else:
                # Adiciona a nova turma ao banco
                self.adicionar_turma(descricao)

                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Nova turma recebida com sucesso!".encode('utf-8'))

        elif self.path.startswith('/cad_atividade'):
            # Obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo
            body = self.rfile.read(content_length).decode('utf-8')
            # Analisa os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            # Extrai os dados do formulário
            codigo = form_data.get('codigo', [''])[0]
            descricao = form_data.get('descricao', [''])[0]

            # Verifica a existência da turma
            if self.atividade_existente(descricao):
                # atividade já existe, não é necessário fazer nada
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Atividade já existe!".encode('utf-8'))
            else:
                # Adiciona a nova turma ao arquivo
                self.adicionar_atividade(descricao)

                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Nova atividade criada com sucesso!".encode('utf-8'))

        elif self.path.startswith('/cad_login_turma'):
            # Obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo
            body = self.rfile.read(content_length).decode('utf-8')
            # Analisa os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            # Extrai os dados do formulário
            email = form_data.get('email', [''])[0]
            descricao = form_data.get('descricao', [''])[0]

            # Verifica a existência da turma
            if self.login_turma_existente(email, descricao):
                # atividade já existe, não é necessário fazer nada
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Já cadastrado!".encode('utf-8'))
            else:
                # Adiciona a nova turma ao arquivo
                with open('dados_login_turma.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{email};{descricao}\n')

                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("com sucesso!".encode('utf-8'))

        elif self.path.startswith('/cad_turm_atividade'):
            # Obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo
            body = self.rfile.read(content_length).decode('utf-8')
            # Analisa os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            # Extrai os dados do formulário
            code = form_data.get('code', [''])[0]
            codigo = form_data.get('codigo', [''])[0]

            print(f'Código da Atividade: {codigo}')

            # Verifica a existência da turma
            if self.turma_atividade_existente(code, codigo):
                # atividade já existe, não é necessário fazer nada
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Já cadastrado!".encode('utf-8'))
            else:
                # Adiciona a nova turma ao arquivo
                with open('dados_turma_atividade.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{code};{codigo}\n')
                

                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Nova lalala3 com sucesso!".encode('utf-8'))

        elif self.path.startswith('/confirmar_turma_professor'):
            # Obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            # Lê o corpo
            body = self.rfile.read(content_length).decode('utf-8')
            # Analisa os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            # Extrai os dados do formulário
            code = form_data.get('code', [''])[0]
            codigo = form_data.get('codigo', [''])[0]

            # Verifica a existência da turma
            if self.turma_atividade_existente(code, codigo):
                # atividade já existe, não é necessário fazer nada
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Já cadastrado!".encode('utf-8'))
            else:
                # Adiciona a nova turma ao arquivo
                with open('dados_turma_atividade.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{code};{codigo}\n')
                

                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Nova lalala3 com sucesso!".encode('utf-8'))

        else:
            self.remover_ultima_linha('dados_login.txt')
            self.send_response(302)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Senha não confere. Retome o procedimento.".encode('utf-8'))


# define a porta a ser utilizada
endereco_ip = "0.0.0.0"
porta = 8000

# configura o manipulador (handler) para o servidor
# handler = http.server.SimpleHTTPRequestHandler

# cria um servidor na porta especificada
with socketserver.TCPServer(("", porta), MyHandler) as httpd:
    print(f"Servidor iniciado na porta {porta}.")
    # mantém o servidor em execução
    httpd.serve_forever()