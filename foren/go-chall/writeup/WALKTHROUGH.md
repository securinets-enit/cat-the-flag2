#  – The Go Supply Chain Mystery

## The Core Idea

This challenge simulates a **supply chain attack in Go**. In Go, importing a library can execute code automatically. If a library contains malicious hooks, a seemingly harmless project can run malicious operations without the user ever calling anything directly.
I'm not a Go developper but I have some attractions to reading about the language, and currently aiming at developping something in Go. So when i read about how the project can import an external from github, it raised my suspicion.


In this scenario:
0. The given History file shows multiple entries about Go. One legit-looking website the victim visited was mimicing the famous `gobyexample.com`.
Visiting the website would lead to nothing because it's no longer hosted, which leads to a dead end if you don't visit the waybackmachine. where you'll find the downloaded `zip` file.
1. The downloaded project (`awesomeCache`) looks like a fully functional caching proxy.  
2. It imports a library called **`cachingio/fastcache`**, which appears to be a standard caching library.  
3. Hidden in this library is a **malicious hook** that executes automatically when imported.  
4. The “malware” is simulated: it searches for sensitive files, records artifacts, and simulates exfiltration to a controlled IP.  

The challenge is to investigate the system, identify the suspicious library, and uncover the hidden flag.

---

## Attack Vectors and Investigation Paths

Players should focus on the **supply chain and library import vectors**:

- **Primary vector**: the imported library `cachingio/fastcache`.  
  - Look for any code that runs automatically (e.g., `init()` functions).  
  - Examine what files or environment variables the library touches.  

- **Secondary vector**: the downloaded project itself (`awesomeCache`).  
  - Understand what functionality it provides (proxy, caching, metrics).  
  - Notice that all the core features are legitimate — the “malware” is hidden in the dependency, not in the main project.

---

## Rabbit Holes to Avoid

To keep players on track and prevent wasted effort, here are the common distractions:

1. **Backend server simulation**: You do **not** need to investigate the backend proxy server’s responses. It’s just a decoy to make the project seem legitimate.  
2. **Metrics, tracing, and logging**: These are there to make the project feel realistic. You don’t need to reverse-engineer every metric or log.  
3. **Rate limiting and CORS setup**: These are normal features and **not malicious**.  
4. **Dockerfile and containerization files**: No need to run the container; the focus is on the import and the library behavior.  
5. **All standard libraries**: Standard Go libraries like `net/http`, `fmt`, or `os` are safe and part of the project’s normal operation.

---

## Investigation Tips

- Focus on **what happens automatically when the project runs**.  
- Identify **which library or dependency** triggers unexpected behavior.  
- Look for **files, environment variables, or network activity** that appear without explicit user actions.  
- Once you find the suspicious library, everything should be clear.

---

## Learning Outcomes

This challenge demonstrates:

1. **Supply chain attacks in Go**: how a trusted-looking library can execute code automatically.  
2. **Forensics investigation**: identifying suspicious artifacts and tracing their origin.  
3. **Safe exploration**: distinguishing real malicious behavior from decoy features.  

Players will not only retrieve the flag but also gain a strong understanding of **how importing untrusted libraries can compromise systems**, even when the main project appears completely safe.

