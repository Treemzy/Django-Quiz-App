from django.urls import include, path
from .views import classroom, students, teachers
from .view import SubjectCreateView, SubjectListView, SubjectUpdateView, SubjectDeleteView

urlpatterns = [
    path('', classroom.home, name='home'),
    path('subjects/', SubjectListView.as_view(), name='Index'),
    path('subjects/new/', SubjectCreateView.as_view(), name='Create'),
    path('subjects/<int:pk>/update/', SubjectUpdateView.as_view(), name='Edit'),
    path('subjects/<int:pk>/delete/', SubjectDeleteView.as_view(), name='Delete'),

    path('students/', include(([
        path('', students.QuizListView.as_view(), name='quiz_list'),
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
    ], 'AppQuiz'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'AppQuiz'), namespace='teachers')),
]
