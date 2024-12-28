from sys import path

from flask import Flask, render_template, request
from flask_socketio import SocketIO
from psutil import net_connections


def run() -> None:
    port = 1090

    if port <= 1024:
        raise ValueError()
    if any((connection.status == "LISTEN" and connection.laddr.port == port) for connection in net_connections()):
        raise #PortOccupancyError()

    app = Flask(
        __name__,
        template_folder="./templates" if __name__ == "__main__" else ".server/templates",
        static_folder="./static" if __name__ == "__main__" else ".server/static"
    )
    app.config['SECRET_KEY'] = 'idunnowuttodo'
    socketio = SocketIO(app)

    @app.route('/')
    def index():
        return render_template('main.html')

    @socketio.on('connect')
    def connect():
        client_ip = request.remote_addr
        print(f"Connected! ip->%s" % (request.remote_addr, ))

    @socketio.on("player_dot")
    def player_dot(data: dict) -> bool:
        try: socketio.emit("player_dot", data)
        except Exception: return False
        return True

    # @socketio.on("sync_map")
    # def sync_map(data: dict) -> bool:
    #     try: socketio.emit("sync_map", data, room=data.get("sid"))
    #     except Exception: return False
    #     return True

    @socketio.on("sync_map_request")
    def sync_map_request() -> bool:
        try: socketio.emit(
            "sync_map_request",
            callback=lambda data: socketio.emit("sync_map", data, room=request.sid)
        )
        except Exception: return False
        return True



    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True, debug=True, use_reloader=False)


def main() -> None:
    run()

if __name__ == '__main__':
    main()