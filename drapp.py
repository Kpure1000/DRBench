from flask import Flask, render_template, jsonify, request
from datasetgen.generate import *


app = Flask(__name__)

# 设置静态文件目录
app.static_folder = 'static'  # 此处的'static'是你存放静态文件的文件夹名


@app.route('/')
def index():
    return render_template('index.html')


# 提供数据集列表
@app.route('/datasets', methods=['GET'])
def get_datasets():
    mng = DatasetsManager('static/datasets/datasets.json')
    data_name = [name for name in mng.load_datasets().keys()]
    return jsonify(data_name)


# 提供当前选中的数据集
@app.route('/selected_dataset', methods=['POST'])
def get_selected_dataset():
    selected_dataset = request.json.get('selected_dataset')
    # 从 datasets 中获取当前选中的数据集信息
    mng = DatasetsManager('static/datasets/datasets.json')
    datasets = mng.load_datasets()
    selected_info = datasets.get(selected_dataset, {})
    path = f'static/datasets/{selected_info["path"]}'
    file = f'{path}/{selected_dataset}.csv'
    return jsonify({
        "name": selected_dataset,
        "type": selected_info["type"],
        "dataset_path": path,
        "embedded_file": file,
        "description": f'Type: {"image" if selected_info["type"] == DT_IMAGE else "other"}, N_samples: {selected_info["n_samples"]}, N_dims: {selected_info["n_dims"]}'
    })


if __name__ == '__main__':
    app.run(debug=True)
