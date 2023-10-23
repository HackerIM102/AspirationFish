# Fastest of all models currently
import chess
import time
from eval import Evaluation

# Global variables for move ordering
killer_moves = [[[None for _ in range(64)] for _ in range(64)] for _ in range(64)]
history_moves = [[0 for _ in range(64)] for _ in range(64)]

# Global variable for transposition table
transposition_table = {}

def minimax(board, depth, alpha, beta, maximizing_player):
    # Check transposition table for cached evaluation
    if board.fen() in transposition_table:
        return transposition_table[board.fen()]

    if depth == 0 or board.is_game_over():
        eval = evaluator.evaluate_board(board)
        transposition_table[board.fen()] = eval
        print(eval, end="\r")  # Print the current evaluation on the same line
        return eval

    if maximizing_player:
        max_eval = float('-inf')
        legal_moves = list(board.legal_moves)  # Convert legal_moves to a list

        # Sort moves based on move ordering heuristics
        legal_moves.sort(key=lambda move: history_moves[move.from_square][move.to_square], reverse=True)

        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        # Update killer moves and history moves
        if max_eval >= beta:
            killer_moves[depth][move.from_square][move.to_square] = move
        history_moves[move.from_square][move.to_square] += depth

        return max_eval
    else:
        min_eval = float('inf')
        legal_moves = list(board.legal_moves)  # Convert legal_moves to a list

        # Sort moves based on move ordering heuristics
        legal_moves.sort(key=lambda move: history_moves[move.from_square][move.to_square], reverse=True)

        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break

        # Update killer moves and history moves
        if min_eval <= alpha:
            killer_moves[depth][move.from_square][move.to_square] = move
        history_moves[move.from_square][move.to_square] += depth

        return min_eval

def get_best_move(board, depth, alpha, beta):
    best_move = None
    max_eval = float('-inf')
    start_time = time.time()
    while time.time() - start_time < 1:  # Run for 1 second
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
                alpha = max(alpha, eval)
            if eval >= beta:
                break

    # Reset killer moves and history moves
    killer_moves[depth] = [[None for _ in range(64)] for _ in range(64)]
    history_moves = [[0 for _ in range(64)] for _ in range(64)]

    print("Current best evaluation:", max_eval)  # Print the current best evaluation
    return best_move

def display_board(board):
    print(board)

def play_chess():
    board = chess.Board()
    while not board.is_game_over():
        display_board(board)
        if board.turn == chess.WHITE:
            print(" ")
            print(">>")
            move = input("Enter your move: ")
            try:
                move = board.parse_san(move)
                if move not in board.legal_moves:
                    raise ValueError
            except:
                print("Invalid move! Try again.")
                continue
        else:
            move = get_best_move(board, depth=4, alpha=float('-inf'), beta=float('inf'))
            print("AI's move:", move)
        board.push(move)

    display_board(board)
    result = board.result()
    if result == "1-0":
        print("White wins!")
    elif result == "0-1":
        print("Black wins!")
    else:
        print("It's a draw!")

# Create an instance of the Evaluation class
evaluator = Evaluation()

# Call the play_chess function to start the game
play_chess()
