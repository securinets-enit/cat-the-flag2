# WALKTHROUGH: Oh Intern, My Intern

## Author's note:

Although I won't provide a solver or anything of that sort, most of the challenges I authored aren't about the difficulty of complexity of the tools, but my objective is to leave you with a new technique, tactic, attack vector or whatever.

It's about understanding and building a strong technical thinking method. 

Making a writeup in itself is more tiring then the authoring, so I will simply write down the story for ChatGPT, and he'll tell you all of what I want. I you find any GPT dashes, do not judge. 

Here is the scenario of this challenge:

## Scenario: 

A junior developer set up a personal FTP service to move work files between machines. Because they treated it as a “private convenience” rather than a production service, the server was left wide open: anonymous access was enabled (anonymous_enable=YES) and no TLS was enforced. An opportunistic attacker found the server, logged in as anonymous:anonymous, and downloaded a seemingly innocuous welcome email sent to the new hires. That email contained the list of recipients — effectively a ready-made username wordlist - and suddenly the attacker had valid targets to try instead of blind guessing.

Not long after, the attacker retrieved a second email from the Head of IT (the HeadOfITNotice) that spelled out the company’s password format: nameinitial<2digits>character<year>lastname. With concrete usernames and a tight password template, the attacker could generate high-probability password candidates instead of wasting time on massive, noisy wordlists. Armed with both artifacts, they switched from reconnaissance to action.

Using the harvested credentials and focused guesses, the attacker authenticated as samirloussif. At 18:46:33 the intruder performed the first authenticated downloads for that account and pulled vsftpd.conf, confirming that anonymous FTP was allowed and SSL was not enabled. From there the attacker freely navigated and uploaded tools - five files in total - to prepare later privilege escalation and lateral movement. The adversary also exfiltrated a particularly sensitive file: /var/www/html/critical_app/db/database.sqlite, demonstrating how a small operational mistake can expose production data.

Earlier FTP activity shows the messy reconnaissance: a transfer of users.eml was aborted at 17:06:45 and then successfully completed at 17:10:53, while HeadOfITNotice.eml was fetched multiple times. Those artifacts show how the attacker iterated between discovery and exploitation, repeatedly pulling emails to refine usernames and passwords before escalating to authenticated access and exfiltration.

With foothold established on the intern’s host, the attacker moved to gain a stable shell. The auth.log reveals a large, noisy SSH brute-force campaign beginning at 19:27:18 from an IP originating in Algeria; the campaign culminated in a successful login for samirloussif at 19:35:47. Even after obtaining valid credentials the attacker continued attempting passwords — a tell-tale script-kiddie pattern — but the damage was already done: exposed credentials + poor hardening = compromise.

This walkthrough illustrates a simple chain: information disclosure (emails) → focused credential generation (password policy + usernames) → misuse of misconfigured service (anonymous FTP + no TLS) → authenticated access and data exfiltration → noisy SSH brute force to solidify access. Fixing it requires basic operational discipline: forbid personal services on shared infrastructure, disable anonymous FTP, enforce TLS/SFTP, avoid emailing password policy or reduce the sensitivity of disclosed policy details, require MFA, and monitor/block abnormal auth patterns and large numbers of failed logins.
