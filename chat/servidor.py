import socket
import threading

#local
#HOST = "127.0.0.1"

#Outros dispositivos
#HOST = "0.0.0.0"
PORTA = 5000

clientes = {}
lock = threading.Lock()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((HOST, PORTA))

servidor.listen()

print(f"Servidor aguardando conexões em {HOST}:{PORTA}...")

while True:
    cliente, endereco = servidor.accept()

    thread = threading.Thread(
        target=atender_cliente,
        args=(cliente, endereco)
    )
    thread.start()   
    
def transmitir(mensagem, cliente_origem=None):
    with lock:
        for cliente in clientes:
            if cliente != cliente_origem:
                try:
                    cliente.send(mensagem.encode())
                except:
                    pass

def listar_usuarios():
    with lock:
        if not clientes:
            return "[Servidor] Nenhum usuário conectado."

        nomes = "\n".join(f"- {nome}" for nome in clientes.values())

        return f"[Servidor] Usuários conectados:\n{nomes}"

def atender_cliente(cliente, endereco):
    nome = None

    try:
        cliente.send("Digite seu nome: ".encode())

        dados = cliente.recv(1024)

        if not dados:
            return

        nome = dados.decode().strip()

        with lock:
            clientes[cliente] = nome

        print(f"{nome} entrou no chat. Endereço: {endereco}")

        transmitir(f"[Servidor] {nome} entrou no chat.", cliente)

        cliente.send(
            "[Servidor] Você entrou no chat. Digite /help para ver os comandos.".encode()
        )

        while True:
            dados = cliente.recv(1024)

            if not dados:
                break

            mensagem = dados.decode().strip()

            if mensagem.lower() == "/sair":
                cliente.send("[Servidor] Você saiu do chat.".encode())
                break

            elif mensagem.lower() == "/usuarios":
                resposta = listar_usuarios()
                cliente.send(resposta.encode())

            elif mensagem.lower() == "/help":
                resposta = (
                    "[Servidor] Comandos disponíveis:\n"
                    "/usuarios - lista os usuários conectados\n"
                    "/help - mostra os comandos\n"
                    "/sair - sai do chat"
                )

                cliente.send(resposta.encode())

            elif mensagem:
                mensagem_chat = f"{nome}: {mensagem}"

                print(mensagem_chat)

                transmitir(mensagem_chat, cliente)

    except ConnectionResetError:
        print(f"{endereco} encerrou a conexão.")

    except Exception as erro:
        print(f"Erro com {endereco}: {erro}")

    finally:
        with lock:
            if cliente in clientes:
                del clientes[cliente]

        if nome:
            transmitir(f"[Servidor] {nome} saiu do chat.", cliente)
            print(f"{nome} saiu do chat.")

        cliente.close()