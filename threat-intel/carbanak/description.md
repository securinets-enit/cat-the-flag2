## Carbanak 

### Description 

You are a cybersecurity analyst at a major Insurance and Banking firm. Recently, your blue team intercepted and detected a what could've been a disaster: suspicious actions around ATMs, some phishing and spear-phishing attempts were detected and well isolated.

After sharing informations with other Threat Intelligence teams, turns out that these techniques were used by a threat actor group known as Carbanak. This group was decalared as neutralized. 

Your job is to investiagate this group and map its weapons. 

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** 7ankalis


### Solution 

The first question could be answered quickly from `MITRE` framework, arriving at the second one, the player is asked about the first ever report by Kaspersky Lab. Seeing this, the players should directly consider the first report as their first source. One might think that maybe a first report could be unsure or not very accurate or whatsoever. Me personally, I consider it a good instinct to cross reference, but I don't think it's possible for a research team that big to post inaccurate technical report. 

Going through the report, the players shouldn't have any trouble finding the necessary stuff. Going through CHatGPT will indeed prove wrong, as usual. 


### Questions & Answers 


```Go 
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
```
