# anime-showrenew
# 动漫，番剧自定义更新显示，与下载
显示番剧的更新(可以自定义追番列表
只会自动查询自己加入追番列表的番
完结后无缝进行下载

## 下载器介绍
搭配本人写的番剧下载器，可以实现完结无缝衔接下载
下载器功能有
自动爬取番剧名字并创建番剧文件夹
下载完自动打开下载路径
因为网站文件一般都是m3u8，内置了自己写的下载器并且自动进行下载！
### 详细可以查看更新日志
# 视频教程在这里哟
v2版本还没有录，这是v1版本的教程https://www.bilibili.com/video/BV1FZ4y1v714
但是是操作都大差不错啦~
# 软件流程
### 流程为
#### 1.自动爬取 anime.txt 里的番的更新时间与状态 并显示
#### 2.如果完结，则可以选择是否删除，只有选择选择删除即输入 ‘y’ 后会自动把番的地址保存到剪贴板，并自动打开下载器
#### 3.ctrl v 复制到下载器里，如果有多部番完结要按下 win(Alt左边那个) + v 打开剪贴板，一部一部复制进下载器
	v2.0版本更新优化掉了这几步，只需要 复制 粘贴 回车 就可以全自动进行下载啦！！！
		4.下载完后会自动打开下载目录和m3u8下载器，请将刚刚下载的番的目录拖到![](README_md_files/a14c3490-f6cc-11ec-8ad3-971a5f455f68_20220628182527.jpeg?v=1&type=image&token=V1:AEGUuumQ7lBYw3DGvGslwwHTMOqAXfcXYcFrCZqtpg8)
		记得选择工作目录啊，如果不选的话就默认下载在文件下的download目录下了
		这一栏，再点击下方的 go 就可以直接进行下载了，其他设置可以自行探索

# 使用方法
## 无需下载python！！！
### 1.把我上传的所有都下载下来，并且解压
### 2.先运行新番列表，把自己感兴趣的番那一条复制到目录下的anime.txt里面，参照我做的
### 3.接着在 config.txt 内的 番剧下载路径 填上你想要下载器把番下到哪，和下载的线程数 （尽量不要超过5
	已经不用这两部步了！！！最近的更新把这步优化掉了，直接跳到第六步就好了！！！
		4.双击打开更目录内的 	
		N_m3u8DL-CLI_v2.9.9_with_ffmpeg_and_SimpleG
		之后点击顶部地址栏随后复制一下即可
		5.再打开 config.txt 在里面的 m3u8下载器路径 填入刚刚复制的
### 6.这样就大功告成了，可以把 ‘我追的番更到哪了？’
![](README_md_files/60b8efe0-f61d-11ec-85ca-8dfdf4262aa8_20220627213058.jpeg?v=1&type=image&token=V1:snUTMUNjdt58oRC8zgf52ly8tZqEOeUyW8HB0Wq0VTM)
### 加入到任务计划管理里面，设置每次开机就运行
