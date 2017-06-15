# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.conf import settings
from upload_form.models import FileNameModel
from pyIyo.ai.rl.QAgent import QAgent
import numpy as np
import pdb
import time
import json
import sys, os


UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'

def form(request):
    if request.method != 'POST':
        return render(request, 'upload_form/form.html')

    file = request.FILES['file']
    if not '.json' in file.name:
        return render(request, 'upload_form/error.html')

    path = os.path.join(UPLOAD_DIR, file.name)
    destination = open(path, 'wb')

    for chunk in file.chunks():
        destination.write(chunk)

    insert_data = FileNameModel(file_name = file.name)
    insert_data.save()

    return redirect('upload_form:complete')


def complete(request):
    print(request)
    dir_path = '/Users/mzntaka0/Work/9DW/IYO/reinforcement_learning/web/RLweb/upload_form/static/files/'
    result_path = '/Users/mzntaka0/Work/9DW/IYO/reinforcement_learning/web/RLweb/upload_form/static/results/'
    uploaded_file = FileNameModel.objects.latest('upload_time').file_name
    with open(dir_path+uploaded_file, 'rb') as f:
        params = json.load(f)

    q_agent = QAgent(params)
    start_time = time.time() 
    final_Q = q_agent.run()
    elapsed_time = time.time() - start_time
    final_Q['process_time'] = elapsed_time

    params['process_time'] = final_Q['process_time']
    params['output'] = final_Q['outputs']

    result_file = 'output_{}'.format(FileNameModel.objects.latest('upload_time').file_name)
    with open(result_path+result_file, 'w') as f:
        json.dump(params, f)

    return render(request, 'upload_form/complete.html', final_Q)
