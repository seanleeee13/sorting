#include <iostream>
#include <vector>

constexpr int INF = 1e9;

int solve(int n, std::vector<int>& a) {
    std::vector<int> max_pos(n + 1, 0);
    std::vector<int> min_pos(n + 1, INF);
    int val;
    for (int i = 1; i <= n; i++) {
        int val = a[i];
        if (max_pos[val] < i) {
            max_pos[val] = i;
        }
        if (min_pos[val] > i) {
            min_pos[val] = i;
        }
    }
    int pre = 0;
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        if (max_pos[i] == 0) {
            continue;
        }
        if (pre != 0 && min_pos[i] < max_pos[pre]) {
            ans++;
        }
        pre = i;
    }
    return ans;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int n;
    std::cin >> n;
    std::vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) {
        std::cin >> a[i];
    }
    int ans = solve(n, a);
    std::cout << ans << "\n";
}