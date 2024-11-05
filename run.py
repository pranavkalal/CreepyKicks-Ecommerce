from sneakpeek import create_app, create_tables

if __name__ == '__main__':
    app = create_app()
    create_tables(app)  # Ensure this is called to set up your DB tables
    app.run(debug=True)
