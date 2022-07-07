import requests
from concurrent.futures import ThreadPoolExecutor
import os
import shutil


# 创建文件夹
def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # print(' 创建过了')
        return False


def get_m3u8(workdir):
    m3u8_path = []
    m3u8_name = []
    files = os.listdir(workdir)
    for file in files:
        if file.find('.m3u8') != -1:
            m3u8_name.append(file)
            file = os.path.join(workdir, file)
            # print(file)
            m3u8_path.append(file)
    if len(m3u8_path) == 0:
        print(f'{workdir}文件夹内没有找到m3u8文件')
        m3u8_path = False
    return m3u8_path, m3u8_name


def get_m3u8_link_download(m3u8_path, m3u8_name, workdir):  # 一集
    all_index = 0
    m3u8_links = []
    with open(m3u8_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.find('#EXT') == -1:
                m3u8_links.append(line)
                all_index += 1
    if len(m3u8_links) == 0:
        print(f'{m3u8_name}文件内未找到链接')
        return
    else:
        # global count
        # count = 0
        print(f'\n下载 {m3u8_name} 中。。。。\n', end='')
        with ThreadPoolExecutor(16) as f:
            for link, i in zip(m3u8_links, range(len(m3u8_links))):
                first_download_path = workdir + '\\' + m3u8_name.replace('.m3u8', '')  # workdir\间谍过家家第1集\
                mkdir(first_download_path)
                f.submit(m3u8_download, link, first_download_path, i, len(m3u8_links))
        # for link, i in zip(m3u8_links, range(len(m3u8_links))):
        #     first_download_path = workdir + '\\' + m3u8_name.replace('.m3u8', '')  # workdir\间谍过家家第1集\
        #     mkdir(first_download_path)
        #     m3u8_download(link, first_download_path, i, len(m3u8_links))
        os.system(f"copy /b {first_download_path}\\*.ts {first_download_path}.mp4")  # 合并
        shutil.rmtree(first_download_path)
        print("转换为mp4 完成")


def m3u8_download(url, name, i, all_i):
    # global count
    while len(str(i)) < 4:
        i = '0' + str(i)
    file_name = f'{name}\\{i}.ts'  # workpath\间谍过家家第1集\间谍过家家第1集0.ts
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
    while 1:
        try:
            resp = requests.get(url, timeout=5).content[212:]
            with open(file_name, 'wb') as f:
                f.write(resp)
            i = int(i)
            if i % 16 == 0:
                show_i = str(round(((i / all_i) * 100), 2)) + '%'
                if i == 0:
                    print(f'{name} 进度为 {i}/{all_i} {show_i}', end='')
                else:
                    print(f'\r{name} 进度为 {i}/{all_i} {show_i}', end='', flush=True)
            break
        except requests.exceptions.RequestException:
            pass


def main(workdir, thread):  # m3u8目录类似 D:\桌面\夏日重现    线程数
    get_m3u8s = get_m3u8(workdir)
    m3u8_paths, m3u8_names = get_m3u8s[0], get_m3u8s[1]
    if m3u8_paths:
        with ThreadPoolExecutor(thread) as f:
            for m3u8_path, m3u8_name in zip(m3u8_paths, m3u8_names):
                f.submit(get_m3u8_link_download, m3u8_path, m3u8_name, workdir)
        # for m3u8_path, m3u8_name in zip(m3u8_paths, m3u8_names):
        #     get_m3u8_link_download(m3u8_path, m3u8_name)
        for path in m3u8_paths:  # 删除m3u8文件
            os.remove(path)


if __name__ == '__main__':
    workdir = input('请输入或拖拽存有m3u8的文件夹\t\t不能为单m3u8文件！！！\n')

    main(workdir, 1)
