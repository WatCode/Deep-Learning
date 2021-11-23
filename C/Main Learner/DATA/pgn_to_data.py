import chess.pgn

pgn = open("Carlsen.pgn")
filew = open("CHESSVALIDATION.txt", "w")

to_write = ""

for i in range(3000):
    game = chess.pgn.read_game(pgn)
    board = game.board()
    headers = game.headers["Result"]

    mod = int(headers[0])
    count = 0
    allmovestr = ""

    if i >= 2950:
        for move in game.mainline_moves():
            score = "0.9"

            if mod != count%2:
                score = "1"
            if "/" in headers:
                score = "0.5"

            movestr = str(move)

            x1 = str(ord(movestr[0])-96)
            y1 = str(int(movestr[1]))
            x2 = str(ord(movestr[2])-96)
            y2 = str(int(movestr[3]))

            allmovestr += x1 + "," + y1 + "," + x2 + "," + y2 + ","

            to_write += allmovestr + ("0,0,0,0,"*(399-count))[:-1] + ":" + score + "\n"

            count += 1

            board.push(move)

filew.write(to_write[:-1])
filew.close()