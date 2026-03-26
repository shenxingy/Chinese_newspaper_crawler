# Chinese Newspaper Crawler

Two Python crawlers for scraping Chinese newspaper articles — one for CNKI (中国知网) using Selenium, and one for Xinmin Daily (新民晚报) using Requests + BeautifulSoup.

## Requirements

- Python 3.7+
- Google Chrome + matching [ChromeDriver](https://chromedriver.chromium.org/downloads) (for CNKI crawler)

Install Python dependencies:

```bash
pip install selenium pandas numpy requests beautifulsoup4
```

---

## CNKI Crawler (`CNKI_Crawler.py`)

Scrapes newspaper articles from [CNKI](https://www.cnki.net/) using Selenium and Chrome.

**Extracted fields:** Number, Title, Author, BanHao, Date, Download count, Links, Contents, Keywords

**Usage:**

```bash
python CNKI_Crawler.py \
  --keyword 疫情 \
  --start_date 2022-04-01 \
  --end_date 2022-06-01 \
  --start_page 1 \
  --end_page 10 \
  --newpaper_url https://navi.cnki.net/knavi/newspapers/JFRB/detail?uniplatform=NZKPT
```

The crawler will open Chrome, prompt you to log in manually, then scrape the specified page range and save results to `CNKI.csv`.

**Arguments:**

| Argument | Default | Description |
|---|---|---|
| `--keyword` | `疫情` | Search keyword |
| `--start_date` | `2022-04-01` | Filter start date (YYYY-MM-DD) |
| `--end_date` | `2022-06-01` | Filter end date (YYYY-MM-DD) |
| `--start_page` | `15` | First page to scrape |
| `--end_page` | `31` | Last page to scrape |
| `--newpaper_url` | JFRB URL | CNKI newspaper detail page URL |

![CNKI Preview](https://github.com/shenxingy/Chinese_newspaper_crawler/blob/main/Sample_Datasets/CNKI_Sample.png)

---

## Xinmin Daily Crawler (`XinMin_Crawler.py`)

Scrapes newspaper articles from [Xinmin Daily (新民晚报)](https://paper.xinmin.cn/) using Requests and BeautifulSoup. No login required.

**Extracted fields:** Special Title, Title, Subtitle, Content, Links, Date, Ban (page headline)

**Usage:**

```bash
python XinMin_Crawler.py \
  --start_date 2022-04-01 \
  --end_date 2022-06-01
```

Results are saved to `XinMin.csv`.

**Arguments:**

| Argument | Default | Description |
|---|---|---|
| `--start_date` | `2022-04-01` | Crawl start date (YYYY-MM-DD) |
| `--end_date` | `2022-06-01` | Crawl end date (YYYY-MM-DD) |

![Xinmin Preview](https://github.com/shenxingy/Chinese_newspaper_crawler/blob/main/Sample_Datasets/Xinmin_Sample.png)

---

## Sample Datasets

The `Sample_Datasets/` folder contains example CSV outputs and screenshots from both crawlers.
