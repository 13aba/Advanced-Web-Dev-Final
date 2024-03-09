from django.shortcuts import redirect

class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #If user is not authenticated redirect users to login page when they try access anything other than
        #regist/login page
        if not request.user.is_authenticated:
            # Redirect to the login page
            if request.path != '/login/' and request.path != '/register/' and request.path !='/media/images/background.jpg':
                return redirect('/login/')
        response = self.get_response(request)
        return response