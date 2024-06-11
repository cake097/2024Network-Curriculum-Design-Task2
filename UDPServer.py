# 导入所需的库
import socket  # 导入 socket 库
import random  # 导入 random 库
import threading  # 导入 threading 库
import time  # 导入 time 库


# 定义 UDP 服务器函数
def udp_server(host='127.0.0.1', port=50000):
    # 创建一个 UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置 socket 选项，允许地址复用
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定 socket 到指定的 host 和 port
    try:
        server_socket.bind((host, port))
    except OSError as e:
        print(f"绑定到 {host}:{port} 失败: {e}")
        # 可以选择退出程序或者尝试绑定到其他端口
        # 退出程序的示例代码：
        import sys
        sys.exit(1)
    print(f'服务器已启动，在 {host}:{port} 监听')

    # 设置初始的丢包率
    drop_probability = 0.3

    # 定义处理客户端消息的函数
    def handle_client_messages():
        while True:
            # 接收客户端的消息
            message, client_address = server_socket.recvfrom(2048)

            # 检查是否为连接请求
            if message == b'CONNECT':
                print(f'收到来自 {client_address} 的连接请求')
                server_socket.sendto(b'CONNECTED', client_address)
                continue

            # 解析消息中的序列号和版本号
            sequence_number = int.from_bytes(message[:2], byteorder='big')
            ver = int.from_bytes(message[2:3], byteorder='big')

            # 根据丢包率随机决定是否丢弃该消息
            if random.random() < drop_probability:
                print(f'丢弃来自 {client_address} 的消息: 序号={sequence_number}, 版本={ver}')
                continue

            print(f'收到来自 {client_address} 的消息: 序号={sequence_number}, 版本={ver}')

            # 获取当前时间，并将其编码为 bytes
            current_time = time.strftime("%H-%M-%S", time.localtime()).encode('utf-8')
            # 构造响应消息
            response = message[:3] + current_time.ljust(200 - len(message[:3]), b' ')
            # 发送响应消息到客户端
            server_socket.sendto(response, client_address)

    # 定义调整丢包率的函数
    def adjust_drop_probability():
        nonlocal drop_probability
        while True:
            # 获取用户输入的新丢包率
            user_input = input("输入新的丢包率 (0 到 1 之间): ")
            try:
                new_drop_probability = float(user_input)
                # 检查新丢包率是否在有效范围内
                if 0 <= new_drop_probability <= 1:
                    # 更新丢包率
                    drop_probability = new_drop_probability
                    print(f'丢包率已更新为: {drop_probability}')
                else:
                    print("请输入 0 到 1 之间的数值。")
            except ValueError:
                print("无效输入，请输入数值。")

    # 创建并启动处理客户端消息的线程
    client_thread = threading.Thread(target=handle_client_messages)
    client_thread.daemon = True
    client_thread.start()

    # 创建并启动调整丢包率的线程
    adjust_thread = threading.Thread(target=adjust_drop_probability)
    adjust_thread.daemon = True
    adjust_thread.start()

    # 等待两个线程结束
    client_thread.join()
    adjust_thread.join()


# 如果该脚本被直接运行，则启动 UDP 服务器
if __name__ == "__main__":
    udp_server()
