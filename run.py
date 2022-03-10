from blogApp import create_app, commands


app = create_app()
commands.register(app)

if __name__ == '__main__':
  app.run()