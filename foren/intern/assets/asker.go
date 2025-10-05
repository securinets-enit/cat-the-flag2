
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
		{"Search a bit about the xferlog file. What protocol does it log exactly?", "FTP"},
		{"The attacker got initial foothold through a poorly configured, poorly secured server. What protocol is it?", "ftp"},
		{"What is the first compromized username thorugh which the attacker got his foothold?", "anonymous"},
		{"What is the access mode?", "a"},
		{"One of the requested files was aborted/cancelled/failed. What is the file's name?", "users.eml"},
		{"At what time did it fail?", "17:06:45"},
		{"When did the successful download occur?", "17:10:53"},
		{"Upon gaining the initial foothold, a file was requested more than once. What is that file's name?", "HeadOfITNotice.eml"},
		{`You should be able to recover the the files in here (use CyberChef and decode from base64):
HeadOfITNotice.eml:
RnJvbTogSGVhZCBvZiBJVCA8aXQtaGVhZEBub3J0aC1iYW5rLmNvbT4NClRvOiBzYW1pcmxvdXNz
aWZAbm9ydGgtYmFuay5jb20NClN1YmplY3Q6IFBhc3N3b3JkIFVwZGF0ZSBSZXF1aXJlZA0KRGF0
ZTogU2F0LCAyMyBBdWcgMjAyNSAxNDowMDowMCArMDEwMA0KTUlNRS1WZXJzaW9uOiAxLjANCkNv
bnRlbnQtVHlwZTogdGV4dC9wbGFpbjsgY2hhcnNldD0iVVRGLTgiDQoNCkhlbGxvIFNhbWlyLA0K
DQpBcyBwYXJ0IG9mIG91ciBzZWN1cml0eSBwcm90b2NvbCwgYWxsIGVtcGxveWVlcyBtdXN0IHVw
ZGF0ZSB0aGVpciBhY2NvdW50IHBhc3N3b3JkcyB0byBjb21wbHkgd2l0aCB0aGUgbmV3IHBvbGlj
eToNCg0KUGFzc3dvcmQgZm9ybWF0OiBuYW1laW5pdGlhbDwyZGlnaXRzPmNoYXJhY3Rlcjx5ZWFy
Pmxhc3RuYW1lICANCg0KUGxlYXNlIHVwZGF0ZSB5b3VyIHBhc3N3b3JkIGltbWVkaWF0ZWx5IGFu
ZCBlbnN1cmUgaXQgZm9sbG93cyB0aGlzIGZvcm1hdC4gRmFpbHVyZSB0byBjb21wbHkgbWF5IHJl
c3VsdCBpbiB0ZW1wb3JhcnkgYWNjb3VudCByZXN0cmljdGlvbnMuDQoNCklmIHlvdSBoYXZlIGFu
eSBxdWVzdGlvbnMgcmVnYXJkaW5nIHRoZSBwb2xpY3kgb3IgbmVlZCBhc3Npc3RhbmNlIHVwZGF0
aW5nIHlvdXIgcGFzc3dvcmQsIHBsZWFzZSBjb250YWN0IHRoZSBJVCBkZXBhcnRtZW50Lg0KDQpU
aGFuayB5b3UgZm9yIHlvdXIgY29vcGVyYXRpb24uDQoNCkJlc3QgcmVnYXJkcywNCkhlYWQgb2Yg
SVQNCk5vcnRoIEJhbmsNCg0K`, ""},
		{`users.eml:
RnJvbTogSFIgRGVwYXJ0bWVudCA8aHJAbm9ydGgtYmFuay5jb20+DQpUbzogQW1pbmEuQmVuQWxp
QG5vcnRoLWJhbmsuY29tLCBLaGFsZWQuU2FpZGlAbm9ydGgtYmFuay5jb20sIExlaWxhLk1haGpv
dWJAbm9ydGgtYmFuay5jb20sDQogICAgSG91c3NlbS5UcmFiZWxzaUBub3J0aC1iYW5rLmNvbSwg
U2FsbWEuSmF6aXJpQG5vcnRoLWJhbmsuY29tLCBZb3Vzc2VmLkJlbkhhc3NpbmVAbm9ydGgtYmFu
ay5jb20sDQogICAgTWFyaWVtLktoYWRocmFvdWlAbm9ydGgtYmFuay5jb20sIEFuaXMuRmFyaGF0
QG5vcnRoLWJhbmsuY29tLCBSYW5pYS5HaGFubm91Y2hpQG5vcnRoLWJhbmsuY29tLA0KICAgIHNh
bWlybG91c3NpZkBub3J0aC1iYW5rLmNvbQ0KU3ViamVjdDogV2VsY29tZSB0byBOb3J0aCBCYW5r
IEludGVybiBQcm9ncmFtDQpEYXRlOiBTYXQsIDIzIEF1ZyAyMDI1IDEyOjAwOjAwICswMTAwDQpN
SU1FLVZlcnNpb246IDEuMA0KQ29udGVudC1UeXBlOiB0ZXh0L3BsYWluOyBjaGFyc2V0PSJVVEYt
OCINCg0KRGVhciBJbnRlcm5zLA0KDQpXZSBhcmUgZXhjaXRlZCB0byB3ZWxjb21lIGFsbCBvdXIg
bmV3IHJlY3J1aXRzIHRvIHRoZSBOb3J0aCBCYW5rIGZhbWlseSEgDQoNCkFzIHBhcnQgb2YgeW91
ciBvbmJvYXJkaW5nLCBwbGVhc2UgcmVtZW1iZXI6DQoNCi0gRG8gTk9UIG9wZW4gYW55IHBvcnRz
IG9yIHNlcnZpY2VzIG9uIGNvbXBhbnkgbWFjaGluZXMgdW5sZXNzIGluc3RydWN0ZWQuDQotIEZv
bGxvdyBhbGwgc2VjdXJpdHkgZ3VpZGVsaW5lcyB5b3Ugd2VyZSBicmllZmVkIG9uLg0KLSBJZiB5
b3UgbmVlZCB0byBleHBvcnQgYW55IGRhdGEgb3IgZG9jdW1lbnRzIG91dHNpZGUgdGhlIGludGVy
bmFsIG5ldHdvcmssIGNvbnRhY3QgeW91ciBzdXBlcnZpc29yIGZpcnN0Lg0KDQpXZSBsb29rIGZv
cndhcmQgdG8geW91ciBjb250cmlidXRpb25zIGFuZCBob3BlIHlvdSBoYXZlIGEgcHJvZHVjdGl2
ZSBhbmQgc2FmZSBpbnRlcm5zaGlwLg0KDQpCZXN0IHJlZ2FyZHMsDQpIUiBEZXBhcnRtZW50DQpO
b3J0aCBCYW5rDQoNCg==`, ""},
		{"For the previously discussed file. What's the email of the sender?", "it-head@north-bank.com"},
		{"What is the email of the recipient?", "samirloussif@north-bank.com"},
		{"A very critical detail about the company's passwords system was leaked. What is it?", "nameinitial<2digits>character<year>lastname"},
		{"I really hope you now know what the attacker has obtained so far :) No answer needed just press enter.", ""},
		{"With too much informations about the users within the company, the attacker got access to more files in the FTP server. What is the compromized account?", "samirloussif"},
		{"At what time did he perform the first download with that account?", "18:46:33"},
		{"A configuration file was first downloaded. What is its name?", "vsftpd.conf"},
		{"You can recover it from here: http://ip:port/", ""},
		{"What is the line that allowed the hacker to get the initial foothold and access the FTP server anonymously?", "anonymous_enable=YES"},
		{"Was SSL enabled?", "no"},
		{"What is the full path of the critical exfiltrated file?:", "/var/www/html/critical_app/db/database.sqlite"},
		{"The attacker dropped some of this tools to the FTP server. How many files were uploaded?", "5"},
		{"Now having A LOT in his hands. The attacker turned to another critical service. What is it?", "SSH"},
		{"When did the brute force attack start? format: HH:MM:SS", "19:27:18"},
		{"What is the hostname of the attacked machine?", "devint-ubu22-001"},
		{"What is the target's username?", "samirloussif"},
		{"From which country the attack is initiated?", "algeria"},
		{"Not only brute-forcing is noisy, the attacker didn't stop the bruteforce attack even after gaining a succesful hit. When did his attack succeeded? format: HH:MM:SS", "19:35:47"},
		{"Should we fire the intern? (yes) no needed answer just press enter.", ""},
	}

	reader := bufio.NewReader(os.Stdin)

	fmt.Println("Hello future Threat Hunter. This is a long forensic quiz. Read carefully and answer each question.")
	fmt.Println("You have 3 attempts for each question.")
	fmt.Println("-----------------------------------------------------")

	for i, q := range questions {
		incorrectAttempts := 0
		for {
			fmt.Printf("\nQuestion %d/%d: %s\n", i+1, len(questions), q.text)
			fmt.Print("Your Answer: ")
			input, _ := reader.ReadString('\n')
			input = strings.TrimSpace(input)

			// Accept empty answer when expected (q.answer == "")
			if q.answer == "" && input == "" {
				fmt.Println("Recorded (no-answer). ✅")
				break
			}

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

	fmt.Println("\nWell done — you've completed the forensic quiz!")

	// --- Print the flag.txt content ---
	flagContent, err := os.ReadFile("flag.txt")
	if err != nil {
		fmt.Println("Error reading flag.txt:", err)
		return
	}
	fmt.Println("\nHere is your flag:")
	fmt.Println(string(flagContent))
}

