from feature_extractor import FeatureExtractor
import pymysql as pysql
from pathlib import Path

import numpy as np
import pandas as pd


# Reading img features
def load_img_list():
    
    # 추출된 특징들을 pandas에 담아서 정리
    features = []
    # img_paths = []
    # url_path = []
    # sorted_img_path = sorted(Path("./static/img"))
    
    for feature_path in sorted(Path("./static/feature_top").glob("*.npy")):
        features.append(np.load(feature_path))
        # img_paths.append(sorted_img_path / (feature_path.stem + ".jpg"))
    features = np.array(features)

    
    # DB에서 table 가져와서 pandas에 담기
    sql = "select * from test_imgs"
    
    conn = pysql.connect(host="db-3team-project.ckirsmdzwudh.ap-northeast-2.rds.amazonaws.com",
                        port=3306,
                        user="admin",
                        password="rladbdbsDL!",
                        db="security",
                        charset="utf8")
    
    result = pd.read_sql_query(sql, conn)    

    result['path_url'] = "https://image-storage01.s3.ap-northeast-2.amazonaws.com/" + result['name']

    result = result.sort_values('name')

    return features, result
    
load_img_list()
