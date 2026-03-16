# dnsquery
DNS lookup tool: forward, reverse, batch, all record types.
```bash
python dnsquery.py lookup google.com --all
python dnsquery.py lookup example.com -t MX -j
python dnsquery.py reverse 8.8.8.8
python dnsquery.py batch hosts.txt -t A
```
## Zero dependencies. Python 3.6+.
