import sys

with open('files/4.txt') as f:
    hex_strings = f.read().splitlines()

frequent_letters = "etaoi "
candidate = ""
candidate_frequency = 0

for hex in hex_strings:
    for plaintext in [''.join([chr(x ^ ord(a)) for a in hex.decode("hex")]) for x in range(128)]:
        frequency = 0

        for char in plaintext:
            if char in frequent_letters:
                frequency += 1

        if frequency > candidate_frequency:
            candidate = plaintext
            candidate_frequency = frequency

print candidate
