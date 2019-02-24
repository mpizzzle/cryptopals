hex_strings = open('files/4.txt').read().splitlines()

frequent_letters = "etaoi "
candidate = ""
candidate_frequency = 0

for hex in hex_strings:
    for plaintext in [''.join([chr(x ^ ord(a)) for a in hex.decode("hex")]) for x in range(256)]:
        frequency = sum([plaintext.count(frequent_letters[n]) for n in range(len(frequent_letters))])

        if frequency > candidate_frequency:
            candidate = plaintext
            candidate_frequency = frequency

print candidate
