import chess
import chess.svg
from IPython.display import SVG, display
import time

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        eval = evaluate_board(board)
        print(eval, end="\r")  # Print the current evaluation on the same line
        return eval

    if maximizing_player:
        max_eval = float('-inf')
        legal_moves = list(board.legal_moves)  # Convert legal_moves to a list
        for move in legal_moves:
            board.push(move)
            if move == legal_moves[0]:
                eval = minimax(board, depth - 1, alpha, beta, False)
            else:
                eval = minimax(board, depth - 1, alpha, alpha + 1, False)
                if eval > alpha:
                    eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        legal_moves = list(board.legal_moves)  # Convert legal_moves to a list
        for move in legal_moves:
            board.push(move)
            if move == legal_moves[0]:
                eval = minimax(board, depth - 1, alpha, beta, True)
            else:
                eval = minimax(board, depth - 1, beta - 1, beta, True)
                if eval < beta:
                    eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval



def get_best_move(board, depth):
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    start_time = time.time()
    while time.time() - start_time < 1:  # Run for 1 second
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
                alpha = max_eval - 1  # Set new aspiration window
            if eval >= beta:
                break
    print("Current best evaluation:", max_eval)  # Print the current best evaluation
    return best_move



def display_board(board):
    svg = chess.svg.board(board=board, size=300)
    display(SVG(svg))

def play_chess():
    board = chess.Board()
    print('\n')
    print(r"""                                        
  ______                    __                    __     __                   ________ __          __       
 /      \                  /  |                  /  |   /  |                 /        /  |        /  |      
/$$$$$$  | _______  ______ $$/  ______  ______  _$$ |_  $$/  ______  _______ $$$$$$$$/$$/  _______$$ |____  
$$ |__$$ |/       |/      \/  |/      \/      \/ $$   | /  |/      \/       \$$ |__   /  |/       $$      \ 
$$    $$ /$$$$$$$//$$$$$$  $$ /$$$$$$  $$$$$$  $$$$$$/  $$ /$$$$$$  $$$$$$$  $$    |  $$ /$$$$$$$/$$$$$$$  |
$$$$$$$$ $$      \$$ |  $$ $$ $$ |  $$//    $$ | $$ | __$$ $$ |  $$ $$ |  $$ $$$$$/   $$ $$      \$$ |  $$ |
$$ |  $$ |$$$$$$  $$ |__$$ $$ $$ |    /$$$$$$$ | $$ |/  $$ $$ \__$$ $$ |  $$ $$ |     $$ |$$$$$$  $$ |  $$ |
$$ |  $$ /     $$/$$    $$/$$ $$ |    $$    $$ | $$  $$/$$ $$    $$/$$ |  $$ $$ |     $$ /     $$/$$ |  $$ |
$$/   $$/$$$$$$$/ $$$$$$$/ $$/$$/      $$$$$$$/   $$$$/ $$/ $$$$$$/ $$/   $$/$$/      $$/$$$$$$$/ $$/   $$/ 
                  $$ |                                                                                      
                  $$ |                V1                                                                      
                  $$/                   
                                                                                                                                          
[.] MINIMAX [DEPTH 4]  
[.] ALPHA-BETA PRUNING
[.] PIECE SQUARE TABLES
[.] PESTO'S EVALUATION FUNCTION
[.] ASPIRATION WINDOW
[.] PRINCIPLE VARIATION SEARCH

        """)
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
            move = get_best_move(board, depth=4)
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

play_chess()
