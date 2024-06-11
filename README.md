# 2024Network-Curriculum-Design-Task2

## 概述

本项目包含一个简单的UDP服务器和客户端的Python实现。服务器可以处理客户端连接，模拟丢包，并返回当前服务器时间。客户端可以连接到服务器，发送多次请求，并计算往返时间（RTT）统计信息。

## 环境要求

- Python 3.x
- 库：`socket`、`random`、`threading`、`time`、`statistics`

## 安装

1. 确保系统上安装了Python 3.x。
2. 克隆此仓库或复制代码文件。

## 使用方法

### 启动服务器

1. 打开终端或命令提示符。
2. 导航到包含服务器脚本的目录。
3. 运行服务器脚本：

    ```bash
    python server.py
    ```

    服务器将默认在 `127.0.0.1:50000` 上启动并监听。

### 启动客户端

1. 打开另一个终端或命令提示符。
2. 导航到包含客户端脚本的目录。
3. 运行客户端脚本，并在提示时输入服务器IP和端口：

    ```bash
    python client.py
    ```

    示例：

    ```bash
    请输入服务器 IP: 127.0.0.1
    请输入服务器端口: 50000
    ```

### 服务器详情

服务器脚本（`server.py`）包括：

- 处理客户端消息的函数。
- 动态调整丢包率的函数。
- 使用线程同时处理客户端消息和调整丢包率。

### 客户端详情

客户端脚本（`client.py`）包括：

- 向服务器发送连接请求的函数。
- 处理数据包重试和计算RTT统计信息的逻辑。
- 发送多次请求后输出详细统计信息。

## 功能

- **UDP 服务器**：处理客户端连接并模拟丢包。
- **丢包模拟**：可调整的丢包率以测试可靠性。
- **客户端-服务器通信**：客户端发送请求，服务器返回当前时间。
- **RTT 计算**：客户端计算并打印RTT统计信息（最小值、最大值、平均值、标准差）。

## 示例输出

### 服务器

```bash
服务器已启动，在 127.0.0.1:50000 监听
收到来自 ('127.0.0.1', 12345) 的连接请求
收到来自 ('127.0.0.1', 12345) 的消息: 序号=1, 版本=2
...
```

### 客户端

```bash
请输入服务器 IP: 127.0.0.1
请输入服务器端口: 50000
连接已建立
接收到响应: 序号=1, 版本=2, 服务器时间=14-30-15, RTT=10.52 ms
...

【汇总】
接收到的 UDP packets 数目: 10
丢包率: 16.67%
最大 RTT: 30.42 ms
最小 RTT: 10.52 ms
平均 RTT: 20.32 ms
RTT 标准差: 5.23 ms
服务器整体响应时间: 14-30-25 - 14-30-15
```

## 注意事项

- 确保在启动客户端之前服务器已运行。
- 根据需要调整丢包率以测试不同的场景。
- 修改服务器和客户端脚本以满足特定需求或扩展功能。
