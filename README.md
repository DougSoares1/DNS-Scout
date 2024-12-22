# DnsXplorer

**Versão:** 0.1  
**Autor:** DougSoares  
**Plataforma recomendada:** Kali Linux

## Descrição

DnsXplorer é uma ferramenta poderosa projetada para assistência em testes de segurança, especializada em enumeração de DNS, brute force de subdomínios e diretórios, bem como varredura de portas com Nmap. Com sua interface intuitiva e recursos eficientes, a ferramenta ajuda analistas de segurança a identificar vulnerabilidades em domínios e subdomínios.

## Recursos

- **Enumeração de DNS:**
  - Consulta de registros A, AAAA, TXT e CNAME.
  - Identifica se o domínio é inexistente (NXDOMAIN).

- **Brute Force de Subdomínios:**
  - Testa subdomínios com base em listas customizáveis ou padrões.

- **Brute Force de Diretórios:**
  - Verifica acessibilidade de diretórios em subdomínios.

- **Varredura de Portas com Nmap:**
  - Identifica portas abertas e serviços associados em IPs de subdomínios encontrados.

- **Exportação de Resultados:**
  - Salva os resultados em um arquivo JSON para análise posterior.

## Requisitos

- **Sistema operacional:** Kali Linux (ou qualquer sistema com suporte a Python 3)
- **Dependências:**
  - Python 3
  - Módulos Python: `dns.resolver`, `colorama`, `tqdm`, `requests`, `pyfiglet`
  - Ferramentas externas: Nmap

Para instalar as dependências Python, execute:
```bash
pip install dnspython colorama tqdm requests pyfiglet
```

Certifique-se de que o Nmap está instalado:
```bash
sudo apt-get install nmap
```
Caso dê algum erro ao instalar as dependências do python considere em usar um ambiente vitual, execute:
```bash
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install dnspython colorama tqdm requests pyfiglet
```
Para desativar o ambiente virtual basta digitar
```bash
deactivate
```
## Uso

### Executando a Ferramenta
1. Clone o repositório do GitHub:
    ```bash
    git clone https://github.com/DougSoares1/DnsXplorer.git
    cd DnsXplorer
    ```
2. Execute o script:
    ```bash
    python3 DnsXplorer.py
    ```

### Opções Interativas
- **Domínio Base:** Informe o domínio que deseja analisar (ex: `https://www.example.com.br/`). o script consegue lidar com endereços completos ou somente o diminio. 
- **Arquivo de Subdomínios Personalizado:** Caso possua uma wordlist, especifique o caminho do arquivo. Caso contrário, a ferramenta usará uma lista padrão. Ex: `/home/local/wordlist.txt`
- **Varredura com Nmap:** Escolha se deseja realizar varredura de portas abertas em subdomínios encontrados.
- **Brute Force de Diretórios:** Informe se deseja realizar brute force em diretórios e, caso positivo, especifique a wordlist a ser utilizada. Ex: `/home/local/wordlist.txt`

### Resultados
Os resultados serão exibidos na tela e salvos em um arquivo JSON no formato `<dominio>_results.json`.

## Exemplo de Saída
```plaintext
Principal:
  example.com -> IPs: 192.168.1.1, 192.168.1.2
  A: 192.168.1.1
  AAAA: Nenhum registro encontrado
  TXT: "v=spf1 include:example.com ~all"
  NX:  Nenhum registro encontrado

Subdomínios encontrados:
  Subdomínio encontrado: www.example.com -> IPs: 192.168.1.3
  A: 192.168.1.3
  AAAA: Nenhum registro encontrado
  TXT: "v=spf1 include:example.com ~all"
  NX:  Nenhum registro encontrado

Resultados do Nmap por IP:
  IP: 192.168.1.3
    Porta: 80, Serviço: http
    Porta: 443, Serviço: https

Diretórios encontrados:
  Subdomínio: www.example.com
    [Acessível] http://www.example.com/admin
    [Acessível] https://www.example.com/login

Resultados exportados para: example.com_results.json
```
## Observações
Em alguns casos o script pode dar falha ao ser executado no terminal, quando acontece podemos executa-lo em nosso ambiente virtual, execute:
```bash
source venv/bin/activate
cd DnsXplorer
python3 DnsXplorer.py
```
O codigo será executado normalmente, para desativar o ambiente virtual basta executar
```bash
deactivate
```
Resalto que o script pode demorar levando em conta o tamnho de sua wordlist e também a varredura, portanto a etapa de varredura e verificação de diretorios pode ser pulada, basta digitar `n`
Em breve novas atualizações para melhorias e aceleração do codigo estará disponível 
Caso goste de outros parâmetros de verredura no nmap basta abrir o codigo em sua maquina e poderá alterar a linha na qual deixei comentada.

## Licença
Este projeto é licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais informações.

## Imangens

![Captura de tela 2024-12-21 205623](https://github.com/user-attachments/assets/5c945137-df83-4005-a76a-7c0ecb44f635)
![Captura de tela 2024-12-21 205702](https://github.com/user-attachments/assets/b8c50af9-1b8b-40a8-a952-9455af283c2a)
![Captura de tela 2024-12-21 205724](https://github.com/user-attachments/assets/9152e173-4460-4a18-8dbf-01dd5f828d10)

Observação: O dominio testado é proprio para teste.

## Contribuições
Contribuições são bem-vindas! Se você encontrar problemas ou tiver sugestões de melhorias, abra uma issue ou envie um pull request.

## Aviso Legal
Esta ferramenta foi desenvolvida para fins educacionais e de pesquisa. O uso indevido para atividades não autorizadas é estritamente proibido. O autor não se responsabiliza por quaisquer danos causados pelo uso desta ferramenta.

