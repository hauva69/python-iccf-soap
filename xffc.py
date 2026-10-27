#!/usr/bin/python3

import getpass
import urllib.request
from suds.client import Client
from suds.transport.http import HttpTransport


class ICCFTransport(HttpTransport):
    """Custom transport to ensure User-Agent is set for all requests, including WSDL retrieval."""

    def __init__(self, timeout=30):
        HttpTransport.__init__(self, timeout=timeout)
        self.urlopener = urllib.request.build_opener()
        # ICCF server requires a common User-Agent to avoid 403 Forbidden
        self.urlopener.addheaders = [
            ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ICCF-Client/1.0")
        ]

    def open(self, request):
        return self.urlopener.open(request.url, data=request.message)


class ICCFClient:
    """Python client for the ICCF (xFCC Basic) SOAP API."""

    WSDL_URL = "https://www.iccf.com/xfccbasic.asmx?WSDL"

    def __init__(self, timeout: int = 30):
        """Initializes the SOAP client with custom transport.

        Args:
            timeout (int): Request timeout in seconds.
        """
        self.transport = ICCFTransport(timeout=timeout)
        self.client = Client(
            self.WSDL_URL,
            transport=self.transport,
        )

    def get_my_games(self, username, password):
        """Fetches the list of games for the specified user.

        Args:
            username (str): ICCF username.
            password (str): ICCF password.

        Returns:
            list: A list of XfccGame objects.
        """
        result = self.client.service.GetMyGames(username=username, password=password)
        if hasattr(result, "XfccGame"):
            # Suds returns a list if there are multiple, or a single object if there's one.
            # We ensure it's always a list for consistent iteration.
            games = result.XfccGame
            if isinstance(games, list):
                return games
            return [games]
        return []

    def print_available_methods(self):
        """Prints all available methods and parameters provided by the SOAP interface."""
        print(self.client)


if __name__ == "__main__":
    # Example usage
    iccf = ICCFClient()

    # Print all available API methods
    print("--- Available API Methods ---")
    iccf.print_available_methods()

    # Prompt for credentials
    print("\n--- Login to ICCF ---")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    try:
        games = iccf.get_my_games(username, password)
        if games:
            print(f"\nFound {len(games)} games:")
            for game in games:
                # Debugging unexpected types
                if not hasattr(game, 'myTurn'):
                    print(f"Unexpected game object structure: {type(game)}")
                    print(game)
                    continue
                turn = "Your turn" if game.myTurn else "Opponent's turn"
                print(f"[{game.id}] {game.white} vs {game.black} - {turn}")
        else:
            print("No active games found or authentication failed.")
    except Exception as e:
        print(f"An error occurred: {e}")
