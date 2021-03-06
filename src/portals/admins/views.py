from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import (
    TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
)

from src.accounts.models import User
from src.portals.admins.dll import QuestionDS
from src.application.models import (
    Article, Subject, Quiz, Question, QuestionStatement, QuestionChoice, QuestionImage, QuestionAudio,
    QuizQuestion, ChoiceVisibility, ImageVisibility, StatementVisibility, AudioVisibility, Screen,
    Relation, Topic, RelationType, StudentGrade, QuizCompleted, LearningResourceResult)
from src.portals.admins.filters import UserFilter
from src.portals.admins.forms import (
    QuestionImageForm, QuestionAudioForm, QuizQuestionForm
)

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]
admin_nocache_decorators = [login_required, user_passes_test(lambda u: u.is_superuser), never_cache]

"""  INIT ------------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserListView(ListView):
    template_name = 'admins/user_list.html'
    queryset = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        user_filter = UserFilter(self.request.GET, queryset=User.objects.exclude(is_superuser=True))
        context['user_filter_form'] = user_filter.form

        paginator = Paginator(user_filter.qs, 10)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['user_list'] = user_page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = self.object
        if user.is_student:
            context['profile'] = user.get_student_profile()
            context['quizzes'] = QuizCompleted.objects.filter(user=user)
            context['learning'] = LearningResourceResult.objects.filter(user=user)
            context['relations'] = Relation.objects.filter(child=user)
        elif user.is_parent:
            relations = Relation.objects.filter(parent=user)
            context['relations'] = relations
            context['relations_total'] = relations.count()
            context['relations_pending'] = relations.filter(is_verified_by_child=False).count()
            context['relations_accepted'] = relations.filter(is_verified_by_child=True).count()
        elif user.is_moderator:
            questions = Question.objects.filter(created_by=user)
            quizzes = Quiz.objects.filter(created_by=user)

            context['questions'] = questions
            context['quizzes'] = quizzes

            context['questions_all'] = questions.count()
            context['single_all'] = quizzes.filter(players='1', learning_purpose=False).count()
            context['learning_all'] = quizzes.filter(learning_purpose=False).count()
            context['team_all'] = quizzes.filter(learning_purpose=False).exclude(players='1').count()

        return context


""" Relations -----------------------------------------------------------"""


@method_decorator(admin_decorators, name='dispatch')
class RelationListView(ListView):
    models = Relation
    queryset = Relation.objects.all()
    template_name = 'admins/relation_list.html'


@method_decorator(admin_decorators, name='dispatch')
class RelationCreateView(CreateView):
    models = Relation
    queryset = Relation.objects.all()
    fields = '__all__'
    template_name = 'admins/relation_create_form.html'
    success_url = reverse_lazy('admin-portal:relation')


@method_decorator(admin_decorators, name='dispatch')
class RelationUpdateView(UpdateView):
    models = Relation
    queryset = Relation.objects.all()
    fields = '__all__'
    template_name = 'admins/relation_create_form.html'
    success_url = reverse_lazy('admin-portal:relation')


@method_decorator(admin_decorators, name='dispatch')
class RelationDeleteView(DeleteView):
    models = Relation
    queryset = Relation.objects.all()
    template_name = 'admins/relation_delete.html'
    success_url = reverse_lazy('admin-portal:relation')


"""  ARTICLES --------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class ArticleListView(ListView):
    models = Article
    queryset = Article.objects.all()
    template_name = 'admins/article_list.html'


@method_decorator(admin_decorators, name='dispatch')
class ArticleDetailView(DetailView):
    models = Article
    queryset = Article.objects.all()
    template_name = 'admins/article_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class ArticleCreateView(CreateView):
    models = Article
    queryset = Article.objects.all()
    fields = '__all__'
    template_name = 'admins/article_create_form.html'
    success_url = reverse_lazy('admin-portal:article')


@method_decorator(admin_decorators, name='dispatch')
class ArticleUpdateView(UpdateView):
    models = Article
    queryset = Article.objects.all()
    fields = '__all__'
    template_name = 'admins/article_create_form.html'
    success_url = reverse_lazy('admin-portal:article')


