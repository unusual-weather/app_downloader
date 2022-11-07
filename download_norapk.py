from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
import time
import os

##SETTING - 뒤에 \\나 / 붙이지 말아용
ChromeDriver_Path = '.\\chromedriver.exe'
Download_Path = 'C:\\Users\\kisan\\OneDrive\\바탕 화면\\malapp'
CSV_PATH = "C:\\PROJECT\\playstore\\crawler_except\\ko_googlestore.csv"


def chrome_init():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Head-less 설정, 브라우저를 열지 않음
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    prefs={}
    prefs["download.default_directory"]=Download_Path
    options.add_experimental_option('prefs', prefs)

    return options    
    
def download_wait(path_to_downloads,download_count):
    tmp_cnt = 0
    for download in os.listdir(path_to_downloads):
        if download.endswith(".crdownload"):
            tmp_cnt+=1
    while tmp_cnt > download_count:
        print("waiting")
        time.sleep(1)
        tmp_cnt = 0
        for download in os.listdir(path_to_downloads):
            if download.endswith(".crdownload"):
                tmp_cnt+=1
    

if __name__=="__main__":
    
    #수집 목록의 csv 읽기
    try:
        df = pd.read_csv(CSV_PATH)
    except:
        print("[+]파일이 없다!!!! - (대소문자 주의)")
        exit(-1)
    
    package_list = list(df['package_name'])
    download_list = list(df['cnt_download'])
    target_download = []
    apk_download_link = []

    #다운로드 목록 확인
    for download in set(download_list):
        print(f"해당 {download}개수의 다운로드된 파일을 다운 받으시겠습니다까?(O/X)\n> ",end='')
        choice = input("")       
        if choice == 'O':
            target_download.append(download)        
    
    #대기줄 개숫 지정
    wait_cnt = int(input("대기줄 :"))
    
    #크롬 드라이버 세팅
    driver =webdriver.Chrome(ChromeDriver_Path, options=chrome_init())
    
    for package,download in tqdm(zip(package_list,download_list)):
        if download in target_download:
            print(f"\t{package} 수행 중")
            
            download_wait(Download_Path,wait_cnt)

            driver.get(url=f"https://apkcombo.com/ko/melon-playground/{package}/download/apk")
            try:
                target = driver.find_element(By.XPATH,f'//*[@id="best-variant-tab"]/div[1]/ul/li/ul/li/a')
                #다운로드
                driver.get(url=target.get_attribute('href'))
            except:
                continue


    #나중에 크롬 꼭 끄세용
