#!/usr/bin/env python3
"""dnsquery - DNS lookup utility."""
import socket, subprocess, argparse, sys, json

def resolve(host, record_type='A'):
    """Use system dig/nslookup for detailed queries."""
    try:
        result = subprocess.run(['dig', '+short', host, record_type], 
                               capture_output=True, text=True, timeout=5)
        return [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]
    except FileNotFoundError:
        # Fallback to socket
        if record_type == 'A':
            try:
                return [socket.gethostbyname(host)]
            except: return []
    except: return []

def reverse_lookup(ip):
    try: return socket.gethostbyaddr(ip)[0]
    except: return None

def main():
    p = argparse.ArgumentParser(description='DNS lookup tool')
    sub = p.add_subparsers(dest='cmd')
    
    lk = sub.add_parser('lookup', help='DNS lookup')
    lk.add_argument('host')
    lk.add_argument('-t', '--type', default='A', help='Record type (A, AAAA, MX, NS, TXT, CNAME, SOA)')
    lk.add_argument('--all', action='store_true', help='Query all common types')
    lk.add_argument('-j', '--json', action='store_true')
    
    rv = sub.add_parser('reverse', help='Reverse DNS lookup')
    rv.add_argument('ip')
    
    bl = sub.add_parser('batch', help='Batch lookup from file')
    bl.add_argument('file')
    bl.add_argument('-t', '--type', default='A')
    
    args = p.parse_args()
    if not args.cmd: p.print_help(); return
    
    if args.cmd == 'lookup':
        if args.all:
            types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        else:
            types = [args.type.upper()]
        
        results = {}
        for t in types:
            records = resolve(args.host, t)
            if records:
                results[t] = records
                if not args.json:
                    for r in records:
                        print(f"  {t:<6} {r}")
        
        if args.json:
            print(json.dumps({'host': args.host, 'records': results}, indent=2))
    
    elif args.cmd == 'reverse':
        hostname = reverse_lookup(args.ip)
        print(f"{args.ip} → {hostname or '(no PTR record)'}")
    
    elif args.cmd == 'batch':
        with open(args.file) as f:
            hosts = [l.strip() for l in f if l.strip() and not l.startswith('#')]
        for host in hosts:
            records = resolve(host, args.type)
            if records:
                print(f"  {host:<30} {', '.join(records)}")
            else:
                print(f"  {host:<30} (no records)")

if __name__ == '__main__':
    main()
