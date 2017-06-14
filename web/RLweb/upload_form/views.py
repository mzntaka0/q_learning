# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.conf import settings
from upload_form.models import FileNameModel
from QLearning.QLearning.q_learning import q_learn
import numpy as np
import pdb
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
    dir_path = '/Users/mzntaka0/Work/9DW/IYO/reinforcement_learning/web/RLweb/upload_form/static/files/'
    result_path = '/Users/mzntaka0/Work/9DW/IYO/reinforcement_learning/web/RLweb/upload_form/static/results/'
    uploaded_file = FileNameModel.objects.latest('upload_time').file_name
    with open(dir_path+uploaded_file, 'rb') as f:
        print('f: {}'.format(f))
        parameters = json.load(f)

    final_Q = {'final_Q': 
                q_learn(
                episode_num=parameters["epsode_num"],
                R=np.array(parameters["R"]),
                goal=parameters["goal"],
                alpha=parameters["alpha"],
                gamma=parameters["gamma"],
                tau=parameters["tau"],
                epsilon=parameters["epsilon"],
                ).tolist()
            }

    parameters['result'] = final_Q['final_Q']

    result_file = 'result_{}'.format(FileNameModel.objects.latest('upload_time').file_name)
    with open(result_path+result_file, 'w') as f:
        json.dump(parameters, f)


    #final_Q['final_Q'] = '\n'.join('{}'.format(final_Q['final_Q']))


    return render(request, 'upload_form/complete.html', final_Q)