@method_decorator(admin_decorators, name='dispatch')
class ArticleDeleteView(DeleteView):
    models = Article
    queryset = Article.objects.all()
    template_name = 'admins/article_delete.html'
    success_url = reverse_lazy('admin-portal:article')


"""  SUBJECTS --------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class SubjectListView(ListView):
    models = Subject
    queryset = Subject.objects.all()
    template_name = 'admins/subject_list.html'


@method_decorator(admin_decorators, name='dispatch')
class SubjectDetailView(DetailView):
    models = Subject
    queryset = Subject.objects.all()
    template_name = 'admins/subject_detail.html'


@method_decorator(admin_decorators, name='dispatch')
class SubjectCreateView(CreateView):
    models = Subject
    queryset = Subject.objects.all()
    fields = '__all__'
    template_name = 'admins/subject_create_form.html'
    success_url = reverse_lazy('admin-portal:subject')


@method_decorator(admin_decorators, name='dispatch')
class SubjectUpdateView(UpdateView):
    models = Subject
    queryset = Subject.objects.all()
    fields = '__all__'
    template_name = 'admins/subject_create_form.html'
    success_url = reverse_lazy('admin-portal:subject')


@method_decorator(admin_decorators, name='dispatch')
class SubjectDeleteView(DeleteView):
    models = Subject
    queryset = Subject.objects.all()
    template_name = 'admins/subject_delete.html'
    success_url = reverse_lazy('admin-portal:subject')


"""  TOPICS --------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class TopicListView(ListView):
    models = Topic
    queryset = Topic.objects.all()
    template_name = 'admins/topic_list.html'


@method_decorator(admin_decorators, name='dispatch')
class TopicCreateView(CreateView):
    models = Topic
    queryset = Topic.objects.all()
    fields = '__all__'
    template_name = 'admins/topic_create_form.html'
    success_url = reverse_lazy('admin-portal:topic')


@method_decorator(admin_decorators, name='dispatch')
class TopicUpdateView(UpdateView):
    models = Topic
    queryset = Topic.objects.all()
    fields = '__all__'
    template_name = 'admins/topic_create_form.html'
    success_url = reverse_lazy('admin-portal:topic')


@method_decorator(admin_decorators, name='dispatch')
class TopicDeleteView(DeleteView):
    models = Topic
    queryset = Topic.objects.all()
    template_name = 'admins/Topic_delete.html'
    success_url = reverse_lazy('admin-portal:topic')


"""  RELATION TYPES --------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class RelationTypeListView(ListView):
    models = RelationType
    queryset = RelationType.objects.all()
    template_name = 'admins/relation_type_list.html'


@method_decorator(admin_decorators, name='dispatch')
class RelationTypeCreateView(CreateView):
    models = RelationType
    queryset = RelationType.objects.all()
    fields = '__all__'
    template_name = 'admins/relation_type_create_form.html'
    success_url = reverse_lazy('admin-portal:relation-type')


@method_decorator(admin_decorators, name='dispatch')
class RelationTypeUpdateView(UpdateView):
    models = RelationType
    queryset = RelationType.objects.all()
    fields = '__all__'
    template_name = 'admins/relation_type_create_form.html'
    success_url = reverse_lazy('admin-portal:relation-type')


@method_decorator(admin_decorators, name='dispatch')
class RelationTypeDeleteView(DeleteView):
    models = RelationType
    queryset = RelationType.objects.all()
    template_name = 'admins/relation_type_delete.html'
    success_url = reverse_lazy('admin-portal:relation-type')


"""  GRADES --------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class StudentGradeListView(ListView):
    models = StudentGrade
    queryset = StudentGrade.objects.all()
    template_name = 'admins/student_grade_list.html'


@method_decorator(admin_decorators, name='dispatch')
class StudentGradeCreateView(CreateView):
    models = StudentGrade
    queryset = StudentGrade.objects.all()
    fields = '__all__'
    template_name = 'admins/student_grade_create_form.html'
    success_url = reverse_lazy('admin-portal:studentgrade')


