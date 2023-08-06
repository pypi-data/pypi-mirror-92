from django.urls import path

from .api_views import LemmaResearchView


urlpatterns = [
    path(r"lemmaresearch/", LemmaResearchView.as_view()),
    path(r"lemmaresearch/<crawlerid>/", LemmaResearchView),
]