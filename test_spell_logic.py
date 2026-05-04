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
     

class TestJumpOpponentPiece:
    "Caster cannot select an opponents piece as the source square."

    def test_jump_source_cannot_be_opponent(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.A8, chess.A6) is False
        
class TestJumpFromEmpty:
    "Jumping from an empty source square should not be allowed."

    def test_jump_from_empty(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.A3, chess.A4) is False
        
class TestJumpDestinationEmpty:
    "The jump destination for any valid piece must be empty."

    def test_jump_on_own_piece(self):
        game = SpellChessGame()
        # white pawn jump on white pawn should reject
        assert game.cast_jump(chess.A2, chess.C2) is False

    def test_jump_on_opponent_piece(self):
        game = SpellChessGame()
        # set a black pawn within valid jumping distance of white pawn, and jump.
        game.board.set_piece_at(chess.A4, chess.Piece(chess.PAWN, chess.BLACK))
        assert game.cast_jump(chess.A2, chess.A4) is False
        
class TestFreezeEffect:

    def test_freeze_lasts_one_opp_turn(self):
        game = SpellChessGame()

        center = chess.E5
        game.cast_freeze(center)

        # Manually setting turn for purposes of test. Dependent on make_move.
        game.board.turn = chess.BLACK

        # Manually setting turn for purposes of test. Dependent on cast_freeze.
        game.freeze_effect_color = chess.BLACK
        assert game.freeze_effect_color == chess.BLACK
        game.freeze_effect_plies_left = 1
        assert game.freeze_effect_plies_left == 1
        area = game.freeze_effect_squares
        area.add(center)
        assert center in area

        assert game.current_turn() == chess.BLACK

        # Need to call after_move_pushed() to switch turns since make_move() has a bug
        move = game.prepare_move(chess.A1, chess.A2)
        game.board.push(move)
        game.after_move_pushed()
        
        assert game.freeze_effect_color is None
        assert len(game.freeze_effect_squares) == 0
        assert game.freeze_effect_plies_left == 0
        
    def test_freeze_affects_opponent_not_caster(self):
        game = SpellChessGame()
        # White casts freeze
        game.cast_freeze(chess.E5)
        
        # # The frozen color should be different from the caster's color
        assert game.freeze_effect_color != game.current_turn()
        
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

    def test_new_game_clears_freeze_effect(self):
        game = SpellChessGame()
        game.freeze_effect_color = chess.BLACK
        game.new_game()
        assert game.freeze_effect_color is None #after reset, should be not active
        
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

class TestJumpCooldown:

    def test_jump_castable_only_on_zero(self):

        game1 = SpellChessGame()
        game2 = SpellChessGame()
        
        game1.jump_cooldown[True] = 1
        game2.jump_cooldown[True] = 0

        failiure = game1.cast_jump(chess.A2, chess.A4)
        success = game2.cast_jump(chess.A2, chess.A4)

        assert (not failiure) & success