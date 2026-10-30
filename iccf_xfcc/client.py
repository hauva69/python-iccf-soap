'''
A client to the ICCF SOAP API.
'''

import urllib.request
from suds.client import Client
from suds.transport.http import HttpTransport

import chess
import chess.pgn

# pylint: disable=too-many-instance-attributes)
# pylint: disable=too-few-public-methods
class ICCFGame(chess.pgn.Game):
    """Extension of chess.pgn.Game to include ICCF-specific fields."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iccf_id = None
        self.my_turn = False
        self.has_white = False
        self.draw_offered = False
        self.white_title = None
        self.black_title = None
        self.white_elo = None
        self.black_elo = None
        self.white_na = None
        self.black_na = None
        self.event_sponsor = None
        self.section = None
        self.stage = None
        self.board_number = None
        self.days_player = None
        self.hours_player = None
        self.minutes_player = None
        self.days_opponent = None
        self.hours_opponent = None
        self.minutes_opponent = None
        self.server_info = None
        self.game_link = None

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
        """Converts a raw suds object into an ICCFGame (chess.pgn.Game) object."""
        game_obj = ICCFGame()

        # Helper to get attributes from suds object or tuple/list
        def get_val(idx, field):
            if hasattr(g, field):
                return getattr(g, field)
            if isinstance(g, (tuple, list)) and idx < len(g):
                return g[idx]
            return None

        # Map fields to ICCFGame attributes and PGN tags
        game_obj.iccf_id = get_val(0, "id")
        game_obj.headers["White"] = str(get_val(1, "white") or "Unknown")
        game_obj.headers["Black"] = str(get_val(2, "black") or "Unknown")
        game_obj.headers["Event"] = str(get_val(3, "event") or "ICCF Event")
        game_obj.headers["Site"] = str(get_val(4, "site") or "ICCF")
        game_obj.my_turn = bool(get_val(5, "myTurn"))
        game_obj.has_white = bool(get_val(6, "hasWhite"))
        # moves = get_val(7, "moves") - could be parsed into game_obj if in SAN/UCI
        game_obj.draw_offered = bool(get_val(8, "drawOffered"))
        game_obj.headers["Message"] = str(get_val(9, "message") or "")
        game_obj.white_title = get_val(10, "whiteTitle")
        game_obj.black_title = get_val(11, "blackTitle")
        game_obj.white_elo = get_val(12, "whiteElo")
        game_obj.black_elo = get_val(13, "blackElo")
        game_obj.white_na = get_val(14, "whiteNA")
        game_obj.black_na = get_val(15, "blackNA")
        game_obj.event_sponsor = get_val(16, "eventSponsor")
        game_obj.section = get_val(17, "section")
        game_obj.stage = get_val(18, "stage")
        game_obj.board_number = get_val(19, "board")
        game_obj.headers["TimeControl"] = str(get_val(20, "timeControl") or "")
        # setup = get_val(21, "setup")
        fen = get_val(22, "fen")
        if fen:
            game_obj.headers["FEN"] = fen
            game_obj.headers["SetUp"] = "1"

        game_obj.headers["Result"] = str(get_val(23, "result") or "*")
        game_obj.headers["Variant"] = str(get_val(24, "variant") or "Standard")
        game_obj.days_player = get_val(25, "daysPlayer")
        game_obj.hours_player = get_val(26, "hoursPlayer")
        game_obj.minutes_player = get_val(27, "minutesPlayer")
        game_obj.days_opponent = get_val(28, "daysOpponent")
        game_obj.hours_opponent = get_val(29, "hoursOpponent")
        game_obj.minutes_opponent = get_val(30, "minutesOpponent")
        game_obj.server_info = get_val(31, "serverInfo")
        game_obj.game_link = get_val(32, "gameLink")
        date = get_val(33, "eventDate")
        if date:
            game_obj.headers["Date"] = str(date)

        return game_obj

    def print_available_methods(self):
        """Print all available methods."""
        print(self.client)
