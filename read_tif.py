import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt

def plot_tif(file_path):
    # 打开tif文件
    with rasterio.open(file_path) as src:
        # 读取栅格数据
        data = src.read(1)  # 读取第一波段

        # 获取栅格数据的元数据信息
        bounds = src.bounds
        title = os.path.basename(file_path)

        # 显示栅格图像
        plt.figure(figsize=(10, 8))
        plt.imshow(data, cmap='viridis', extent=[bounds.left, bounds.right, bounds.bottom, bounds.top])
        plt.colorbar(label='Pixel Value')
        plt.title(title)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()

def plot_all_tifs(source_dir):
    # 遍历源文件夹中的所有子文件夹和文件
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 检查文件是否以.tif结尾
            if file.lower().endswith('.tif'):
                file_path = os.path.join(root, file)
                print(f"Plotting {file_path}")

                # 绘制tif文件
                plot_tif(file_path)

if __name__ == "__main__":
    # 设置源文件夹路径
    source_directory = 'merge_tif'  # 这里替换为你的tif文件夹路径

    # 绘制所有的tif文件
    plot_all_tifs(source_directory)
