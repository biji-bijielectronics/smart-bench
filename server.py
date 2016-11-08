# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = 'gevent'

import time
from flask import Flask, render_template
import socketio

import redis
sio = socketio.Server(logger=True, async_mode=async_mode)

app = Flask(__name__)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)
app.config['SECRET_KEY'] = 'secret!'
thread = None
r = redis.Redis()

pubsub = r.pubsub()
pubsub.subscribe(['adc'])


    

def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        count = 0

        item1 = pubsub.get_message()
        item2 = pubsub.get_message()
        if item1 is not None:
            count += 1
            msg = str(item1['data'])
            print "sending: " + msg
            sio.emit('my response', {'data': msg},
                    namespace='/test')
        if item2 is not None:
            msgc = str(item2['data'])
            print "sending: " + msgc
            sio.emit('my responsec', {'data': msgc},
                     namespace='/test')
        sio.sleep(0.01)            


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return render_template('index.html')


@sio.on('my event', namespace='/test')
def test_message(sid, message):
    sio.emit('my response', {'data': message['data']}, room=sid,
             namespace='/test')
			 
@sio.on('my eventc', namespace='/test')			 
def test_message(sid, message):
	sio.emit('my responsec', {'data': message['data']}, room=sid,
             namespace='/test')





if __name__ == '__main__':
    
    # if sio.async_mode == 'threading':
    #     # deploy with Werkzeug
    #     app.run(threaded=True)
    # elif sio.async_mode == 'eventlet':
    #     # deploy with eventlet
    #     import eventlet
    #     import eventlet.wsgi
    #     eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    # elif sio.async_mode == 'gevent':
        # deploy with gevent
        from gevent import pywsgi
        try:
            from geventwebsocket.handler import WebSocketHandler
            websocket = True
        except ImportError:
            websocket = False
        if websocket:
            pywsgi.WSGIServer(('', 5000), app,
                              handler_class=WebSocketHandler).serve_forever()
        else:
            pywsgi.WSGIServer(('', 5000), app).serve_forever()
    # elif sio.async_mode == 'gevent_uwsgi':
    #     print('Start the application through the uwsgi server. Example:')
    #     print('uwsgi --http :5000 --gevent 1000 --http-websockets --master '
    #           '--wsgi-file app.py --callable app')
    # else:
    #     print('Unknown async_mode: ' + sio.async_mode)