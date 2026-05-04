import argparse
from core.scanner import Scanner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--scan", required=True, help="Scan type (xss, sqli, ...)")

    args = parser.parse_args()

    scanner = Scanner(args.url, args.scan)
    scanner.run()

if __name__ == "__main__":
    main()