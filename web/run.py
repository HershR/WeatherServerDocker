from flaskr import create_app

if __name__ == "__main__":
    app = create_app()
    # alter as seen fit
    app.run(host='localhost', port=5000, debug=True)
