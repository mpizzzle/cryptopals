package main

import (
	"encoding/binary"
	"fmt"
	"math/rand"
	"io/ioutil"
	"./sha_1"
	"strings"
	"time"
)

func padding(msg []byte) []byte {
	length := len(msg)

	// Padding.  Add a 1 bit and 0 bits until 56 bytes mod 64.
	var tmp [64]byte
	tmp[0] = 0x80
	if length % 64 < 56 {
		return tmp[0 : 56-length%64]
	} else {
		return tmp[0 : 64+56-length%64]
	}
}

func main() {
	rand.Seed(time.Now().UTC().UnixNano())
	file, _ := ioutil.ReadFile("/usr/share/dict/cracklib-small")
	lines := strings.Split(string(file), "\n")
	key := lines[rand.Intn(len(lines))]
	msg := "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"

	hash := sha_1.Sum([]byte(key + msg))

	var registers [5]uint32

	for i := 0; i < 5; i++ {
		registers[i] = binary.BigEndian.Uint32(hash[i * 4 : (i * 4) + 4])
	}

	injected := ";admin=true"
	forged := append(append(hash[:], []byte(injected)...), padding([]byte(msg + key))...)

	fmt.Printf("%x\n", sha_1.SumForged(forged, registers))
	fmt.Printf("%x\n", sha_1.Sum([]byte(key + msg + injected)))
}
