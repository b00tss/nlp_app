from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template import loader
from django.urls import reverse
import csv
import logging
import pandas as pd
from bertopic import BERTopic
import os
#from sentence_transformers import SentenceTransformer
#import torch

#test_data = pd.read_csv('add_csv/data_chunks/500k-500k10.csv')
#test_data = test_data['msg'].values.tolist()

    
def predict(request):
    #template = loader.get_template('form.html')
    #return HttpResponse(template.render())

    data = {}
    if "GET" == request.method:
        return render(request, "add_csv.html", data)
    # if not GET, then proceed
    #try:
    elif 'POST' in request.method:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("add_csv"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("add_csv"))

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        #if 'BERTopic' in request.POST:
        #if 'POST' in request.method:
        #embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        BERT_model = BERTopic.load('add_csv/BERT_model/model_nocuda')
        #BERT_model = torch.load("add_csv/BERT_model/model.pt", map_location=torch.device('cpu'))
        topic, prediction = BERT_model.transform(' '.join(lines))
        topics = BERT_model.custom_labels_[topic[0]]
        #output = pd.DataFrame(topics)
        #output.to_csv('topics_found.csv')
        
        #filename = 'topics_found.csv'
        #response = HttpResponse(open(filename, 'rb').read(), content_type='text/csv')
        #response['Content-Length'] = os.path.getsize(filename)
        #response['Content-Disposition'] = 'attachment; filename=%s' % 'topics_found.csv'
        #return response
        #mymembers = Member.objects.all().values()
        template = loader.get_template('add_csv.html')
        context = {'topics': topics,}
        return HttpResponse(template.render(context, request))

   # except Exception as e:
   #     logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
   #     messages.error(request,"Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("add_csv"))
