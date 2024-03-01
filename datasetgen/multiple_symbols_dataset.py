import cv2
import numpy as np
import random
from umap import UMAP
import os
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from generate import *

# 随机生成符号并模拟手写效果
def generate_symbols(image, canvas_size, num_symbols):
    
    font = cv2.FONT_HERSHEY_SIMPLEX  # 字体类型
    font_thickness = 1
    color = (0, 0, 0)  # 黑色
    
    has_contour = random.randint(0, 10)
    if has_contour < 6:
        symbol = random.choice(['O', 'F'])
        x = random.randint(2, 3)  # 随机位置
        y = random.randint(28, 29)  # 随机位置
        cv_img = cv2.UMat(image)
        image = cv2.putText(cv_img, symbol, (x, y), font, 1.3, color, font_thickness, cv2.LINE_AA)
    for _ in range(num_symbols):
        symbol = random.choice(['X', 'U'])
        x = random.randint(-5, canvas_size[0] - 18)  # 随机位置
        y = random.randint(20, canvas_size[1] - 5)  # 随机位置
        cv_img = cv2.UMat(image)
        image = cv2.putText(cv_img, symbol, (x, y), font, 0.8, color, font_thickness, cv2.LINE_AA)
    
    # image = cv2.UMat.get(image)
    
    # 添加高斯模糊
    kernel_size = np.random.choice([3, 5])  # 选择随机的卷积核大小
    image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    return image


def generate_dataset(num_samples, num_symbols_per_image, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    canvas_size = (32, 32, 3)  # 符号大小和通道数
    background_color = (255, 255, 255)  # 白色

    images = []
    draw_images = []
    image_files = []

    for i in range(num_samples):
        canvas = np.ones(canvas_size, dtype=np.uint8) * background_color
        canvas_with_symbols = generate_symbols(canvas, canvas_size, num_symbols_per_image)
        file_name = f"image_{i}.jpg"
        file_path = os.path.join(output_dir, file_name)
        cv2.imwrite(file_path, canvas_with_symbols)
        images.append(canvas_with_symbols.get().flatten())
        draw_images.append(canvas_with_symbols)  # 将图像展平并添加到列表中
        image_files.append(file_name)  # 记录图像文件名

    return np.array(images), draw_images, image_files


def generate_labels(data, groups_num):
    
    kmeans = KMeans(n_clusters=groups_num)
    kmeans.fit(data)
    # 获取聚类结果
    g = np.array(kmeans.labels_)

    return g


def embed_dataset(images):
    # 转换图像数据为 numpy 数组
    data = np.array(images)

    # 使用TSNE进行降维
    tsne = TSNE(n_components=2,perplexity=50)  # 指定降维到二维
    # embedded_data = tsne.fit_transform(data)

    # 使用UMAP进行降维
    umap = UMAP(n_components=2)  # 指定降维到二维
    embedded_data = umap.fit_transform(data)

    # 使用PCA进行降维
    pca = PCA(n_components=2)  # 指定降维到二维
    # embedded_data = pca.fit_transform(data)

    return embedded_data


if __name__ == "__main__":
    # 生成数据集
    num_samples = 300  # 样本数量
    num_symbols_per_image = 4  # 每张图叠加的符号数量
    output_dir = '../static/datasets/multiple_symbols_dataset'

    images, draw_images, image_files = generate_dataset(num_samples, num_symbols_per_image, output_dir)

    print("dataset generated")

    labels = generate_labels(data=images, groups_num=2)

    print("labels generated")

    embedded_data = embed_dataset(images)

    print("dataset embedded")

    csv_file_path = f'{output_dir}/multiple_symbols_dataset.csv'
    with open(csv_file_path, 'w') as csv_file:
        # 写入 CSV 文件的列名
        csv_file.write("x,y,g,image_file\n")
        
        # 写入每个样本的降维结果和对应的原始图像路径
        for i, (x, y) in enumerate(embedded_data):
            line = f"{x},{y},{labels[i]},{image_files[i]}\n"
            csv_file.write(line)

    gen = DatasetsManager('../static/datasets/datasets.json')
    gen.generate('multiple_symbols_dataset', 'multiple_symbols_dataset', DT_IMAGE, len(labels), images.shape[1])