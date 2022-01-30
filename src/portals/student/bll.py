from src.accounts.models import User
from src.application.models import Team


def get_user_with_username(username):

    users = User.objects.filter(username=username)
    return users[0] if users else None


def is_participation_already_enrolled(player, quiz):
    teams = Team.objects.filter(participants__username=player.username, quiz=quiz)
    return True if teams else False


def quiz_enrollment_logic():
    pass


def question_grading_logic(question):
    total_attempts = question.total_times_attempted_in_quizzes
    total_correct = question.total_times_correct_in_quizzes

    result = (total_correct/total_attempts)*100
    if result >= 85:
        question.level = 'e'
    elif 60 <= result < 85:
        question.level = 'n'
    elif result < 60:
        question.level = 'h'

    question.save()
