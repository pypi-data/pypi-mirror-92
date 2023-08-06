search_text = 'hugo award best novel liu'
import requests
page = requests.get(
    'https://wikipedia.org/w/index.php',
    {'search': search_text},
)
import bs4
soup = bs4.BeautifulSoup(page.text)
hugo_url = soup.find('div', {'class': 'searchresults'}).find('ul').find('li').find('a').get('href')
hugo_url
base_url = 'https://en.wikipedia.org'

'/'.join(base_url, hugo_url)
'/'.join((base_url, hugo_url))
import requests
base_url = 'https://en.wikipedia.org'
search_text = 'hugo award best novel liu'
page = requests.get(
    'https://en.wikipedia.org/w/index.php',
    {'search': search_text},
)
page
!more ~ / .config / pep8
