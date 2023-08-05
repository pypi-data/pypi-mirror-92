from django.urls import path
import api_views

app_name = "apis_research"

urlpatterns = [
    path("lemmaresearch/", api_views.LemmaResearchView),
    path("lemmaresearch/<crawlerid>/", api_views.LemmaResearchView)
]