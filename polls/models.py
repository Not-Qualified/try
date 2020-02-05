import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=150)
	pub_date = models.DateTimeField("date published")

	def was_published_recently(self):
		current = timezone.now()
		one_day_delta = datetime.timedelta(days=1)
		return ( current - one_day_delta <= self.pub_date <= current )


	def __str__(self):
		return f"{self.question_text}"


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=50)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.choice_text}"