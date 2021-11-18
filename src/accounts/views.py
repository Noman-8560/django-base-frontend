from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):

    def get(self, request):

        if not request.user.is_completed:
            return redirect('accounts:identification-check')

        if request.user.is_superuser:
            return redirect('admin-portal:dashboard')
        else:
            return redirect('student-portal:dashboard')


@method_decorator(login_required, name='dispatch')
class IdentificationCheckView(View):

    def get(self, request):

        # IS USER ALREADY IDENTIFIED
        if request.user.is_completed:
            return redirect('accounts:cross-auth-view')

        return render(request, 'accounts/identification-check.html')

    def post(self, request):

        # IF USER ALREADY IDENTIFIED
        if request.user.is_completed:
            return redirect('accounts:cross-auth-view')

        # IF USER HAS TYPE
        if request.POST['user_type']:
            user_type = request.POST['user_type']
            user = request.user

            # IF USER HAS CORRECT TYPE
            if user_type == 's' or user_type == 'm' or user_type == 'p':
                if user_type == 's':
                    messages.success(request, "You are identified as Student")
                    user.is_student = True
                elif user_type == 'm':
                    messages.success(request, "You are identified as Moderator")
                    user.is_moderator = True
                else:
                    messages.success(request, "You are identified as Parent")
                    user.is_parent = True
                # user.save()
                redirect('accounts:cross-auth-view')
            else:
                messages.error(request, "Please provide correct user type")

        return render(request, 'accounts/identification-check.html')
