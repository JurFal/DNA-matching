import os
import time
from find2 import read_file, sliding_window_align, format_output
from test import calculate_value

def test_window_sizes():
    """测试不同滑动窗口大小的效果"""
    # 读取序列文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ref = read_file(os.path.join(current_dir, 'ref.txt'))
    query = read_file(os.path.join(current_dir, 'query.txt'))
    
    # 定义不同的窗口大小配置
    window_configs = [
        (20, 10, "小窗口-密集步长"),
        (30, 15, "中小窗口-中等步长"),
        (40, 20, "中等窗口-中等步长"),
        (50, 25, "大窗口-大步长"),
        (60, 30, "较大窗口-较大步长"),
        (35, 17, "中等窗口-小步长"),
        (25, 5, "小窗口-很小步长"),
        (45, 15, "大窗口-小步长"),
        (55, 35, "很大窗口-很大步长"),
        (15, 7, "很小窗口-很小步长")
    ]
    
    print("=" * 80)
    print("不同滑动窗口大小的序列比对结果比较")
    print("=" * 80)
    print(f"参考序列长度: {len(ref)}")
    print(f"查询序列长度: {len(query)}")
    print("=" * 80)
    
    results = []
    
    for window_size, step, description in window_configs:
        print(f"\n测试配置: {description}")
        print(f"窗口大小: {window_size}, 步长: {step}")
        
        # 记录开始时间
        start_time = time.time()
        
        # 执行滑动窗口比对
        alignments = sliding_window_align(ref, query, window_size=window_size, step=step)
        
        # 记录结束时间
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 格式化结果
        result_tuples = format_output(alignments)
        
        # 计算总分
        total_score = calculate_value(result_tuples, ref, query)
        
        # 统计信息
        num_alignments = len(alignments)
        total_aligned_length = sum(q_end - q_start for q_start, q_end, r_start, r_end in alignments)
        coverage = total_aligned_length / len(query) * 100 if len(query) > 0 else 0
        
        print(f"比对片段数量: {num_alignments}")
        print(f"总比对长度: {total_aligned_length}")
        print(f"查询序列覆盖率: {coverage:.2f}%")
        print(f"总分: {total_score}")
        print(f"执行时间: {execution_time:.4f}秒")
        
        # 保存结果
        results.append({
            'config': description,
            'window_size': window_size,
            'step': step,
            'num_alignments': num_alignments,
            'total_aligned_length': total_aligned_length,
            'coverage': coverage,
            'total_score': total_score,
            'execution_time': execution_time,
            'result_tuples': result_tuples
        })
        
        print("-" * 60)
    
    # 分析结果
    print("\n" + "=" * 80)
    print("结果分析")
    print("=" * 80)
    
    # 按总分排序
    results_by_score = sorted(results, key=lambda x: x['total_score'], reverse=True)
    print("\n按总分排序的结果:")
    for i, result in enumerate(results_by_score[:5], 1):
        print(f"{i}. {result['config']} (窗口:{result['window_size']}, 步长:{result['step']})")
        print(f"   总分: {result['total_score']}, 覆盖率: {result['coverage']:.2f}%, 时间: {result['execution_time']:.4f}s")
    
    # 按覆盖率排序
    results_by_coverage = sorted(results, key=lambda x: x['coverage'], reverse=True)
    print("\n按覆盖率排序的结果:")
    for i, result in enumerate(results_by_coverage[:5], 1):
        print(f"{i}. {result['config']} (窗口:{result['window_size']}, 步长:{result['step']})")
        print(f"   覆盖率: {result['coverage']:.2f}%, 总分: {result['total_score']}, 时间: {result['execution_time']:.4f}s")
    
    # 按执行时间排序
    results_by_time = sorted(results, key=lambda x: x['execution_time'])
    print("\n按执行时间排序的结果:")
    for i, result in enumerate(results_by_time[:5], 1):
        print(f"{i}. {result['config']} (窗口:{result['window_size']}, 步长:{result['step']})")
        print(f"   时间: {result['execution_time']:.4f}s, 总分: {result['total_score']}, 覆盖率: {result['coverage']:.2f}%")
    
    # 找出最佳配置
    best_score = max(results, key=lambda x: x['total_score'])
    print(f"\n最佳总分配置: {best_score['config']}")
    print(f"窗口大小: {best_score['window_size']}, 步长: {best_score['step']}")
    print(f"总分: {best_score['total_score']}, 覆盖率: {best_score['coverage']:.2f}%")
    
    # 保存详细结果到文件
    with open('window_size_comparison_results.txt', 'w') as f:
        f.write("滑动窗口大小比较结果\n")
        f.write("=" * 50 + "\n")
        for result in results_by_score:
            f.write(f"\n配置: {result['config']}\n")
            f.write(f"窗口大小: {result['window_size']}, 步长: {result['step']}\n")
            f.write(f"总分: {result['total_score']}\n")
            f.write(f"覆盖率: {result['coverage']:.2f}%\n")
            f.write(f"执行时间: {result['execution_time']:.4f}秒\n")
            f.write(f"比对结果: {result['result_tuples']}\n")
            f.write("-" * 40 + "\n")
    
    print("\n详细结果已保存到 'window_size_comparison_results.txt' 文件中")
    
    return results

if __name__ == "__main__":
    test_window_sizes()