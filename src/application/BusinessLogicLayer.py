

def identify_user_in_team(team, request, quiz):

    if quiz.players == '3':
        if team.participants.first() == request.user:
            return 1
        elif team.participants.last() == request.user:
            return 3
        else:
            return 2

    elif quiz.players == '2':
        if team.participants.first() == request.user:
            return 1
        else:
            return 2
    else:
        return 1


def is_guardian(user):
    return user.email.endswith('@example.com')


