# importações
import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs


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

            # # adiciona mensagem de erro
            mensagem = 'Login e/ou senha incorreto. Tente novamente.'
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
            # # envia pro cliente
            self.wfile.write(content.encode('utf-8'))
            # self.wfile.write("Senha incorreta".encode('utf-8'))

        else:
            # se não achar a rota "/login", continua o comportamento padrão
            super().do_GET()

    def usuario_existente(self, login, senha):
        # verifica a existência do login
        with open('dados_login.txt', 'r', encoding='utf-8') as file:
            for line in file:
                stored_login, stored_senha = line.strip().split(';')
                if login == stored_login:
                    print("Cheguei aqui significando que localizei o login informado.")
                    print("Senha:" + senha)
                    print("Senha armazenada:" + senha)
                    return senha == stored_senha
        return False

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
                        file.write(f"{login};{senha}\n")
                    # responde com boas vindas
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    mensagem = f"Olá, {login}, seja bem-vindo! Percebemos que você é novo por aqui."
                    self.wfile.write(mensagem.encode('utf-8'))

        else:
            # se não for a rota "/login", continua com o comportamento padrão
            super(MyHandler, self).do_POST()


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
