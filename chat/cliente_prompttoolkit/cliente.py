import socket
import threading
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

HOST = "127.0.0.1"
PORTA = 5000

def receber_mensagens(cliente):
    while True:
        try:
            dados = cliente.recv(1024)

            if not dados:
                break

            mensagem = dados.decode()

            print(mensagem)

        except ConnectionResetError:
            break

        except OSError:
            break

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((HOST, PORTA))

mensagem = cliente.recv(1024).decode()

print(mensagem)

nome = input("Nome: ")

cliente.send(nome.encode())

thread_receber = threading.Thread(
    target=receber_mensagens,
    args=(cliente,)
)

thread_receber.daemon = True
thread_receber.start()

print()
print("Você está conectado ao chat.")
print("Digite /help para ver os comandos.")
print()

session = PromptSession()

with patch_stdout():
    while True:

        try:
            mensagem = session.prompt("Você: ")

            if not mensagem:
                continue

            cliente.send(mensagem.encode())

            if mensagem.lower() == "/sair":
                break

        except (KeyboardInterrupt, EOFError):
            break

cliente.close()

print("Conexão encerrada.")