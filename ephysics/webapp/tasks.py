from celery import shared_task
from .models import AppUser
from PIL import Image as img
import io, os
from django.core.files.uploadedfile import SimpleUploadedFile

#Tasks that will be completed async using Celery workers
@shared_task
def create_icon(image_url, user_id):
    try:
        #Get user profile
        profile = AppUser.objects.get(id = user_id)
        image = img.open(os.getcwd() + image_url)
        #Resize image using pillow
        icon = image.resize((60, 60))
        
        # Save the icon 
        icon.save("icon.jpg")
        
        byteArr = io.BytesIO()
        #Save the icon to bytearr
        icon.save(byteArr, format='jpeg')
        #Create new jpeg file with out user name
        file = SimpleUploadedFile("icon_"+str(profile),
        byteArr.getvalue())
        #Update user model and save
        profile.icon = file
        profile.save()  
        
        return f"Image uploaded successfully for user {profile}"

    except Exception as e:
        return f"An error occurred: {str(e)}"