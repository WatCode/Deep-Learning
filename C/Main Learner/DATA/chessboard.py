import chess.pgn

pgn = open("CHESSBOARDRAW.pgn")

game_list = []

while True:
    game = chess.pgn.read_game(pgn)
    
    if not game:
        break

    game_list.append(game)

pgn.close()

to_write_lines = []

for game in game_list[:10]:
    board = game.board()
    
    prev_state = str(board).replace("\n", " ").replace(" ", ",").replace(".", "0").replace("p", "0.2").replace("P", "-0.2").replace("n", "0.4").replace("N", "-0.4").replace("b", "0.6").replace("B", "-0.6").replace("r", "0.8").replace("R", "-0.8").replace("q", "1.0").replace("Q", "-1.0").replace("k", "1.2").replace("K", "-1.2")

    for move in game.mainline_moves():
        board.push(move)
        
        current_state = str(board).replace("\n", " ").replace(" ", ",").replace(".", "0").replace("p", "0.2").replace("P", "-0.2").replace("n", "0.4").replace("N", "-0.4").replace("b", "0.6").replace("B", "-0.6").replace("r", "0.8").replace("R", "-0.8").replace("q", "1.0").replace("Q", "-1.0").replace("k", "1.2").replace("K", "-1.2")
        
        to_write_lines.append(prev_state + ":" + current_state)
        
        prev_state = current_state

to_write_train = ""
to_write_validate = ""
to_write_test = ""

for i in range(len(to_write_lines)):
    if i%2 == 0:
        to_write_train += to_write_lines[i] + "\n"
    else:
        to_write_validate += to_write_lines[i] + "\n"
    to_write_test += to_write_lines[i] + "\n"

filew = open("CHESSBOARDTRAIN.txt", "w")
filew.write(to_write_train[:-1])
filew.close()

filew = open("CHESSBOARDVALIDATE.txt", "w")
filew.write(to_write_validate[:-1])
filew.close()

filew = open("CHESSBOARDTEST.txt", "w")
filew.write(to_write_test[:-1])
filew.close()