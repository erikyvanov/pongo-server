import json
from flask import Flask, request
import socketio
from game.constansts import PADDLE_HEIGHT, PADDLE_SPEED, SCREEN_HEIGHT
from game.game import Game, Player

from flask_socketio import SocketIO, send, emit

game = Game()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('connect')
def connect():
    # Get the ID of the client to disconnect
    client_id = request.sid

    if game.isGameReady:
        # Force the client to disconnect
        socketio.disconnect(client_id)
        return

    player = None
    if not game.hasPlayerZero:
        player = Player(0, client_id)
    else:
        player = Player(1, client_id)

    game.players.append(player)
    data = {
        'player': player.numberOfPlayer,
        'score': player.score,
        'Y_possition': player.Y_possition,
    }
    json_data = json.dumps(data)
    emit('on_player_connected', json_data, broadcast=False)

    if game.isGameReady:
        emit('on_game_is_ready', True, broadcast=True)

    
@socketio.on('disconnect')
def test_disconnect():
    client_id = request.sid
    game.delete_player(client_id)

    print('Client disconnected')
    emit('on_player_disconnected', True, broadcast=True)


@socketio.on('on_player_move')
def handle_move(data):
    """
    data = {
        'player': 0,
        'isUp': True,
    }
    """
    response = json.loads(data)
    numberOfPlayer = response['player']
    isUp = response['isUp']
    paddle_y_possition = game.players[numberOfPlayer].Y_possition

    if isUp and paddle_y_possition > 0:
            paddle_y_possition -= PADDLE_SPEED
    if not isUp and paddle_y_possition < SCREEN_HEIGHT - PADDLE_HEIGHT:
        paddle_y_possition += PADDLE_SPEED

    game.players[numberOfPlayer].Y_possition = paddle_y_possition

    response = {
        'player': numberOfPlayer,
        'Y_possition': paddle_y_possition,
    }
    response_data = json.dumps(response)
    emit('on_player_possition_update', response_data, broadcast=True)

if __name__ == '__main__':
    print('Server is running')
    socketio.run(app)