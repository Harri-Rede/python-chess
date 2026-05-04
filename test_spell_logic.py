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

class TestJumpCannotObtainCheckmatePosition:
    "The jump spell cannot be used to obtain a checkmate position at the destination square"

    def test_jump_cannot_obtain_checkmate_position(self):
        game = SpellChessGame()
        # set up the board for checkmate position prior to jump, then jump
        game.board.clear()
        game.board.set_piece_at(chess.H8, chess.Piece(chess.KING, chess.BLACK))
        game.board.set_piece_at(chess.A1, chess.Piece(chess.KING, chess.WHITE))
        game.board.set_piece_at(chess.H7, chess.Piece(chess.PAWN, chess.BLACK))
        game.board.set_piece_at(chess.G1, chess.Piece(chess.ROOK, chess.WHITE))
        game.board.set_piece_at(chess.F7, chess.Piece(chess.QUEEN, chess.WHITE))
        # ensure game state is currently NOT in check or checkmate
        assert game.board.is_check() is False
        assert game.board.is_checkmate() is False
        # then jump, should reject
        assert game.cast_jump(chess.F7, chess.G8) is False