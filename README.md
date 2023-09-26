# Chinese Newspaper Crawler
### Utilizing Chrome Driver for Web Scraping CNKI Newspapers (China National Knowledge Infrastructure, 中国知网, https://www.cnki.net/)
CNKI is a valuable resource for accessing academic and research articles. With `CNKI_Crawler.py`, we can extract the following attributes from CNKI newspapers:
- **Number**: The unique identifier or reference number of the newspaper article.
- **Title**: The headline or title of the newspaper article.
- **Author**: The name(s) of the author(s) responsible for the article's content.
- **banHao**: The "issue number" or "edition number" of the article.
- **Date**: The date when the newspaper article was published.
- **Download**: The count of how many times the article has been downloaded.
- **Links**: The link that leads to the full newspaper article.
- **Contents**: The actual content of the newspaper article.
- **Keywords**: Keywords or tags associated with the article, providing insights into its topic or subject matter.
![Preview](https://github.com/shenxingy/Chinese_newspaper_crawler/blob/main/Sample_Datasets/CNKI_Sample.png)

### Xinmin_Crawler
While CNKI provides access to a wide range of newspapers, there are still some newspapers not available on the platform. For such cases, `XinMin_Crawler.py` is developed, an example that utilizes the Requests and the Beautiful Soup packages to crawl newspapers from XMWB(新民晚报，https://paper.xinmin.cn/). The attributes include: *Special Title*, *Title*, *Subtitle*, *Content*, *Links*, *Date*, *Ban(Page Headline)*.
![Preview](https://github.com/shenxingy/Chinese_newspaper_crawler/blob/main/Sample_Datasets/Xinmin_Sample.png)

