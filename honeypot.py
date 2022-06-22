import logging
import socket
import threading
"""
HoneyPot 为socket 密罐类
初始化 密罐socket侦听 端口 502 666 等等
初始化 logging handle
"""


class HoneyPot:

    # 绑定的ip, port, logfilepath ip 127.0.0.1为本地 0.0.0.0为局域网
    def __init__(self, bind_ip, ports, log_filepath):

        # 判断 ports是不是合法
        if not ports:
            raise Exception("没有提供合适的端口.")

        for port in ports:
            try:
                if int(port) < 0 or int(port) > 9999:
                    raise Exception("端口介于0～9999")
            except ValueError:
                raise Exception("端口仅由数字组成")

        self.bind_ip = bind_ip
        self.ports = ports
        self.log_filepath = log_filepath

        # 侦听sockets 线程
        self.listener_threads = {}

        # 初始化 logger
        self.logger = self.prepare_logger()

        self.logger.info("密罐初始化...")
        self.logger.info(f"所有侦听端口: {'|'.join(ports)}")
        self.logger.info(f"Log 文件路径: {str(log_filepath)}")

    # 处理侦听到的扫描信息， 记录，并放送拒绝访问信息
    def handle_connection(self, client_socket, port, ip, remote_port):
        self.logger.info(f"收到- {ip}:{remote_port} 连接请求!")
        # 设置接受数据时长
        client_socket.settimeout(4)
        try:
            client_socket.sendall("Access denied.\n".encode())
            data = client_socket.recv(1024)
            self.logger.info(f"收到- {ip}:{remote_port} 数据{data}!")
        except socket.timeout:
            pass

    # 对不同侦听端口，创建socket
    def start_new_listener_thread(self, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            listener.bind((self.bind_ip, int(port)))
        except PermissionError:
            self.logger.info(f"端口号:{port} 需要权限绑定！")
            return
        listener.listen(5)
        # 对该侦听端口下不同的连接采用多线程处理
        while True:
            client, addr = listener.accept()
            client_handler = threading.Thread(target=self.handle_connection,
                                              args=(client, port, addr[0],
                                                    addr[1]))
            client_handler.start()

    # 初始化多个端口socket, 多线程处理
    def start_listening(self):
        for port in self.ports:
            t = threading.Thread(target=self.start_new_listener_thread,
                                 args=(port, ))
            t.start()
            self.listener_threads[port] = t

    # HoneyPot运行入口
    def run(self):
        self.start_listening()

    # 初始化logger
    def prepare_logger(self):
        # logger基础设置
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%s',
                            filename=self.log_filepath,
                            filemode='w')
        logger = logging.getLogger()
        # logger 控制台handle
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        return logger
