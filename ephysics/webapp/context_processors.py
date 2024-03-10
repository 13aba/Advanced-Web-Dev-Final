from .models import Notification

def user_notifications(request):
    if request.user.is_authenticated:
        #return all the nofitician thats not read if user is logged on
        notifications = Notification.objects.filter(recipient=request.user.appuser, is_read=False).order_by('-created_at')
        return {'notifications': notifications}
    #Return empty query if user is not authenicateed
    return {}