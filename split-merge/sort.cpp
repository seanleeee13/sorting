#include <iostream>
#include <vector>

constexpr int INF = 1e9;

std::vector<int> solve(int n, std::vector<int>& a) {
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
    std::vector<int> x_list;
    int pre = -1;
    for (int i = 0; i < length; i++) {
        if (min_pos[i] == INF) {
            continue;
        }
        if (pre != -1 && min_pos[i] < max_pos[pre]) {
            x_list.push_back(pre + mn);
        }
        pre = i;
    }
    std::vector<int> ans = a;
    std::vector<int> b;
    for (int x: x_list) {
        std::vector<int> above;
        for (int val: ans) {
            if (val <= x) {
                b.push_back(val);
            } else {
                above.push_back(val);
            }
        }
        ans = above;
    }
    b.insert(b.end(), ans.begin(), ans.end());
    ans = b;
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
    std::vector<int> ans = solve(n, a);
    for (int val: ans) {
        std::cout << val << " ";
    }
    std::cout << "\n";
}