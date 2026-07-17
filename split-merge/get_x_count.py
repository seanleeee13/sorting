import sys
import math

def solve(n, a):
    max_pos = [0] * (n + 1)
    min_pos = [math.inf] * (n + 1)
    for i, val in enumerate(a, start=1):
        if max_pos[val] < i:
            max_pos[val] = i
        if min_pos[val] > i:
            min_pos[val] = i
    ans = 0
    pre = 0
    for i in range(1, n + 1):
        if max_pos[i] == 0:
            continue
        if pre != 0 and min_pos[i] < max_pos[pre]:
            ans += 1
        pre = i
    return ans

if __name__ == "__main__":
    n = int(sys.stdin.readline())
    a = [0] + list(map(int, sys.stdin.readline().split()))
    ans = solve(n, a)
    print(ans)