from django.test import TestCase
import datetime

from django.utils import timezone
from django.core.urlresolvers import reverse

from .models import Question

class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertEqual(future_question.was_published_recently(), False)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exists, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('health_graph:index'))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "No health_graph are available.")

        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('health_graph:index'))
        #self.assertContains(response, "No health_graph are available.", status_code=200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

# Create your tests here.
