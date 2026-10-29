#!/usr/bin/python3

'''
Print my ICCF games.
'''

import getpass
import urllib.error
import sys
import suds
from iccf_xfcc import ICCFClient

def _main():
    print("\n--- Login to ICCF (using library) ---")
    username = input("Username (ICCF ID): ")
    password = getpass.getpass("Password: ")

    try:
        iccf = ICCFClient()
        games = iccf.get_my_games(username, password)
        if games:
            print(f"\nFound {len(games)} active game(s):")
            for game in games:
                game_id = getattr(game, 'id', 'Unknown')
                white = getattr(game, 'white', 'Unknown')
                black = getattr(game, 'black', 'Unknown')
                my_turn = getattr(game, 'myTurn', False)
                turn_str = "Your turn" if my_turn else "Opponent's turn"
                print(f"[{game_id}] {white} vs {black} - {turn_str}")
        else:
            print("\nNo active games found.")
    except (urllib.error.URLError, ConnectionError) as e:
        print(f"\nNetwork error: {e}", file=sys.stderr)
    except suds.WebFault as e:
        print(f"\nICCF service error: {e}", file=sys.stderr)
    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    _main()
