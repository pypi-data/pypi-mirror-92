#-*- coding:utf-8 -*-
import os

# 遍历文件夹
def walk_file(filedir, reverse=False):
    absolute_paths = []
    for root, dirs, files in os.walk(filedir):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            absolute_paths.append(os.path.join(root, f))

        if reverse:
            # 遍历所有的文件夹
            for d in dirs:
                absolute_paths.append(os.path.join(root, d))
    return absolute_paths