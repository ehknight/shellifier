import os
from flask import Flask, render_template, request
from ardour import main as shelly

DEBUG = True
app = Flask(__name__)

shellified=""""""

@app.route('/')
def index():
    return render_template('index.html', shellified = shellified)

@app.route('/stupid.css')
def stupid():
    return render_template('stupid.css')

@app.route('/upload', methods=['POST'])
def upload():
    preshellified = request.form['to']
    reps = int(request.form['multiplier'])
    print(reps)
    if 'adv' in request.form:
        advanced=True
    else:
        advanced=False
    if 'linebreaks' in request.form:
        linebreaks=True
    else:
        linebreaks=False
    return render_template('index.html', shellified=shelly(
                           preshellified, not advanced, linebreaks, reps))

if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port, debug = DEBUG)
