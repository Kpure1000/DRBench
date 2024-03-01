import json

DT_IMAGE = 0    # 图片类型数据
DT_OTHER = 1    # 其他类型数据


class DatasetsManager:
    def __init__(self, datasets_file) -> None:
        self.datasets_file = datasets_file

    def load_datasets(self):
        with open(self.datasets_file, 'r') as f:
            str = f.read()
            datasets = {}
            if str != "":
                datasets = json.loads(str)
        return datasets


    def generate(self, name, path, type, n_samples, n_dims):
        with open(self.datasets_file, 'r') as f:
            str = f.read()
            datasets = {}
            if str != "":
                datasets = json.loads(str)
        datasets[name] = {
            "path": path,
            "type": type,
            "n_samples": n_samples,
            "n_dims": n_dims
        }
        with open(self.datasets_file, 'w') as f:
            str = json.dumps(datasets, indent=4)
            f.write(str)


# if __name__ == '__main__':
    # gen = DatasetsManager('../static/datasets.json')
    # gen.generate('multiple_symbols_dataset', 'multiple_symbols_dataset', DT_IMAGE)
    # gen.generate('swissroll', 'swissroll', DT_OTHER)
