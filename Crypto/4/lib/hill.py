# -*- coding: utf-8 -*-

import affine

# def mult(A, B):
#     return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
#             [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]
# def mult_mod(A, B, mod):
#     return [[(A[0][0]*B[0][0] + A[0][1]*B[1][0])%mod, (A[0][0]*B[0][1] + A[0][1]*B[1][1])%mod],
#             [(A[1][0]*B[0][0] + A[1][1]*B[1][0])%mod, (A[1][0]*B[0][1] + A[1][1]*B[1][1])%mod]]


# A - матрица 2x2
# P - вектор
def mult_AP_mod(A, P, mod=256):
    return [(A[0][0]*P[0] + A[0][1]*P[1]) % mod, (A[1][0]*P[0] + A[1][1]*P[1]) % mod]

# А - матрица 2x2
def get_inverse_matrix_mod(A, mod=256):
    d = A[0][0]*A[1][1] - A[0][1]*A[1][0]
    inv_d = affine.get_inverse_mod(abs(d), mod)
    return [[(A[1][1]*inv_d) % mod, (-A[0][1]*inv_d) % mod],
            [(-A[1][0]*inv_d) % mod, (A[0][0]*inv_d) % mod]]

def ed(data, A, mod=256):
    res = []
    for i in range(0, len(data), 2):
        x = mult_AP_mod(A, [data[i], data[i+1]], mod)
        res.append(x[0])
        res.append(x[1])
    return res

def dd(data, A, mod=256):
    res = []
    inv_A = get_inverse_matrix_mod(A, mod)
    for i in range(0, len(data), 2):
        x = mult_AP_mod(inv_A, [data[i], data[i+1]], mod)
        res.append(x[0])
        res.append(x[1])
    return res