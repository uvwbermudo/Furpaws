from flaskr import create_app, socketio
from dotenv import load_dotenv  


load_dotenv('.env')

app = create_app()
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0',port='8080')

    