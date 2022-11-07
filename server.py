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
features = []
img_paths = []

for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
features = np.array(features)

@app.route("/upload", methods=["POST"])
def index():
    # if request.method == "POST":
        # return flask.jsonify({"result":"...."})
        # img = None
        # file = request.get_json()
        # print(file)
        file = request.get_json()["file"].split(",")[1]
        print(f'file : {file}')
        
        decoded_file = base64.b64decode(file)
        
        img_np = np.fromstring(decoded_file, dtype=np.uint8)
        
        img = cv2.imdecode(img_np, flags=cv2.IMREAD_COLOR)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        img = Image.fromarray(img.astype('uint8'))
        
        img.show() 
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        # img = None
    #     # Save query img
    #     img = Image.open(decoded_file.stream) # PIL image
    #     uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename
    #     img.save(uploaded_img_path)
        
    #     # Run Search
    #     query = fe.extract(img)
    #     dists = np.linalg.norm(features - query, axis=1) # L2 distance to the features
    #     ids = np.argsort(dists)[:30]    # Top 30 results
    #     scores = [(dists[id], img_paths[id]) for id in ids]
        
    #     print(scores)
        
        # return render_template("index.html", query_path=uploaded_img_path, scores=scores)
    # else:
    #     return render_template("index.html")
    
        return flask.jsonify({"result":"...."})

if __name__=="__main__":
    app.run()







# app = Flask(__name__)
# CORS(app, supports_credentials=True) # 다른 포트번호에 대한 보안 제거
# api = Api(app)

# # Reading img features
# fe = FeatureExtractor()
# features_top = []
# img_paths_top = []

# features_bottom = []
# img_paths_bottom = []

# for feature_path in Path("./static/feature_top").glob("*.npy"):
#     features_top.append(np.load(feature_path))
#     img_paths_top.append(Path("./static/img_top") / (feature_path.stem + ".jpg"))

# for feature_path in Path("./static/feature_bottom").glob("*.npy"):
#     features_bottom.append(np.load(feature_path))
#     img_paths_bottom.append(Path("./static/img_bottom") / (feature_path.stem + ".jpg"))
    
# features_top = np.array(features_top)
# features_bottom = np.array(features_bottom)

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