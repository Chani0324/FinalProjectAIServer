import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_restful import Api
from pathlib import Path
import flask
import base64
import cv2
import requests
import json
from data_list import load_img_list

### 원본 코드 ###
# app = Flask(__name__)

# # Reading img features
# fe = FeatureExtractor()
# features = []
# img_paths = []

# for feature_path in Path("./static/feature").glob("*.npy"):
#     features.append(np.load(feature_path))
#     img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
# features = np.array(features)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         file = request.files["query_img"]
        
#         # Save query img
#         img = Image.open(file.stream) # PIL image
#         uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
#         img.save(uploaded_img_path)
        
#         # Run Search
#         query = fe.extract(img)
#         dists = np.linalg.norm(features - query, axis=1) # L2 distance to the features
#         ids = np.argsort(dists)[:30]    # Top 30 results
#         scores = [(dists[id], img_paths[id]) for id in ids]
        
#         print(scores)
        
#         return render_template("index.html", query_path=uploaded_img_path, scores=scores)
#     else:
#         return render_template("index.html")

# if __name__=="__main__":
#     app.run()
    
### 여기까지 ###







app = Flask(__name__)
CORS(app, supports_credentials=True) # 다른 포트번호에 대한 보안 제거
api = Api(app)

# Reading img features
fe = FeatureExtractor()

features, df_img = load_img_list()

@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        file = request.get_json()["file"].split(",")[1]
        
        decoded_file = base64.b64decode(file)
        
        img_np = np.fromstring(decoded_file, dtype=np.uint8)
        
        img = cv2.imdecode(img_np, flags=cv2.IMREAD_COLOR)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        img = Image.fromarray(img.astype('uint8'))
        
        img.show() 
        
    #     # Run Search
        query = fe.extract(img)
        # dists = np.linalg.norm(features - query, axis=1) # L2 distance to the features
        dists = np.linalg.norm(features - query, axis=1) # L2 distance to the features
        print("================")
        print(features / query)
        print("================")
        print(features - query)
        ids = np.argsort(dists)[:5]    # Top 30 results
        # scores = {(dists[id], df_img.iloc[id]['path_url'], df_img.iloc[id]['url']) for id in ids}
        result_img_path = [df_img.iloc[id]['path_url'] for id in ids]
        result_img_link = [df_img.iloc[id]['url'] for id in ids]
        result_img_score = [dists[id] for id in ids]
        
        # new_path = [str(img_paths[id]).replace("\\", "/") for id in ids]
        
        return flask.jsonify({"result_img_path":str(result_img_path),
                              "result_img_link":str(result_img_link),
                              "result_img_score":str(result_img_score)})
    else:
        return flask.jsonify({"result":"잘못된 요청입니다."})
    

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

if __name__=="__main__":
    # app.run(host=0.0.0.0, port=5000) 모든 호스트로 접속 가능.
    app.run()   
