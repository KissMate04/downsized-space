class GameState:
    """A class to represent the current state of the game.

    Args:
        player_position: A tuple representing the player's current position (x, y).
        enemy_positions: A list of tuples representing the positions of all enemies.
        score: An integer representing the player's current score.

    """
    def __init__(self,current_scene_name, starting_health):
        self.starting_health = starting_health
        self.current_health = starting_health
        # volume
        self.music_volume = 0.5
        self.sound_volume = 0.5
        # projectile

        self.score = 0
        self.in_menu = True

        self.current_scene_name = current_scene_name
        self.level_num = 0
