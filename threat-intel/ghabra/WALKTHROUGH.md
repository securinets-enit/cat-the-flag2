
## WALKTHROUGH

Although I'm not a blue teamer or trying to land a blue teaming job, but I enjoy reading and consuming blue teaming content as it highly benefits my red teaming thinking process and my overall skills in networking.

I've noticed that blue teaming is considered to be digital forensics in CTFs, so I decided to introduce this field in our CTF.

For this challenge, It is an easy one, nothing very technical to analyse or to extract, you just need to dig and find the right resources.

In most of the challenges, you just need the right report/blog. I tried my best to find stories that have missmatching references so the players don't get confused.

### Description

Date: July 19, 2024.


CrowdStrike has just pushed its infamous faulty update, crippling critical infrastructure worldwide; airports grounded, hospitals offline, BSODs everywhere.

Tunisia, however, seems “miraculously” untouched: can't affoard the crowdstrike solutions, nor the windows license..


You arrive at your corporate job expecting a normal day, but your phone rings:


HQ: “We’ve just seen a new Mandiant report: Something tied to APT41 and exploiting this chaos. You’re the analyst on duty. You don’t leave until we know whether our organization is compromised. Grab coffee: it’s going to be a long night.”


Your task: investigate artifacts provided by HQ, extract IOCs, map techniques to MITRE ATT&CK, and confirm whether APT41 is inside your network. This isn't a normal day as you expected.


**Author:** 7ankalis

### Solution

So it starts really slow, I've give you the exact date, the service provided `crowdstrike`, the worldwide crisis it created, the APT reference `APT41` and to finish things off, the `MITRE ATT&CK` framework. 
The player isn't given any attachements so it is obvious that everything is given in the description. 

### Solution

Upon searching a bit in the web about what an `APT (advanced persistent threat)` is, players should know by now that they're a -let's say- a group of sophisticated hackers with new and advanced techniques. 
Searching for the `MITRE ATT&CK` framework leads directly to answer all the questions.

Most players didn't find a difficulty or opened tickets in this challenge, but here is an interesting one: 

Question: {"DUSTPAN was disguised as a legitimate binary named conn.exe. what is the technique used ? format T****.***", "T1036.004"},

The answer was "T1036.004" but the player said it was `T1036.005`, which was understandable because here is what both techniques are: 

- `T1036.005`: DUSTPAN is often disguised as a legitimate Windows binary such as w3wp.exe or conn.exe.
- `T1036.004`: APT41 has created services to appear as benign system tools.

APT41 DUST disguised DUSTPAN as a legitimate Windows binary such as w3wp.exe or conn.exe.

During C0017, APT41 used SCHTASKS /Change to modify legitimate scheduled tasks to run malicious code.

The difference is that `005` is just referencing the name of the file it created, but `004` is the act of disguising the binary as a completely legit one not just its name but making them look like legit system tools. 

Although I consider this a fault in my end I could've made it more clear to eliminate any mistakes or potential misunderstanding. Although this is an isolated case but could've been better. 

Here are the answers to the questions, everything should be clear in [Here](https://attack.mitre.org/groups/G0096/) or more technical in [Here](https://cloud.google.com/blog/topics/threat-intelligence/apt41-arisen-from-dust) (the report mentionned in the descrption)

#### Answers & Questions 

```Go 
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
```
To Obtain the flag: `SecurinetsENIT{e4068a5dace9f29a0c6cf19406b9360a}`
