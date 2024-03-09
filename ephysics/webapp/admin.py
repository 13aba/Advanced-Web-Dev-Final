from django.contrib import admin
from .models import *


admin.site.register(AppUser)
admin.site.register(Course)
admin.site.register(Post)
admin.site.register(Enrollment)
admin.site.register(Status)
admin.site.register(BlockedStudent)
admin.site.register(Feedback)
admin.site.register(Deadline)



# Register your models here.
