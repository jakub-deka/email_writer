from haystack.components.fetchers import LinkContentFetcher

urls = [
    "https://www.118118money.com/",
    "https://jaja.co.uk/",
    "https://uk.virginmoney.com/",
]

fetcher = LinkContentFetcher()
fetcher_res = fetcher.run(urls=urls)
print(fetcher_res)
