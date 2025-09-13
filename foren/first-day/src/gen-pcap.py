import random
import time
from ipaddress import ip_address, IPv4Network

# Scapy is a powerful interactive packet manipulation program.
# We disable the verbose output to keep the console clean during script execution.
from scapy.all import (
    ARP,
    DNS,
    DNSQR,
    DNSRR,
    Ether,
    IP,
    TCP,
    UDP,
    ICMP,
    Raw,
    wrpcap,
)

# This is for simulating a basic TLS handshake.
from scapy.layers.tls.all import (
    TLS,
    TLSClientHello,
    TLSServerHello,
    TLSCertificate,
    TLSServerKeyExchange,
    TLSServerHelloDone,
    TLSClientKeyExchange,
    TLSChangeCipherSpec,
    TLSFinished,
)


class PcapGenerator:
    """
    A class to generate a highly realistic PCAP file for a cybersecurity training scenario.
    It simulates a complex mix of normal corporate network traffic and a multi-stage cyberattack
    originating from a compromised host.
    """

    def __init__(self, pcap_file):
        # --- Network Configuration ---
        self.pcap_file = pcap_file
        self.network = IPv4Network("10.10.10.0/24")
        self.gateway_ip = "10.10.10.254"
        self.compromised_host_ip = "10.10.10.68"
        self.fileserver_ip = "10.10.10.100"
        self.mail_server_ip = "104.47.57.110" # Fictional external mail server
        self.benign_hosts = ["10.10.10.12", "10.10.10.35", "10.10.10.77"]
        self.all_internal_hosts = self.benign_hosts + [self.compromised_host_ip, self.fileserver_ip, self.gateway_ip]
        self.dns_server_ip = "8.8.8.8"

        # MAC addresses for realistic Layer 2 traffic
        self.mac_map = {
            self.gateway_ip: "00:00:5e:00:53:ff", self.compromised_host_ip: "00:0c:29:1c:bf:2b",
            self.fileserver_ip: "00:0c:29:5a:d7:c8", self.benign_hosts[0]: "00:0c:29:a1:b2:c3",
            self.benign_hosts[1]: "00:0c:29:d4:e5:f6", self.benign_hosts[2]: "00:0c:29:11:22:33",
            "ff:ff:ff:ff:ff:ff": "ff:ff:ff:ff:ff:ff"
        }

        # --- Attacker Configuration ---
        self.malicious_domain = "update-office369-microsoft.one"
        self.c2_server_ip = "185.177.53.15"

        # --- Benign Traffic Configuration ---
        self.legit_domains = {
            "www.google.com": "142.250.184.196", "www.microsoft.com": "104.215.148.63",
            "www.github.com": "140.82.121.4", "http.badssl.com": "104.154.89.105", # For HTTP traffic
        }
        self.packets = []
        self.current_time = time.time()
        self.tcp_sessions = {}

    def _get_dest_mac(self, dest_ip):
        return self.mac_map[self.gateway_ip] if ip_address(dest_ip) not in self.network else self.mac_map.get(dest_ip, "ff:ff:ff:ff:ff:ff")

    def _add_packets(self, new_packets):
        if not isinstance(new_packets, list): new_packets = [new_packets]
        for pkt in new_packets:
            self.current_time += random.uniform(0.001, 0.04)
            pkt.time = self.current_time
            if pkt.haslayer(IP) and not pkt.haslayer(Ether):
                src_mac = self.mac_map.get(pkt[IP].src)
                dst_mac = self._get_dest_mac(pkt[IP].dst)
                if src_mac and dst_mac: pkt = Ether(src=src_mac, dst=dst_mac) / pkt
                else: continue
            self.packets.append(pkt)

    def _get_tcp_session(self, src_ip, sport, dst_ip, dport):
        session_key = (src_ip, sport, dst_ip, dport)
        if session_key not in self.tcp_sessions:
            self.tcp_sessions[session_key] = {'seq': random.randint(1000, 50000), 'ack': 0}
        return self.tcp_sessions[session_key]

    def _create_tcp_packet(self, src_ip, sport, dst_ip, dport, flags, payload=None):
        client_session = self._get_tcp_session(src_ip, sport, dst_ip, dport)
        server_session = self._get_tcp_session(dst_ip, dport, src_ip, sport)
        client_session['ack'] = server_session['seq']
        pkt = IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags=flags, seq=client_session['seq'], ack=client_session['ack'])
        if payload: pkt /= payload
        payload_len = len(payload) if payload else 0
        if 'S' in flags or 'F' in flags: client_session['seq'] += 1
        client_session['seq'] += payload_len
        return pkt

    # --- BENIGN TRAFFIC FUNCTIONS ---
    def create_arp_traffic(self):
        print("  [+] Simulating ARP traffic...")
        for ip_to_discover in self.all_internal_hosts:
            requester_ip = random.choice(self.benign_hosts)
            if requester_ip == ip_to_discover: continue
            arp_req = Ether(src=self.mac_map[requester_ip], dst="ff:ff:ff:ff:ff:ff") / ARP(op=1, psrc=requester_ip, pdst=ip_to_discover)
            arp_rep = Ether(src=self.mac_map[ip_to_discover], dst=self.mac_map[requester_ip]) / ARP(op=2, hwsrc=self.mac_map[ip_to_discover], psrc=ip_to_discover, hwdst=self.mac_map[requester_ip], pdst=requester_ip)
            self._add_packets([arp_req, arp_rep])
    
    def create_dns_traffic(self, src_ip, domain, resolved_ip):
        sport = random.randint(1024, 65535)
        dns_query = IP(src=src_ip, dst=self.dns_server_ip) / UDP(sport=sport, dport=53) / DNS(id=random.randint(1, 65535), rd=1, qd=DNSQR(qname=domain))
        dns_response = IP(src=self.dns_server_ip, dst=src_ip) / UDP(sport=53, dport=sport) / DNS(id=dns_query[DNS].id, qr=1, ancount=1, qd=dns_query[DNS].qd, an=DNSRR(rrname=domain, ttl=300, rdata=resolved_ip))
        self._add_packets([dns_query, dns_response])

    def create_benign_ping(self, src_ip, dst_ip):
        print(f"  [+] Simulating benign ICMP: {src_ip} -> {dst_ip}")
        ping_req = IP(src=src_ip, dst=dst_ip) / ICMP()
        ping_rep = IP(src=dst_ip, dst=src_ip) / ICMP(type="echo-reply", id=ping_req[ICMP].id, seq=ping_req[ICMP].seq)
        self._add_packets([ping_req, ping_rep])

    def create_http_session(self, src_ip, domain, server_ip):
        print(f"  [+] Simulating HTTP traffic: {src_ip} -> {domain}")
        sport = random.randint(1024, 65535)
        syn = self._create_tcp_packet(src_ip, sport, server_ip, 80, 'S')
        syn_ack = self._create_tcp_packet(server_ip, 80, src_ip, sport, 'SA')
        ack = self._create_tcp_packet(src_ip, sport, server_ip, 80, 'A')
        self._add_packets([syn, syn_ack, ack])
        
        http_req = self._create_tcp_packet(src_ip, sport, server_ip, 80, 'PA', Raw(load=f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"))
        self._add_packets(http_req)
        http_res = self._create_tcp_packet(server_ip, 80, src_ip, sport, 'PA', Raw(load=f"HTTP/1.1 200 OK\r\nServer: nginx\r\nContent-Length: 12\r\n\r\nHello World!"))
        self._add_packets(http_res)
        
        fin = self._create_tcp_packet(src_ip, sport, server_ip, 80, 'FA')
        self._add_packets(fin)
    
    def create_sftp_session(self, src_ip, dest_ip):
        print(f"  [+] Simulating SFTP/SSH traffic: {src_ip} -> {dest_ip}")
        sport = random.randint(1024, 65535)
        # Simplified TCP session creation for brevity
        packets = [self._create_tcp_packet(src_ip, sport, dest_ip, 22, 'S'),
                   self._create_tcp_packet(dest_ip, 22, src_ip, sport, 'SA'),
                   self._create_tcp_packet(src_ip, sport, dest_ip, 22, 'A'),
                   self._create_tcp_packet(src_ip, sport, dest_ip, 22, 'PA', Raw(load=b'SSH-2.0-OpenSSH_8.2p1\r\n')),
                   self._create_tcp_packet(dest_ip, 22, src_ip, sport, 'PA', Raw(load=b'SSH-2.0-paramiko_2.7.2\r\n'))]
        for _ in range(random.randint(3, 6)):
            packets.append(self._create_tcp_packet(src_ip, sport, dest_ip, 22, 'PA', Raw(load=random.randbytes(random.randint(40, 200)))))
            packets.append(self._create_tcp_packet(dest_ip, 22, src_ip, sport, 'A'))
        self._add_packets(packets)
    
    def create_benign_smb_session(self, src_ip, dest_ip):
        print(f"  [+] Simulating multi-step SMBv2 traffic: {src_ip} -> {dest_ip}")
        sport = random.randint(1024, 65535)
        # Raw payloads for various SMB2 commands
        smb_negotiate_req = b'\xfeSMB@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00$\x00\x02\x00\x01\x00\x00\x00\x02\x02\x10\x02 \x03\x02\x03\x11\x03'
        smb_tree_connect_req = b'\xfeSMB@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\t\x00\x00\x00' + f'\\\\{dest_ip}\\IPC$\x00'.encode()
        # Full TCP and SMB conversation
        packets = [self._create_tcp_packet(src_ip, sport, dest_ip, 445, 'S'),
                   self._create_tcp_packet(dest_ip, 445, src_ip, sport, 'SA'),
                   self._create_tcp_packet(src_ip, sport, dest_ip, 445, 'A'),
                   self._create_tcp_packet(src_ip, sport, dest_ip, 445, 'PA', Raw(load=smb_negotiate_req)),
                   self._create_tcp_packet(dest_ip, 445, src_ip, sport, 'PA', Raw(load=random.randbytes(120))), # Dummy response
                   self._create_tcp_packet(src_ip, sport, dest_ip, 445, 'PA', Raw(load=smb_tree_connect_req)),
                   self._create_tcp_packet(dest_ip, 445, src_ip, sport, 'PA', Raw(load=random.randbytes(80)))] # Dummy response
        self._add_packets(packets)

    def create_nfs_rpc_session(self, src_ip, dest_ip):
        print(f"  [+] Simulating NFS/RPC traffic: {src_ip} -> {dest_ip}")
        # RPC Portmapper query for NFS service
        portmapper_payload = b'\x72\xfe\x1d\x13\x00\x00\x00\x00\x00\x00\x00\x02\x00\x01\x86\xa0\x00\x01\x86\xa3\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00'
        portmapper_req = IP(src=src_ip, dst=dest_ip) / UDP(sport=random.randint(32768, 60999), dport=111) / Raw(load=portmapper_payload)
        self._add_packets(portmapper_req)
        # This is enough to indicate NFS activity for a CTF.

    def create_smtp_session(self, src_ip, dest_ip):
        print(f"  [+] Simulating SMTP traffic: {src_ip} -> {dest_ip}")
        sport = random.randint(1024, 65535)
        packets = [self._create_tcp_packet(src_ip, sport, dest_ip, 25, 'S'),
                   self._create_tcp_packet(dest_ip, 25, src_ip, sport, 'SA'),
                   self._create_tcp_packet(src_ip, sport, dest_ip, 25, 'A'),
                   self._create_tcp_packet(dest_ip, 25, src_ip, sport, 'PA', Raw(load=b'220 mx.google.com ESMTP\r\n')),
                   self._create_tcp_packet(src_ip, sport, dest_ip, 25, 'PA', Raw(load=b'HELO client.local\r\n')),
                   self._create_tcp_packet(dest_ip, 25, src_ip, sport, 'PA', Raw(load=b'250 mx.google.com\r\n')),
                   self._create_tcp_packet(src_ip, sport, dest_ip, 25, 'PA', Raw(load=b'QUIT\r\n')),
                   self._create_tcp_packet(dest_ip, 25, src_ip, sport, 'PA', Raw(load=b'221 2.0.0 Bye\r\n'))]
        self._add_packets(packets)
    
    def create_tls_session(self, src_ip, dst_ip, dport=443):
        print(f"  [+] Simulating HTTPS/TLS Handshake: {src_ip} -> {dst_ip}")
        sport = random.randint(1024, 65535)
        packets = [self._create_tcp_packet(src_ip, sport, dst_ip, dport, 'S'),
                   self._create_tcp_packet(dst_ip, dport, src_ip, sport, 'SA'),
                   self._create_tcp_packet(src_ip, sport, dst_ip, dport, 'A')]
        dummy_verify = b'\xde\xad\xbe\xef' * 3
        packets.extend([
            self._create_tcp_packet(src_ip, sport, dst_ip, dport, 'PA', TLS(msg=[TLSClientHello()])),
            self._create_tcp_packet(dst_ip, dport, src_ip, sport, 'PA', TLS(msg=[TLSServerHello(), TLSCertificate(), TLSServerKeyExchange(), TLSServerHelloDone()])),
            self._create_tcp_packet(src_ip, sport, dst_ip, dport, 'PA', TLS(msg=[TLSClientKeyExchange(), TLSChangeCipherSpec(), TLSFinished(dummy_verify)])),
            self._create_tcp_packet(dst_ip, dport, src_ip, sport, 'PA', TLS(msg=[TLSChangeCipherSpec(), TLSFinished(dummy_verify)]))
        ])
        self._add_packets(packets)

    # --- MALICIOUS TRAFFIC FUNCTIONS ---
    def create_icmp_sweep(self):
        print(f"\n[!] Simulating ICMP Sweep from {self.compromised_host_ip}...")
        for i in range(1, 255):
            if i % 10 != 0: continue
            target_ip = f"10.10.10.{i}"
            if target_ip == self.compromised_host_ip: continue
            ping_req = IP(src=self.compromised_host_ip, dst=target_ip)/ICMP(id=random.randint(1,65535), seq=random.randint(1,65535))
            self._add_packets(ping_req)
            if target_ip in self.all_internal_hosts:
                ping_rep = IP(src=target_ip, dst=self.compromised_host_ip)/ICMP(type="echo-reply", id=ping_req[ICMP].id, seq=ping_req[ICMP].seq)
                self._add_packets(ping_rep)

    def create_smb_sweep(self):
        print(f"\n[!] Simulating SMBv1 Sweep from {self.compromised_host_ip}...")
        for i in range(1, 255):
             if i % 5 != 0: continue
             target_ip = f"10.10.10.{i}"
             if target_ip == self.compromised_host_ip: continue
             sport = random.randint(1024, 65535)
             syn = self._create_tcp_packet(self.compromised_host_ip, sport, target_ip, 445, 'S')
             self._add_packets(syn)
             if target_ip in self.all_internal_hosts:
                print(f"  [!] SMBv1 probe (gets response): {self.compromised_host_ip} -> {target_ip}")
                smb_payload = (b'\x00\x00\x00\x84\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x53\xc8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xfe\x00\x00\x00\x00\x00\x6c\x00\x02NT LM 0.12\x00')
                packets = [self._create_tcp_packet(target_ip, 445, self.compromised_host_ip, sport, 'SA'),
                           self._create_tcp_packet(self.compromised_host_ip, sport, target_ip, 445, 'A'),
                           self._create_tcp_packet(self.compromised_host_ip, sport, target_ip, 445, 'PA', Raw(load=smb_payload))]
                self._add_packets(packets)

    # --- SIMULATION ORCHESTRATION ---
    def generate_simulation(self):
        print("Starting PCAP generation process...")
        
        print("\n[PHASE 1] Generating initial, heavy background noise...")
        self.create_arp_traffic()
        for i in range(50):
            activity = random.choice(['dns_https', 'smb', 'sftp', 'ping', 'http', 'nfs', 'smtp'])
            host = random.choice(self.benign_hosts)
            if activity == 'dns_https':
                domain, ip = random.choice(list(self.legit_domains.items()))
                self.create_dns_traffic(host, domain, ip)
                self.create_tls_session(host, ip)
            elif activity == 'http':
                self.create_http_session(host, "http.badssl.com", "104.154.89.105")
            elif activity == 'smb': self.create_benign_smb_session(host, self.fileserver_ip)
            elif activity == 'sftp': self.create_sftp_session(host, self.fileserver_ip)
            elif activity == 'ping': self.create_benign_ping(host, self.gateway_ip)
            elif activity == 'nfs': self.create_nfs_rpc_session(host, self.fileserver_ip)
            elif activity == 'smtp': self.create_smtp_session(host, self.mail_server_ip)
        
        print("\n[PHASE 2] Compromised host begins network reconnaissance...")
        self.create_icmp_sweep()
        print("\n[*] Interleaving more benign traffic...")
        for _ in range(20): self.create_benign_smb_session(random.choice(self.benign_hosts), self.fileserver_ip)
        self.create_smb_sweep()

        print("\n[PHASE 3] Compromised host establishes Command & Control...")
        self.create_dns_traffic(self.compromised_host_ip, self.malicious_domain, self.c2_server_ip)
        self.create_tls_session(self.compromised_host_ip, self.c2_server_ip)

        print("\n[PHASE 4] Generating final background noise to mask C2 activity...")
        for i in range(40):
            activity = random.choice(['dns_https', 'smb', 'sftp', 'ping', 'http', 'smtp'])
            host = random.choice(self.benign_hosts)
            if activity == 'dns_https':
                domain, ip = random.choice(list(self.legit_domains.items()))
                self.create_dns_traffic(host, domain, ip)
                if random.random() > 0.5: self.create_tls_session(host, ip)
            elif activity == 'smb': self.create_benign_smb_session(host, self.fileserver_ip)
            elif activity == 'sftp': self.create_sftp_session(host, self.fileserver_ip)
            elif activity == 'smtp': self.create_smtp_session(host, self.mail_server_ip)
            else: self.create_http_session(host, "http.badssl.com", "104.154.89.105")

        print(f"\nWriting {len(self.packets)} packets to {self.pcap_file}...")
        self.packets.sort(key=lambda p: p.time)
        wrpcap(self.pcap_file, self.packets)
        print(f"PCAP file generation complete! Total packets: {len(self.packets)}")

if __name__ == "__main__":
    output_filename = "attack_simulation.pcap"
    generator = PcapGenerator(output_filename)
    generator.generate_simulation()
