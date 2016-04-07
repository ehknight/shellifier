from flask import Flask, render_template, request
from ardour import main as shelly

app = Flask(__name__)

shellified=""""""

@app.route('/')
def index():
    return render_template('index.html', shellified = shellified)

@app.route('/upload', methods=['POST'])
def upload():
    preshellified = request.form['to']
    if 'adv' in request.form:
        advanced=True
    else:
        advanced=False
    return render_template('index.html', shellified=shelly(preshellified, not advanced))

if __name__=='__main__':
    app.run(host='0.0.0.0', port = 80)

