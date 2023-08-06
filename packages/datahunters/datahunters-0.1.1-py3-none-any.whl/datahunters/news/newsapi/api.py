"""API wrapper for news api.
"""

from newsapi import NewsApiClient

from datahunters.news.base import Article, NewsAPIBase


def article_from_newsapi_res(res_json):
  """Convert newsapi response to article object.
  """
  article = Article()
  article.title = res_json["title"]
  article.description = res_json["description"]
  article.author = res_json["author"]
  article.url = res_json["url"]
  article.cover_img_url = res_json["urlToImage"]
  article.publish_date = res_json["publishedAt"]
  article.source = res_json["source"]["name"]
  return article


class NewsAPI(NewsAPIBase):
  """Class for news api.

  https://newsapi.org/
  """
  API_KEY = "ae2d6e0ba8454c6a8eb11f3e1362b7ec"
  BASE_URL = "https://newsapi.org/v2"
  client = None

  def __init__(self):
    self.client = NewsApiClient(api_key=self.API_KEY)

  def search_headlines(self,
                       query,
                       sources=None,
                       category=None,
                       language="en",
                       country="us",
                       limit=50,
                       page=1):
    """Retrieve headlines.
    """
    headlines = self.client.get_top_headlines(q=query,
                                              sources=sources,
                                              category=category,
                                              language=language,
                                              country=country,
                                              page_size=limit,
                                              page=page)
    articles = [article_from_newsapi_res(x) for x in headlines["articles"]]
    return articles

  def search_articles(self,
                      query,
                      sources=None,
                      domains=None,
                      date_from=None,
                      date_to=None,
                      language="en",
                      country="us",
                      limit=100,
                      page=1,
                      sort_by="publishedAt"):
    """Retrieve articles.
    """
    res = self.client.get_everything(q=query,
                                     sources=sources,
                                     domains=domains,
                                     from_param=date_from,
                                     to=date_to,
                                     page_size=limit,
                                     page=page,
                                     language=language,
                                     sort_by=sort_by)
    articles = [article_from_newsapi_res(x) for x in res["articles"]]
    return articles


if __name__ == "__main__":
  api = NewsAPI()
  articles = api.search_headlines("computer vision",
                                  category="technology",
                                  limit=10)
  print(articles[0].to_json())