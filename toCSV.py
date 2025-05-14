import pandas as pd
import os

# 設定目錄路徑
input_dir = 'top15Articles'
output_dir = 'article_contents'

# 如果輸出目錄不存在，創建它
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 用於收集所有標題
all_titles = []

# 遍歷所有 CSV 檔案
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        # 讀取 CSV 檔案
        file_path = os.path.join(input_dir, filename)
        df = pd.read_csv(file_path)
        
        # 提取 content 欄位
        if 'content' in df.columns:
            # 創建對應的 txt 檔案名稱
            txt_filename = filename.replace('.csv', '.txt')
            txt_path = os.path.join(output_dir, txt_filename)
            
            # 將所有內容寫入 txt 檔案
            with open(txt_path, 'w', encoding='utf-8') as f:
                for content in df['content']:
                    f.write(str(content) + '\n\n')  # 每個內容之間加入空行分隔
            
            print(f'已處理: {filename} -> {txt_filename}')
            
            # 收集標題
            if 'original_title' in df.columns:
                for title in df['original_title']:
                    all_titles.append(f"{filename}: {title}")
        else:
            print(f'警告: {filename} 中沒有找到 content 欄位')

# 將所有標題寫入一個檔案
titles_path = os.path.join(output_dir, 'all_titles.txt')
with open(titles_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_titles))

print(f'\n所有標題已保存到: {titles_path}') 