import argparse         # cmd arguments
import urllib.request   # HTTP requests
import json

def check_ping(ip, port, endpoint):
    url = f"http://{ip}:{port}/{endpoint}"  # makes a url based on args passed in cli
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            print(f"CPU Utilized: {data.get('cpuPercent')}%")
            print(f"Ram Utilized: {data.get('ramUsage')}%")
            print(f"Disk Utilized: {data.get('diskUsage')}%")
    except Exception as e:
        print(f"Could not reach {ip}:{port}")
        print(f"  Error details: {e}")
        return False


def main():
    # main command
    parser = argparse.ArgumentParser(description="View status of Raspberry Pi")
    parser.add_argument('--host', required=True, help='Local IP of the Pi')
    parser.add_argument('--port', default=8080, type=int)
    
    # Create subcommand 'stats'
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # stats subcommand
    statsParser = subparsers.add_parser('stats', help='Recieve hardware utilization')

    args = parser.parse_args()
    print(f"Pinging Pi at {args.host}...")

    if args.command == 'stats':
        check_ping(args.host, args.port, 'stats')

if __name__ == '__main__':
    main()