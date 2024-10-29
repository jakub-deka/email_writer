import json
import requests
from functools import cached_property
import diskcache as dc
from IPython.display import Markdown, display


class MicrolinkClient:

    def __init__(self, cache_dir: str = "./cache_microlinkclient"):
        self.cache = dc.Cache(cache_dir)
        self.base_url = "https://api.microlink.io"

    def get_info(self, url: str):
        if url in self.cache:
            print("Using cache...")
            return self.cache[url]

        params = {"url": url, "palette": True}
        response = requests.get(self.base_url, params).json()
        if response["status"] != "fail":
            self.cache[url] = response
            return response
        else:
            raise Exception(
                f"Call returned failed status with following response {response}"
            )

    def get_palette(self, url: str):
        info = self.get_info(url)
        return info["data"]["logo"]["palette"]

    def print_palette_in_jupyter(self, url: str):
        palette = self.get_palette(url)
        t = [
            f'<span style="font-family: monospace">{color} <span style="color: {color}">████████</span></span><br>'
            for color in palette
        ]
        display(Markdown("".join(t)))
