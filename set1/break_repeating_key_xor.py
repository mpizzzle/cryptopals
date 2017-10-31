frequent_letters = "etaoi ETAOI"

def distance(str1, str2):
    return ''.join([bin(ord(a) ^ ord(b)) for a, b in zip(str1, str2)]).count('1')

def get_candidate_key_length(file, accuracy):
    candidate_distance = 9999999
    candidate_length = 0

    for key_length in range(2, 40):
        this_distance = sum([distance(file[key_length * x:key_length * (x + 1)], file[key_length * (x + 1):key_length * (x + 2)]) for x in range(accuracy)])
        average_distance = this_distance / float(key_length * (accuracy))

        if average_distance < candidate_distance:
            candidate_distance = average_distance
            candidate_length = key_length

    return candidate_length

def get_candidate_key_byte(transposed_block):
    candidate = ''
    candidate_frequency = 0

    for c in range(256):
        plaintext = ''.join([chr(c ^ ord(a)) for a in transposed_block])
        frequency = sum([plaintext.count(frequent_letters[n]) for n in range(len(frequent_letters))])

        if frequency > candidate_frequency:
            candidate = chr(c)
            candidate_frequency = frequency

    return candidate

def decrypt(key, msg):
    return ''.join([chr(ord(key[i % len(key)]) ^ ord(char)) for i, char in enumerate(msg)])

def get_key(file):
    key_length = get_candidate_key_length(file, 10)
    split_file = [file[i:i + key_length] for i in range(0, len(file), key_length)]
    transposed_blocks = [''.join([block[x] for block in split_file[:len(split_file) - 1]]) for x in range(key_length)]
    return ''.join([get_candidate_key_byte(block) for block in transposed_blocks])

with open('files/6.txt') as f:
    file = f.read().decode("base64")

with open('files/p059_cipher.txt') as f2:
    project_euler_59 = ''.join([chr(int(c)) for c in f2.read().split(',')])

key1 = get_key(file)
key2 = get_key(project_euler_59)

print "key: \"" + key1 + "\"\n" + decrypt(key1, file)
print "key: \"" + key2 + "\"\n" + decrypt(key2, project_euler_59)