@method_decorator(admin_decorators, name='dispatch')
class StudentGradeUpdateView(UpdateView):
    models = StudentGrade
    queryset = StudentGrade.objects.all()
    fields = '__all__'
    template_name = 'admins/student_grade_update_form.html'
    success_url = reverse_lazy('admin-portal:studentgrade')


@method_decorator(admin_decorators, name='dispatch')
class StudentGradeDeleteView(DeleteView):
    models = StudentGrade
    queryset = StudentGrade.objects.all()
    template_name = 'admins/student_grade_delete.html'
    success_url = reverse_lazy('admin-portal:studentgrade')


""" QUIZ -------------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class QuizListView(ListView):
    queryset = Quiz.objects.all()
    template_name = 'admins/quiz_list.html'


@method_decorator(admin_nocache_decorators, name='dispatch')
class QuizDetailView(DetailView):
    template_name = 'admins/quiz_detail.html'
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        quiz = self.object

        quiz_questions = QuizQuestion.objects.filter(quiz=quiz)
        questions = Question.objects.filter(subject__in=quiz.subjects.all(), age_limit__lte=quiz.age_limit)
        total = questions.count()
        questions = questions.exclude(id__in=quiz_questions.values_list('question__id', flat=True))

        questionsDS = []
        for quiz_question in quiz_questions:

            question_exists = False
            if quiz_question.question in quiz.questions.all():
                question_exists = True

            questionDS = QuestionDS(
                id=quiz_question.pk, question_id=quiz_question.question.pk, question_exists=question_exists,
                level=quiz_question.question.level, subject=quiz_question.question.subject,
                question_type=quiz_question.question.question_type, age_limit=quiz_question.question.age_limit,
                submission_control=quiz_question.submission_control
            )

            for choice_v in ChoiceVisibility.objects.filter(
                    quiz_question=quiz_question, quiz_question__quiz=quiz):
                questionDS.add_choice(
                    id=choice_v.id, description=choice_v.choice.text, is_correct=choice_v.choice.is_correct,
                    screen1=choice_v.screen_1, screen2=choice_v.screen_2, screen3=choice_v.screen_3
                )

            for statement_v in StatementVisibility.objects.filter(
                    quiz_question=quiz_question, quiz_question__quiz=quiz):
                questionDS.add_statment(
                    id=statement_v.id, description=statement_v.statement.statement,
                    screen1=statement_v.screen_1, screen2=statement_v.screen_2, screen3=statement_v.screen_3
                )

            for image_v in ImageVisibility.objects.filter(
                    quiz_question=quiz_question, quiz_question__quiz=quiz):
                if image_v.image.image:
                    questionDS.add_image(
                        id=image_v.id, url=image_v.image.url, image=image_v.image.image.url,
                        screen1=image_v.screen_1, screen2=image_v.screen_2, screen3=image_v.screen_3
                    )
                else:
                    questionDS.add_image(
                        id=image_v.id, url=image_v.image.url, image=None,
                        screen1=image_v.screen_1, screen2=image_v.screen_2, screen3=image_v.screen_3
                    )

            for audio_v in AudioVisibility.objects.filter(
                    quiz_question=quiz_question, quiz_question__quiz=quiz):
                if audio_v.audio.audio:
                    questionDS.add_audio(
                        id=audio_v.id, url=audio_v.audio.url, audio=audio_v.audio.audio.url,
                        screen1=audio_v.screen_1, screen2=audio_v.screen_2, screen3=audio_v.screen_3
                    )
                else:
                    questionDS.add_audio(
                        id=audio_v.id, url=audio_v.audio.url, audio=None,
                        screen1=audio_v.screen_1, screen2=audio_v.screen_2, screen3=audio_v.screen_3
                    )

            questionsDS.append(questionDS)

        context = {
            'questionDS': questionsDS,
            'questions': questions,
            'subjects': quiz.subjects.all(),
            'form': QuizQuestionForm(instance=QuizQuestion.objects.first()),
            'quiz_id': quiz.pk,
            'quiz_title': quiz.title,
            'total': total,
            'selected': quiz.questions.count(),
            'remaining': questions.count(),
            'players': quiz.players,
        }

        return context


@method_decorator(admin_decorators, name='dispatch')
class QuizCreateView(CreateView):
    models = Quiz
    queryset = Quiz.objects.all()
    fields = [
        'thumbnail', 'learning_purpose', 'title', 'description', 'age_limit',
        'subjects', 'grade', 'players', 'start_time', 'end_time',
        'visible_on_home'
    ]
    template_name = 'admins/quiz_create_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if form.instance.learning_purpose:
            form.instance.start_time = timezone.now()
            form.instance.end_time = timezone.now()
        return super(QuizCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin-portal:quiz-detail', kwargs={'pk': self.object.pk})


@method_decorator(admin_decorators, name='dispatch')
class QuizUpdateView(UpdateView):
    models = Quiz
    queryset = Quiz.objects.all()
    fields = [
        'thumbnail', 'learning_purpose', 'title', 'description', 'age_limit', 'subjects',
        'grade', 'players', 'start_time', 'end_time', 'visible_on_home'
    ]
    template_name = 'admins/quiz_update_form.html'

    def get_success_url(self):
        return reverse('admin-portal:quiz-detail', kwargs={'pk': self.object.pk})


@method_decorator(admin_decorators, name='dispatch')
class QuizDeleteView(DeleteView):
    models = Quiz
    queryset = Quiz.objects.all()
    template_name = 'admins/quiz_delete.html'
    success_url = reverse_lazy('admin-portal:quiz')


""" QUESTION ---------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class QuestionListView(ListView):
    models = Question
    queryset = Question.objects.all()
    template_name = 'admins/question_list.html'


