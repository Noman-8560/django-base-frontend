from django.shortcuts import redirect, render
from django.views import View


class CrossAuthView(View):

    def get(self, request):

        if not request.user.is_completed:
            return redirect('accounts:identification-check')

        if request.user.is_superuser:
            return redirect('admin-portal:dashboard')
        else:
            return redirect('student-portal:dashboard')


class IdentificationCheckView(View):

    def get(self, request):
        return render(request, 'accounts/identification-check.html')

    def post(self, request):
        return render(request, 'accounts/identification-check.html')
