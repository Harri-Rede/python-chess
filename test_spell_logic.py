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
            
class TestSpellCooldown:

    def test_freeze_cast_decrement(self):
        game = SpellChessGame()
        before = game.freeze_remaining
        success = game.cast_freeze(chess.square(0, 0))
        after = game.freeze_remaining
        assert success == True
        assert (after[True] == (before[True] - 1) & (after[False] == before[False]))
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
class TestJumpOnOpponentKing:
    "Jump spell cannot be used to capture king."

    def test_jump_on_opponent_king(self):
        game = SpellChessGame()
        # set a white pawn within jump range of the black king, and jump
        game.board.set_piece_at(chess.E6, chess.Piece(chess.PAWN, chess.WHITE))
        assert game.cast_jump(chess.E6, chess.E8) is False
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
        
        # # The frozen color should be different from the caster's color
        assert game.freeze_effect_color != game.current_turn()

        game2 = SpellChessGame()
        game2.board.turn = chess.BLACK
        game2.cast_freeze(chess.E5)
        assert game2.freeze_effect_color != game2.current_turn()
        
    def test_freeze_no_moves(self):
        game = SpellChessGame()
        game.board.clear()
        
        game.board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
        game.board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
        game.board.set_piece_at(chess.B5, chess.Piece(chess.BISHOP, chess.BLACK))
        game.board.turn = chess.BLACK
        # print(game.get_legal_moves())

        # Freeze white
        game.cast_freeze(chess.E2)
        game.freeze_effect_color = chess.WHITE

        game.board.turn = chess.WHITE
        assert len(game.get_legal_moves()) == 0

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

class TestFreezeCooldown:

    def test_freeze_cooldown(self):
        game = SpellChessGame()
        start = game.freeze_cooldown[True]
        success = game.cast_freeze(chess.E5)
        end = game.freeze_cooldown[True]
        assert (start == 0) & success & (end == 3)
class TestJumpCooldown:

    def test_jump_castable_only_on_zero(self):

        game1 = SpellChessGame()
        game2 = SpellChessGame()
        
        game1.jump_cooldown[True] = 1
        game2.jump_cooldown[True] = 0

        failiure = game1.cast_jump(chess.A2, chess.A4)
        success = game2.cast_jump(chess.A2, chess.A4)

        assert (not failiure) & success
    def test_jump_cooldown_decrement(self):

        game1 = SpellChessGame()
        game2 = SpellChessGame()

        game1.jump_cooldown[True] = 1
        game2.jump_cooldown[True] = 0

        game1.on_turn_start()
        game2.on_turn_start()
        
        one = game1.jump_cooldown[True]
        two = game2.jump_cooldown[True]

        assert (one == 0) & (two == 0)

    def test_jump_cooldown(self):
        game = SpellChessGame()
        start = game.jump_cooldown[True]
        success = game.cast_jump(chess.A2, chess.A4)
        end = game.jump_cooldown[True]
        assert (start == 0) & success & (end == 2)
class TestFreezeCooldown:

    def test_freeze_castable_only_on_zero(self):
        game1 = SpellChessGame()
        game2 = SpellChessGame()
        game3 = SpellChessGame()

        game1.freeze_cooldown[True] = 2
        game2.freeze_cooldown[True] = 1
        game3.freeze_cooldown[True] = 0

        failiure1 = game1.cast_freeze(chess.E5)
        failiure2 = game2.cast_freeze(chess.E5)
        success = game3.cast_freeze(chess.E5)

        assert (not failiure1) & (not failiure2) & success
        three = game3.freeze_cooldown[True]

        assert (one == 1) & (two == 0) & (three == 0)
