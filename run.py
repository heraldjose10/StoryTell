from blogApp import create_app, commands


app = create_app()
commands.register(app)
app.run()