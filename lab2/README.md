# 存在结构变异的DNA序列比对问题

## 算法概述

本项目实现了一个基于分块滑动窗口动态规划的DNA序列匹配算法，用于在存在结构变异的DNA序列之间寻找重复片段和反向互补重复片段。

## 算法原理

### 滑动窗口分块匹配

滑动窗口分块匹配算法是一种高效的序列比对方法，通过将查询序列分割成固定大小的窗口，在参考序列中寻找最佳匹配位置。该算法的核心思想包括：

1. **窗口划分**：将查询序列按照固定窗口大小W和步长S1进行分割，生成多个重叠或非重叠的子序列窗口

2. **双向匹配**：对每个查询窗口，同时考虑正向序列和反向互补序列，以处理DNA序列中可能存在的反向互补重复

3. **滑动搜索**：在参考序列中以步长S2滑动搜索，寻找与当前查询窗口最佳匹配的位置

4. **编辑距离评估**：使用edlib库计算编辑距离，评估匹配质量，选择编辑距离最小的匹配

5. **后处理优化**：
   - 去重：移除重叠的匹配片段，保留质量更高的匹配
   - 合并：将相邻的连续匹配片段合并为更长的匹配区域
   - 过滤：根据匹配阈值过滤低质量匹配

### 伪代码

```pseudocode
function sliding_window_align(ref, query, window_size, step):
    alignments = []
    // 外层循环：遍历查询序列的所有窗口
    for q_start = 0 to len(query) - window_size step step:
        q_end = q_start + window_size
        query_window = query[q_start:q_end]
        query_rc = reverse_complement(query_window)
        
        best_score = -1
        best_match = null
        
        // 内层循环：在参考序列中搜索最佳匹配
        for r_start = 0 to len(ref) - window_size step step:
            r_end = r_start + window_size
            ref_window = ref[r_start:r_end]
            
            // 计算正向和反向互补匹配的编辑距离
            dist1 = edit_distance(ref_window, query_window)
            dist2 = edit_distance(ref_window, query_rc)
            
            score = window_size - min(dist1, dist2)
            
            if score > best_score and score >= threshold:
                best_score = score
                best_match = (q_start, q_end, r_start, r_end)
        
        if best_match != null:
            alignments.append(best_match)

    return alignments

function align_sequences(ref, query):
    all_alignments = sliding_window_align(ref, query, W, S1)
    // 后处理：去重、合并、过滤
    merged_alignments = merge_overlapping(all_alignments)
    final_alignments = merge_consecutive(merged_alignments)

    return final_alignments
```

## 算法复杂度分析

### 时间复杂度

设参数如下：

- W：滑动窗口大小
- S1：查询序列上的步长
- S2：参考序列上的步长  
- Q：查询序列长度
- R：参考序列长度

**主要操作的复杂度分析：**

1. **外层循环次数**：⌊(Q - W)/S1⌋ + 1 ≈ O(Q/S1)

2. **内层循环次数**：⌊(R - W)/S2⌋ + 1 ≈ O(R/S2)

3. **编辑距离计算**：每次调用edlib.align的复杂度为O(W²)（最坏情况）

4. **总体时间复杂度**：
   - 滑动窗口匹配：O((Q/S1) × (R/S2) × W²)
   - 后处理（排序、去重、合并）：O(k log k)，其中k是匹配片段数量
   - **整体复杂度**：O((Q×R×W²)/(S1×S2) + k log k)

**特殊情况分析：**

- 当S1 = S2 = 1时（密集搜索）：O(Q×R×W²)
- 当S1 = S2 = W时（无重叠窗口）：O((Q×R×W²)/W²) = O(Q×R)
- 实际应用中通常S1 ≈ W, S2 ≈ 1，复杂度约为O(Q×R×W)

### 空间复杂度

- **窗口存储**：O(W)，存储当前处理的窗口
- **匹配结果**：O(k)，其中k是找到的匹配片段数量，通常k << Q/W
- **临时变量**：O(W)，用于编辑距离计算
- **总体空间复杂度**：O(W + k)

### 参数优化建议

- **窗口大小W**：建议设置为50-200，平衡匹配精度和计算效率
- **步长S1**：建议设置为W/2到W，控制窗口重叠程度
- **步长S2**：建议设置为1到W/4，在精度和速度间平衡
- **实际复杂度**：通过合理设置参数，可将复杂度控制在O(Q×R)到O(Q×R×W)之间

## 使用方法

1. 准备两个DNA序列文件：
   - `ref.txt`：参考序列
   - `query.txt`：查询序列

2. 运行程序：

    ```bash
        python find2.py
    ```

3. 程序将输出：

- 匹配片段的坐标元组：(query_start, query_end, ref_start, ref_end)
- 总匹配得分：用于评估比对质量

## 算法优化方向

1. **并行化**：外层和内层循环可以并行处理，提高计算效率
2. **近似算法**：使用更快的近似编辑距离算法替代精确计算
3. **图算法**：使用DAG图等数据结构优化搜索过程
