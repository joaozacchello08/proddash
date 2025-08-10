from app import create_app
from app.extensions import db
from socketserver import TCPServer
import os

if __name__ == "__main__":
    app = create_app()

    # db
    with app.app_context():
        db.create_all()

    # set a valid port
    with TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
        os.environ["PRODDASH_BACKEND_LOCALHOST_PORT"] = str(free_port)
    
    #int(os.environ["PRODDASH_BACKEND_LOCALHOST_PORT"]) 
    port = 6769 

    app.run(debug=True, port=port, host="localhost")
