from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import (
    ListView, UpdateView, DeleteView, CreateView, DetailView,
    TemplateView)

from src.accounts.decorators import moderator_required, identification_required
from src.application.forms import QuestionImageForm
from src.application.models import (
    Quiz, QuizQuestion, Question, ChoiceVisibility, StatementVisibility, ImageVisibility,
    AudioVisibility,
    Subject, QuestionStatement, QuestionChoice, QuestionAudio, QuestionImage, Screen, Topic)
from src.portals.admins.dll import QuestionDS
from src.portals.admins.forms import QuizQuestionForm, QuestionAudioForm


moderator_decorators = [moderator_required, identification_required]
moderator_nocache_decorators = [moderator_required, identification_required, never_cache]


@method_decorator(moderator_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'moderator/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


""" QUIZ """
@method_decorator(moderator_decorators, name='dispatch')
class QuizListView(ListView):
    models = Quiz
    template_name = 'moderator/quiz_list.html'

    def get_queryset(self):
        return Quiz.objects.filter(created_by=self.request.user)


@method_decorator(moderator_decorators, name='dispatch')
class QuizCreateView(CreateView):
    models = Quiz
    queryset = Quiz.objects.all()
    fields = ['learning_purpose', 'title', 'age_limit', 'subjects', 'players', 'start_time', 'end_time']
    template_name = 'moderator/quiz_create_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=True)
        quiz.created_by = self.request.user
        quiz.save()
        return super(QuizCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('moderator-portal:quiz-detail', kwargs={'pk': self.object.pk})


@method_decorator(moderator_decorators, name='dispatch')
class QuizUpdateView(UpdateView):
    models = Quiz
    fields = ['learning_purpose', 'title', 'age_limit', 'subjects', 'players', 'start_time', 'end_time']
    template_name = 'moderator/quiz_update_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Quiz.objects.filter(created_by=self.request.user), pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('moderator-portal:quiz-detail', kwargs={'pk': self.object.pk})


@method_decorator(moderator_decorators, name='dispatch')
class QuizDeleteView(DeleteView):
    models = Quiz
    template_name = 'moderator/quiz_delete.html'
    success_url = reverse_lazy('moderator-portal:quiz')

    def get_object(self, queryset=None):
        return get_object_or_404(Quiz.objects.filter(created_by=self.request.user), pk=self.kwargs['pk'])


@method_decorator(moderator_nocache_decorators, name='dispatch')
class QuizDetailView(DetailView):
    template_name = 'moderator/quiz_detail.html'
    model = Quiz

    def get_object(self, queryset=None):
        return get_object_or_404(Quiz.objects.filter(created_by=self.request.user), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        quiz = self.get_object()

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


""" QUESTION """


@method_decorator(moderator_decorators, name='dispatch')
class QuestionListView(ListView):
    models = Question
    template_name = 'moderator/question_list.html'

    def get_queryset(self):
        return Question.objects.filter(created_by=self.request.user)


@method_decorator(moderator_decorators, name='dispatch')
class QuestionDeleteView(DeleteView):
    models = Question
    template_name = 'moderator/question_delete.html'
    success_url = reverse_lazy('moderator-portal:question')

    def get_object(self, queryset=None):
        return get_object_or_404(Question.objects.filter(
            created_by=self.request.user), pk=self.kwargs.get('pk'))


@method_decorator(moderator_decorators, name='dispatch')
class QuestionCreateView(View):

    def get(self, request):
        question_subjects = Subject.objects.all()
        context = {'subjects': question_subjects, 'topics': Topic.objects.all()}
        return render(request=request, template_name='moderator/question_add_form.html', context=context)

    def post(self, request):
        topics = request.POST.getlist('topics[]')
        corrects = request.POST.getlist('corrects[]')
        options = request.POST.getlist('options[]')

        # 1: CREATE QUESTION
        question = Question.objects.create(
            age_limit=request.POST['age'],
            subject=Subject.objects.get(pk=request.POST['subject_id']), created_by=request.user
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


@method_decorator(moderator_decorators, name='dispatch')
class QuestionUpdateView(View):

    def get(self, request, pk):

        question = get_object_or_404(Question.objects.filter(created_by=request.user), pk=pk)
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
            'image_form': QuestionImageForm(),
            'audio_form': QuestionAudioForm(),
            'topics': topics,
            'topics_selected': topics_selected
        }
        return render(request=request, template_name='moderator/question_update_form.html', context=context)
    
    
""" C-API ------------------------------------------------------------------------- """
""" QUESTION UPDATE RELATED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


@method_decorator(moderator_decorators, name='dispatch')
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


@method_decorator(moderator_decorators, name='dispatch')
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


@method_decorator(moderator_decorators, name='dispatch')
class QuestionStatementDeleteJSON(View):

    def get(self, request, pk):
        QuestionStatement.objects.get(pk=pk).delete()
        return JsonResponse(data={"message": "success"}, safe=False)


@method_decorator(moderator_decorators, name='dispatch')
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


@method_decorator(moderator_decorators, name='dispatch')
class QuestionChoiceDeleteJSON(View):

    def get(self, request, pk):
        QuestionChoice.objects.get(pk=pk).delete()
        return JsonResponse(data={"message": "success"}, safe=False)


@method_decorator(moderator_decorators, name='dispatch')
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
        return redirect('moderator-portal:question-update', question_id, permanent=True)


@method_decorator(moderator_decorators, name='dispatch')
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
        return redirect('moderator-portal:question-update', question_id, permanent=True)


@method_decorator(moderator_decorators, name='dispatch')
class QuestionImageDeleteView(View):

    def get(self, request, pk):
        try:
            question_image = QuestionImage.objects.get(pk=pk)
            question_id = question_image.question.pk
            question_image.delete()

            messages.success(request=request, message=f"Image of Question > {question_id} deleted successfully")
            return redirect('moderator-portal:question-update', question_id, permanent=True)
        except QuestionImage.DoesNotExist:
            messages.error(request=request, message=f"Failed To Delete > Requested Image ({pk}) Does not Exist ")

        return redirect('moderator-portal:question', permanent=True)


@method_decorator(moderator_decorators, name='dispatch')
class QuestionAudioDeleteView(View):

    def get(self, request, pk):
        try:
            question_audio = QuestionAudio.objects.get(pk=pk)
            question_id = question_audio.question.pk
            question_audio.delete()

            messages.success(request=request, message=f"Audio of Question > {question_id} deleted successfully")
            return redirect('moderator-portal:question-update', question_id, permanent=True)
        except QuestionAudio.DoesNotExist:
            messages.error(request=request, message=f"Failed To Delete > Requested audio ({pk}) Does not Exists")

        return redirect('moderator-portal:question', permanent=True)


""" QUESTION DETAIL RELATED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


@method_decorator(moderator_decorators, name='dispatch')
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


@method_decorator(moderator_decorators, name='dispatch')
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


@method_decorator(moderator_decorators, name='dispatch')
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


@method_decorator(moderator_decorators, name='dispatch')
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


@method_decorator(moderator_decorators, name='dispatch')
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


@method_decorator(moderator_nocache_decorators, name='dispatch')
class QuizQuestionAddJSON(View):

    def get(self, request, quiz_id, question_id):

        try:
            quiz = Quiz.objects.get(pk=quiz_id)
            question = Question.objects.get(pk=question_id)

        except [Quiz.DoesNotExist, Question.DoesNotExist]:
            messages.error(request=request, message=f'Requested Quiz or Question Does not Exists.')
            return redirect('moderator-portal:quiz-create')

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
            question.total_times_used_in_quizzes = question.total_times_used_in_quizzes + 1
            question.save()
            # -------------------------------------------------------------------------------

        return redirect('moderator-portal:quiz-update', quiz_id, permanent=True)


@method_decorator(moderator_nocache_decorators, name='dispatch')
class QuizQuestionDeleteJSON(View):

    def get(self, request, quiz_id, question_id):
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
            question = Question.objects.get(pk=question_id)

            quiz.questions.remove(question)
            messages.success(request=request, message=f'Requested Question [ID: {question_id}] deleted successfully.')

            # TODO: statistics for quiz -----------------------------------------------------
            question.total_times_used_in_quizzes = question.total_times_used_in_quizzes - 1
            if question.total_times_used_in_quizzes < 0:
                question.total_times_used_in_quizzes = 0
            question.save()
            # -------------------------------------------------------------------------------

            return redirect('moderator-portal:quiz-update', quiz_id, permanent=True)
        except [Quiz.DoesNotExist, Question.DoesNotExist]:
            messages.error(request=request, message=f'Requested Quiz or Question Does not Exists.')
            return HttpResponseRedirect(reverse('moderator-portal:quiz-create'))


""" CHNAGE ====================================================================================================== """
