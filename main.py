from mod_30.src.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8080)
