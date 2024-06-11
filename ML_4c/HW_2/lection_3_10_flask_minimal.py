from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!1'

@app.route('/one')
def goodbye_world():
    return 'World, GoodBye!'
  
if __name__ == '__main__':
    app.run()