from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from News.models import News
from News.serializer import NewsSerializer
import requests
from drf_spectacular.utils import extend_schema, OpenApiParameter

API_KEY = "e17836aab9e24c0484f75501606c3a77"

@extend_schema(tags=['News'])
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    @extend_schema(
        methods=["GET"],
        parameters=[
            OpenApiParameter(name='q', description='Search query', required=False, type=str)
        ],
        description="Fetch news from NewsAPI and store it in the database."
    )
    @action(detail=False, methods=["get"], url_path='fetch-news')
    def fetch_news(self, request):
        query = request.query_params.get("q", "technology")
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch news"}, status=status.HTTP_400_BAD_REQUEST)

        data = response.json()
        articles = data.get("articles", [])
        for article in articles:
            News.objects.create(
                name=article.get("source", {}).get("name", "Unknown"),
                url=article.get("url"),
                category=query,
                language="en",
                logo_url=article.get("urlToImage"),
            )
        return Response({"message": f"{len(articles)} articles saved."})
