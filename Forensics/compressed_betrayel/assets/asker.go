package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

// question represents a single question in the quiz.
type question struct {
	text   string
	answer string
}

func main() {
	questions := []question{
		{"What is the link of the malicious downloaded tool?", "https://github.com/goerge-billard/"},
		{"What is the link to the main developer's github?", "https://github.com/goerge-billard"},
		{"How many arguments does the tool expect?", "2"},
		{"What is the suspicious function that's being called in the main function? Notice that it gets called by providing any argument.", "optimize_compression()"},
		{"How many arguments does `optimize_compression()` take?", "0"},
		{"If the user provides something other than `compress`, `decompress` or `optimize`, what does the program print to screen?", "Unknown command"},
		{"Another function gets called. What is it?", "optimize_compression()"},
		{"In which file is the `optimize_compression` function defined?", "optimize.cpp"},
		{"When optimize_compression is invoked, how many functions get executed?", "4"},
		{"Which one is the malicious one?", "optimize_session()"},
		{"What is the IP address of the threat actor?", "20.74.81.63"},
		{"What is the requested file name?", "test.sh"},
		{"From what port is this file requested?", "2982"},
		{"What protocol is used for the transfer?", "http"},
		{"What is the SimpleHTTP version of the malicious actor's server?", "0.6"},
		{"Reconstruct the test.sh file. What IP address does the script call?", "20.74.81.63"},
		{"What port?", "23765"},
		{"What files are being requested? format file1,file2.", "cleaup.sh, compress.c"},
		{"What is the absolute path of the directory where the script saves the payloads?", ""},
		{"What legit system service is the threat actor trying to mimic?", "systemd"},
		{"Check the c source code. How many imports are there?", "5"},
		{"Is compress.c alone able to be compiled?", ""},
		{"Another file is downloaded and manipulated. What is the IP address where this file gets downloaded from?", "20.74.81.63"},
		{"What port?", "55612"},
		{"What is the file name?", "decompress.c"},
		{"To obtain a full rev shell written in c, what is the full command that the script runs to obtain the complete file?", "cat decompress.c >> compress.c"},
		{"What is the resulting binary name?", "systemdihh"},
		{"The resulting binary is calling a rev shell on a specific ip. What is it?", "20.74.81.63"},
		{"On what port?", "9476"},
	}

	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Hello future Threat Hunter. This is a long challenge but not a hard one. Understand the chain, get your flag!")
	fmt.Println("You have 3 attempts for each question.")
	fmt.Println("-----------------------------------------------------")

	for i, q := range questions {
		incorrectAttempts := 0
		for {
			fmt.Printf("\nQuestion %d/%d: %s\n", i+1, len(questions), q.text)
			fmt.Print("Your Answer: ")
			input, _ := reader.ReadString('\n')
			input = strings.TrimSpace(input)

			if strings.EqualFold(input, q.answer) {
				fmt.Println("Correct! ✅")
				break // Move to the next question
			} else {
				incorrectAttempts++
				if incorrectAttempts >= 3 {
					fmt.Println("Incorrect. ❌ You have exceeded the maximum number of attempts for this question. The quiz is over.")
					return // End the program
				}
				fmt.Printf("Incorrect. ❌ You have %d attempts remaining for this question.\n", 3-incorrectAttempts)
			}
		}
	}

	fmt.Println("\nOMG MALLA MONGALA")
	fmt.Println("Aw l flag")

	// --- Print the flag.txt content ---
	flagContent, err := os.ReadFile("flag.txt")
	if err != nil {
		fmt.Println("Error reading flag.txt:", err)
		return
	}
	fmt.Println("\nHere is your flag:")
	fmt.Println(string(flagContent))
}

