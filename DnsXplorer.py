import dns.resolver
from colorama import Fore, Style, init
from tqdm import tqdm
import os
import json
import subprocess
import requests
from concurrent.futures import ThreadPoolExecutor
import signal
import sys
import warnings
import urllib3
import pyfiglet
import re

# Inicializar o colorama
init(autoreset=True)

# Desabilitar os avisos de verificação de SSL do urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Exibir o banner
def display_banner():
    banner = pyfiglet.figlet_format("DnsXplorer")
    print(f"{Fore.CYAN}{Style.BRIGHT}{banner}")
    print(f"{Fore.YELLOW}{Style.NORMAL}by: DougSoares V: 0.1\n")

# Tratar o sinal de interrupção (Ctrl+C)
def signal_handler(signal, frame):
    print(f"\n{Fore.RED}Execução interrompida pelo usuário. Finalizando...")
    sys.exit(0)  # Encerra o programa

# Registrar o sinal de interrupção (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# Realizar o DNS lookup
def dns_lookup(domain, record_type='A'):
    try:
        result = dns.resolver.resolve(domain, record_type)
        return [ip.to_text() for ip in result]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return None
    except Exception as e:
        return str(e)

# Realizar a enumeração de DNS com tipos adicionais
def dns_lookup_extended(domain):
    results = {
        "A": [],
        "AAAA": [],
        "TXT": [],
        "CNAME": [],
        "NX": None
    }
    try:
        # Busca os registros A
        a_records = dns.resolver.resolve(domain, 'A')
        results["A"] = [ip.to_text() for ip in a_records]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        results["A"] = None
    
    try:
        # Busca os registros AAAA
        aaaa_records = dns.resolver.resolve(domain, 'AAAA')
        results["AAAA"] = [ip.to_text() for ip in aaaa_records]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        results["AAAA"] = None
    
    try:
        # Busca os registros TXT
        txt_records = dns.resolver.resolve(domain, 'TXT')
        results["TXT"] = [txt.to_text() for txt in txt_records]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        results["TXT"] = None
    
    try:
        # Busca os registros CNAME
        cname_records = dns.resolver.resolve(domain, 'CNAME')
        results["CNAME"] = [cname.to_text() for cname in cname_records]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        results["CNAME"] = None

    # Verificando se o domínio existe
    if not any(results.values()):
        results["NX"] = "Nenhum registro encontrado"
    
    return results

# Brute force de subdomínios com barra de progresso
def brute_force_subdomains(base_domain, subdomains):
    found_subdomains = {}
    print()
    print(f"{Fore.YELLOW}{Style.BRIGHT}Realizando brute force em subdomínios para {base_domain}...\n")
    
    # Barra de progresso
    with tqdm(total=len(subdomains), desc="Progresso", ncols=100) as pbar:
        for sub in subdomains:
            subdomain = f"{sub}.{base_domain}"
            ips = dns_lookup(subdomain)
            if ips and not isinstance(ips, str):
                found_subdomains[subdomain] = ips
            pbar.update(1)  # Atualiza a barra de progresso
    return found_subdomains

# Varredura com Nmap e exibir resultados por IP
def scan_with_nmap_ips(subdomains):
    print()
    print(f"\n{Fore.YELLOW}Iniciando varredura com Nmap...\n")
    nmap_results = {}
    for subdomain, ips in subdomains.items():
        for ip in ips:
            print(f"{Fore.CYAN}Escaneando {subdomain} ({ip})...")
            try:
                # Executa o comando Nmap e captura portas abertas e serviços
                result = subprocess.check_output(
                    ["nmap", "-p-", "--open", ip],  #Altere essa linha caso deseje adicionar algo a mais em sua varredura com o Nmap
                    universal_newlines=True
                )
                open_ports_services = parse_ports_and_services(result)
                nmap_results[ip] = open_ports_services
            except Exception as e:
                print(f"{Fore.RED}Erro ao escanear {ip}: {e}")
    print(f"{Fore.GREEN}Varredura concluída!\n")
    return nmap_results

