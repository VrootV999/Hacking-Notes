# Finds directory and documents present in the web page

# Basics
## Syntax
- `-w`                    wordlist
- -`u `                  url
- `-H`                    headers like cookies or session id (e.g., `-H "Cookie: sessionid=12345"`)
- `-X`                    HTTP method (GET, POST, PUT, DELETE, HEAD, etc.)
- `-d`                    POST data (e.g., `-d "username=test&password=FUZZ")`
- -`t`                  Number of Concurrent threads used
- - `-o`: Output results to a file in various formats:
    - `-of csv` (Comma separated)
    - `-of json`
    - `-of html`
## Filtering Results

- `-mc`: Match response by HTTP status code (e.g., `-mc 200` for OK)
- `-ms`: Match response by size (e.g., `-ms 500` for sizes around 500 bytes)
- `-fc`: Filter by status code (e.g., `-fc 404` to exclude Not Found)
- `-fs`: Filter by response size
- `-fw`: Filter by words present in the response
## Examples
#### Virtual host Discovery
- ffuf -w vhosts.txt -u https://target.com/FUZZ -H "Host: FUZZ.site.com" -mc 200 -fc 403 -fs 57
#### Match and filter
- ffuf -w wordlist.txt -u https://example.org/FUZZ -fs 42 -mc 200 
#### With a Header
- ffuf -w passwords.txt -u https://example.org/login -X POST 
  -d "username=admin&password=FUZZ" -H "User-Agent: EvilCorp-Browser" 
#### Simple Directory Discovery
- ffuf -w /path/to/directory_wordlist.txt -u https://target.com/FUZZ 
#### Basic scan
- ffuf -w wordlist.txt -u https://target.com/FUZZ 
