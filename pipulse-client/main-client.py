import argparse         # cmd arguments
import urllib.request   # HTTP requests
import json

def fetchJSON(url):
    with urllib.request.urlopen(url, timeout=1000) as response:
        return json.loads(response.read().decode())

def check_ping(ip, port, endpoint):
    url = f"http://{ip}:{port}/{endpoint}"  # makes a url based on args passed in cli
    mainEndpoint = endpoint.split('?', 1)[0]
    try:
        data = fetchJSON(url)
    except Exception as e:
            print(f"Could not reach {ip}:{port}")
            print(f"  Error details: {e}")
            return False
    
    if mainEndpoint == 'stats':
        print(f"CPU Utilized: {data.get('cpuPercent')}%")
        print(f"RAM Utilized: {data.get('ramUsage')}%")
        print(f"Disk Utilized: {data.get('diskUsage')}%\n\n")
    elif mainEndpoint == 'disk':
        print(f"Total Disk Space: {data.get('total')} GB")
        print(f"Used Disk Space: {data.get('used')} GB")
        print(f"Free Disk Space: {data.get('free')} GB")
        print(f"Disk Utilized: {data.get('percent')}%\n\n")
    elif mainEndpoint == 'memory':
        print(f"Total RAM Size: {data.get('total')} GB")
        print(f"Used RAM: {data.get('used')} GB")
        print(f"Available RAM: {data.get('available')} GB")
        print(f"RAM Utilized: {data.get('percent')}%\n\n")
    elif mainEndpoint == 'cpu':
        print(f"CPU Cores: {data.get('count')}")
        print(f"Physical CPU Cores: {data.get('physical')}")
        print(f"CPU Usage: {data.get('usage')}%")
        print("Core Usage: ")
        for i, core in enumerate(data.get('coreUsage')):
            print(f"    Core {i+1}: {core}%")


def main():
    # main command
    parser = argparse.ArgumentParser(description="View status of Raspberry Pi")
    parser.add_argument('--host', required=True, help='Local IP of the Pi')
    parser.add_argument('--port', default=8000, type=int)
    
    # Create subparsers to add to the main parser
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    statsParser = subparsers.add_parser('stats', help='Recieve hardware utilization')
    diskParser = subparsers.add_parser('disk', help="Recieve detailed disk information")
    memoryParser = subparsers.add_parser('memory', help="Recieve detailed RAM information")

    cpuParser = subparsers.add_parser('cpu', help="Recieve detailed CPU information")
    cpuParser.add_argument(
        '--seconds', 
        type=int,
        default=2,
        dest='secondsFlag',
        help="Set a interval to record CPU usage"
        )

    args = parser.parse_args()
    print(f"\n\nPinging Pi at {args.host}...\n")


    if args.command == 'stats':
        check_ping(args.host, args.port, 'stats')
    elif args.command == 'disk':
        check_ping(args.host, args.port, 'disk')
    elif args.command == 'memory':
        check_ping(args.host, args.port, 'memory')
    elif args.command == 'cpu':
        print(f"Recording interval for {args.secondsFlag} seconds...\n")
        check_ping(args.host, args.port, f'cpu?seconds={args.secondsFlag}')

if __name__ == '__main__':
    main()