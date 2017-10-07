import sys

def hamming_distance(str1, str2):
	return ''.join([bin(ord(a) ^ ord(b)) for a, b in zip(str1, str2)]).count('1')

print hamming_distance("this is a test", "wokka wokka!!!")