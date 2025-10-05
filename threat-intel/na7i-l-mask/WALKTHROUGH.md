
## WALKTHROUGH

So, the last challenge in the threat intel series. This has more questions indeed, but the same concept and idea: Search for reports, blogs, `MITRE` framework and any known technical reference and build the answers around it.
### Description 

Your country was a target of a cyber espionnage compaign lead by a nation-state threat actor from 2007 until 2014. 

No one suspected a thing, until a report was released. Turns out that many high-profile organizations like govermental institutions, dimplomatic entities has been spied on for years. Not only your country but Cuba, Morroco, Spain ;) , Tunisia, Brasil totalling 31 countries. After that report many people claimed that Spain as behind the compaign, which, of course, was denied by both the researchers who did the report, and the accused country. 


Now, it's been 10 years since the incident, and life's good.


Yes but why are you considered? 


Because after 10 years of "inactivity", a new report has been released. And now, your day at work is, once again, full of action. 


Buckle up, do your research, you're asked to do a whole report on this cyber espionnage compaign, threat actor, and how the fuck did he came back after 10 years, and what is its new mask. We need to know his stuff, what were their techniques, targets and what tools they used.


The challenge isn't hard, if you look at the right places.


Remember: the name of the challenge is a hint. Don't overcomplicate things.


**Author:** 7ankalis

### Walkthrough

So, the questions I mdae literally lead the players to search for the [Kaspersky Lab report](https://media.kasperskycontenthub.com/wp-content/uploads/sites/43/2018/03/20133638/unveilingthemask_v1.0.pdf). Searching within the report the player is easily solving the challenge and gaining the 500 points. 



```Go
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
```


















