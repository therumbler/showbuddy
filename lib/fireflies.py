import json
from urllib.request import Request, urlopen


class Fireflies:
    """Fireflies class"""

    def __init__(self, api_key):
        self._api_key = api_key

    def _fetch(self, query):
        url = "https://api.fireflies.ai/graphql"
        data = {"query": query}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        req = Request(url, data=json.dumps(data).encode(), headers=headers)
        with urlopen(req) as response:
            return json.load(response)

    def fetch_user(self):
        query = "{ users { name user_id } }"
        return self._fetch(query)


def main():
    """let's kick this off"""
    import os

    api_key = os.environ["FIREFLIES_API_KEY"]
    fireflies = Fireflies(api_key)
    print(fireflies.fetch_user())


if __name__ == "__main__":
    main()
