import csv
from flask import Flask, render_template, request
from io import StringIO
import time


ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)


def allowed_file(filename):
    ''' Checks filename of file import and only takes the allowed extension'''
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('import.html')

@app.route('/upload',methods=['POST'])
def upload():
    times = []
    file = request.files['file']

    csvf = StringIO(file.read().decode())
    reader = csv.DictReader(csvf, delimiter=',')
    for row in reader:
        train = {
            "trip" : row['Trip '],
            "scheduledTime" : time.strftime('%H:%M',time.localtime(int(row['ScheduledTime ']))),
            "origin" : row['Origin '],
            "destination" : row['Destination '],
            "lateness": row['Lateness '],
            "track" : row['Track '],
            "status" : row['Status'],
            "departureTime" : time.strftime('%H:%M',time.localtime(int(row['ScheduledTime ']) + int(row['Lateness ']))),
        }
        times.append(train)
    times = sorted(times,key=lambda k: k["departureTime"])
    return render_template('schedule.html',times=times)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
