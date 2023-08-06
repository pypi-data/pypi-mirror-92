import requests

class YoutubeDataApiV3Manager:
    def __init__(self, *args, **kwargs):
        self.key = kwargs["key"]
        self.max_results = 10
        self.part = "snippet"

    def search(self, headers, keyword):
        base_url = "https://www.googleapis.com/"
        prefix = "youtube/v3/search/"
        queries = f"?part={self.part}&maxResults={self.max_results}&key={self.key}&q={keyword}"
        full_url = base_url + prefix + queries
        return requests.get(full_url, headers=headers)
