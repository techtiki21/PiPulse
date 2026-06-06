import argparse         # cmd arguments
import urllib.request   # HTTP requests
import json

def fetchJSON(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode())

def check_ping(ip, port, endpoint):
    url = f"http://{ip}:{port}/{endpoint}"  # makes a url based on args passed in cli
    try:
        data = fetchJSON(url)
    except Exception as e:
            print(f"Could not reach {ip}:{port}")
            print(f"  Error details: {e}")
            return False
    
    if endpoint == 'stats':
        print(f"CPU Utilized: {data.get('cpuPercent')}%")
        print(f"Ram Utilized: {data.get('ramUsage')}%")
        print(f"Disk Utilized: {data.get('diskUsage')}%\n\n")
    elif endpoint == 'disk':
        print(f"Total Disk Space: {data.get('total')} GB")
        print(f"Used Disk Space: {data.get('used')} GB")
        print(f"Free Disk Space: {data.get('free')} GB")
        print(f"Disk Utilized: {data.get('percent')}%\n\n")


def main():
    # main command
    parser = argparse.ArgumentParser(description="View status of Raspberry Pi")
    parser.add_argument('--host', required=True, help='Local IP of the Pi')
    parser.add_argument('--port', default=8080, type=int)
    
    # Create subcommand 'stats'
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # stats subcommand
    statsParser = subparsers.add_parser('stats', help='Recieve hardware utilization')

    # disk subcommand
    diskParser = subparsers.add_parser('disk', help="Recieve detailed disk information")

    args = parser.parse_args()
    print(f"\n\nPinging Pi at {args.host}...\n")

    if args.command == 'stats':
        check_ping(args.host, args.port, 'stats')
    elif args.command == 'disk':
        check_ping(args.host, args.port, 'disk')

if __name__ == '__main__':
    main()