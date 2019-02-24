package main

import (
	"encoding/binary"
	"fmt"
	"math/rand"
	//"io/ioutil"
	"./sha_1"
	//"strings"
	"time"
)

func get_padding(msg []byte) []byte {
	length := uint64(len(msg))

	// Padding.  Add a 1 bit and 0 bits until 56 bytes mod 64.
	var tmp [64]byte
	tmp[0] = 0x80
	//if length % 64 < 56 {
	//	return tmp[0 : 56-length%64]
	//	length = 56-length%64
	//} else {
	//	return tmp[0 : 64+56-length%64]
	//	length = 64+56-length%64
	//}

	length <<= 3
	sha_1.PutUint64(tmp[:], length)
	return tmp[:]
	//d.Write(tmp[0:8])
}

func main() {
	rand.Seed(time.Now().UTC().UnixNano())
	//file, _ := ioutil.ReadFile("/usr/share/dict/cracklib-small")
	//lines := strings.Split(string(file), "\n")
	key := "a"//lines[rand.Intn(len(lines))]
	msg := "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"

	secret_prefix_hash := sha_1.Sum([]byte(key + msg))

	var registers [5]uint32

	for i := 0; i < 5; i++ {
		registers[i] = binary.BigEndian.Uint32(secret_prefix_hash[i * 4 : (i * 4) + 4])
	}

	injected := ";admin=true"
	pad := get_padding([]byte(key + msg))
	forged := append(pad, []byte(injected)...)[1:]
	//forged := []byte(injected)
	forged_digest := sha_1.SumForged(forged, registers)

	//fmt.Printf("%x\n", sha_1.SumForged(forged, registers))
	fmt.Printf("%x\n", sha_1.Sum([]byte(key + msg + string(pad) + injected)))
	fmt.Printf("%x\n", sha_1.Sum(append(forged, forged_digest[:]...)))
	fmt.Printf("%x\n", sha_1.Sum(append(forged_digest[:], forged...)))
	fmt.Printf("%x\n", sha_1.Sum(append([]byte(key), forged...)))
	fmt.Printf("%x\n", secret_prefix_hash)
	fmt.Printf("%x\n", sha_1.Sum([]byte(msg + key)))
}
