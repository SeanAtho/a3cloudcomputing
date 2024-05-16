from app import create_app

app = create_app()

if __name__ == '__main__':
    # Ensure debug mode is disabled for production
    app.run()
