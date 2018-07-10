# -*- coding: euc-kr -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import os
import time

def progress_bar(now, end):
    print(now,"/",end,"[",end='')
    white = int(now / end * 20)
    print('+'*white,end='')
    print(' '*(20-white)+']')

def download_epi(epi_num) :
    url = 'https://comic.naver.com/webtoon/detail.nhn?titleId='+str(title_id)+'&no='+str(epi_num)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    list = soup.select('#comic_view_area > div.wt_viewer > img')
    try:
        os.stat(dir + '\\'+name+'\\'+str(epi_num))
    except:
        os.mkdir(dir + '\\'+name+'\\'+str(epi_num))
    dir_size = 0 
    calc_time = time.time()
    for i in list :
        img_src = i.get('src')
        img_ext = img_src[img_src.rfind('.'):]
        img_name = img_src[img_src.rfind('_')+1:img_src.rfind('.')]
        img_name = name+'_' +str(epi_num)+'_'+img_name
        req = urllib.request.Request(
            img_src, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        f = urllib.request.urlopen(req)
        data = f.read()
        fout = open(dir + '\\'+name+'\\'+str(epi_num)+'\\'+img_name+img_ext, 'wb')
        fout.write(data)
        fout.close()
        stat = os.path.getsize(dir + '\\'+name+'\\'+str(epi_num)+'\\'+img_name+img_ext)
        dir_size = dir_size + stat
    elap_time = time.time() - start_time
    epi_time = time.time() - calc_time
    os.system('cls')
    print(name,"Epi",epi_num,"Download Complete!")
    progress_bar(epi_num,n)
    print("Estimate time  : ",round(elap_time / epi_num * n,3),"s")
    print(" Elapsed time  : ",round(elap_time,3),"s")
    print("    Epi Size   : ",round(dir_size / (1024 * 1024),3),"MB")
    print("Download Speed : ",round(dir_size / epi_time / 1000 / 1000,3),"Mbps")

if __name__ == '__main__':
    global options
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36")

    global driver
    driver = webdriver.Chrome(os.getcwd()+'\\chromedriver.exe',chrome_options=options)
    NW_url = 'https://comic.naver.com/webtoon/'
    driver.implicitly_wait(5)
    time.sleep(3)
    global title_id
    os.system('cls')
    title_id = int(input("Webtoon Code : "))
    driver.get(NW_url + 'list.nhn?titleId=' + str(title_id))

    global dir
    global name
    dir = os.getcwd()
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    name = soup.select('head > title')[0].string
    name = name[:name.find('::')-1]
    print("Webtoon Name : ",name)
    last_epi = soup.select('#content > table > tbody > tr > td > a')
    last_epi = last_epi[1].get('href')
    n = int(last_epi[last_epi.find('no=')+3:last_epi.rfind('&')])
    print("Episode : ",n)
    try:
        os.stat(dir + '\\'+name)
    except:
        os.mkdir(dir + '\\'+name) 
    start_time = time.time()
    for i in range(1,n+1) :
        download_epi(i)
    driver.quit()