from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question
# Create your views here.

class HomeView(generic.ListView):
	template_name = "polls/home.html"
	context_object_name = "latest_question_list"

	def get_queryset(self):
		""" Returns the last five published question """
		return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = "polls/detail.html"


class ResultView(generic.DetailView):
	model = Question
	template_name = "polls/results.html"


def vote(request, question_id, **kwargs):
	question = get_object_or_404(Question, pk=question_id)
	# if "choice" in request.POST:
	try:
		selected_choice = question.choice_set.get(pk=request.POST["choice"])
	except (KeyError, Choice.DoesNotExist):
		return render(request, "polls/detail.html", {
				"question": question,
				"error_message": "You didn't select a choice",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse("polls:results", args=(question.id, )))
	# else:
	# 	return render(request, "polls/detail.html", {
	# 				"question": question,
	# 				"error_message": "You didn't select a choice",
	# 			})
