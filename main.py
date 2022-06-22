from pathlib import Path
import argparse

from honeypot import HoneyPot

# 定义logger文件路径
FOLD = Path(__file__).resolve().parent / "log"

# 确保logger文件夹存在
if not FOLD.is_dir():
    FOLD.mkdir()


# 主程序入口
def main():
    # 控制台输入参数处理
    # 例如 python main.py -H 127.0.0.1 -p 8080,80 -l new_socket_log
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',
                        '-H',
                        default='127.0.0.1',
                        type=str,
                        help='host address')
    parser.add_argument('--port',
                        '-p',
                        default='502, 666',
                        type=str,
                        help='port defalut 502,666')
    parser.add_argument('--log_file',
                        '-l',
                        default='socket_log_',
                        type=str,
                        help='log file path')
    args = parser.parse_args()

    # 从控制台获取参数
    host = args.host
    port = args.port
    log_file = FOLD / args.log_file

    # 处理端口
    if ',' in port:
        ports = port.split(",")
    else:
        ports = [port]
    # 创建 HoneyPot实例，并运行
    honeypot = HoneyPot(host, ports, log_file)
    honeypot.run()


if __name__ == "__main__":
    main()
