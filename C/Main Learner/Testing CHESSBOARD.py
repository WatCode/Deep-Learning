from DeepLearner import *
import chess.pgn

model_name0 = input("Model name 0: ")
model_name1 = input("Model name 1: ")

Model0 = Model()
Model0.load(model_name0)

Model1 = Model()
Model1.load(model_name1)

Data0 = Data(Model0.input_count)

game = chess.pgn.Game()

board = game.board()

state = str(board)

for i in range(5):
    print(state)
    
    input_values = [Decimal(i) for i in (state.replace("\n", " ").replace(" ", ",").replace(".", "0").replace("p", "0.2").replace("P", "-0.2").replace("n", "0.4").replace("N", "-0.4").replace("b", "0.6").replace("B", "-0.6").replace("r", "0.8").replace("R", "-0.8").replace("q", "1.0").replace("Q", "-1.0").replace("k", "1.2").replace("K", "-1.2")).split(",")]
    
    Data0.load([], [], [], [], input_values, [])
    
    if i%2 == 0:
        Model0.test(Data0)
        output_values = Model0.output_values
    else:
        Model1.test(Data0)
        output_values = Model1.output_values

    output_values = [str(round(i*Decimal(5))/5) for i in output_values]
    
    part_output_values = []
    
    for i in range(int(len(output_values)/8)):
        part_output_values.append(" ".join(output_values[i*8:i*8+8]).replace("0.0", ".").replace("-0.2", "P").replace("0.2", "p").replace("-0.4", "N").replace("0.4", "n").replace("-0.6", "B").replace("0.6", "b").replace("-0.8", "R").replace("0.8", "r").replace("-1.0", "Q").replace("1.0", "q").replace("-1.2", "K").replace("1.2", "k"))
    
    state = "\n".join(part_output_values)