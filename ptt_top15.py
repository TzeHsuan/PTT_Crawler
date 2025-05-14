# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import json
import os

def get_article_content(article_url, original_title):
    """爬取單篇文章的內容和留言"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 獲取文章內容
        main_content = soup.find('div', id='main-content')
        if not main_content:
            return None, []
            
        # 獲取文章標題
        title = main_content.find('span', class_='article-meta-value')
        title = title.text.strip() if title else ''
        
        # 獲取作者
        author = main_content.find('span', class_='article-meta-value')
        author = author.text.strip() if author else ''
        
        # 獲取發文時間
        post_time = main_content.find_all('span', class_='article-meta-value')
        post_time = post_time[-1].text.strip() if len(post_time) > 0 else ''
        
        # 獲取文章內容
        content = ''
        for element in main_content.stripped_strings:
            if element not in [title, author, post_time]:
                content += element + '\n'
        
        # 找到所有推文
        comments = []
        push_tags = soup.find_all('div', class_='push')
        
        for push in push_tags:
            try:
                push_type = push.find('span', class_='push-tag').text.strip()
                user_id = push.find('span', class_='push-userid').text.strip()
                content = push.find('span', class_='push-content').text.strip()
                time = push.find('span', class_='push-ipdatetime').text.strip()
                
                comments.append({
                    'type': 'comment',  # 標記為留言
                    'title': '',  # 留言沒有標題
                    'author': user_id,
                    'content': content,
                    'date': time,
                    'push_tag': push_type,
                    'original_title': original_title  # 加入原始標題
                })
            except Exception as e:
                print(f"處理留言時出錯: {e}")
                continue
        
        # 將文章內容也加入列表
        all_content = [{
            'type': 'article',  # 標記為文章
            'title': title,
            'author': author,
            'content': content,
            'date': post_time,
            'push_tag': '',  # 文章沒有推文標籤
            'original_title': original_title  # 加入原始標題
        }]
        
        # 將留言加入列表
        all_content.extend(comments)
        
        return all_content
        
    except Exception as e:
        print(f"爬取文章時出錯: {e}")
        return None

def main():
    # 讀取CSV檔案
    df = pd.read_csv('ptt_articles.csv')
    
    # 篩選標題包含「新手」或「開戶」的文章
    filtered_df = df[df['title'].str.contains('新手|開戶', na=False)]
    print(f"找到 {len(filtered_df)} 篇標題包含「新手」或「開戶」的文章")
    
    # 處理推文數
    def convert_push_count(x):
        if x == '爆':
            return 100  # 設定一個很大的數字
        try:
            return int(x)
        except:
            return 0
    
    # 轉換推文數並排序
    filtered_df['push_count_num'] = filtered_df['push_count'].apply(convert_push_count)
    df_sorted = filtered_df.sort_values('push_count_num', ascending=False)
    
    # 取前15篇文章
    top_15 = df_sorted.head(15)
    print(f"從中選出推文數最高的 {len(top_15)} 篇文章")
    
    # 建立儲存目錄
    if not os.path.exists('top15Articles'):
        os.makedirs('top15Articles')
    
    # 爬取每篇文章的內容和留言
    for index, row in top_15.iterrows():
        print(f"\r正在爬取第 {index + 1}/15 篇文章", end="")
        all_content = get_article_content(row['link'], row['title'])
        
        if all_content:
            # 將所有內容轉換為DataFrame
            content_df = pd.DataFrame(all_content)
            
            # 儲存到單一CSV檔案
            content_df.to_csv(f'top15_articles/article_{index + 1}.csv', 
                            index=False, encoding='utf-8-sig')
        
        # 避免請求過於頻繁
        time.sleep(0.5)
    
    print("\n爬取完成！")
    print("所有文章內容和留言已分別儲存在 top15_articles 目錄下")

if __name__ == '__main__':
    main()
