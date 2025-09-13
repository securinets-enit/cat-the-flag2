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
		{"Starting slowly, what was the name of the Lab that released the first report and revealed the big campaign? format: <name> Lab", "Kaspersky Lab"},
		{"At what year?", "2014"},
		{"At what month? ", "february"},
		{"What did they call the APT back then?", "Careto"},
		{"At that date, how many countries were infected?", "31"},
		{"At that date, approximately, how many unique victims?", "380"},
		{"What language was this threat actor suspected to be speaking?", "spanish"},
		{"Analyzing the Careto's toolset, they found it exploiting older versions of a company's products to hide its traces. What is the company's name? format: <name> lab", "kaspersky lab"},
		{"The threat actor was attempting to exploit vulnerabilities in Kaspersky Lab products to avoid being detected. To what Tactic does this map to?", "TA0005"},
		{"To which technique exactly does this map to?", "T1211"},
		{"To make it look legitimate and bypass evasion, the malware samples were signed by a fake or Unknown company. What tactic does this map to?", "TA0005"},
		{"To what technique and subtechnique does it map to ? format T****.***", "T1553.002"},
		{"The attack in itself was highly sophisticated. Despite many artifacts, two main packages stood up. The first one was Careto. The second one, deeper in kernel-mode, was called?", "sgh"},
		{"The malware had an encrypted CAB file that contained shlink32.dll and shlink64.dll. Inside resided multiple executable files. What was the extension of these executables? It's not .exe format: .<extension>", ".jpg"},
		{"What was the encryption method of this CAB file?", "RC4"},
		{"What was the compilation time of these executables? Format: DD:MM:YYYY", "14:07:2009"},
		{"The C2 server needed commands. Using one command, the malware can write a file from the CAB archive and run it. What is this command?", "UPLOADEXEC"},
		{"Communication: The Careto implant used double encryption. What was the encryption method to encrypt incoming data from the C2?", "AES"},
		{"What is the encryption method of the AES key?", "RSA"},
		{"Apart from custom exploits, the malware exploited several CVEs. One was demonstrated but not released. What is the CVE id?", "CVE-2012-0773"},
		{"This CVE was the first known exploit to escape a sandbox of a famous Application. What was the software?", "Chrome"},
		{"Using this CVE the team won a famous contest at 2012. What is the contest's name?", "pwn2own"},
		{"To neutralize and contain the threat, Kaspersky Lab stopped infected machines from talking to C2 domains. What is the protection technique name? format: *** ********", "DNS sinkhole"},
		{"Now back to December 2024. Kaspersky Lab once again found traces of The Mask APT in a corporate environment. What was the infected email software?", "MDaemon"},
		{"Attackers used scheduled tasks to spread infection. To what technique does this map to?", "T1053"},
	}

	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Hello future Threat Hunter. This is a Careto / The Mask APT challenge. Collect data, answer the questions, and earn the flag! Good luck!")
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
				break // Move to next question
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

	fmt.Println("\nExcellent work, hunter! 🕵️‍♂️")
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
