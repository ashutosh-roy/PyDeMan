from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus


def home(request):
    return render(request, 'pydeman/index.html')


def search(request):
    BASE_PYDEMAN_URL = 'https://pypi.org/search/?q={}'
    s = request.POST.get('search')
    print(s)
    # models.Search.objects.create(search=s)

    # Dynamically creates the URL by storing the SEARCH USER INPUTS replacing spaces with +
    # user input = python tutor
    # url = python+tutor attached to base url
    final_url = BASE_PYDEMAN_URL.format(quote_plus(s))

    # Web Scraping Begins
    # Deriving HTML / CSS from the Craigslist URL
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='lxml')

    post_listings = soup.find_all('a', {'class': 'package-snippet'})
    print(post_listings)
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='package-snippet__name').text
        post_version = post.find(class_='package-snippet__version').text
        post_desc = post.find(class_='package-snippet__description').text
        final_postings.append((post_title, post_version, post_desc))

    stuff_for_frontend = {'s': s, 'final_postings': final_postings}
    return render(request, 'pydeman/newsearch.html', stuff_for_frontend)


def newsearch(request):
    BASE_PYDEMAN_URL = 'https://pypi.org/project/{}/'
    s = request.POST.get('search')
    print(s)
    final_url = BASE_PYDEMAN_URL.format(quote_plus(s))

    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='lxml')
    post_listings = soup.find_all('div', {'class': 'banner'})
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='package-header__name').text
        print("Title = {}".format(post_title.replace('\n', '')))

        post_command = post.find(id='pip-command').text
        print("Command = {}".format(post_command))

    post_desc = soup.find(
        'p', {'class': 'package-description__summary'}).get_text()
    print("Summary = {}".format(post_desc))
    final_postings.append((post_title, post_command, post_desc))
    print(final_postings)
    stuff_for_frontend = {'final_postings': final_postings}
    return render(request, 'pydeman/newsearch.html', stuff_for_frontend)
