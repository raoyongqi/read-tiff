import os
import shutil

def copy_tif_files(source_dir, destination_dir):
    # 创建目标文件夹（如果不存在）
    os.makedirs(destination_dir, exist_ok=True)

    # 遍历源文件夹中的所有子文件夹
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # 检查文件是否以.tif结尾
            if file.lower().endswith('.tif'):
                # 构建完整的源文件路径
                source_file_path = os.path.join(root, file)
                # 构建目标文件路径
                destination_file_path = os.path.join(destination_dir, file)

                # 打印正在复制的文件信息
                print(f"Copying {source_file_path} to {destination_file_path}")

                # 将文件复制到目标文件夹
                shutil.copy2(source_file_path, destination_file_path)

    print("所有的.tif文件已复制完成。")

if __name__ == "__main__":
    # 设置源文件夹路径和目标文件夹路径
    source_directory = 'glc302'  # 这里替换为你的源文件夹路径
    destination_directory = 'tif'  # 这里替换为你的目标文件夹路径

    # 复制.tif文件
    copy_tif_files(source_directory, destination_directory)
