from rest_framework.routers import DefaultRouter
from bluedot_rest_framework import import_string

Question = import_string('question.views')
QuestionUserView = import_string('question.user_views')


router = DefaultRouter(trailing_slash=False)
router.register(r'questionnaire/user', QuestionUserView,
                basename='questionnaire-user')
router.register(r'questionnaire', Question, basename='questionnaire')

urlpatterns = router.urls
