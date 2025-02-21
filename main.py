from module_30_ci_linters.homework.hw1.src.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8080)
