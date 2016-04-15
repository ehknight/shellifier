import os
from flask import Flask, render_template, request
from ardour import main as shelly
from itertools import groupby

DEBUG = True
app = Flask(__name__)

shellified=""""""

def removeRepeated(txt, remrep):
    #https://stackoverflow.com/questions/17238587/python-regular-expression-to-remove-repeated-words
    if remrep==True:
        return " ".join([k for k,v in groupby(txt.split())])
    else:
        return txt

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
    if 'remrep' in request.form:
        remrep=True
    else:
        remrep=False
    return render_template('index.html', shellified=removeRepeated(shelly(
                           preshellified, not advanced, linebreaks, reps), remrep))

if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port, debug = DEBUG)
