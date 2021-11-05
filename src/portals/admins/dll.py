class StatementDS:
    def __init__(self, id, description, screen1, screen2, screen3):
        self.id = id
        self.description = description
        self.screen1 = screen1
        self.screen2 = screen2
        self.screen3 = screen3


class ChoiceDS:
    def __init__(self, id, description, is_correct, screen1, screen2, screen3):
        self.id = id
        self.description = description
        self.is_correct = is_correct
        self.screen1 = screen1
        self.screen2 = screen2
        self.screen3 = screen3


class ImageDS:
    def __init__(self, id, url, image, screen1, screen2, screen3):
        self.id = id
        self.url = url
        self.image = image
        self.screen1 = screen1
        self.screen2 = screen2
        self.screen3 = screen3


class AudioDS:
    def __init__(self, id, url, audio, screen1, screen2, screen3):
        self.id = id
        self.url = url
        self.audio = audio
        self.screen1 = screen1
        self.screen2 = screen2
        self.screen3 = screen3


class QuestionDS:
    def __init__(self, id, question_id, question_exists, level, subject, question_type, submission_control, age_limit):
        self.id = id
        self.question_id = question_id
        self.question_exists = question_exists
        self.level = level
        self.subject = subject
        self.question_type = question_type
        self.age_limit = age_limit
        self.submission_control = submission_control
        self.choices = []
        self.statements = []
        self.images = []
        self.audios = []

    def add_choice(self, id, description, is_correct, screen1, screen2, screen3):
        self.choices.append(
            ChoiceDS(
                id=id, description=description, is_correct=is_correct,
                screen1=screen1, screen2=screen2, screen3=screen3
            )
        )

    def add_statment(self, id, description, screen1, screen2, screen3):
        self.statements.append(
            StatementDS(
                id=id, description=description,
                screen1=screen1, screen2=screen2, screen3=screen3
            )
        )

    def add_image(self, id, url, image, screen1, screen2, screen3):
        self.images.append(
            ImageDS(
                id=id, url=url, image=image,
                screen1=screen1, screen2=screen2, screen3=screen3
            )
        )

    def add_audio(self, id, url, audio, screen1, screen2, screen3):
        self.audios.append(
            AudioDS(
                id=id, url=url, audio=audio,
                screen1=screen1, screen2=screen2, screen3=screen3
            )
        )