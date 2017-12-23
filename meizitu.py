# -*- coding=utf-8 -*-
import re
import urllib3
import os
import sys
import time
import urllib2
import urllib

#获取网页内容，并处理 \n ，以便于方便使用正则匹配
def get_html(url):
		userAgent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
		Chrome/32.0.1667.0 Safari/537.36'
		http = urllib3.PoolManager(timeout=2)
		response = http.request('get', url, headers={'User_Agent': userAgent})
		html = response.data
		html = html.replace('\n', '////')
		return html

#获取网页标题名称
def get_headtitle(html):
    title = re.search('(?<=<title>).*?-.*?(?=-)', html).group()
    title = title.strip()
    title = title.replace('-', '_')
    title = title.replace(':', '')
    title = title.replace(';', '')
    title = title.replace('!', '')
    title = title.replace('?', '')
    title = title.replace('.', '')
    return title

#获取网页中图片地址
def get_meizi(html):
    #怕改版后图片链接变多，会抓到多个图片链接，所以先用div过滤一遍，之后在抓取
    fanwei = re.search('(?<=<div class="main-image">).*?(?=</div>)', html).group()
    picture = re.search('(?<=\<img src=").*?(?=")', fanwei).group()
    return picture

#获取图片真实二进制数据
def get_true_picture(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    		Chrome/32.0.1667.0 Safari/537.36',
              'Referer': 'http://www.mzitu.com',
              # 'Cookie': 'AspxAutoDetectCookieSupport=1'
              }
    request = urllib2.Request(url, headers=header)
    response = urllib2.urlopen(request)
    page = response.read()
    fw = open(str(a) + '.jpg', 'wb')
    fw.write(page)
    fw.close()

#获取本网页有多少个页面
def get_num(html):
    num = re.findall('(?<=<span>)\d{1,3}(?=</span>)', html)
    return num[-1]

#判断有无文件夹，创建文件夹
def mkdir(title):
    path = 'D:\meizitu\\' + title.strip()
    #兼容win10（win10 是 gb2312 的编码格式，utf-8 不识别，会乱码）
    path = path.decode('utf-8').encode('gb2312')
    # 判断路径是否存在
    isExists = os.path.exists(path)
    #判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print path + ' 创建成功'.decode('utf-8').encode('gb2312')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path + ' 目录已存在,请手动删除该文件夹再继续操作'.decode('utf-8').encode('gb2312')
        sys.exit()


#定义指定的抓取页面
try:
	page = input("请输入你想要下载的妹子编号\n\
例如http://www.mzitu.com/1的1，只要http://www.mzitu.com/后面的那串数字即可\n\
如果不输入，默认编号为1的妹子图组：".decode('utf-8').encode('gb2312'))
except (SyntaxError,NameError):
	print '用户什么也没有输入或输入了非数字字符，程序自动中断。\
如需下载请重新运行............'.decode('utf-8').encode('gb2312')
	sys.exit()
user_url = 'http://www.mzitu.com/' + str(page)

#最开始只请求web_num和
html = get_html(user_url)
try:
	web_num = get_num(html)
except IndexError:
	print '该妹子不存在，请输入准确的妹子编号进行下载，谢谢。\n\
本程序自动退出.............'.decode('utf').encode('gb2312')
	sys.exit()

title = get_headtitle(html)
print('@@@@@@@@@@@@@@@@当前图组内共有  %s 个图片@@@@@@@@@@@@@@@@'.decode('utf-8').encode('gb2312') %int(web_num))
try:
	mkdir(title)
except WindowsError:
	print '编码图组名遇到错误，图组名存在英文符号。\n\
请发送主题为“妹子图脚本”，内容为图组编号的邮件至2791055435@qq.com\n\
改完会及时联络您，此前请下载不包含英文符号的图组，感谢理解\n\
本程序自动退出..........'.decode('utf-8').encode('gb2312')
	sys.exit()



#开始抓取文件并保存文件
for a in range(1,int(web_num)+1):
    if a != 1:
        url = user_url + '/' + str(a)
    else:
        url = user_url

    load_html = get_html(url)
    picture = get_meizi(load_html)
    print('正在下载第 %s 张图片..........'.decode('utf-8').encode('gb2312') %a)
    file_path = 'D:\meizitu\\' + title.strip()
    file_path = file_path.decode('utf-8').encode('gb2312')
    os.chdir(file_path)
    get_true_picture(picture)
    time.sleep(0.3)

print '@@@@@@@@@@@@@@@@@@@下载完成，程序退出@@@@@@@@@@@@@@@@@@@@@'.decode('utf-8').encode('gb2312')
