import socket
import threading

#local
#HOST = "127.0.0.1"

#outros dispositivos(ip da maquida que roda o servidor)
#HOST = "..."
PORTA = 5000

def receber_mensagens(cliente):
    while True:
        try:
            dados = cliente.recv(1024)

            if not dados:
                break

            mensagem = dados.decode()

            print(f"\n{mensagem}")
            print("Você: ", end="", flush=True)

        except ConnectionResetError:
            break

        except:
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

while True:
    mensagem = input("Você: ")

    cliente.send(mensagem.encode())

    if mensagem.lower() == "/sair":
        break

cliente.close()

print("Conexão encerrada.")