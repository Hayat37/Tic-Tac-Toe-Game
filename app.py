from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global game state
board = [[" " for _ in range(3)] for _ in range(3)]
current_player = "X"

def check_winner(player):
    # rows and cols
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): return True
        if all(board[j][i] == player for j in range(3)): return True
    # diagonals
    if all(board[i][i] == player for i in range(3)): return True
    if all(board[i][2-i] == player for i in range(3)): return True
    return False

def board_full():
    return all(cell != " " for row in board for cell in row)

@app.route("/")
def index():
    return render_template("index.html", board=board, current_player=current_player)

@app.route("/move/<int:row>/<int:col>")
def move(row, col):
    global current_player, board

    if board[row][col] == " ":
        board[row][col] = current_player
        if check_winner(current_player):
            return render_template("index.html", board=board,
                                   message=f"Player {current_player} wins! 🎉",
                                   current_player=current_player)
        elif board_full():
            return render_template("index.html", board=board,
                                   message="It's a draw! 🤝",
                                   current_player=current_player)
        else:
            current_player = "O" if current_player == "X" else "X"

    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    global board, current_player
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)