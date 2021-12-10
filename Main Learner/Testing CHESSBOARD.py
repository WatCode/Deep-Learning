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
    
    input_values = [Decimal(i) for i in (state.replace("\n", " ").replace(" ", ",").replace(".", "0").replace("p", "0.1").replace("P", "-0.1").replace("n", "0.2").replace("N", "-0.2").replace("b", "0.3").replace("B", "-0.3").replace("r", "0.4").replace("R", "-0.4").replace("q", "0.5").replace("Q", "-0.5").replace("k", "0.6").replace("K", "-0.6")).split(",")]
    
    Data0.load([], [], [], [], input_values, [])
    
    if i%2 == 0:
        Model0.test(Data0)
        output_values = Model0.output_values
    else:
        Model1.test(Data0)
        output_values = Model1.output_values

    output_values = [str(round(i*Decimal(10))/10) for i in output_values]
    
    part_output_values = []
    
    for i in range(int(len(output_values)/8)):
        part_output_values.append(" ".join(output_values[i*8:i*8+8]).replace("0.0", ".").replace("-0.1", "P").replace("0.1", "p").replace("-0.2", "N").replace("0.2", "n").replace("-0.3", "B").replace("0.3", "b").replace("-0.4", "R").replace("0.4", "r").replace("-0.5", "Q").replace("0.5", "q").replace("-0.6", "K").replace("0.6", "k"))
    
    state = "\n".join(part_output_values)