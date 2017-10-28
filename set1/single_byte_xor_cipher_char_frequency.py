hex = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
frequent_letters = "etaoi "
candidate = ""
candidate_frequency = 0

for plaintext in [''.join([chr(x ^ ord(a)) for a in hex.decode("hex")]) for x in range(128)]:
    frequency = sum([plaintext.count(frequent_letters[n]) for n in range(len(frequent_letters))])

    if frequency > candidate_frequency:
        candidate = plaintext
        candidate_frequency = frequency

print candidate
