# token_screener_cli.py
# CLI tool to screen tokens using Pulse Screener

import argparse
from screener.screener_engine import get_token_profile, screen_token_list
from config import VALID_USER_TOKENS


def print_token_profile(profile):
    print("\n=== Token Profile ===")
    for key, value in profile.items():
        print(f"{key}: {value}")


def main():
    parser = argparse.ArgumentParser(description="Pulse Screener CLI")
    parser.add_argument("--symbol", type=str, help="Token symbol to screen (e.g., GORK)")
    parser.add_argument("--mint", type=str, help="Token mint address")
    parser.add_argument("--all", action="store_true", help="Screen all monitored tokens")
    parser.add_argument("--verbose", action="store_true", help="Print full debug info")

    args = parser.parse_args()

    if args.symbol and args.mint:
        profile = get_token_profile(args.symbol, args.mint, include_logs=args.verbose)
        print_token_profile(profile)
    elif args.all:
        results = screen_token_list(VALID_USER_TOKENS, show_all=True)
        print(f"\nScreened {len(results)} tokens:")
        for p in results:
            print_token_profile(p)
    else:
        print("Please provide either --symbol + --mint or use --all.")
        parser.print_help()


if __name__ == "__main__":
    main()
