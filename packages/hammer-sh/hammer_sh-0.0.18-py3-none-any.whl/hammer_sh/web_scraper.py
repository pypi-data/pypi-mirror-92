import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm.notebook import trange, tqdm
import pickle
import pkg_resources
__name__ = "hammer_sh"
base_url = "https://link.springer.com"


def load_saved_abstracts():
    """

    :return:
    """
    stream = pkg_resources.resource_filename(__name__, 'sample_data/abstracts.pickle')
    with open(stream, 'rb') as file:
        df = pickle.load(file)
    return df


def extract_abstracts():
    """

    :return:
    """
    urls_to_search = {
        "Computer Sience": 'https://link.springer.com/search?facet-discipline=%22Computer+Science%22&facet-content'
                           '-type=%22Article%22&facet-language=%22En%22',
        "Chemistry": 'https://link.springer.com/search?facet-discipline=%22Chemistry%22&facet-content-type=%22Article'
                     '%22&facet-language=%22En%22',
        'Medicine': 'https://link.springer.com/search?facet-discipline=%22Medicine+%26+Public+Health%22&facet-content'
                    '-type=%22Article%22&facet-language=%22En%22 '
    }

    data = {}
    for key, url_to_search in urls_to_search.items():
        data[key] = __scrape_over_pages(url_to_search, 50)

    df = []
    for category, abstracts in data.items():
        for abstract in abstracts:
            df.append([category, abstract])

    df = pd.DataFrame(df)
    df.head()
    return df


def __get_abstracts(article_links):
    """

    :param article_links:
    :return:
    """
    abstracts = []
    with tqdm(total=len(article_links)) as progress_bar:
        for link in article_links:
            url = base_url + link['href']
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            abstract = soup.find("div", {"id": "Abs1-content"})
            if abstract is not None:
                abstracts.append(abstract.text)
            progress_bar.update(1)
    return abstracts


def __analyze_page(url):
    """

    :param url:
    :return:
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    article_links = soup.findAll('a', class_="title", href=True)
    next_page_object = soup.findAll('a', class_="next", href=True)
    next_page_link = base_url + next_page_object[0]['href']
    return article_links, next_page_link


def __scrape_over_pages(start_url, number_of_results):
    """

    :param start_url:
    :param number_of_results:
    :return:
    """
    results = []
    url = start_url
    while len(results) < number_of_results:
        article_links, url = __analyze_page(url)
        abstracts = __get_abstracts(article_links)
        results = results + abstracts
    return results
