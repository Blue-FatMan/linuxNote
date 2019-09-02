#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time :    2019/9/2 20:21
@Author:  LQ
@Email: LQ65534@163.com
@File: get_catalog.py
@Software: PyCharm

the progress is for get markdown catalog
"""

import re


def get_catalog(file_path):
    """
    :param file_path: file md path
    :return:
    """
    encoding = "gbk"
    with open(file_path, 'r', encoding=encoding) as fr:
        lines_list = fr.readlines()

    catalog_list = []
    catalog_format = "[{}](#{})\n\n"
    catalog_space = "&nbsp;"
    for line in lines_list:
        if line.startswith("#" * 6):
            space_count = 20
            catalog = line.split("#" * 6)[1].strip()
        elif line.startswith("#" * 5):
            space_count = 16
            catalog = line.split("#" * 5)[1].strip()
        elif line.startswith("#" * 4):
            space_count = 12
            catalog = line.split("#" * 4)[1].strip()
        elif line.startswith("#" * 3):
            space_count = 8
            catalog = line.split("#" * 3)[1].strip()
        elif line.startswith("#" * 2):
            space_count = 4
            catalog = line.split("#" * 2)[1].strip()
        elif line.startswith("#" * 1):
            space_count = 0
            catalog = line.split("#" * 1)[1].strip()
        else:
            space_count = None
            catalog = None
        if catalog:
            # 下面的判断是为了找到标题里面本身就带有链接的情况，此时目录链接设置为失效
            if all((("[" in catalog), ("]" in catalog), ("(" in catalog), (")" in catalog))):
                catalog_url = ""
                catalog = re.search(r'\[(.*?)\]', catalog)
                catalog = catalog.group().replace("[", "").replace("]", "")
            else:
                catalog_url = catalog.lower()
                catalog_url = catalog_url.replace(" ", "-")
            catalog_list.append(space_count * catalog_space + catalog_format.format(catalog, catalog_url))
    if catalog_list:
        catalog_list.insert(0,"# 目录\n\n")
        catalog_list.append("=" * 20)
        catalog_list.append("\n")
        catalog_list.append("\n")
        # 判断目前是否已经存在目录，如果存在则删除当前目录，重新生成目录
        if "=" * 20 + "\n" in lines_list:
            catalog_list.extend(lines_list[lines_list.index("=" * 20 + "\n") + 2:])
        else:
            catalog_list.extend(lines_list)
        try:
            with open(file_path, 'w', encoding=encoding) as fw:
                fw.write("".join(catalog_list))

        except:
            with open(file_path, 'w', encoding=encoding) as fw:
                fw.write("".join(lines_list))


if __name__ == '__main__':
    file_path = "字符串切割.md"
    get_catalog(file_path)
