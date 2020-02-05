from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
	path("", views.HomeView.as_view(), name="home"),
	path("<int:pk>/", views.DetailView.as_view(), name="detail"),
	path("result/<int:pk>/", views.ResultView.as_view(), name="results"),
	path("vote/<int:question_id>/", views.vote, name="vote"),
]