from django.shortcuts import redirect
from django.views import View


class CrossAuthView(View):

    def get(self, request):
        if request.user.is_superuser:
            return redirect('admin-portal:dashboard')
        else:
            return redirect('student-portal:dashboard')

