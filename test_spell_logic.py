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

class TestJumpInRange:
    "Diagonal, horizontal, and vertical, jumps should all be allowed if they are in range and empty destination squares."

    def test_one_diagonal_jump(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.A2, chess.B3) is True
    
    def test_two_diagonal_jump(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.A2, chess.C4) is True

    def test_one_vertical_jump(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.A2, chess.A3) is True
    
    def test_two_vertical_jump(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.A2, chess.A4) is True
    
    def test_one_horizontal_jump(self):
        game = SpellChessGame()
        # remove the piece one to the right of the source square for valid jump.
        game.board.remove_piece_at(chess.B2)
        assert game.cast_jump(chess.A2, chess.B2) is True
    
    def test_two_horizontal_jump(self):
        game = SpellChessGame()
        # remove the piece two to the right of the source square for valid jump.
        game.board.remove_piece_at(chess.C2)
        assert game.cast_jump(chess.A2, chess.C2) is True