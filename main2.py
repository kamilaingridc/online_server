# importações
import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs, urlparse


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

        else:
            # se não achar a rota "/login", continua o comportamento padrão
            super().do_GET()

    def usuario_existente(self, login, senha):
        # verifica a existência do login
        with open('dados_login.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    stored_login, stored_senha, stored_nome = line.strip().split(';')
                    if login == stored_login:
                        print("Cheguei aqui significando que localizei o login informado.")
                        print("Senha:" + senha)
                        print("Senha armazenada:" + senha)
                        return senha == stored_senha
        return False

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
                # with open(os.path.join(os.getcwd(), 'index.html'), 'r') as file:
                #     content = file.read()
                # self.wfile.write(content.encode('utf-8'))
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
                    with open('dados_login.txt', 'a', encoding='utf-8') as file:
                        file.write(f"{login};{senha};" + "none\n")

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

            print(f'Nome: {nome}')

            # verifica existencia do usuario
            if self.usuario_existente(login, senha):

                # atualiza o arquivo com o nome, se a senha estiver correta
                with open('dados_login.txt', 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                with open('dados_login.txt', 'w', encoding='utf-8') as file:
                    for line in lines:
                        stored_login, stored_senha, stored_nome = line.strip().split(';')
                        if login == stored_login and senha == stored_senha:
                            line = f'{login};{senha};{nome}\n'
                        file.write(line)

                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("Registro recebido com sucesso!".encode('utf-8'))

        else:
            self.remover_ultima_linha('dados_login.txt')
            self.send_response(302)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("RSenha não confere. Retome o procedimento.".encode('utf-8'))


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
