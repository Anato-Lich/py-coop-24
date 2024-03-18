import socket
from cowsay import cowsay

class CowChatServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.users = {}  # Словарь для хранения пользователей и их сокетов
        self.cows = set(cowsay.get_cow_list())  # Список доступных имен коров

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Сервер запущен на {self.host}:{self.port}")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Подключение клиента {client_address}")
                client_socket.send("Добро пожаловать в коровий чат!\n".encode())

                while True:
                    try:
                        data = client_socket.recv(1024).decode().strip()
                        if not data:
                            print(f"Клиент {client_address} отключился")
                            break

                        command = data.split()
                        if command[0] == 'who':
                            client_socket.send(str(list(self.users.keys())).encode() + b'\n')
                        elif command[0] == 'cows':
                            client_socket.send(str(list(self.cows)).encode() + b'\n')
                        elif command[0] == 'login':
                            if len(command) < 2:
                                client_socket.send("Использование: login <название_коровы>\n".encode())
                            else:
                                cow_name = command[1]
                                if cow_name in self.cows:
                                    self.users[cow_name] = client_socket
                                    client_socket.send(f"Вы успешно зарегистрированы под именем {cow_name}\n".encode())
                                else:
                                    client_socket.send(f"Коровы с именем {cow_name} не существует\n".encode())
                        elif command[0] == 'say':
                            if len(command) < 3:
                                client_socket.send("Использование: say <название_коровы> <текст_сообщения>\n".encode())
                            else:
                                recipient = command[1]
                                message = ' '.join(command[2:])
                                if recipient in self.users:
                                    self.users[recipient].send(cowsay(message).encode() + b'\n')
                                else:
                                    client_socket.send(f"Пользователь с именем {recipient} не найден\n".encode())
                        elif command[0] == 'yield':
                            message = ' '.join(command[1:])
                            for user_socket in self.users.values():
                                user_socket.send(cowsay(message).encode() + b'\n')
                        elif command[0] == 'quit':
                            client_socket.send("До свидания!\n".encode())
                            del self.users[client_address]
                            break
                        else:
                            client_socket.send("Неверная команда\n".encode())
                    except Exception as e:
                        print(f"Ошибка: {e}")
                        break

if __name__ == "__main__":
    server = CowChatServer()
    server.run()
