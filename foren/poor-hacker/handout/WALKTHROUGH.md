# Poor Hacker

The challenge is about doing some enumeration of the disk image. It is not a big-sized one so it's not about the quantity but about the methodology.

The goal is to enumerate through hidden directory to find a python sciprt that interacts with `google.com` which is resolved to a custom instance of the hacker where he has the rest of his tools in there. The goal is to check the /etc/hosts (relative to the disk image) and see where it is being resolved.

Upon replicating the interaction the hacker did, the server sends back a custom request header. which is the answer to the last question.


