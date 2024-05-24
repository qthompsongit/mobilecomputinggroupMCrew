from flask import Flask, request, jsonify
import subprocess
import pandas as pd
import sys
app = Flask(__name__)
#The code below runs a flask server to receive, predict on, and send back predictions on the data provided
@app.route('/', methods=['GET', 'POST'])
def run_script():
    data = request.json
    #print(str(request))
    #print(str(request.json))
    #print("TEXT:", jsonify(data))
    #print(data)
    #print(list(data.keys()))
    input_data = data['input']
    #print(input_data)
    #input_data =  sys.argv[1]

    # Run your Python script here (replace 'your_script.py' with your actual script)
    result = subprocess.run(['python', 'myrandforcheck.py', input_data], capture_output=True, text=True)
    print(result)
    # Get the output of the script
    output = result.stdout.strip()
    print(output)
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)