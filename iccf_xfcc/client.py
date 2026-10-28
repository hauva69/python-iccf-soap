import urllib.request
from suds.client import Client
from suds.transport.http import HttpTransport

class ICCFTransport(HttpTransport):
    """Custom transport to ensure User-Agent is set for all requests."""

    def __init__(self, timeout=30):
        HttpTransport.__init__(self, timeout=timeout)
        self.urlopener = urllib.request.build_opener()
        self.urlopener.addheaders = [
            ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ICCF-Client/1.0")
        ]

    def open(self, request):
        return self.urlopener.open(request.url, data=request.message)

class ICCFClient:
    """Python client for the ICCF (xFCC Basic) SOAP API."""

    WSDL_URL = "https://www.iccf.com/xfccbasic.asmx?WSDL"

    def __init__(self, timeout: int = 30):
        self.transport = ICCFTransport(timeout=timeout)
        self.client = Client(self.WSDL_URL, transport=self.transport)

    def get_my_games(self, username, password):
        """Fetches the list of games and ensures they are returned as usable objects."""
        response = self.client.service.GetMyGames(username=username, password=password)

        raw_games = []
        if response:
            if hasattr(response, "XfccGame"):
                raw_games = response.XfccGame
            elif isinstance(response, list):
                raw_games = response
            else:
                raw_games = [response]

        if not isinstance(raw_games, list):
            raw_games = [raw_games]

        return [self._parse_game(g) for g in raw_games if g]

    def _parse_game(self, g):
        """Converts a raw suds object or tuple into a dictionary with known keys."""
        if hasattr(g, "id") and hasattr(g, "myTurn"):
            return g

        if isinstance(g, (tuple, list)):
            fields = [
                "id", "white", "black", "event", "site", "myTurn", "hasWhite",
                "moves", "drawOffered", "message", "whiteTitle", "blackTitle",
                "whiteElo", "blackElo", "whiteNA", "blackNA", "eventSponsor",
                "section", "stage", "board", "timeControl", "setup", "fen",
                "result", "variant", "daysPlayer", "hoursPlayer", "minutesPlayer",
                "daysOpponent", "hoursOpponent", "minutesOpponent", "serverInfo",
                "gameLink", "eventDate"
            ]
            class Game: pass
            game_obj = Game()
            for i, field in enumerate(fields):
                if i < len(g):
                    setattr(game_obj, field, g[i])
                else:
                    setattr(game_obj, field, None)
            return game_obj
        
        return g

    def print_available_methods(self):
        """Print all available methods."""
        print(self.client)
