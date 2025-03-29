#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
朴素算法（O(n²)）的动态规划程序，用于寻找DNA序列中的重复片段和互补重复片段
"""

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r') as f:
        return f.read().strip()

def find_repeats(reference, query):
    """
    使用动态规划方法寻找两个序列中的重复片段
    时间复杂度：O(n²)，其中n是序列长度
    """
    ref_len = len(reference)
    query_len = len(query)
    
    # 创建动态规划表，dp[i][j]表示以reference[i]和query[j]结尾的最长公共子串长度
    dp = [[0 for _ in range(query_len + 1)] for _ in range(ref_len + 1)]
    
    # 记录最长重复片段的长度和位置
    max_length = 0
    max_ref_end = 0
    max_query_end = 0
    
    # 填充动态规划表
    for i in range(1, ref_len + 1):
        for j in range(1, query_len + 1):
            if reference[i-1] == query[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    max_ref_end = i
                    max_query_end = j
    
    # 找出所有重复片段（长度大于等于10的子串）
    repeats = []
    threshold = 10  # 设置最小重复长度阈值
    
    for i in range(1, ref_len + 1):
        for j in range(1, query_len + 1):
            if dp[i][j] >= threshold:
                # 检查是否是极大重复片段（即不能再向两边扩展）
                if i < ref_len and j < query_len and reference[i] == query[j]:
                    continue  # 可以向右扩展，不是极大重复片段
                
                # 提取重复片段
                length = dp[i][j]
                ref_start = i - length
                query_start = j - length
                ref_segment = reference[ref_start:i]
                query_segment = query[query_start:j]
                
                # 添加到结果列表
                repeats.append({
                    'length': length,
                    'ref_position': ref_start,
                    'query_position': query_start,
                    'segment': ref_segment
                })
    
    # 按长度降序排序
    repeats.sort(key=lambda x: x['length'], reverse=True)
    
    return repeats

def print_results(repeats, title):
    """打印重复片段结果"""
    # 过滤出长度不小于最小重复长度阈值(10)的两倍的重复片段
    threshold = 10  # 最小重复长度阈值
    filtered_repeats = [repeat for repeat in repeats if repeat['length'] >= threshold * 2]
    
    print(f"找到 {len(filtered_repeats)} 个{title}（长度≥{threshold*2}）：")
    for i, repeat in enumerate(filtered_repeats, 1):  # 输出所有结果，不限制为前10个
        print(f"{title} {i}:")
        print(f"  长度: {repeat['length']}")
        print(f"  参考序列位置: {repeat['ref_position']}")
        print(f"  查询序列位置: {repeat['query_position']}")
        print(f"  片段: {repeat['segment'][:50]}{'...' if len(repeat['segment']) > 50 else ''}")
        print()

def write_results_to_file(repeats, title, file):
    """将重复片段结果写入文件"""
    # 过滤出长度不小于最小重复长度阈值(10)的两倍的重复片段
    threshold = 10  # 最小重复长度阈值
    filtered_repeats = [repeat for repeat in repeats if repeat['length'] >= threshold * 2]
    
    file.write(f"找到 {len(filtered_repeats)} 个{title}（长度≥{threshold*2}）：\n")
    for i, repeat in enumerate(filtered_repeats, 1):  # 输出所有结果，不限制为前10个
        file.write(f"{title} {i}:\n")
        file.write(f"  长度: {repeat['length']}\n")
        file.write(f"  参考序列位置: {repeat['ref_position']}\n")
        file.write(f"  查询序列位置: {repeat['query_position']}\n")
        file.write(f"  片段: {repeat['segment'][:50]}{'...' if len(repeat['segment']) > 50 else ''}\n")
        file.write("\n")

def get_complement_sequence(sequence):
    """生成DNA序列的反向互补序列
    A-T互换，C-G互换，并反向排列
    """
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    complement_sequence = ''
    for base in reversed(sequence):
        complement_sequence += complement_map.get(base, base)
    return complement_sequence

def main():
    # 读取参考序列和查询序列
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    reference = read_file(os.path.join(current_dir, 'ref.txt'))
    query = read_file(os.path.join(current_dir, 'query.txt'))
    
    print(f"参考序列长度: {len(reference)}")
    print(f"查询序列长度: {len(query)}")
    
    # 寻找普通重复片段
    normal_repeats = find_repeats(reference, query)
    # 按长度降序排序
    normal_repeats.sort(key=lambda x: x['length'], reverse=True)
    
    # 生成查询序列的反向互补序列
    complement_query = get_complement_sequence(query)
    
    # 寻找互补重复片段
    complement_repeats = find_repeats(reference, complement_query)
    # 按长度降序排序
    complement_repeats.sort(key=lambda x: x['length'], reverse=True)
    
    # 分别打印正向重复片段和反向互补重复片段
    print("\n=== 正向重复片段 ===")
    print_results(normal_repeats, "正向重复片段")
    
    print("\n=== 反向互补重复片段 ===")
    print_results(complement_repeats, "反向互补重复片段")
    
    # 将结果写入文件
    result_file_path = os.path.join(current_dir, 'result.txt')
    with open(result_file_path, 'w') as result_file:
        result_file.write("=== 正向重复片段 ===\n")
        write_results_to_file(normal_repeats, "正向重复片段", result_file)
        
        result_file.write("\n=== 反向互补重复片段 ===\n")
        write_results_to_file(complement_repeats, "反向互补重复片段", result_file)
    
    print(f"\n结果已保存到文件: {result_file_path}")

if __name__ == "__main__":
    main()