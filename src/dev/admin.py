from django.contrib import admin
from .models import (
    DevelopmentIteration, DevelopmentFeedback,
    DevelopmentDiscussion, DevelopmentDiscussionAnswer,
    DevelopmentProject
)


admin.site.register(DevelopmentProject)
admin.site.register(DevelopmentIteration)
admin.site.register(DevelopmentDiscussion)
admin.site.register(DevelopmentDiscussionAnswer)
admin.site.register(DevelopmentFeedback)

'''_______________________________________________________________________________________________________________'''
