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
