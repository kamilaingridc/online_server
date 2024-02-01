# importa o módulo http.server
import http.server
import socketserver

# define a porta a ser utilizada
porta = 8000

# configura o manipulador (handler) para o servidor
handler = http.server.SimpleHTTPRequestHandler

# cria um servidor na porta especificada
with socketserver.TCPServer(("", porta), handler) as httpd:
    print(f"Servidor iniciado na porta {porta}.")
    # mantém o servidor em execução
    httpd.serve_forever()