@method_decorator(admin_decorators, name='dispatch')
class QuestionDeleteView(DeleteView):
    models = Question
    queryset = Question.objects.all()
    template_name = 'admins/question_delete.html'
    success_url = reverse_lazy('admin-portal:question')


@method_decorator(admin_decorators, name='dispatch')
class QuestionCreateView(View):

    def get(self, request):
        question_subjects = Subject.objects.all()
        question_grade = StudentGrade.objects.all()
        context = {
            'subjects': question_subjects,
            'grades': question_grade,
            'topics': Topic.objects.all()
        }
        return render(request=request, template_name='admins/question_add_form.html', context=context)

    def post(self, request):

        corrects = request.POST.getlist('corrects[]')
        options = request.POST.getlist('options[]')
        topics = request.POST.getlist('topics[]')

        # 1: CREATE QUESTION
        question = Question.objects.create(
            age_limit=request.POST['age'], created_by=request.user,
            subject=Subject.objects.get(pk=request.POST['subject_id']),
            grade=StudentGrade.objects.get(pk=request.POST['grade_id'])
        )

        # 2: CREATE STATEMENTS
        for statement in request.POST.getlist('statements[]'):
            QuestionStatement.objects.create(
                statement=statement,
                question=question
            )

        # 3 CREATE TOPICS
        for topic_id in topics:
            try:
                topic = Topic.objects.get(pk=topic_id)
                question.topics.add(topic)
            except Topic.DoesNotExist:
                continue

        # 4 CREATE OPTIONS
        for index, value in enumerate(options):

            choice = False
            if corrects[index] == '1':
                choice = True

            QuestionChoice.objects.create(
                text=options[index],
                is_correct=choice,
                question=question
            )

        return JsonResponse(data={'message': 'success', 'question': question.pk}, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionUpdateView(View):

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)

        topics_selected = question.topics.all()
        topics = Topic.objects.exclude(pk__in=topics_selected.values_list('pk'))

        context = {
            'statements': QuestionStatement.objects.filter(question=question),
            'choices': QuestionChoice.objects.filter(question=question),
            'images': QuestionImage.objects.filter(question=question),
            'audios': QuestionAudio.objects.filter(question=question),
            'question_id': question.pk,
            'question': question,
            'subjects': Subject.objects.all(),
            'grades': StudentGrade.objects.all(),
            'image_form': QuestionImageForm(),
            'audio_form': QuestionAudioForm(),
            'topics': topics,
            'topics_selected': topics_selected
        }
        return render(request=request, template_name='admins/question_update_form.html', context=context)


