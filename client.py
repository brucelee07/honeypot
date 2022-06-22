import socket
"""
socket 客户端测试模块
"""


# 连接单个端口
def connect_service(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置接收数据超时
    sock.settimeout(5)
    try:
        # 连接服务器
        sock.connect((ip, int(port)))
        # 连接， 并尝试接收数据
        rec = sock.recv(1024)
        print(rec)
        print(f"主机 {ip}, 端口 {port} 开放")
    except ConnectionRefusedError:
        print(f"主机 {ip}, 端口 {port} 关闭")
    except socket.timeout:
        pass
    finally:
        # 关闭sock
        sock.close()


# 扫描多个端口
def scan(ip, ports):
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, int(port)))
            rec = sock.recv(1024)
            print(rec)
            print(f"主机 {ip}, 端口 {port} 开放")
        except ConnectionRefusedError:
            print(f"主机 {ip}, 端口 {port} 关闭")
        finally:
            sock.close()


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = "502"
    connect_service(ip, port)

    ports = ['503', '502', '666']
    scan(ip, ports)
