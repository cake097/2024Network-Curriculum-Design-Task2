import socket  # 导入 socket 模块
import time  # 导入 time 模块
import statistics  # 导入 statistics 模块用于计算统计信息


# 定义一个 UDP 客户端函数
def udp_client(target_server_ip, target_server_port, num_requests=12, timeout=0.1):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建 UDP 套接字
    client_socket.settimeout(timeout)  # 设置套接字超时时间

    # 发送连接请求
    connect_request = b'CONNECT'
    client_socket.sendto(connect_request, (target_server_ip, target_server_port))
    # 等待连接确认
    try:
        response, _ = client_socket.recvfrom(2048)
        if response == b'CONNECTED':
            print('连接已建立')
        else:
            print('连接建立失败')
            return
    except socket.timeout:
        print('连接请求超时')
        return

    sequence_number = 1  # 初始化序列号为 1
    received_packets = 0  # 初始化接收数据包数为 0
    rtts = []  # 初始化 RTT 列表
    server_times = []  # 初始化服务器时间列表

    # 循环发送请求数据包
    for i in range(num_requests):
        sequence_number_bytes = sequence_number.to_bytes(2, byteorder='big')  # 序列号转换为字节
        ver = (2).to_bytes(1, byteorder='big')  # 版本号转换为字节
        data = sequence_number_bytes + ver + b'a' * 197  # 构建请求数据包

        retries = 0  # 初始化重试次数为 0
        while retries < 3:  # 最多重试 3 次
            start_time = time.time()  # 记录发送时间
            client_socket.sendto(data, (target_server_ip, target_server_port))  # 发送数据包到服务器

            try:
                response, _ = client_socket.recvfrom(2048)  # 接收服务器响应数据包
                rtt = (time.time() - start_time) * 1000  # 计算 RTT（单位：毫秒）
                recv_sequence_number = int.from_bytes(response[:2], byteorder='big')  # 解析响应中的序列号
                recv_ver = int.from_bytes(response[2:3], byteorder='big')  # 解析响应中的版本号
                server_time = response[3:12].decode('utf-8').strip()  # 解析响应中的服务器时间
                print(
                    f'接收到响应: 序号={recv_sequence_number}, 版本={recv_ver}, 服务器时间={server_time}, RTT={rtt:.2f} ms')
                # 打印接收到的响应信息

                received_packets += 1  # 接收的数据包数加一
                rtts.append(rtt)  # 将 RTT 添加到列表中
                server_times.append(server_time)  # 将服务器时间添加到列表中
                break  # 跳出重试循环
            except socket.timeout:  # 如果超时
                print(f'序号 {sequence_number}: 请求超时')  # 打印超时信息
                retries += 1  # 重试次数加一

        sequence_number += 1  # 序列号加一

    client_socket.close()  # 关闭套接字

    # 打印汇总信息
    print("\n【汇总】")
    print(f"接收到的 UDP packets 数目: {received_packets}")
    print(f"丢包率: {((num_requests - received_packets) / num_requests) * 100:.2f}%")
    if rtts:
        print(f"最大 RTT: {max(rtts):.2f} ms")
        print(f"最小 RTT: {min(rtts):.2f} ms")
        print(f"平均 RTT: {statistics.mean(rtts):.2f} ms")
        print(f"RTT 标准差: {statistics.stdev(rtts):.2f} ms")
    if server_times:
        print(f"服务器整体响应时间: {server_times[-1]} - {server_times[0]}")


if __name__ == "__main__":
    server_ip = input("请输入服务器 IP: ")  # 输入服务器 IP 地址
    server_port = int(input("请输入服务器端口: "))  # 输入服务器端口号
    udp_client(server_ip, server_port)  # 调用 UDP 客户端函数
