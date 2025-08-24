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
			{"which is the reference for this group?", "APT41"},
			{"Researchers claim this is a state-sponsored group. what is their spoken language?", "Chinese"},
			{"As of August, 2025, there are 3 associated groups for this APT. Wicked Panda, BARIUM. What is the third one?", "Brass Typhoon"},
			{"When was the last time this APT has been seen?", "June 2024"},
			{"How many compaigns did this apt peform?", "2"},
			{"What was the name of the compaign the HQ called you about? Format ( APT** <NAME>) example: APT10 SALUT.", "APT41 DUST"},
			{"what is its ID on the MITRE?", "C0040"},
			{"When did it start? format: month year, example 05/1999.", "01/2023"},
			{"In order to execute their malware, they used two known web shells. What is their names? format: NAME1, NAME2.", "ANTSWORD, BLUEBEAM"},
			{"In order to establish a connection between the victim and thei C2 servers, What was the dropper used?", "DUSTPAN"},
			{"In order to get DUSTPAN on the victim's host, they ran certutil.exe to download DUSTPAN? what is the technique used? format: T****", "T1105"},
			{"DUSTPAN was disguised as a legitimate binary named conn.exe. what is the technique used ? format T****.*** answer: 1036.004*", "T1036.004"},
		}

		reader := bufio.NewReader(os.Stdin)

		fmt.Println("Hello future Threat Hunter. This is a relatively easy challenge, no big deal. Collect data, answer the questions, get the flag! Good luck!")
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

		// --- New Part: Print the flag.txt content ---
		flagContent, err := os.ReadFile("flag.txt")
		if err != nil {
			fmt.Println("Error reading flag.txt:", err)
			return
		}
		fmt.Println("\nHere is your flag:")
		fmt.Println(string(flagContent))
	}
