from flask import Flask, render_template, request
# from flask_bootstrap import Bootstrap - does not want to work :( 
# TO DO: deal with that later 
import RPi.GPIO as GPIO
import curses
import time
from datetime import datetime

app = Flask(__name__)
# bootstrap = Bootstrap(app)


GPIO.setmode(GPIO.BOARD)

# rover setup
list_F = [11, 15, 12, 18]
list_B = [40, 13, 16, 38]
list_L = [11, 15, 16, 38]
list_R = [40, 13, 12, 18]

GPIO.setup(list_F, GPIO.OUT)
GPIO.setup(list_B, GPIO.OUT)
GPIO.setup(list_L, GPIO.OUT)
GPIO.setup(list_R, GPIO.OUT)

# PIR setup
GPIO.setup(7, GPIO.IN)

history = [None]


@app.route('/catwatcher')
def catwatcher():
    template_data = {
            'title': 'catwatcher',
            }

    return render_template('main.html', **template_data)


@app.route('/rover_camera')
def rover_camera():
    stdscr = curses.initscr()	# curses initialization
    curses.noecho()				# to turn-off echoing of keybord to screen
    curses.cbreak()				# no waiting key response
    stdscr.keypad(True)			# spciecial values for cursor keys - keypad mode
   	# halfdelay(3)
    
    while True:
        c = stdscr.getch()

        if c == ord('q'):
            break

        elif c == ord('s'):
            GPIO.output(list_F, GPIO.LOW)
            GPIO.output(list_B, GPIO.LOW)
            GPIO.output(list_L, GPIO.LOW)
            GPIO.output(list_R, GPIO.LOW)

        elif c == curses.KEY_UP:
            GPIO.output(list_F, GPIO.HIGH)

        elif c == curses.KEY_DOWN:
            GPIO.output(list_B, GPIO.HIGH)

        elif c == curses.KEY_LEFT:
            GPIO.output(list_L, GPIO.HIGH)

        elif c == curses.KEY_RIGHT:
            GPIO.output(list_R, GPIO.HIGH)

		# return 'I am cathing the cat'


@app.route('/motion_detector')
def motion_detector():
    while True:
        
        if GPIO.input(7) == 1:
            msg = 'Last movement was detected on '
            date_time = str(datetime.now().strftime('%d-%m-%Y %H:%M'))
            history.append(date_time)

        else:
            msg = 'No movement detected. The last one detected during this conection was:'
        
        template_data = {
            'title': 'motion detector',
            'message': msg,
            'history': history
            }

        return render_template('motion_detector.html', **template_data)


@app.route('/check_history')
def check_history():
    template_data ={
        'title': 'checking history',
        'history': history
        }
    
    return render_template('check.html', **template_data)


@app.route('/delete_history', methods=['GET', 'POST'])
def delete_history():
    global history
    if request.method == 'GET':
        template_data ={
        'title': 'deleting history',
        'history': history
        }
    
        return render_template('delete.html', **template_data)
        
    elif request.method == 'POST':
        if request.form['delete_history'] == 'deleting':
            del history[:]

        template_data ={
        'title': 'deleting confirmation',
        'message': 'History is deleted'
        }
    
        return render_template('delete_confirm.html', **template_data)


if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)
   
    
    curses.nocbreak()   		# to leave halfdelay mode
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

    GPIO.cleanup()

