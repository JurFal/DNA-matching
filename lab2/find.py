import edlib
import os
import test

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r') as f:
        return f.read().strip()

def get_rc(s):
    """获取反向互补序列"""
    map_dict = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}
    l = []
    for c in s:
        l.append(map_dict[c])
    l = l[::-1]
    return ''.join(l)

def calculate_edit_distance(ref, query, ref_start, ref_end, query_start, query_end):
    """计算两个序列片段之间的编辑距离"""
    ref_seq = ref[ref_start:ref_end]
    query_seq = query[query_start:query_end]
    query_rc = get_rc(query_seq)
    
    dist1 = edlib.align(ref_seq, query_seq)['editDistance']
    dist2 = edlib.align(ref_seq, query_rc)['editDistance']
    
    return min(dist1, dist2)

def sliding_window_align(ref, query, window_size=50, step=25, step_r=1):
    """滑动窗口比对，用于填补空隙"""
    alignments = []
    
    for q_start in range(0, len(query) - window_size + 1, step):
        q_end = min(q_start + window_size, len(query))
        query_window = query[q_start:q_end]
        query_rc = get_rc(query_window)
        
        best_score = -1
        best_match = None
        
        # 在参考序列中搜索最佳匹配
        for r_start in range(0, len(ref) - len(query_window) + 1, step_r):
            r_end = r_start + len(query_window)
            ref_window = ref[r_start:r_end]
            
            # 正向匹配
            dist1 = edlib.align(ref_window, query_window)['editDistance']
            score1 = len(query_window) - dist1
            
            # 反向互补匹配
            dist2 = edlib.align(ref_window, query_rc)['editDistance']
            score2 = len(query_window) - dist2
            
            score = max(score1, score2)
            
            if score > best_score and score >= len(query_window) * 0.1:  # 调整匹配阈值
                best_score = score
                best_match = (q_start, q_end, r_start, r_end)
        
        if best_match:
            alignments.append(best_match)
    
    return alignments

def align_sequences(ref, query):
    """主要的序列比对函数"""
    all_alignments = []
    
    # 合适尺寸的滑动窗口比对
    window_alignments = sliding_window_align(ref, query, window_size=161, step=161, step_r=1)
    all_alignments.extend(window_alignments)
    
    # 合并和去重
    if not all_alignments:
        return []
    
    # 按query位置排序
    all_alignments.sort(key=lambda x: x[0])
    
    # 去重并合并重叠区域
    merged = []
    for alignment in all_alignments:
        q_start, q_end, r_start, r_end = alignment
        merged_flag = False
        
        for i, (mq_start, mq_end, mr_start, mr_end) in enumerate(merged):
            # 检查重叠
            if (q_start < mq_end and q_end > mq_start):
                # 选择更长的片段
                if (q_end - q_start) > (mq_end - mq_start):
                    merged[i] = alignment
                merged_flag = True
                break
        if not merged_flag:
            merged.append(alignment)
    
    # 接合连续区域：当q_end为下一个序列的q_start且r_end为下一个序列的r_start时合并
    final_merged = []
    i = 0
    while i < len(merged):
        current = merged[i]
        q_start, q_end, r_start, r_end = current
        
        # 查找可以接合的连续区域
        j = i + 1
        while j < len(merged):
            next_q_start, next_q_end, next_r_start, next_r_end = merged[j]
            
            # 检查是否可以接合：当前序列的结束位置等于下一个序列的开始位置
            if q_end == next_q_start and r_end == next_r_start:
                # 合并为连续区域
                q_end = next_q_end
                r_end = next_r_end
                j += 1
            else:
                break
        
        # 添加合并后的区域
        final_merged.append((q_start, q_end, r_start, r_end))
        i = j
    
    return final_merged

def format_output(alignments):
    """格式化输出"""
    result = []
    for q_start, q_end, r_start, r_end in alignments:
        result.append(f"({q_start}, {q_end}, {r_start}, {r_end})")
    return "[" + ", ".join(result) + "]"

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ref = read_file(os.path.join(current_dir, 'ref2.txt'))
    query = read_file(os.path.join(current_dir, 'query2.txt'))
    
    # 执行比对
    alignments = align_sequences(ref, query)
    
    # 输出结果
    result_tuples = format_output(alignments)
    print(result_tuples)
    
    # 计算分数（用于验证）
    total_score = test.calculate_value(result_tuples, ref, query)
    print(f"Total score: {total_score}")
    