""" C-API ------------------------------------------------------------------------- """
""" QUESTION UPDATE RELATED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


@method_decorator(admin_decorators, name='dispatch')
class QuestionStatementAddJSON(View):

    def post(self, request):
        text = request.POST['text']
        # screen = request.POST['screen']
        question_id = request.POST['pk']
        statement = QuestionStatement()
        statement.statement = text
        # statement.screen = Screen.objects.get(no=screen)
        statement.question = Question.objects.get(pk=question_id)
        statement.save()
        response = {
            'statement': text
        }
        return JsonResponse(data=response, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionStatementDeleteJSON(View):

    def get(self, request, pk):
        QuestionStatement.objects.get(pk=pk).delete()
        return JsonResponse(data={"message": "success"}, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionTopicAddJSON(View):

    def post(self, request, question_id):
        message = "Failed Request"
        is_error = True
        try:
            question = Question.objects.get(pk=question_id)
            topic = Topic.objects.get(pk=request.POST['topic'])
            question.topics.add(topic)
            message = "Topic added successfully"
            is_error = False
        except Question.DoesNotExist:
            message = "Question or Topic Doesn't exists"
        except Topic.DoesNotExist:
            message = "Question or Topic Doesn't exists"

        return JsonResponse(data={"message": message, "is_error": is_error}, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionTopicDeleteJSON(View):

    def post(self, request, question_id):
        message = "Failed Request"
        is_error = True
        try:
            question = Question.objects.get(pk=question_id)
            topic = Topic.objects.get(pk=request.POST['topic'])
            question.topics.remove(topic)
            message = "Topic deleted successfully"
            is_error = False
        except Question.DoesNotExist:
            message = "Question or Topic Doesn't exists"
        except Topic.DoesNotExist:
            message = "Question or Topic Doesn't exists"

        return JsonResponse(data={"message": message, "is_error": is_error}, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionChoiceAddJSON(View):

    def post(self, request):
        is_correct = str(request.POST['is_correct']) == 'true'
        question_id = request.POST['pk']
        text = request.POST['text']
        choice = QuestionChoice()
        choice.text = text
        choice.question = Question.objects.get(pk=question_id)
        choice.is_correct = is_correct
        choice.save()
        response = {'choice': text}
        return JsonResponse(data=response, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionChoiceDeleteJSON(View):

    def get(self, request, pk):
        QuestionChoice.objects.get(pk=pk).delete()
        return JsonResponse(data={"message": "success"}, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionImageCreateView(View):

    def post(self, request, question_id):
        form = QuestionImageForm(request.POST, request.FILES)

        if form.is_valid():
            question_ref = Question.objects.get(pk=question_id)
            url = form.cleaned_data['url']
            image = form.cleaned_data['image']

            question_image = QuestionImage.objects.create(
                url=url, image=image, question=question_ref
            )
            question_image.save()
            messages.success(
                request=request, message="Image attached to question Successfully - Redirected to Question Description."
            )
        else:
            messages.error(request=request, message=f'Error in adding images')
        return redirect('admin-portal:question-update', question_id, permanent=True)


@method_decorator(admin_decorators, name='dispatch')
class QuestionAudioCreateView(View):

    def post(self, request, question_id):
        form = QuestionAudioForm(request.POST, request.FILES)

        if form.is_valid():
            question_ref = Question.objects.get(pk=question_id)
            url = form.cleaned_data['url']
            audio = form.cleaned_data['audio']

            question_audio = QuestionAudio.objects.create(
                url=url, audio=audio, question=question_ref
            )
            question_audio.save()
            messages.success(
                request=request, message="Audio attached to question Successfully - Redirected to Question Description."
            )
        else:
            messages.error(request=request, message=f'Error in adding audios')
        return redirect('admin-portal:question-update', question_id, permanent=True)


@method_decorator(admin_decorators, name='dispatch')
class QuestionImageDeleteView(View):

    def get(self, request, pk):
        try:
            question_image = QuestionImage.objects.get(pk=pk)
            question_id = question_image.question.pk
            question_image.delete()

            messages.success(request=request, message=f"Image of Question > {question_id} deleted successfully")
            return redirect('admin-portal:question-update', question_id, permanent=True)
        except QuestionImage.DoesNotExist:
            messages.error(request=request, message=f"Failed To Delete > Requested Image ({pk}) Does not Exist ")

        return redirect('admin-portal:question', permanent=True)


@method_decorator(admin_decorators, name='dispatch')
class QuestionAudioDeleteView(View):

    def get(self, request, pk):
        try:
            question_audio = QuestionAudio.objects.get(pk=pk)
            question_id = question_audio.question.pk
            question_audio.delete()

            messages.success(request=request, message=f"Audio of Question > {question_id} deleted successfully")
            return redirect('admin-portal:question-update', question_id, permanent=True)
        except QuestionAudio.DoesNotExist:
            messages.error(request=request, message=f"Failed To Delete > Requested audio ({pk}) Does not Exists")

        return redirect('admin-portal:question', permanent=True)


""" QUESTION DETAIL RELATED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


