import requests
import json
import datetime

class CyberThreatIntel:
    def __init__(self):
        self.bing_api_key = "YOUR_BING_API_KEY"
        self.google_api_key = "YOUR_GOOGLE_API_KEY"
        self.google_cx = "YOUR_GOOGLE_CX"

    def search_bing(self, query):
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": self.bing_api_key}
        params = {"q": query, "count": 10, "responseFilter": "Webpages"}
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def search_google(self, query):
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.google_api_key,
            "cx": self.google_cx,
            "q": query,
            "num": 10,
        }
        response = requests.get(url, params=params)
        return response.json()

    def get_recent_articles(self, search_engine):
        articles = []
        if search_engine == "bing":
            response = self.search_bing("cyber threats")
            print("Bing response:", response)  # Print the Bing response
            if "webPages" in response and "value" in response["webPages"]:
                articles = [
                    {"title": item["name"], "link": item["url"]}
                    for item in response["webPages"]["value"]
                ]
        elif search_engine == "google":
            response = self.search_google("cyber threats")
            print("Google response:", response)  # Print the Google response
            if "items" in response:
                articles = [
                    {"title": item["title"], "link": item["link"]}
                    for item in response["items"]
                ]
        return articles

    def get_articles(self):
        bing_articles = self.get_recent_articles("bing")
        google_articles = self.get_recent_articles("google")
        return bing_articles + google_articles

    def create_summary(self, articles):
        summary = []

        for article in articles:
            summary.append({"title": article["title"], "link": article["link"]})

        return summary

if __name__ == "__main__":
    cti = CyberThreatIntel()
    articles = cti.get_articles()
    summary = cti.create_summary(articles)

    print("Summary:", summary)  # Print the summary before saving to file

    with open("summary.json", "w") as f:
        json.dump(summary, f, indent=4)
