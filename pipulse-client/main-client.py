import argparse         # cmd arguments
import urllib.request   # HTTP requests
import json
import sqlite3
from datetime import datetime, timezone

dataList = ["0", 0, 0, 0, 0]

def fetchJSON(url):
    with urllib.request.urlopen(url, timeout=20) as response:
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
    
    global dataList
    if mainEndpoint == 'stats':
        dataList = [data.get('cpuPercent'), data.get('ramUsage'), data.get('diskUsage')]
        print(f"CPU Utilized: {dataList[0]}%")
        print(f"RAM Utilized: {dataList[1]}%")
        print(f"Disk Utilized: {dataList[2]}%\n\n")

    elif mainEndpoint == 'disk':
        dataList = [data.get('total'), data.get('used'), data.get('free'), data.get('percent')]
        print(f"Total Disk Space: {dataList[0]} GB")
        print(f"Used Disk Space: {dataList[1]} GB")
        print(f"Free Disk Space: {dataList[2]} GB")
        print(f"Disk Utilized: {dataList[3]}%\n\n")

    elif mainEndpoint == 'memory':
        dataList = [data.get('total'), data.get('used'), data.get('available'), data.get('percent')]
        print(f"Total RAM Size: {dataList[0]} GB")
        print(f"Used RAM: {dataList[1]} GB")
        print(f"Available RAM: {dataList[2]} GB")
        print(f"RAM Utilized: {dataList[3]}%\n\n")

    elif mainEndpoint == 'cpu':
        dataList = [data.get('count'), data.get('physical'), data.get('usage')]
        print(f"CPU Cores: {dataList[0]}")
        print(f"Physical CPU Cores: {dataList[1]}")
        print(f"CPU Usage: {dataList[2]}%")
        print("Core Usage: ")
        for i, core in enumerate(data.get('coreUsage')):
            print(f"    Core {i+1}: {core}%")

    dateUTC = datetime.now(timezone.utc)
    timestamp = dateUTC.strftime('%Y-%m-%d %H:%M:%S')
    dataList.append(timestamp)


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
    
    # create/connect to database
    db = sqlite3.connect('pipulse.db')
    cursor = db.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpu INTEGER,
            gpu INTEGER,
            ram INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP
        );
                   
        CREATE TABLE IF NOT EXISTS disk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total INTEGER,
            taken INTEGER,
            avail INTEGER,
            usage INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP
        );
                   
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total INTEGER,
            taken INTEGER,
            avail INTEGER,
            usage INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP
        );
                   
        CREATE TABLE IF NOT EXISTS cpu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cores INTEGER,
            physical INTEGER,
            usage INTEGER,
            time DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    args = parser.parse_args()
    print(f"\n\nPinging Pi at {args.host}...\n")

    if args.command == 'stats':
        check_ping(args.host, args.port, 'stats')
        cursor.execute('''
            INSERT INTO stats (cpu, gpu, ram, time)
            VALUES (?, ?, ?, ?)
        ''', dataList)

    elif args.command == 'disk':
        check_ping(args.host, args.port, 'disk')
        cursor.execute('''
            INSERT INTO disk (total, taken, avail, usage, time)
            VALUES (?, ?, ?, ?, ?)
        ''', dataList[:5])

    elif args.command == 'memory':
        check_ping(args.host, args.port, 'memory')
        cursor.execute('''
            INSERT INTO memory (total, taken, avail, usage, time)
            VALUES (?, ?, ?, ?, ?)
        ''', dataList[:5])

    elif args.command == 'cpu':
        print(f"Recording interval for {args.secondsFlag} seconds...\n")
        check_ping(args.host, args.port, f'cpu?seconds={args.secondsFlag}')
        cursor.execute('''
            INSERT INTO cpu (cores, physical, usage, time)
            VALUES (?, ?, ?, ?)
        ''', dataList[:4])

    db.commit()
if __name__ == '__main__':
    main()