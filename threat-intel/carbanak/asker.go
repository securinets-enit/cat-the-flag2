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
		{"What other name is the Carbanak campaign known by?", "ANUNAK"},
		{"In what year was the Carbanak campaign first publicly reported by Kaspersky Lab?", "2015"},
		{"Which industry was primarily targeted by Carbanak?", "Banking"},
		{"What is the MITRE ATT&CK ID assigned to Carbanak?", "G0008"},
		{"Carbanak named their malware svchost.exe to match a legitimate service name. What is the ID of this technique?", "T1036.005"},
		{"What was the main initial access vector used by Carbanak? (Technique ID)", "T1566.001"},
		{"Carbanak used mutiple CVEs in their attacks. Which Microsoft Word CVE was exploited? (format: CVE-YYYY-NNNN)", "CVE-2014-1761"},
		{"Upon sucessful exploitation, the shellcode decrypts and executes the backdoor. What is the backdoor's name?", "Carbanak"},
		{"For remote interactive C2 communications with the target/victim, Carbanak used legitimate tools like TeamViewer. What is this technique's ID?", "T1219"},
		{"In order to render the malware less suspicious, some of Carbanak's tools were signed. What is the MD5 hash of their PAExec-6980-PB-FS-01.ex_", "86A5C466947A6A84554843D852478248"},
		{"What Sysinternals tool did Carbanak use to execute commands remotely across hosts?", "PsExec"},
		{"Carbanak installs VNC server software that executes through rundll32. For this SAME TECHNIQUE, Lazarus group abused another legit Windows executable. What is its name? Example: tool.exe", "wuauclt.exe"},
		{"Carbanak operators recorded victims’ screens to study banking workflows. What MITRE TACTIC NAME does this fall under? Tactic NOT technique!", "Collection"},
		{"Which protocol did Carbanak often use for C2 communication, disguising it as normal traffic?", "HTTP"},
		{"Which tool was used to dump credentials from memory?", "Mimikatz"},
		{"Kaspersky provided an open file to test for Carbanak's presence in your network. What is the extension of this file? Examples: .pdf, .txt..etc", ".ioc"},
		{"In its communication with the C2 servers, Carbanak uses different commands. One of which changes the C2 server. What is this command. Examples: change, change_sv..etc", "server"},
		{"According to reporting, approximately how many billion dollars did Carbanak steal worldwide? (in USD) Just submit a number", "1"},
		{"In which year did Europol announce the arrest of a key Carbanak leader?", "2018"},
	}

	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Hello future Threat Hunter. This isn't a hard challenge, if you look at the right places.")
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
	fmt.Println("Aya haw l flag")

	// --- Print the flag.txt content ---
	flagContent, err := os.ReadFile("flag.txt")
	if err != nil {
		fmt.Println("Error reading flag.txt:", err)
		return
	}
	fmt.Println("\nHere is your flag:")
	fmt.Println(string(flagContent))
}
