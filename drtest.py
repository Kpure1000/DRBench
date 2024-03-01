import cv2
import numpy as np
import os
from umap import UMAP
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import mplcursors

# 加载图像数据
data_dir = 'static/multiple_symbols_dataset'
images = []
draw_images = []
image_files = []
for file_name in os.listdir(data_dir):
    if file_name.endswith('.jpg'):
        file_path = os.path.join(data_dir, file_name)
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)  # 读取为灰度图像
        images.append(image.flatten())  # 将图像展平并添加到列表中
        draw_images.append(image)  # 将图像展平并添加到列表中
        image_files.append(file_name)  # 记录图像文件名

# 转换图像数据为 numpy 数组
data = np.array(images)

# 使用TSNE进行降维
tsne = TSNE(n_components=2,perplexity=50)  # 指定降维到二维
embedded_data = tsne.fit_transform(data)

# 使用UMAP进行降维
# umap = UMAP(n_components=2)  # 指定降维到二维
# embedded_data = umap.fit_transform(data)

# 使用PCA进行降维
# pca = PCA(n_components=2)  # 指定降维到二维
# embedded_data = pca.fit_transform(data)

csv_file_path = 'static/multiple_symbols_dataset/multiple_symbols_dataset.csv'
with open(csv_file_path, 'w') as csv_file:
    # 写入 CSV 文件的列名
    csv_file.write("x,y,image_file\n")
    
    # 写入每个样本的降维结果和对应的原始图像路径
    for i, (x, y) in enumerate(embedded_data):
        line = f"{x},{y},{image_files[i]}\n"
        csv_file.write(line)


# 可视化降维后的数据
# plt.scatter(embedded_data[:, 0], embedded_data[:, 1], marker='.', color='b')
# plt.title('DR of multiple_symbols_dataset')
# plt.xlabel('D1')
# plt.ylabel('D2')

# 创建图形和子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# 散点图显示降维后的数据
scatter = ax1.scatter(embedded_data[:, 0], embedded_data[:, 1], marker='.', color='b')
ax1.set_title('Visualization of Image Data')
ax1.set_xlabel('D1')
ax1.set_ylabel('D2')

# 在图中显示缩略图
def on_hover(sel):
    index = sel.index
    if sel.artist == scatter:
        image = draw_images[index]
        ax2.imshow(image, cmap='gray')
        ax2.set_title(f'Preview of Image {index}')
        ax2.axis('off')  # 关闭坐标轴
        plt.draw()

mplcursors.cursor(scatter).connect("add", on_hover)

plt.tight_layout()
plt.show()