# Parsear portas e serviços do Nmap
def parse_ports_and_services(output):
    ports_services = []
    lines = output.splitlines()
    capture = False
    for line in lines:
        if line.startswith("PORT"):
            capture = True
            continue
        if capture and line.strip() == "":
            break
        if capture:
            parts = line.split()
            port = parts[0].split("/")[0]
            service = " ".join(parts[1:])
            ports_services.append((port, service))
    return ports_services

# Brute force de diretórios em subdomínios
def brute_force_directories(subdomains, wordlist):
    print(f"\n{Fore.YELLOW}Iniciando verificação de diretórios...\n")
    found_directories = {}

    def check_directory(url):
        try:
            response = requests.get(url, timeout=5, verify=False)  # Ignora verificação de certificado SSL
            if response.status_code == 200:
                return (url, 'Acessível')
            elif response.status_code == 403:
                return (url, 'Não Acessível')
            else:
                return (url, 'Presente, mas Não Acessível')
        except requests.RequestException:
            return (url, 'Erro ao acessar')

    for subdomain, ips in subdomains.items():
        with ThreadPoolExecutor(max_workers=200) as executor:
            # Tentando tanto http quanto https
            urls = [f"http://{subdomain}/{word.strip()}" for word in wordlist] + [f"https://{subdomain}/{word.strip()}" for word in wordlist]
            results = list(tqdm(executor.map(check_directory, urls), total=len(urls), desc=f"Diretórios ({subdomain})", ncols=100))

        # Filtrar apenas os diretórios acessíveis
        accessible_directories = [(url, status) for url, status in results if status == 'Acessível']
        found_directories[subdomain] = accessible_directories

    return found_directories

# Exibir resultados detalhados
def display_results_ips(base_domain, base_ips, found_subdomains, nmap_results=None, directory_results=None):
    # Exibição dos registros DNS do domínio base
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Principal:")
    if base_ips:
        print(f"  {Fore.GREEN}{base_domain} -> IPs: {', '.join(base_ips)}")
    else:
        print(f"  {Fore.RED}Nenhum registro encontrado para {base_domain}")

    # Enumeração dos registros DNS para o domínio base
    dns_results = dns_lookup_extended(base_domain)
    for record_type, records in dns_results.items():
        if records:
            print(f"  {Fore.GREEN}{record_type}: {', '.join(records)}")
        else:
            print(f"  {Fore.RED}{record_type}: Nenhum registro encontrado")

    # Subdomínios e registros DNS
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Subdomínios encontrados:")
    for subdomain, ips in found_subdomains.items():
        print()
        print(f"  {Fore.CYAN}{Style.BRIGHT}Subdomínio encontrado: {subdomain} -> IPs: {', '.join(ips)}")
        
        # Enumeração dos registros DNS para cada subdomínio
        subdomain_dns_results = dns_lookup_extended(subdomain)
        for record_type, records in subdomain_dns_results.items():
            if records:
                print(f"    {Fore.GREEN}{record_type}: {', '.join(records)}")
            else:
                print(f"    {Fore.RED}{record_type}: Nenhum registro encontrado")

    # Resultados do Nmap
    if nmap_results:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Resultados do Nmap por IP:")
        for ip, ports_services in nmap_results.items():
            print(f"\n  {Fore.CYAN}IP: {ip}")
            for port, service in ports_services:
                print(f"    {Fore.YELLOW}Porta: {port}, Serviço: {service}")

    # Diretórios encontrados
    if directory_results:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Diretórios encontrados:")
        for subdomain, directories in directory_results.items():
            print(f"\n  {Fore.CYAN}Subdomínio: {subdomain}")
            if directories:
                for directory, status in directories:
                    print(f"    {Fore.GREEN}[Acessível] {directory}")
            else:
                print(f"    {Fore.RED}[Nenhum diretório acessível encontrado]")

