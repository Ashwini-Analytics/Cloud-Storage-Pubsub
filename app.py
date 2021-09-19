import os
# imported GetDataToPub.py
import GetDataToPub
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    target = os.environ.get('TARGET', 'World')
    #once you hit the api, the GetDataToPub.py will be called.
    GetDataToPub.getAndPublish()
    return 'Successfully uploaded to GCS {}!\n'.format(target)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
