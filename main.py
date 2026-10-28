import getpass
from iccf_xfcc import ICCFClient

def main():
    iccf = ICCFClient()
    print("\n--- Login to ICCF (using library) ---")
    username = input("Username (ICCF ID): ")
    password = getpass.getpass("Password: ")

    try:
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
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
