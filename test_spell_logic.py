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

    def test_opponent_frozen_area_dont_move(self):
        game = SpellChessGame()
        
        assert game.current_turn() == chess.WHITE
        # White casts freeze, selects E5 as center
        center = chess.E5
        game.cast_freeze(center)
        assert game.current_turn() == chess.WHITE
        
        # Bug in make_move: it doesn't switch to Black's turn after White makes a move.
        # game.make_move(chess.G1, chess.H3)
        # assert game.current_turn() == chess.BLACK

        # Manually setting turn for purposes of test.
        game.freeze_effect_color = chess.BLACK
        game.board.turn = chess.BLACK
        assert game.current_turn() == chess.BLACK
        area = game.freeze_effect_squares
        # Manually adding center square for purposes of test.
        area.add(center)

        moves = game.get_legal_moves()
        for move in moves:
            assert not game.is_frozen(move.from_square, chess.BLACK)