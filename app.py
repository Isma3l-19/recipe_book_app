from config import app, db
import routes

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
