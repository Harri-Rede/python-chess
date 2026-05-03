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

class TestOncePerTurn:

    def test_freeze_once_per_turn(self):
        # Checks if you can cast more than one freeze on a turn.
        game1 = SpellChessGame()
        success = game1.cast_freeze(chess.E5)
        failiure = game1.cast_freeze(chess.E5)
        assert success & (not failiure)

        # Checks if you can cast a freeze spell after moving.
        game2 = SpellChessGame()
        success = game2.make_move(chess.A2, chess.A4)
        failiure = game2.cast_freeze(chess.E5)
        assert success & (not failiure)
    
    def test_jump_once_per_turn(self):
        # Checks if you can cast more than one jump on a turn.
        game1 = SpellChessGame()
        success = game1.cast_jump(chess.A2, chess.A4)
        failiure = game1.cast_jump(chess.A4, chess.A5)
        assert success & (not failiure)

        # Checks if you can cast a jump spell after moving.
        game2 = SpellChessGame()
        success = game2.make_move(chess.A2, chess.A4)
        failiure = game2.cast_jump(chess.A4, chess.A5)
        assert success & (not failiure)