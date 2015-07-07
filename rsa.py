#!/usr/bin/python

import sys

# Generate RSA pk/sk-pair
def rsa_keygen(rsa_P = 1500450271, rsa_Q = 3267000013, rsa_exponent = 65537):

    # Basic RSA initialization
    rsa_N = rsa_P * rsa_Q
    rsa_phi_of_n = (rsa_P-1) * (rsa_Q-1)

    # RSA Exponent e must be 1 < e < rsa_phi_of_n and coprime to rsa_phi_of_n (not yet implemented)
    if rsa_exponent > rsa_phi_of_n or rsa_exponent < 1:
        print("Invalid RSA Exponent")
        return

    # Computation buffers. Lists so we can have an arbitrary number of iterations
    exponent_buffer = list()
    phi_buffer = list()
    division_buffer = list()
    remainder_buffer = list()

    # Initialize computation buffers
    remainder = -1
    exponent_buffer.append(rsa_exponent)
    phi_buffer.append(rsa_phi_of_n)

    # Extended Euclidean algorithm to find the multiplicative inverse to rsa_e
    # Forwards
    i = 0
    while remainder != 0:
        division_buffer.append(int(exponent_buffer[i] / phi_buffer[i]))
        remainder_buffer.append(exponent_buffer[i] % phi_buffer[i])

        exponent_buffer.append(phi_buffer[i])
        phi_buffer.append(remainder_buffer[i])
        remainder = exponent_buffer[i] % phi_buffer[i]
        i += 1
    i -= 1

    left = list()
    right = list()
    left.append(0)
    right.append(1)

    # Backwards
    for c in range(1, i):
        left.append(right[c-1])
        right.append(left[c-1] - (division_buffer[c] * right[c-1]))

    # Make rsa_d valid
    while right[len(right)-1] < 0:
        right[len(right)-1] += rsa_phi_of_n

    rsa_d = right[len(right)-1]

    print("pk(%d, %d)\nsk(%d, %d)" % (rsa_N, rsa_exponent, rsa_N, rsa_d))

if __name__ == "__main__":
    rsa_keygen(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
