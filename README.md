# PTT_Crawler

## 📌 Description

As part of the project I participated in NTHU DTDA, I was assigned a task to crawl the comments from the top 15 posts on PTT (A forum platform in Taiwan) that has the most comments.

## 📌 Project Goals
- Collect PTT articles (title, push count, author) from 2023 onward
- Filter articles containing keywords like "新手" (newbie) or "開戶" (account opening)
- Sort filtered articles by push count and crawl the top 15 most engaged posts
- Save data in `.csv` and `.txt` formats for analysis and LLM usage

## Built With
- [Cursor](https://www.cursor.com/en)



## 🛠 Tech Stack
- Python
- [ptt-crawler by PTT-Analyzer](https://github.com/henryyang42/PTT-Analyzer)
- Cursor (AI pair programmer)

## 🧭 Workflow

1. **Collect Article Metadata**
    - Scrape all articles from 2023 onward
    - Extract: title, push count, author

2. **Filter & Sort**
    - Keep only articles with "新手" or "開戶" in the title
    - Sort them by number of pushes (engagement)

3. **Deep Crawl Top 15 Articles**
    - Retrieve full content and comments from the top 15 most pushed posts

4. **Save Data**
    - `.csv`: for structured, multi-column analysis (e.g., title, push count, content)
    - `.txt`: for feeding into LLMs like NotebookLM or ChatGPT

## 📂 Project Structure