# Exportar os resultados para um arquivo JSON
def save_results_to_json(base_domain, base_ips, found_subdomains, nmap_results=None, directory_results=None):
    results = {
        "base_domain": base_domain,
        "dns_records": dns_lookup_extended(base_domain),
        "base_ips": base_ips,
        "found_subdomains": found_subdomains,
        "nmap_results": nmap_results,
        "directory_results": directory_results
    }

    # Caminho para o arquivo de resultados
    output_file = f"{base_domain}_results.json"

    # Salvar os resultados no arquivo JSON
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)
    print()
    print()
    print(f"{Fore.GREEN}Resultados exportados para: {output_file}")

# Função principal
def main():
    display_banner()
    
    # Recebe o domínio e remove http://, https:// e a barra final "/"
    base_domain = input(f"{Fore.YELLOW}{Style.BRIGHT}Digite o domínio base para enumeração de DNS (ex: example.com): {Fore.WHITE}").strip()
    base_domain = re.sub(r"^https?://(www\.)?", "", base_domain).rstrip("/")

    use_custom_subdomains = input(f"{Fore.YELLOW}{Style.BRIGHT}Deseja usar um arquivo personalizado de subdomínios? (s/n): {Fore.WHITE}").strip().lower()
    subdomains = []

    if use_custom_subdomains == "s":
        file_name = input(f"{Fore.YELLOW}{Style.BRIGHT}Digite o nome do arquivo com a lista de subdomínios: {Fore.WHITE}").strip()
        try:
            with open(file_name, "r") as file:
                subdomains = file.readlines()
            subdomains = [subdomain.strip() for subdomain in subdomains]
        except FileNotFoundError:
            print(f"{Fore.RED}Arquivo não encontrado. Usando lista padrão.")
            subdomains = ["www", "mail", "ftp", "blog"]
    else:
        subdomains = ["www", "mail", "ftp", "blog"]

    # Enumeração de DNS para o domínio base
    print(f"\n{Fore.YELLOW}Obtendo registros DNS para o domínio base: {base_domain}")
    base_ips = dns_lookup(base_domain) 

    # Brute Force para subdomínios
    found_subdomains = brute_force_subdomains(base_domain, subdomains)

    # Perguntar se deseja realizar varredura com Nmap
    print()
    run_nmap = input(f"{Fore.YELLOW}{Style.BRIGHT}Deseja realizar varredura com Nmap? (s/n): {Fore.WHITE}").strip().lower()
    nmap_results = None
    if run_nmap == "s":
        nmap_results = scan_with_nmap_ips(found_subdomains)

    # Perguntar se deseja realizar brute force de diretórios
    print()
    run_directory_enum = input(f"{Fore.YELLOW}{Style.BRIGHT}Deseja realizar brute force de diretórios? (s/n): {Fore.WHITE}").strip().lower()
    directory_results = None
    if run_directory_enum == "s":
        wordlist_file = input(f"{Fore.YELLOW}Digite o caminho para o arquivo de wordlist (pressione Enter para usar a padrão): {Fore.WHITE}").strip()
        
        if wordlist_file and os.path.exists(wordlist_file):
            with open(wordlist_file, "r") as file:
                wordlist = file.readlines()
            wordlist = [line.strip() for line in wordlist]
        else:
            print(f"{Fore.YELLOW}Usando wordlist padrão...")
            wordlist = ["admin", "login", "test", "wp-login", "admin.php", "index.php"]  # Wordlist padrão
        
        directory_results = brute_force_directories(found_subdomains, wordlist)

    # Exibir e salvar os resultados
    display_results_ips(base_domain, base_ips, found_subdomains, nmap_results, directory_results)
    save_results_to_json(base_domain, base_ips, found_subdomains, nmap_results, directory_results)

if __name__ == "__main__":
    main()
