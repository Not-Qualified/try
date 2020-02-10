import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

# Create your tests here.
class QuestionModelTests(TestCase):
	def test_was_published_recently_with_future_question(self):
		"""Future Question Test - was_published_recently() returns False for Question whose Published Date is in future
		"""
		time = timezone.now()+datetime.timedelta(days=30)
		future_question = Question(pub_date=time)

		self.assertIs(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""Old Question Test - Returns False if Question in Older than one Day
		"""
		time = timezone.now() - datetime.timedelta(days=1, seconds=1)
		old_question = Question(pub_date=time)

		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_with_recent_question(self):
		"""Recent Question Test - Returns True if Question is within One Day Posted
		"""

		time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
		recent_question = Question(pub_date=time)

		self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
	"""Creating Question with question_text and days with offset to "now"
	If Number of Days in Positive, The Question is set to be for Future,
	or else Negetive Days will set it to past dates
	"""

	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionHomeViewTest(TestCase):
	def test_no_questions(self):
		"""If No Questions are there message to be Printed """

		response = self.client.get(reverse("polls:home"))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No Questions available")

		self.assertQuerysetEqual(response.context["latest_question_list"], [])


	def test_past_question(self):
		"""If Question's pub_date is in past then it should've been displayed """
		create_question(question_text="Question", days=-30)

		response = self.client.get(reverse("polls:home"))
		self.assertQuerysetEqual(
			response.context["latest_question_list"],
			["<Question: Question>"])

	def test_future_question(self):
		"""If Question's pub_date is in future then they shouldn't have to be displayed """

		create_question(question_text="Question", days=30)

		response = self.client.get(reverse("polls:home"))
		self.assertContains(response, "No Questions available")

		self.assertQuerysetEqual(response.context["latest_question_list"], [])

	def test_future_question_and_past_question(self):
		""" Even if Both Past & Future's Question available only Past One need to be Displayed """

		create_question(question_text="Future Question", days=30)
		create_question(question_text="Past Question", days=-30)

		response = self.client.get(reverse("polls:home"))
		self.assertQuerysetEqual(
			response.context["latest_question_list"],
			["<Question: Past Question>"]
			)

	def test_two_past_questions(self):
		""" Even if Both Past & Future's Question available only Past One need to be Displayed """

		create_question(question_text="Past Question", days=-30)
		create_question(question_text="Past Question", days=-7)

		response = self.client.get(reverse("polls:home"))
		self.assertQuerysetEqual(
			response.context["latest_question_list"],
			["<Question: Past Question>", "<Question: Past Question>"]
			)

class QuestionDetailViewTests(TestCase):
	def test_future_question(self):
		""" The Detail view of pub_date with future date will Return 404 Page Not Found Error """

		future_question = create_question(question_text="Future Question", days=30)
		response = self.client.get(reverse("polls:detail", args=(future_question.id, )))

		self.assertEqual(response.status_code, 404)

	def test_past_question(self):
		""" The Detail View of Past Question's contain Question text """

		past_question = create_question(question_text="Past Question", days=-5)

		response = self.client.get(reverse("polls:detail", args=(past_question.id, )))

		self.assertContains(response, past_question.question_text)