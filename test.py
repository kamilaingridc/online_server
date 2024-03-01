# importações
from flask import Flask, request
import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs, urlparse
import hashlib


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
        with open('dados_login.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    stored_login, stored_senha_hash, stored_nome = line.strip().split(';')
                    if login == stored_login:
                        print("Cheguei aqui significando que localizei o login informado.")
                        print("Senha:" + senha)
                        print("Senha armazenada:" + senha)

                        senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
                        return senha_hash == stored_senha_hash
        return False
    
    def turma_existente(self, code, descricao):
        # Verifica a existência da turma
        with open('dados_turmas.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    code_line, descricao_line = line.strip().split(';')
                    if code == code_line and descricao == descricao_line:
                        print("Código: ", code)
                        return True
        return False
    
    def atividade_existente(self, codigo, descricao):
        # Verifica a existência da turma
        with open('dados_atividades.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    codigo_line, descricao_line = line.strip().split(';')
                    if codigo == codigo_line and descricao == descricao_line:
                        print("Código: ", codigo)
                        return True
        return False
    
    def login_turma_existente(self, login, turma):
# Verifica se a login existe no arquivo de turmas
        with open("dados_login.txt", "r", encoding="utf-8") as login_file:
            for line in login_file:
                stored_login = line.strip().split(';')[0]  
                if login == stored_login:
                    break
            else:
                return False
        
        # Verifica se a turma existe no arquivo de turmas
        with open("dados_turmas.txt", "r", encoding="utf-8") as turma_file:
            for line in turma_file:
                stored_turma = line.strip().split(';')[0]
                if turma == stored_turma:
                    return True
        return False
    
    def turma_atividade_existente(self, login, turma):
# Verifica se a login existe no arquivo de turmas
        with open("dados_turmas.txt", "r", encoding="utf-8") as login_file:
            for line in login_file:
                stored_login = line.strip().split(';')[0]  
                if login == stored_login:
                    print("Turma IF check :)")
                    break
            else:
                print("tURMA ELSE CHECK :)")
                return False
        
        # Verifica se a turma existe no arquivo de turmas
        with open("dados_atividades.txt", "r", encoding="utf-8") as turma_file:
            for line in turma_file:
                stored_turma = line.strip().split(';')[0]
                if turma == stored_turma:
                    print("tURMA if CHECK 2 :)")
                    return True
        print("tURMA false CHECK 2 :)")
        return False

    def adicionar_usuario(self, login, senha, nome):
        senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
        with open('dados_login.txt', 'a', encoding='utf-8') as file:
            file.write(f'{login};{senha_hash};{nome}\n')

    def adicionar_turma(self, code, descricao):
        # Adiciona uma nova turma ao arquivo
        with open('dados_turmas.txt', 'a', encoding='utf-8') as file:
            file.write(f'{code};{descricao};\n')

    def adicionar_turma(self, codigo, descricao):
        # Adiciona uma nova turma ao arquivo
        with open('dados_atividades.txt', 'a', encoding='utf-8') as file:
            file.write(f'{codigo};{descricao};\n')

    def remover_ultima_linha(self, arquivo):
        print("Vou excluir a última linha.")
        with open(arquivo, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(arquivo, 'w', encoding='utf-8') as file:
            file.writelines(lines[:-1])

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
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                mensagem = f'Usuário {login} logado com sucesso!'
                self.wfile.write(mensagem.encode('utf-8'))
                # SUBSTITUIR POR UMA PÁGINA HTML
              
            else:
                # verifica se existe
                if any(line.startswith(f"{login};") for line in open('dados_login.txt', 'r', encoding='utf-8')):
                    # redirecionamento
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    return  # adiciona para evitar rodar o resto do código
                else:
                    # adc novo usuário
                    self.adicionar_usuario(login, senha, nome='None')

                    # redireciona
                    self.send_response(302)
                    self.send_header('Location', f'/cadastro?login={login}&senha{senha}')
                    self.end_headers()

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

            senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()

            print(f'Nome: {nome}')

            # verifica existencia do usuario
            if self.usuario_existente(login, senha):

                # atualiza o arquivo com o nome, se a senha estiver correta
                with open('dados_login.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                with open('dados_login.txt', 'w', encoding='utf-8') as file:
                    for line in lines:
                        stored_login, stored_senha, stored_nome = line.strip().split(';')
                        if login == stored_login and senha_hash == stored_senha:
                            line = f'{login};{senha_hash};{nome}\n'
                        file.write(line)

                self.send_response(302)
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

            print(f'Turma: {descricao}')

            # Verifica a existência da turma
            if self.turma_existente(code, descricao):
                # Turma já existe, não é necessário fazer nada
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Turma já existe!".encode('utf-8'))
            else:
                # Adiciona a nova turma ao arquivo
                with open('dados_turmas.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{code};{descricao}\n')

                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Nova turma recebida com sucesso!".encode('utf-8'))
                print('laldlasdal')

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

            print(f'Atividade: {descricao}')

            # Verifica a existência da turma
            if self.atividade_existente(codigo, descricao):
                # atividade já existe, não é necessário fazer nada
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Atividade já existe!".encode('utf-8'))
            else:
                # Adiciona a nova turma ao arquivo
                with open('dados_atividades.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{codigo};{descricao}\n')

                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Nova lalala com sucesso!".encode('utf-8'))

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

            print(f'Turma: {descricao}')

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
                self.wfile.write("Nova lalala2 com sucesso!".encode('utf-8'))

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
                print("IF POST LALAL")
            else:
                # Adiciona a nova turma ao arquivo
                with open('dados_turma_atividade.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{code};{codigo}\n')
                
                print("Else do post llalal")

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
