from wannaWatch import create_app, db

if __name__ == "__main__":
    app = create_app()
    app.app_context().push()
    with app.app_context():
        db.create_all()
    app.run(debug=True)