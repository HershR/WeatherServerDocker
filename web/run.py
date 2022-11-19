from flaskr import create_app

if __name__ == "__main__":
    app = create_app()
    # alter as seen fit
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
