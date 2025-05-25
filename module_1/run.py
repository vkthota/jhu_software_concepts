from PersonalWebsite import create_app

app = create_app()

if __name__ == '__main__':
    # You can configure the port and debug settings here
    # These match your current command: --port 8000 --debug
    app.run(host='0.0.0.0', port=8000, debug=True)