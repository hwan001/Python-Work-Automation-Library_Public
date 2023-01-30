"""
6 5
1 1 0 1 1
0 1 1 0 0
0 0 0 0 0
1 0 1 1 1
0 0 1 1 1
0 1 1 1 1
"""
from collections import deque
import sys

n, m = map(int, sys.stdin.readline().split())
arr = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]


for i in range(0, n):
    for j in range(0, m):
        print(arr[i][j])
    print("")

a = deque()
print(a)


