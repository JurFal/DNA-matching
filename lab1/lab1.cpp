#include<bits/stdc++.h>
using namespace std;

int dp[2005][2005];
int previous_chain[2005][2005];

char match(char xx) {
    switch(xx) {
        case 'A': return 'T';
        case 'T': return 'A';
        case 'C': return 'G';
        case 'G': return 'C';
        default: return 0;
    }
    return 0;
}

int solve(string reference_str, string query_str) {
    int ref_len = reference_str.size();
    int query_len = query_str.size();
    int reward = 1;
    int penalty = -5;
    for(int i = 1; i < ref_len; i++) {
        int last_highest = 0, last_highest_index = -1;
        for(int j = 1; j < query_len; j++) {
            int score1 = 0, score2 = 0, score3 = 0, score_final;
            int mode = 0;
            int previous1, previous2, previous3;
            if(reference_str[i] == query_str[j]) {
                if(reference_str[i - 1] == query_str[j - 1]) {
                    score1 = dp[i - 1][j - 1] + reward;
                    previous1 = j - 1;
                }
                else {
                    score1 = 0;
                    previous1 = -1;
                }
                score2 = last_highest + reward + penalty;
                previous2 = last_highest_index;
                score3 = reward;
                previous3 = -1;
                
                score_final = max(score1, max(score2, score3));
                dp[i][j] = score_final;
                if(score_final == score1) {
                    previous_chain[i][j] = previous1;
                    mode = 1;
                }
                else if(score_final == score2) {
                    previous_chain[i][j] = previous2;
                    mode = 2;
                }
                else {
                    previous_chain[i][j] = previous3;
                    mode = 3;
                }
                if(dp[i][j] > last_highest) {
                    last_highest = dp[i][j];
                    last_highest_index = j;
                }
            }
            else if(reference_str[i] == match(query_str[j])) {
                if(reference_str[i - 1] == match(query_str[j + 1])) {
                    score1 = dp[i - 1][j + 1] + reward;
                    previous1 = j + 1;
                }
                else {
                    score1 = INT_MIN;
                    previous1 = -1;
                }
                score2 = last_highest + reward + penalty;
                previous2 = last_highest_index;
                score3 = reward;
                previous3 = -1;
                
                score_final = max(score1, max(score2, score3));
                dp[i][j] = score_final;
                if(score_final == score1) {
                    previous_chain[i][j] = previous1;
                }
                else if(score_final == score2) {
                    previous_chain[i][j] = previous2;
                }
                else {
                    previous_chain[i][j] = previous3;
                }
                if(dp[i][j] > last_highest) {
                    last_highest = dp[i][j];
                    last_highest_index = j;
                }
            }
            else {
                dp[i][j] = dp[i - 1][j];
                previous_chain[i][j] = previous_chain[i - 1][j];
            }
            printf("i:%d j:%d mode:%d %d %d\n", i, j, mode, dp[i][j], previous_chain[i][j]);
        }
    }
    int for_prev = query_len - 1;
    while(previous_chain[ref_len - 1][for_prev] != -1) {
        printf("%d: %c\n", for_prev, query_str[for_prev]);
        for_prev = previous_chain[ref_len - 1][for_prev];

    }
}

int main() {
    string reference_str = "CTGCAACGTTCGTGGTTCATGTTTGAGCGATAGGCCGAAACTAACCGTGCATGCAACGTTAGTGGATCATTGTGGAACTATAGACTCAAACTAAGCGAGCTTGCAACGTTAGTGGACCCTTTTTGAGCTATAGACGAAAACGGACCGAGGCTGCAAGGTTAGTGGATCATTTTTCAGTTTTAGACACAAACAAACCGAGCCATCAACGTTAGTCGATCATTTTTGTGCTATTGACCATATCTCAGCGAGCCTGCAACGTGAGTGGATCATTCTTGAGCTCTGGACCAAATCTAACCGTGCCAGCAACGCTAGTGGATAATTTTGTTGCTATAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTTACCATCGGACCTCCACGAATCTGAAAAGTTTTAATTTCCGAGCGATACTTACGACCGGACCTCCACGAATCAGAAAGGGTTCACTATCCGCTCGATACATACGATCGGACCTCCACGACTCTGTAAGGTTTCAAAATCCGCACGATAGTTACGACCGTACCTCTACGAATCTATAAGGTTTCAATTTCCGCTGGATCCTTACGATCGGACCTCCTCGAATCTGCAAGGTTTCAATATCCGCTCAATGGTTACGGACGGACCTCCACGCATCTTAAAGGTTAAAATAGGCGCTCGGTACTTACGATCGGACCTCTCCGAATCTCAAAGGTTTCAATATCCGCTTGATACTTACGATCGCAACACCACGGATCTGAAAGGTTTCAATATCCACTCTATA";
    string query_str = "CTGCAACGTTCGTGGTTCATGTTTGAGCGATAGGCCGAAACTAACCGTGCATGCAACGTTAGTGGATCATTGTGGAACTATAGACTCAAACTAAGCGAGCTTGCAACGTTAGTGGACCCTTTTTGAGCTATAGACGAAAACGGACCGAGGCTGCAAGGTTAGTGGATCATTTTTCAGTTTTAGACACAAACAAACCGAGCCATCAACGTTAGTCGATCATTTTTGTGCTATTGACCATATCTCAGCGAGCCTGCAACGTGAGTGGATCATTCTTGAGCTCTGGACCAAATCTAACCGTGCCAGCAACGCTAGTGGATAATTTTGTTGCTATAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCCTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCTAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCTAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCTAGACCAACACTAATCGAGACTGCCTCGTTAGTGCATCATTTTTGCGCCATAGACCATAGCTAAGCGAGCGCTCGCTTAGCTATGGTCTATGGCGCAAAAATGATGCACTAACGAGGCAGTCTCGATTAGTGTTGGTCTATAGCAACAAAATTATCCACTAGCGTTGCTGGCTCGCTTAGCTATGGTCTATGGCGCAAAAATGATGCACTAACGAGGCAGTCTCGATTAGTGTTGGTCTATAGCAACAAAATTATCCACTAGCGTTGCTGCTTACCATCGGACCTCCACGAATCTGAAAAGTTTTAATTTCCGAGCGATACTTACGACCGGACCTCCACGAATCAGAAAGGGTTCACTATCCGCTCGATACATACGATCGGACCTCCACGACTCTGTAAGGTTTCAAAATCCGCACGATAGTTACGACCGTACCTCTACGAATCTATAAGGTTTCAATTTCCGCTGGATCCTTACGATCGGACCTCCTCGAATCTGCAAGGTTTCAATATCCGCTCAATGGTTACGGACGGACCTCCACGCATCTTAAAGGTTAAAATAGGCGCTCGGTACTTACGATCGGACCTCTCCGAATCTCAAAGGTTTCAATATCCGCTTGATACTTACGATCGCAACACCACGGATCTGAAAGGTTTCAATATCCACTCTATA";
    string reference_str1 = "refer";
    string query_str1 = "refeer";
    solve(reference_str1, query_str1);
    return 0;
}