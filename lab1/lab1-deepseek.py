def reverse_complement(s):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join([complement[c] for c in reversed(s)])

def compute_failure_function(pattern):
    n = len(pattern)
    fail = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and pattern[i] != pattern[j]:
            j = fail[j-1]
        if pattern[i] == pattern[j]:
            j += 1
            fail[i] = j
        else:
            fail[i] = 0
    return fail

def find_min_period(s):
    if not s:
        return 0
    fail = compute_failure_function(s)
    period = len(s) - fail[-1]
    return period if len(s) % period == 0 else len(s)

def find_repeats_optimized(query, reference):
    rc_reference = reverse_complement(reference)
    q_len, r_len = len(query), len(reference)
    repeats = []
    q_start = r_start = 0

    while q_start < q_len and r_start < r_len:
        # 寻找最长公共前缀 (LCP)
        lcp = 0
        while (q_start + lcp < q_len and r_start + lcp < r_len and 
               query[q_start + lcp] == reference[r_start + lcp]):
            lcp += 1

        # 寻找最长公共后缀 (LCS)
        q_end, r_end = q_len - 1, r_len - 1
        lcs = 0
        while (q_end - lcs >= q_start and r_end - lcs >= r_start and 
               query[q_end - lcs] == reference[r_end - lcs]):
            lcs += 1

        # 提取差异区域
        diff_q = query[q_start + lcp : q_end - lcs + 1]
        diff_r = reference[r_start + lcp : r_end - lcs + 1]
        m, l = len(diff_q), len(diff_r)

        if m == 0 or l == 0:
            break

        # 检测周期
        period = find_min_period(diff_q)
        valid_forward, valid_reverse = False, False

        # 正向重复检查
        if l == period and diff_r == diff_q[:period]:
            k = m // period - 1
            if k > 0:
                repeats.append((r_start + lcp, period, k, False))
                valid_forward = True

        # 反向重复检查
        rc_diff_r = reverse_complement(diff_r)
        if l == period and rc_diff_r == diff_q[:period]:
            k = m // period - 1
            if k > 0:
                repeats.append((r_start + lcp, period, k, True))
                valid_reverse = True

        # 移动指针
        if valid_forward or valid_reverse:
            q_start += lcp + m
            r_start += lcp + l
        else:
            # 无重复结构，跳过当前字符
            q_start += lcp + 1
            r_start += lcp + 1

    # 按长度降序、位置升序排序
    repeats.sort(key=lambda x: (-x[1], x[0]))
    return repeats

def __main__():
    reference_str = "CTGCAACGTTCGTGGTTCATGTTTGAGCGATAGGCCGAAACTAACCGTGCATGCAACGTTAGTGGATCATTGTGGAACTATAGACTCAAACTAAGCGAGCTTGCAACGTTAGTGGACCCTTTTTGAGCTATAGACGAAAACGGACCGAGGCTGCAAGGTTAGTGGATCATTTTTCAGTTTTAGACACAAACAAACCGAGCCATCAACGTTAGTCGATCATTTTTGTGCTATTGACCATATCTCAGCGAGCCTGCAACGTGAGTGGATCATTCTTGAGCTCTGGACCAAATCTAACCGTGCCAGCAACGCTAGTGGATAATTTTGTTGCTATAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTTACCATCGGACCTCCACGAATCTGAAAAGTTTTAATTTCCGAGCGATACTTACGACCGGACCTCCACGAATCAGAAAGGGTTCACTATCCGCTCGATACATACGATCGGACCTCCACGACTCTGTAAGGTTTCAAAATCCGCACGATAGTTACGACCGTACCTCTACGAATCTATAAGGTTTCAATTTCCGCTGGATCCTTACGATCGGACCTCCTCGAATCTGCAAGGTTTCAATATCCGCTCAATGGTTACGGACGGACCTCCACGCATCTTAAAGGTTAAAATAGGCGCTCGGTACTTACGATCGGACCTCTCCGAATCTCAAAGGTTTCAATATCCGCTTGATACTTACGATCGCAACACCACGGATCTGAAAGGTTTCAATATCCACTCTATA"
    query_str = "CTGCAACGTTCGTGGTTCATGTTTGAGCGATAGGCCGAAACTAACCGTGCATGCAACGTTAGTGGATCATTGTGGAACTATAGACTCAAACTAAGCGAGCTTGCAACGTTAGTGGACCCTTTTTGAGCTATAGACGAAAACGGACCGAGGCTGCAAGGTTAGTGGATCATTTTTCAGTTTTAGACACAAACAAACCGAGCCATCAACGTTAGTCGATCATTTTTGTGCTATTGACCATATCTCAGCGAGCCTGCAACGTGAGTGGATCATTCTTGAGCTCTGGACCAAATCTAACCGTGCCAGCAACGCTAGTGGATAATTTTGTTGCTATAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCTAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCTAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCTAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCGCTCGCTTAGCTATGGTCTATGGCGCAAAAATGATGCACTAACGAGGCAGTCTCGATTAGTGTTGGTCTATAGCAACAAAATTATCCACTAGCGTTGCTGGCTCGCTTAGCTATGGTCTATGGCGCAAAAATGATGCACTAACGAGGCAGTCTCGATTAGTGTTGGTCTATAGCAACAAAATTATCCACTAGCGTTGCTGCTTACCATCGGACCTCCACGAATCTGAAAAGTTTTAATTTCCGAGCGATACTTACGACCGGACCTCCACGAATCAGAAAGGGTTCACTATCCGCTCGATACATACGATCGGACCTCCACGACTCTGTAAGGTTTCAAAATCCGCACGATAGTTACGACCGTACCTCTACGAATCTATAAGGTTTCAATTTCCGCTGGATCCTTACGATCGGACCTCCTCGAATCTGCAAGGTTTCAATATCCGCTCAATGGTTACGGACGGACCTCCACGCATCTTAAAGGTTAAAATAGGCGCTCGGTACTTACGATCGGACCTCTCCGAATCTCAAAGGTTTCAATATCCGCTTGATACTTACGATCGCAACACCACGGATCTGAAAGGTTTCAATATCCACTCTATA"
    
    print(find_repeats_optimized(query_str, reference_str))
    # print(query_str)
    
    # split_prefix_and_suffix(reference_str, query_str)



if __name__ == "__main__":
    __main__()