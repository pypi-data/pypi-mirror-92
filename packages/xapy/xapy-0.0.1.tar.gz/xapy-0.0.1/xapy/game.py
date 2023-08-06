# encoding: utf-8

class Game:

    XBOX_360 = 'Xbox 360'
    XBOX_ONE = 'Xbox One'
    WINDOWS = 'Windows'
    UNKNOWN = 'Unknown platform'

    def __init__(self, title_id: int, title: str, total_gamerscore: int, current_gamerscore: int,
                 current_achievements: int, platform: str = UNKNOWN):
        """Create a new Game.

        :param title_id: The numerical ID of the game on Xbox
        :param title: The title of the game
        :param total_gamerscore: The maximum obtainable gamerscore
        :param current_gamerscore: The user's current gamerscore
        :param current_achievements: The number of achievements the user has unlocked
        :param platform: The game's platform.
        """
        self.title_id = title_id
        self.title = title
        self.total_gamerscore = total_gamerscore
        self.current_gamerscore = current_gamerscore
        self.current_achievements = current_achievements
        self.platform = platform

    def __repr__(self):
        return 'Game {} ({} - {})'.format(self.title_id, self.title, self.platform)

    def __str__(self):
        return self.title
