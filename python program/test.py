import numpy as np

A = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]
])

B = np.array([
    [1,1,0],
    [1,0,0],
    [0,1,0]
])

print(np.dot(A, B))
print(np.cross(A, B))
print(A*B)