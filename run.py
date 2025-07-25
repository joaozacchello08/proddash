from app import create_app
from app.extensions import db

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True, host="localhost", port=8080)
