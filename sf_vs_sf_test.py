import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("stockfish")

board = chess.Board()
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=11))
    board.push(result.move)
    print(str(board.peek()))

engine.quit()
