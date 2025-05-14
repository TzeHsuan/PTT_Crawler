# -*- coding: utf-8 -*-
import time
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def get_ptt_articles():
    # 設定PTT網址
    base_url = 'https://www.ptt.cc/bbs/Bank_Service/index1669.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    articles = []
    page = 0
    is_first_page = True  # 用於標記是否為起始頁面
    
    print("開始爬取PTT銀行服務版文章...")
    print("從2023年1月開始爬取")
    
    while True:
        try:
            # 發送請求
            response = requests.get(base_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 找到所有文章
            article_entries = soup.find_all('div', class_='r-ent')
            
            print(f"\r目前正在爬取第 {page + 1} 頁，已收集 {len(articles)} 篇文章", end="")
            
            for entry in article_entries:
                try:
                    # 獲取文章標題和連結
                    title_tag = entry.find('div', class_='title').find('a')
                    if not title_tag:
                        continue
                        
                    title = title_tag.text.strip()
                    link = 'https://www.ptt.cc' + title_tag['href']
                    
                    # 獲取作者
                    author = entry.find('div', class_='author').text.strip()
                    
                    # 獲取日期
                    date = entry.find('div', class_='date').text.strip()
                    
                    # 獲取推文數
                    nrec = entry.find('div', class_='nrec')
                    push_count = nrec.text.strip() if nrec else '0'
                    
                    try:
                        article_date = datetime.strptime(date, '%m/%d')
                        # 只在第一頁（起始頁面）跳過12月的文章
                        if is_first_page and article_date.month == 12:
                            continue
                            
                        articles.append({
                            'title': title,
                            'author': author,
                            'date': date,
                            'link': link,
                            'push_count': push_count
                        })
                        print(f"\r目前正在爬取第 {page + 1} 頁，已收集 {len(articles)} 篇文章", end="")
                    except ValueError:
                        continue
                        
                except Exception as e:
                    print(f"\n處理文章時出錯: {e}")
                    continue
            
            # 找到下一頁的連結
            next_page = soup.find('a', string='下頁 ›')
            if not next_page:
                break
                
            base_url = 'https://www.ptt.cc' + next_page['href']
            page += 1
            is_first_page = False  # 標記已經不是第一頁了
            
            # 避免請求過於頻繁
            time.sleep(0.5)
            
        except Exception as e:
            print(f"\n爬取頁面時出錯: {e}")
            break
    
    print("\n爬取完成！")
    # 將結果保存為CSV文件
    df = pd.DataFrame(articles)
    df.to_csv('ptt_bank_service_articles.csv', index=False, encoding='utf-8-sig')
    print(f"共爬取到 {len(articles)} 篇文章")
    return articles

if __name__ == '__main__':
    get_ptt_articles()
