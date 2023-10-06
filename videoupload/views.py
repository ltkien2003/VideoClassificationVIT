import os
import time
from datetime import timedelta

import firebase_admin
from django.shortcuts import render
from firebase_admin import credentials, storage
from videoupload.forms import VideoUploadForm
from vivit.vivit import vivit

print(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'videoupload/firebase-key.json'))

firebase_credentials = credentials.Certificate(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'videoupload'
                                                                                                        '/firebase'
                                                                                                        '-key.json'))
firebase_admin.initialize_app(firebase_credentials, {'storageBucket': 'vivit-f07ee.appspot.com'})

from django.http import JsonResponse

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.cleaned_data['video']
            video_name = video.name
            bucket = storage.bucket()
            blob = bucket.blob(video_name)
            blob.upload_from_file(video)
            download_url = blob.generate_signed_url(expiration=timedelta(days=1))
            result = vivit(download_url)
            blob.delete()
            return JsonResponse({"result": result})
    else:  # This block handles GET requests
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})

