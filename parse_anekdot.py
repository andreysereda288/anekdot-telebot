import requests
from bs4 import BeautifulSoup

URL_ANEK = 'https://www.anekdot.ru/random/anekdot/'
URL_STORY = 'https://www.anekdot.ru/last/story/'


def parse_anekdots(content_type='/anekdots'):
    if content_type == '/anekdots':
        url = URL_ANEK
    elif content_type == '/stories':
        url = URL_STORY
    else:
        return 'No content'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")

    topic_divs = soup.find_all('div', class_='topicbox')
    try:
        final_str = ''
        for div in topic_divs:
            if div.has_attr('data-id'):
                if content_type == '/anekdots':
                    date = div.find('p', class_='title')
                    final_str += date.text + '\n'
                text = div.find('div', class_='text')
                text = str(text).replace('<div class="text">', '').replace('</div>', '')
                text = text.replace('<br/>', '\n')
                final_str += text + 2*'\n'
                if content_type == '/stories':
                    final_str += '-------\n'
    except:
        final_str = 'Something went wrong'
    return final_str
