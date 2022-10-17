# perfect-crawler
Trying to create the perfect crawler for my projects

It is pretty simples to use:
```
# If we are trying to crawl google.com for example
with Crawler() as crawler:
        print(crawler.get("https://www.google.com/"))
        print(crawler.content)  # returns the HTML
        print(crawler.status_code)  # status code (ex: 200, 404, 503)
        print(crawler.cookies)  # cookies
```
