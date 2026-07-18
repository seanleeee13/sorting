#include <iostream>
#include <vector>
#include <unordered_map>

constexpr int INF = 1e9;

std::vector<int> bucket_merge_sort(int n, std::vector<int>& a) {
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
    std::unordered_map<int, int> bucket_num;
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
    std::vector<std::vector<int>> buckets(set_num + 1);
    for (int val: a) {
        buckets[bucket_num[val]].push_back(val);
    }
    std::vector<int> ans(n);
    int idx = 0;
    for (std::vector<int> bucket: buckets) {
        for (int val: bucket) {
            ans[idx++] = val;
        }
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
    std::vector<int> ans = bucket_merge_sort(n, a);
    for (int i = 0; i < n; i++) {
        std::cout << ans[i] << " ";
    }
    std::cout << "\n";
}