import os
import rasterio
from rasterio.enums import Resampling
from rasterio.merge import merge
from tqdm import tqdm
import dask.array as da
import numpy as np
import xarray as xr
import datashader as ds
import holoviews as hv
from holoviews.operation.datashader import rasterize
hv.extension('bokeh')  # 使用 Bokeh 后端进行交互可视化

def merge_tifs(source_dir, output_tif):
    # 创建一个存储数据集的列表
    datasets = []

    # 初始化一个进度条
    print("开始读取 .tif 文件...")
    # 计算文件总数
    tif_files = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.tif'):
                tif_files.append(os.path.join(root, file))
    
    # 初始化读取文件的进度条
    with tqdm(total=len(tif_files), desc='读取文件') as pbar:
        for file_path in tif_files:
            # 打开tif文件并附加到数据集列表中
            src = rasterio.open(file_path)
            datasets.append(src)
            pbar.update(1)

    # 使用rasterio.merge合并数据集
    print("开始合并...")
    mosaic, transform = merge(datasets, resampling=Resampling.bilinear)
    
    # 从第一个数据集获取元数据信息
    out_meta = datasets[0].meta.copy()

    # 更新元数据以反映拼接后的图像尺寸和变换
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": transform,
        "crs": datasets[0].crs
    })

    # 写入输出tif文件
    with rasterio.open(output_tif, "w", **out_meta) as dest:
        dest.write(mosaic)

    # 关闭所有数据集
    for src in datasets:
        src.close()

    print(f"Merged TIF saved as {output_tif}")

    return mosaic, transform, out_meta

def visualize_large_tif(mosaic, transform, meta):
    # 创建一个 xarray 数据数组
    dask_array = da.from_array(mosaic, chunks=(1, 2048, 2048))
    xarr = xr.DataArray(dask_array, dims=("band", "y", "x"))
    
    # 设置坐标
    xarr.coords['x'] = xr.Variable('x', np.arange(meta['width']) * transform[0] + transform[2])
    xarr.coords['y'] = xr.Variable('y', np.arange(meta['height']) * transform[4] + transform[5])

    # 使用 datashader 进行可视化
    img = hv.Image(xarr.sel(band=1), kdims=['x', 'y'])
    rasterized_img = rasterize(img)

    # 设置绘图参数
    plot = rasterized_img.opts(
        width=800,
        height=600,
        cmap='viridis',
        colorbar=True,
        title='Large TIF Visualization'
    )
    
    return plot

if __name__ == "__main__":
    # 设置源文件夹路径
    source_directory = 'tif'  # 这里替换为你的tif文件夹路径

    # 设置输出tif文件路径
    output_tif_path = 'merge_tif/merged_output.tif'  # 这里替换为你的输出tif文件路径

    # 合并所有的tif文件
    mosaic, transform, meta = merge_tifs(source_directory, output_tif_path)

    # 可视化合并后的tif文件
    plot = visualize_large_tif(mosaic, transform, meta)
    hv.save(plot, 'output.html')  # 保存为 HTML 文件
    hv.show(plot)  # 在浏览器中打开可视化
