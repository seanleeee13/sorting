#include <iostream>
#include <vector>
#include <map>

constexpr int INF = 1e9;

std::vector<std::vector<int>> solve(int n, std::vector<int>& a) {
    int mx = -INF;
    int mn = INF;
    for (int val: a) {
        if (val < mn) {
            mn = val;
        }
        if (val > mx) {
            mx = val;
        }
    }
    int length = mx - mn + 1;
    std::vector<int> max_pos(length, -INF);
    std::vector<int> min_pos(length, INF);
    for (int i = 0; i < n; i++) {
        int offset_val = a[i] - mn;
        if (max_pos[offset_val] < i + 1) {
            max_pos[offset_val] = i + 1;
        }
        if (min_pos[offset_val] > i + 1) {
            min_pos[offset_val] = i + 1;
        }
    }
    std::map<int, int> bucket_num;
    int pre = -1;
    int set_num = 0;
    for (int i = 0; i < length; i++) {
        if (min_pos[i] == INF) {
            continue;
        }
        if (pre != -1 && min_pos[i] < max_pos[pre]) {
            set_num++;
        }
        bucket_num[i + mn] = set_num;
        pre = i;
    }
    std::vector<std::vector<int>> ans(set_num + 1);
    for (int val: a) {
        ans[bucket_num[val]].push_back(val);
    }
    return ans;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int n;
    std::cin >> n;
    std::vector<int> a(n);
    for (int i = 0; i < n; i++) {
        std::cin >> a[i];
    }
    std::vector<std::vector<int>> ans = solve(n, a);
    for (int i = 1; i <= ans.size(); i++) {
        std::cout << "Bucket " << i << ": ";
        for (int val: ans[i - 1]) {
            std::cout << val << " ";
        }
        std::cout << "\n";
    }
}