@method_decorator(admin_decorators, name='dispatch')
class QuestionStatementStatusUpdateJSON(View):

    def post(self, request, pk):
        success = False
        message = "Failed to update record"
        screen_id = request.POST['screen_id']
        status = request.POST['is_checked']
        status = True if status == 'true' else False

        # STATEMENT VISIBILITY CHANGE
        try:
            statement_visibility = StatementVisibility.objects.get(pk=pk)
            if screen_id == '1':
                statement_visibility.screen_1 = status
            elif screen_id == '2':
                statement_visibility.screen_2 = status
            elif screen_id == '3':
                statement_visibility.screen_3 = status
            statement_visibility.save()

            message = "Record updated successfully"
            success = True
        except StatementVisibility.DoesNotExist:
            message = "This question is not associated with Quiz"
            success = False

        context = {'success': success, 'message': message}
        return JsonResponse(data=context, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionChoiceStatusUpdateJSON(View):

    def post(self, request, pk):
        success = False
        message = "Failed to update record"
        screen_id = request.POST['screen_id']
        status = request.POST['is_checked']
        status = True if status == 'true' else False

        try:
            choice_visibility = ChoiceVisibility.objects.get(pk=pk)
            if screen_id == '1':
                choice_visibility.screen_1 = status
            elif screen_id == '2':
                choice_visibility.screen_2 = status
            elif screen_id == '3':
                choice_visibility.screen_3 = status
            choice_visibility.save()

            message = "Record updated successfully"
            success = True
        except ChoiceVisibility.DoesNotExist:
            message = "This question is not associated with quiz"
            success = False

        context = {'success': success, 'message': message}
        return JsonResponse(data=context, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionAudioStatusUpdateJSON(View):

    def post(self, request, pk):
        success = False
        message = "Failed to update record"
        screen_id = request.POST['screen_id']
        status = request.POST['is_checked']
        status = True if status == 'true' else False

        try:
            audio_visibility = AudioVisibility.objects.get(pk=pk)
            if screen_id == '1':
                audio_visibility.screen_1 = status
            elif screen_id == '2':
                audio_visibility.screen_2 = status
            elif screen_id == '3':
                audio_visibility.screen_3 = status
            audio_visibility.save()

            message = "Record updated successfully"
            success = True
        except AudioVisibility.DoesNotExist:
            message = "Not associated with Quiz"
            success = False

        context = {'success': success, 'message': message}
        return JsonResponse(data=context, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionImageStatusUpdateJSON(View):

    def post(self, request, pk):
        success = False
        message = "Failed to update record"
        screen_id = request.POST['screen_id']
        status = request.POST['is_checked']
        status = True if status == 'true' else False

        try:
            image_visibility = ImageVisibility.objects.get(pk=pk)
            if screen_id == '1':
                image_visibility.screen_1 = status
            elif screen_id == '2':
                image_visibility.screen_2 = status
            elif screen_id == '3':
                image_visibility.screen_3 = status
            image_visibility.save()

            message = "Record updated successfully"
            success = True

        except ImageVisibility.DoesNotExist:
            message = "Not associated with quiz"
            success = False

        context = {'success': success, 'message': message}
        return JsonResponse(data=context, safe=False)


@method_decorator(admin_decorators, name='dispatch')
class QuestionSubmitStatusUpdateJSON(View):

    def post(self, request, pk):
        success = False
        message = "Failed to update record"

        # POST METHOD HERE
        screen_id = request.POST['screen_id']

        # STATEMENT VISIBILITY CHANGE
        question = QuizQuestion.objects.get(pk=pk)
        if screen_id == '1':
            question.submission_control = Screen.objects.first()
        elif screen_id == '2':
            question.submission_control = Screen.objects.all()[1]
        elif screen_id == '3':
            question.submission_control = Screen.objects.last()
        question.save()

        # EXTRA DATA HERE
        message = "Record updated successfully"
        success = True

        context = {'success': success, 'message': message}
        return JsonResponse(data=context, safe=False)


@method_decorator(admin_nocache_decorators, name='dispatch')
class QuizQuestionAddJSON(View):

    def get(self, request, quiz_id, question_id):

        try:
            quiz = Quiz.objects.get(pk=quiz_id)
            question = Question.objects.get(pk=question_id)

        except [Quiz.DoesNotExist, Question.DoesNotExist]:
            messages.error(request=request, message=f'Requested Quiz or Question Does not Exists.')
            return redirect('admin-portal:quiz-create')

        # ALREADY ASSOCIATED OR NOT ---------------------------------
        if quiz.questions.filter(pk=question_id):
            messages.warning(request=request,
                             message=f'Failed to add > Requested Question [ID: {question_id}] already associated with this quiz.')
        else:
            messages.success(request=request, message=f'Requested Question [ID: {question_id}] added successfully.')

            # STEP1 => Add Question to Quiz
            quiz.questions.add(question)
            quiz.save()

            quiz_question = QuizQuestion.objects.filter(question=question, quiz=quiz)[0]

            # STEP2 => Add Statements Visibility
            for statement in question.questionstatement_set.all():
                StatementVisibility(
                    quiz_question=quiz_question, statement=statement
                ).save()

            # STEP3 => Add Choices Visibility
            for choice in question.questionchoice_set.all():
                ChoiceVisibility(
                    quiz_question=quiz_question, choice=choice
                ).save()

            # STEP3 => Add Images Visibility
            for image in question.questionimage_set.all():
                ImageVisibility(
                    quiz_question=quiz_question, image=image
                ).save()

            # STEP4 => Add audios Visibility
            for audio in question.questionaudio_set.all():
                AudioVisibility(
                    quiz_question=quiz_question, audio=audio
                ).save()

            # TODO: statistics for quiz -----------------------------------------------------
            if quiz.learning_purpose:
                question.total_times_used_in_learning = question.total_times_used_in_learning + 1
            else:
                question.total_times_used_in_quizzes = question.total_times_used_in_quizzes + 1
            question.save()
            # -------------------------------------------------------------------------------

        return redirect('admin-portal:quiz-update', quiz_id, permanent=True)


@method_decorator(admin_nocache_decorators, name='dispatch')
class QuizQuestionDeleteJSON(View):

    def get(self, request, quiz_id, question_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
            question = Question.objects.get(pk=question_id)

            quiz.questions.remove(question)
            messages.success(request=request, message=f'Requested Question [ID: {question_id}] deleted successfully.')

            # TODO: statistics for quiz -----------------------------------------------------
            if quiz.learning_purpose:
                question.total_times_used_in_learning = question.total_times_used_in_learning - 1
                if question.total_times_used_in_learning < 0:
                    question.total_times_used_in_learning = 0
            else:
                question.total_times_used_in_quizzes = question.total_times_used_in_quizzes - 1
                if question.total_times_used_in_quizzes < 0:
                    question.total_times_used_in_quizzes = 0
            question.save()
            # -------------------------------------------------------------------------------
            return redirect('admin-portal:quiz-update', quiz_id, permanent=True)
        except [Quiz.DoesNotExist, Question.DoesNotExist]:
            messages.error(request=request, message=f'Requested Quiz or Question Does not Exists.')
            return HttpResponseRedirect(reverse('admin-portal:quiz-create'))


""" CHNAGE ====================================================================================================== """
