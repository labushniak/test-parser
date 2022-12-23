import requests as requests
from bs4 import BeautifulSoup
import re

url = "https://lifehacker.ru/topics/sport/"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46',
    'Accept-Language': 'ru,en;q=0.9'
}


# формируем страницу со ссылками
# response_page = requests.get(url=url, headers=headers)
# with open(file='posts.html', mode='w', encoding='utf-8') as file:
#    file.write(response_page.text)
# beautifulsoup: BeautifulSoup = BeautifulSoup(markup=response_page.text, features='lxml')

# обращаемся к сохраненной странице со списком ссылок
with open(file='posts.html', mode='r', encoding='utf-8') as file:
    response_page = file.read()

beautifulsoup: BeautifulSoup = BeautifulSoup(markup=response_page, features='lxml')

cards = beautifulsoup.find_all(name='div', class_='article-card__small-wrapper')

print(f'На странице найдено {len(cards)} карточек')

for card in cards:
    # link = f"https://lifehacker.ru{card.find('a')['href']}"
    link = 'https://lifehacker.ru/gornye-lyzhi/'
    # print(link)

    # делаем запрос и создаем файл

    # result_card = requests.get(url=link, headers=headers)
    # with open(file='post.html', mode='w', encoding='utf-8') as file:
    #     file.write(result_card.text)
    #
    # beautifulsoup_card: BeautifulSoup = BeautifulSoup(markup=result_card.text, features='lxml')

    # -----------------------------
    # обращаемся к записанному файлу

    with open(file='post.html', mode='r', encoding='utf-8') as file:
        result_card = file.read()
        beautifulsoup_card: BeautifulSoup = BeautifulSoup(markup=result_card, features='lxml')

    result_card = requests.get(url=link, headers=headers)

    beautifulsoup_card: BeautifulSoup = BeautifulSoup(markup=result_card.text, features='lxml')

    with open(file='post.html', mode='r', encoding='utf-8') as file:
        result_card = file.read()

    title = beautifulsoup_card.find(name='h1', attrs={'class': 'article-card__title'}).text
    print(f'Получили заголовок: {title}')

    article = beautifulsoup_card.find(name='article').find(name='div')
    # article_text = beautifulsoup_card.find(name='article').text
    print(f'Получили статью целиком:\r\n{article.text}')

    for read_also in beautifulsoup_card.find_all(name='div', class_=re.compile('read-also')):
        read_also.decompose()

    for subscription_form in beautifulsoup_card.find_all(name='div', class_=re.compile('newsletter-subscription-form')):
        subscription_form.decompose()

    for widgets in beautifulsoup_card.find_all(name='div', class_=re.compile('widgets-renderer')):
        widgets.decompose()

    # получаем все дочерние элементы статьи

    elements = article.find_all(recursive=False)
    print(elements)

    for element in elements:
        # print(f'Получили тег <{element.name}> с текстом: «{element.text}»')
        tags = element.find_all(recursive=False)
        for tag in tags:
            if tag.name == 'ol' or tag.name == 'ul':
                for el in tag.find_all(name='li'):
                    print(el.text)
            elif tag.name == 'h1' or tag.name == 'h2' or tag.name == 'h3' or tag.name == 'h4':
                print(tag.text)
            elif tag.name == 'p' and tag.text:
                print(tag.text)
            elif tag.name == 'figure':
                # url = tag.find(name='a', attrs={'href': re.compile("^https://")})['href']
                img = tag.find(name='img')
                img_url = tag.find(name='img').attrs['src']

                caption = 'Фото взято из открытых источников'
                if tag.find(name='figcaption'):
                     caption = tag.find(name='figcaption').text
                print(img_url)
                print(caption)
