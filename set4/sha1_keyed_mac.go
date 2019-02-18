package main

import (
	"bufio"
	"fmt"
        "os"
	"./sha_1"
)

func main() {
	if len(os.Args) > 2 {
		key := []byte(os.Args[1])
		msg := []byte(os.Args[2])
		fmt.Printf("%x\n", sha_1.Sum(append(key, msg...)))
	} else if len(os.Args) == 2 {
		msg := []byte(os.Args[1])
		fmt.Printf("%x\n", sha_1.Sum(msg))
		//af 06 49 23 bb f2 30 15 96 aa c4 c2 73 ba 32 17 8e bc 4a 96
	} else {
		msg, _ := bufio.NewReader(os.Stdin).ReadString('\n')
		m := []byte(msg[:len(msg) - 1])
		fmt.Printf("%x\n", sha_1.Sum(m))
	}
}
