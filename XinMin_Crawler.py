import datetime
import requests
import argparse
import pandas as pd
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Xinmin Daily Crawler')
parser.add_argument('--start_date', type=str, default='2022-04-01', help='start date')
parser.add_argument('--end_date', type=str, default='2022-06-01', help='end date')

args = parser.parse_args()

def url_builder(start_date, end_date):
    current_date = start_date
    urls = []
    for i in range((end_date - start_date).days + 1):
        urls.append('https://paper.xinmin.cn/html/xmwb/' + current_date.strftime('%Y-%m-%d') + '/1.htm')
        current_date += datetime.timedelta(days=1)
    return urls

def get_news(url):
    data_list = []
    date = url.split('/')[-2]
    print("processing date: ", date)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # collect the catalog of news in the newspaper
    elements = soup.find_all(class_="dzb-enter-wrap dzb-enter-mulu-wrap")
    catalog_text = ""
    for element in elements:
        catalog_text += element.get_text()
        catalog_text += "\n"
    catalog = catalog_text.split('\n')
    catalog = list(filter(None, catalog))
    
    for i in range(len(catalog)):
        current_page_name = catalog[i]
        current_ban = current_page_name.split(':')[0]
        current_ban = current_ban.replace('/', '-')[1:-1]
        current_url = url.replace('1.htm', current_ban + '.htm')
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the parent element with both classes
        parent = soup.find(class_="dzb-enter-desc-box dzb-enter-heng-desc-box")
        title = soup.find(class_="dzb-title-box").get_text()
        special_title = soup.find(class_="dzb-special-title-box")
        if special_title:
            special_title = special_title.get_text()
        else:
            special_title = ''
        
        subtitle = soup.find(class_="dzb-sub-title-box")
        if subtitle:
            subtitle = subtitle.get_text()
        else:
            subtitle = ''
        if parent:
            # Find the child class
            content_element = parent.find(class_="dzb-desc-box")
            if content_element:
                content = content_element.get_text()
            else:
                content = ''
        else:
            parent = soup.find(class_="dzb-enter-info-box dzb-shu-info-box")
            if parent:
                # Find the child class
                content_element = parent.find(class_="dzb-desc-box")
                if content_element:
                    content = content_element.get_text()
                else:
                    content = ''
                
                subtitle = soup.find(class_="dzb-sub-title-box")
                if subtitle:
                    subtitle = subtitle.get_text()
                else:
                    subtitle = ''
        data_list.append({'Special Title': special_title, 'Title': title, 'Subtitle': subtitle, 'Content': content, 'Links': current_url, 'Date': date})
    news = pd.DataFrame(data_list)
    news['Ban'] = catalog
    return news

def main():
    start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d').date()
    urls = url_builder(start_date, end_date)
    papers = pd.DataFrame(columns=['Special Title', 'Title', 'Subtitle', 'Content', 'Links', 'Date', 'Ban'])
    for url in urls:
        news = get_news(url)
        papers = pd.concat([papers, news], ignore_index=True)
    papers.to_csv('XinMin.csv', index=False, encoding='utf-8-sig')
        
if __name__ == '__main__':
    main()