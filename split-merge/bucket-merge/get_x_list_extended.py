import sys
import math

def solve(n, a):
    mx = -math.inf
    mn = math.inf
    for val in a:
        if val < mn:
            mn = val
        if val > mx:
            mx = val
    length = mx - mn + 1
    max_pos = [-math.inf] * length
    min_pos = [math.inf] * length
    for i in range(n):
        offset_val = a[i] - mn
        if max_pos[offset_val] < i + 1:
            max_pos[offset_val] = i + 1
        if min_pos[offset_val] > i + 1:
            min_pos[offset_val] = i + 1
    ans = []
    pre = -1
    for i in range(length):
        if min_pos[i] == math.inf:
            continue
        if pre != -1 and min_pos[i] < max_pos[pre]:
            ans.append(pre + mn)
        pre = i
    return ans

if __name__ == "__main__":
    n = int(input())
    a = list(map(int, sys.stdin.readline().split()))
    ans = solve(n, a)
    print(*ans)