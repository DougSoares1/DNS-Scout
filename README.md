# DnsXplorer

**Version:** 0.1  
**Author:** DougSoares  
**Recommended Platform:** Kali Linux  

## Description  

DnsXplorer is a powerful tool designed to assist in security testing, specializing in DNS enumeration, brute force for subdomains and directories, as well as port scanning with Nmap. With its intuitive interface and efficient features, the tool helps security analysts identify vulnerabilities in domains and subdomains.  

## Features  

- **DNS Enumeration:**  
  - Queries A, AAAA, TXT, and CNAME records.  
  - Identifies if the domain is nonexistent (NXDOMAIN).  

- **Subdomain Brute Force:**  
  - Tests subdomains based on customizable or standard wordlists.  

- **Directory Brute Force:**  
  - Checks the accessibility of directories on subdomains.  

- **Port Scanning with Nmap:**  
  - Identifies open ports and associated services on the IPs of discovered subdomains.  

- **Export Results:**  
  - Saves results to a JSON file for later analysis.  

## Requirements  

- **Operating System:** Kali Linux (or any system supporting Python 3)  
- **Dependencies:**  
  - Python 3  
  - Python modules: `dns.resolver`, `colorama`, `tqdm`, `requests`, `pyfiglet`  
  - External tools: `Nmap`  

To install Python dependencies, run:  
```bash  
pip install dnspython colorama tqdm requests pyfiglet  
```  

Ensure Nmap is installed:  
```bash  
sudo apt-get install nmap  
```  

If there is an error when installing Python dependencies, consider using a virtual environment:  
```bash  
sudo apt-get install python3-venv  
python3 -m venv venv  
source venv/bin/activate  
pip install dnspython colorama tqdm requests pyfiglet  
```  

To deactivate the virtual environment, run:  
```bash  
deactivate  
```  

## Usage  

### Running the Tool  

1. Clone the GitHub repository:  
   ```bash  
   git clone https://github.com/DougSoares1/DnsXplorer.git  
   cd DnsXplorer  
   ```  

2. Run the script:  
   ```bash  
   python3 DnsXplorer.py  
   ```  

### Interactive Options  
- **Base Domain:** Enter the domain to analyze (e.g., `https://www.example.com.br/`). The script can handle complete addresses or just the domain name.  
- **Custom Subdomain Wordlist:** If you have a wordlist, specify its file path. Otherwise, the tool will use a default list. E.g., `/home/local/wordlist.txt`  
- **Nmap Scanning:** Choose whether to perform open port scanning on discovered subdomains.  
- **Directory Brute Force:** Indicate if you want to brute force directories and, if so, specify the wordlist to use. E.g., `/home/local/wordlist.txt`  

### Results  
Results will be displayed on the screen and saved to a JSON file in the format `<domain>_results.json`.  

## Example Output  
```plaintext  
Main Domain:  
  example.com -> IPs: 192.168.1.1, 192.168.1.2  
  A: 192.168.1.1  
  AAAA: No records found  
  TXT: "v=spf1 include:example.com ~all"  
  NX: No records found  

Discovered Subdomains:  
  Subdomain found: www.example.com -> IPs: 192.168.1.3  
  A: 192.168.1.3  
  AAAA: No records found  
  TXT: "v=spf1 include:example.com ~all"  
  NX: No records found  

Nmap Results by IP:  
  IP: 192.168.1.3  
    Port: 80, Service: http  
    Port: 443, Service: https  

Discovered Directories:  
  Subdomain: www.example.com  
    [Accessible] http://www.example.com/admin  
    [Accessible] https://www.example.com/login  

Results exported to: example.com_results.json  
```  

## Notes  

If the script fails to execute in the terminal, try running it in your virtual environment:  
```bash  
source venv/bin/activate  
cd DnsXplorer  
python3 DnsXplorer.py  
```  

To deactivate the virtual environment, run:  
```bash  
deactivate  
```  

- Note that the script might take time depending on the size of your wordlist and IP scanning. You can skip the scanning and directory verification steps by typing `n`.
- If you're using a large wordlist and your machine has sufficient processing power, you can modify the line
  
  ```bash
      with ThreadPoolExecutor(max_workers=200)
  ```
  from `200` to up to `500.`
- New updates to improve and accelerate the code will be available soon.  
- If you prefer custom Nmap scanning parameters, you can edit the script locally by modifying the commented line.  

## Images  
![Captura de tela 2024-12-22 225410](https://github.com/user-attachments/assets/eaae4ed8-5ffc-4068-90bc-bdbeaf4eda57)
![Captura de tela 2024-12-22 225436](https://github.com/user-attachments/assets/92ae659f-7144-4709-a1e7-4ef8784619d7)
![Captura de tela 2024-12-22 225507](https://github.com/user-attachments/assets/4de975fa-3dd0-408c-9947-5da03cd07111)
![Captura de tela 2024-12-22 225533](https://github.com/user-attachments/assets/10362e57-92af-4d12-8341-726df3f25d99)



Note: The tested domain is specifically designed for this purpose.  

## License  
This project is licensed under the MIT License. See the LICENSE file for more details.  

## Contributions  
Contributions are welcome! If you find any issues or have suggestions for improvement, open an issue or submit a pull request.  

## Disclaimer  
This tool was developed for educational and research purposes. Unauthorized use for malicious activities is strictly prohibited. The author is not responsible for any damage caused by the use of this tool.

