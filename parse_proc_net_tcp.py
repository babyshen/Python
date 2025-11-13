#!/usr/bin/env python3
"""
解析 /proc/net/tcp 文件，将十六进制格式的地址、端口和状态转换为易读格式
"""

import sys
import os
from collections import defaultdict

# TCP 状态码映射表
TCP_STATUS = {
    "00": "ERROR_STATUS",
    "01": "TCP_ESTABLISHED",
    "02": "TCP_SYN_SENT", 
    "03": "TCP_SYN_RECV",
    "04": "TCP_FIN_WAIT1",
    "05": "TCP_FIN_WAIT2",
    "06": "TCP_TIME_WAIT",
    "07": "TCP_CLOSE",
    "08": "TCP_CLOSE_WAIT",
    "09": "TCP_LAST_ACK",
    "0A": "TCP_LISTEN",
    "0B": "TCP_CLOSING"
}

def hex_ip_to_readable(hex_ip, hex_port):
    """
    将十六进制的IP地址和端口转换为可读格式 
    IP地址是网络字节序（大端序），需要反转处理
    """
    try:
        # 将IP地址从十六进制转换为十进制，并反转顺序
        ip_parts = []
        for i in range(0, 8, 2):
            hex_part = hex_ip[i:i+2]
            if hex_part:  # 确保hex_part不为空
                ip_parts.append(str(int(hex_part, 16)))
        
        # 确保有4个IP部分
        if len(ip_parts) == 4:
            readable_ip = ".".join(reversed(ip_parts))
        else:
            readable_ip = f"Invalid_IP_{hex_ip}"
        
        # 转换端口
        readable_port = str(int(hex_port, 16))
        
        return readable_ip, readable_port
    except ValueError as e:
        return f"Invalid_IP_{hex_ip}", f"Invalid_Port_{hex_port}"

def parse_proc_net_tcp(file_path="/proc/net/tcp"):
    """
    解析 /proc/net/tcp 文件 [1,2](@ref)
    """
    connections = []
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"错误: 找不到文件 {file_path}")
        return []
    except PermissionError:
        print(f"错误: 没有权限读取文件 {file_path}，请使用sudo运行")
        return []
    
    # 跳过标题行 [1](@ref)
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        if len(parts) < 4:
            continue
            
        try:
            # 解析本地地址和远程地址
            local_address = parts[1]  # 格式: 010310AC:9C4C
            remote_address = parts[2]  # 格式: 030310AC:1770
            state_hex = parts[3]  # 状态码(十六进制)
            
            # 分离IP和端口
            local_ip_hex, local_port_hex = local_address.split(':')
            remote_ip_hex, remote_port_hex = remote_address.split(':')
            
            # 转换地址格式 [3](@ref)
            local_ip_readable, local_port_readable = hex_ip_to_readable(local_ip_hex, local_port_hex)
            remote_ip_readable, remote_port_readable = hex_ip_to_readable(remote_ip_hex, remote_port_hex)
            
            # 获取状态描述
            state_description = TCP_STATUS.get(state_hex, f"UNKNOWN({state_hex})")
            
            # 获取其他有用信息 [4](@ref)
            uid = parts[7] if len(parts) > 7 else "N/A"
            inode = parts[9] if len(parts) > 9 else "N/A"
            
            connection_info = {
                'local_address': f"{local_ip_readable}:{local_port_readable}",
                'remote_address': f"{remote_ip_readable}:{remote_port_readable}",
                'state_hex': state_hex,
                'state': state_description,
                'uid': uid,
                'inode': inode,
                'local_ip_hex': local_ip_hex,
                'local_port_hex': local_port_hex,
                'remote_ip_hex': remote_ip_hex,
                'remote_port_hex': remote_port_hex
            }
            
            connections.append(connection_info)
            
        except (ValueError, IndexError) as e:
            print(f"警告: 解析行时出错 - {line}")
            continue
    
    return connections

def print_connections_table(connections):
    """
    以表格形式打印连接信息
    """
    if not connections:
        print("未找到TCP连接信息")
        return
    
    print("\n" + "="*120)
    print(f"{'本地地址':<25} {'远程地址':<25} {'状态':<20} {'UID':<8} {'Inode':<10} {'状态码'}")
    print("="*120)
    
    for conn in connections:
        print(f"{conn['local_address']:<25} {conn['remote_address']:<25} {conn['state']:<20} "
              f"{conn['uid']:<8} {conn['inode']:<10} {conn['state_hex']}")

def print_connection_statistics(connections):
    """
    打印连接统计信息 [6](@ref)
    """
    if not connections:
        return
        
    state_stats = defaultdict(int)
    for conn in connections:
        state_stats[conn['state']] += 1
    
    print("\n" + "="*50)
    print("TCP连接状态统计")
    print("="*50)
    for state, count in sorted(state_stats.items()):
        print(f"{state:<20}: {count}")

def main():
    """
    主函数
    """
    file_path = "/proc/net/tcp"
    
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在")
        sys.exit(1)
    
    print("正在解析 /proc/net/tcp 文件...")
    connections = parse_proc_net_tcp(file_path)
    
    if connections:
        print_connections_table(connections)
        print_connection_statistics(connections)
        
        # 可选: 保存到文件
        save_to_file = input("\n是否将结果保存到文件? (y/n): ").lower()
        if save_to_file == 'y':
            filename = "tcp_connections.txt"
            with open(filename, 'w') as f:
                # 重定向输出到文件
                import sys
                original_stdout = sys.stdout
                sys.stdout = f
                print_connections_table(connections)
                print_connection_statistics(connections)
                sys.stdout = original_stdout
            print(f"结果已保存到 {filename}")
    else:
        print("未解析到任何TCP连接信息")

if __name__ == "__main__":
    main()
