from app import create_app
from app.extensions import db
from socketserver import TCPServer
from config_functions import get_programdata_path, get_db_path, add_cfg, edit_cfg

app_path = get_programdata_path("ProdDash")
cfg_file_path = app_path / "app_cfg.json"
app_path.mkdir(parents=True, exist_ok=True)
db_path = get_db_path(app_path)

add_cfg(cfg_file_path, {
    "db_uri": db_path,
    "port": 0
})

if __name__ == "__main__":
    app = create_app()

    # db
    with app.app_context():
        db.create_all()

    # get port
    with TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
        
    edit_cfg(cfg_file_path, { "port": free_port })

    app.run(debug=True, port=free_port, host="localhost")

# how to access port in js
# ./test/conn.js
