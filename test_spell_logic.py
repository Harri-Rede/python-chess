"""
Unit tests for Spell Chess game logic.

Run with:
    pytest test_spell_logic.py -v

These tests verify the Spell Chess rules described in SPELL_CHESS_RULES.md.
Each test creates a fresh SpellChessGame, sets up a position, performs an
action, and checks that the result matches the specification.
"""

import chess
from spell_logic import SpellChessGame, squares_in_3x3, squares_in_jump_range


# ------------------------------------------------------------------ #
#  Demo tests — provided to students as examples                      #
# ------------------------------------------------------------------ #

class TestFreezeTarget:
    """Casting Freeze should mark the opponent's color as frozen."""

    def test_freeze_affects_opponent_not_caster(self):
        game = SpellChessGame()
        # White casts freeze
        game.cast_freeze(chess.E5)
        # The frozen color should be Black (the opponent), not White
        assert game.freeze_effect_color == chess.BLACK


class TestNewGameResetsBoard:
    """Calling new_game() should bring the board back to the starting position."""

    def test_board_resets_after_moves(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.new_game()
        assert game.board.fen() == chess.STARTING_FEN


# ------------------------------------------------------------------ #
#  YOUR TESTS GO BELOW                                                #
#  Write tests that check the rules from SPELL_CHESS_RULES.md.        #
#  If a test fails, you've found a bug — document it!                 #
# ------------------------------------------------------------------ #

# https://python-chess.readthedocs.io/en/latest/core.html

class TestFreezeCasting:

    def test_freeze_any_square_center(self):
        for square in chess.SQUARES:
            game = SpellChessGame()
            success = game.cast_freeze(square)  # returns True if cast succeeded
            assert success is True
            # print(f"{chess.square_name(square)}: {success}")

class TestNewGameReset:

    def test_new_game_resets_freeze_charges(self):
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE] = 2
        game.freeze_remaining[chess.BLACK] = 1
        game.new_game() #resets the game
        #charge return to default values
        assert game.freeze_remaining[chess.WHITE] == 5
        assert game.freeze_remaining[chess.BLACK] == 5

    def test_new_game_resets_jump_charges(self):
        game = SpellChessGame()
        game.jump_remaining[chess.WHITE] = 1
        game.jump_remaining[chess.BLACK] = 0
        game.new_game()
        #charge return to default values
        assert game.jump_remaining[chess.WHITE] == 3
        assert game.jump_remaining[chess.BLACK] == 3

    def test_new_game_resets_all_spell_cooldowns(self):
        game = SpellChessGame()
        game.freeze_cooldown[chess.WHITE] = 2
        game.freeze_cooldown[chess.BLACK] = 2
        game.jump_cooldown[chess.WHITE] = 2
        game.jump_cooldown[chess.BLACK] = 2
        game.new_game()
        assert game.freeze_cooldown[chess.WHITE] == 0;
        assert game.freeze_cooldown[chess.BLACK] == 0;
        assert game.jump_cooldown[chess.WHITE] == 0;
        assert game.jump_cooldown[chess.BLACK] == 0;
        
    def test_freeze_includes_bordering_squares(self):
        for center in chess.SQUARES:
            # print(f"Test {chess.square_rank(center)} {chess.square_file(center)} {chess.square_name(center)}")
            square = squares_in_3x3(center)
            for s in square:
                dist = chess.square_distance(center, s)
                assert dist <= 1

    def test_freeze_includes_center(self):
        for square in chess.SQUARES:
            area = squares_in_3x3(square)
            # print(f"{chess.square_name(square)}")
            assert square in area
            
class TestKingJump:
    "The king cannot be selected for use with jump spell."

    def test_king_cannot_jump(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.E1, chess.E3) is False
        
class TestJumpRange:
    "Chebyshev distance 3 should be rejected."

    def test_over_chebyshev_range(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.B1, chess.B4) is False
