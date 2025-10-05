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
		{"What is the compromized host's IP address?", "10.10.10.68"},
		{"The attacker tried to query a legit-looking website. what is it?", "update-office369-microsoft.one"},
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
	fmt.Println("\nImagine I've bought the domain name and created a website in which is has a custom c2 and tooling. I m so tired. Here is the flag:", "SecurinetsENIT{33358610d1330b2244844ab8baf8c2e2}")
	fmt.Println(string(flagContent))
}

