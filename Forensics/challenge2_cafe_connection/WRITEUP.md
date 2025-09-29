# Challenge 2: The Café Connection — Writeup

## Summary
- The provided `cafe_connection.zip` is unlocked with the password from the pastebin: `P4cK3t_N1nj4`.
- Inside is `cafe_connection.pcap` with realistic café Wi‑Fi traffic (ARP, DNS, HTTP).
- The flag is encoded across HTTP response headers as the `Content-Length` values in chronological order from the server `172.16.10.20:80` to the client.

## Steps
1. Unzip
```bash
unzip -P P4cK3t_N1nj4 cafe_connection.zip
```
2. Open the capture in Wireshark and filter on server responses:
```wireshark
ip.src==172.16.10.20 && tcp.port==80 && http
```
3. For each HTTP/1.1 200 OK response, read the `Content-Length` header.
4. Convert each `Content-Length` integer to ASCII using its decimal value → character.
5. Concatenate in order of time to recover the message.

### Quick extraction via tshark (organizer reference)
```bash
tshark -r cafe_connection.pcap -Y "ip.src==172.16.10.20 && tcp.port==80 && http && http.content_length" -T fields -e http.content_length \
| awk '{printf("%s", sprintf("%c", $1))} END {print ""}'
```
OR
# Extract content lengths
```bash
tshark -r cafe_connection.pcap -Y "http.response.code == 200" -T fields -e http.content_length
```
and then
# Convert to characters
```
tshark -r cafe_connection.pcap -Y "http.response.code == 200" -T fields -e http.content_length | grep -v "^$" | while read line; do printf "\\$(printf "%03o" $line)"; done
```
Output:
```
SecurinetsENIT{4r3_Y0u_R34LLY_4_N1Nj4??}
```