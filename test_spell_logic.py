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

class TestFreezeEffect:

    def test_frozen_check_block_no_select(self):
        game = SpellChessGame()
        game.board.clear()
        
        # https://www.chess.com/terms/check-chess
        game.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
        game.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
        game.board.set_piece_at(chess.B5, chess.Piece(chess.BISHOP, chess.WHITE))
        game.board.turn = chess.BLACK
        assert game.board.is_check() is True

        # Freeze bishop
        game.cast_freeze(chess.B5)
        game.freeze_effect_squares.add(chess.B5)  # Dependent on squares_in_3x3 - bug
        game.freeze_effect_color = chess.WHITE

        assert game.is_frozen(chess.B5, chess.WHITE) is True
        assert game.board.is_check() is True