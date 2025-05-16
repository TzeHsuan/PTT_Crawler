# PTT_Crawler

## 📌 Description

As part of the project I participated in NTHU DTDA, I was assigned a task to crawl the comments from the top 15 posts on PTT (A forum platform in Taiwan) that has the most comments.

## 🎯 Project Goals
- Collect PTT articles (title, push count, author) from 2023 onward
- Filter articles containing keywords like "新手" (newbie) or "開戶" (account opening)
- Sort filtered articles by push count and crawl the top 15 most engaged posts
- Save data in `.csv` and `.txt` formats for analysis and LLM usage

## 🛠️ Built With
- Python
- [Cursor](https://www.cursor.com/en)

## 🧭 Workflow

1. **Collect Article**
    - Scrape all articles from 2023 onward
    - Extract: title, push count, author, date

2. **Filter & Sort**
    - Keep only articles with "新手" or "開戶" in the title
    - Sort them by number of push count

3. **Deep Crawl Top 15 Articles**
    - Retrieve full content and comments from the top 15 most pushed posts

4. **Save Data**
    - `.csv`: for structured, multi-column analysis
    - `.txt`: for feeding into LLMs

## 📂 Project Structure
├── article_contents<br>
│   ├── all_titles.txt<br>
│   └── article_1159.txt<br>
│   └── article_1211.txt<br>
│   └── ........<br>
├── top15Articles<br>
│   └── article_1159.csv<br>
│   └── article_1211.csv<br>
│   └── ........<br>
├── ptt.py : scrapes all articles from 20023 onward and saves the result in ptt_articles.csv<br>
├── ptt_articles.csv<br>
├── ptt_top15.py : sorts ptt_articles.csv, finds the top 15 articles, and saves the results in the top15Articles folder <br>
├── toCSV.py : reads all the files in the top15Articles folder, extracts the top 15 articles' title and corresponding file name <br>
├── toTXT.py : reads all the files in the top15Articles folder and converts them into .txt <br>
└── README.md

## ▶️ Getting Started
1. Get all the files from this repository
```
git clone https://github.com/TzeHsuan/PTT_Crawler.git
```
2. Install required Python packages (i.e. pandas, bs4 etc.) if not installed previously.


