from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.shortcuts import render , redirect
from converter.forms import HomeForm
from csv import reader
import string
import json
import re
# Create your views here.

class CypherToText(TemplateView):
    
    template_name = 'templatesviews/cyphertotext.html'

    def get(self, request, *args, **kwargs):
        form = HomeForm()
        return render(request,self.template_name, {'form':form})
    
    def post(self,request):
        with open('peritable.txt') as infile:
            peritable = json.load(infile)
            
        # define an alphabet
        alfa = "abcdefghijklmnopqrstuvwxyz0"
        
        # define reverse lookup dict
        rdict = dict([ (x[1],x[0]) for x in enumerate(alfa) ])
        
        def flip_dict(dict):
            new = {}
            for key, value in peritable.items():
                if not value in new:
                    new[value] = []
                new[value].append(key)
            return new   
        
        def cypher_to_string(text):
            cypher = text.split() 
            result = ""
            for item in cypher:
                if item[-1] == "<":
                    res = peritable[item[0:-1]]
                    result = result + alfa[rdict[res]-1]
                elif item[-1] == ">":
                    res = peritable[item[0:-1]]
                    result = result + alfa[rdict[res]+1]
                elif item =="-":
                    result = result + " "
                else:
                    if item not in peritable:
                        print("error")
                    else:
                        result = result + peritable[item]
            return result

        form = HomeForm(request.POST)
        
        if form.is_valid():
            text = form.cleaned_data['text']
            if 'convert' in request.POST:
                result = cypher_to_string(text)

            form = HomeForm()
            #return redirect ('home:home')

        args = {'form': form , 'result': result, 'text':text}
        return render(request, self.template_name, args )
        
class TextToCypher(TemplateView):
    
    template_name = 'templatesviews/texttocypher.html'

    def get(self, request, *args, **kwargs):
        form = HomeForm()
        return render(request,self.template_name, {'form':form})

    def post(self,request):
        with open('peritable.txt') as infile:
            peritable = json.load(infile)

        # define an alphabet
        alfa = "abcdefghijklmnopqrstuvwxyz0"

        # define reverse lookup dict
        rdict = dict([ (x[1],x[0]) for x in enumerate(alfa) ])

        def flip_dict(dict):
            new = {}
            for key, value in peritable.items():
                if not value in new:
                    new[value] = []
                new[value].append(key)
            return new   

        def string_to_cypher(text):
            rperitable = flip_dict(peritable)
            regex = re.compile('[^a-z]')
            text = regex.sub(' ', text.lower())
            result = []
            i = 0
            while i < len(text):
                if text[i] == " ":
                    result.append("-")
                    i = i + 1
                elif text[i] in rperitable:
                    result = result + rperitable[text[i][0]]
                    i = i + 1
                elif text[i:i+2] in rperitable:
                    result = result + rperitable[text[i:i+2]]
                    i = i + 2
                else: # Letter does not exist in periodic table. Find a letter to the left or right in the alphabet and signal which way it found it.
                    if alfa[rdict[text[i]]+1] in rperitable:
                        result.append(rperitable[alfa[rdict[text[i]]+1]][0] + "<") 
                    elif alfa[rdict[text[i]]- 1] in rperitable:
                        result.append(rperitable[alfa[rdict[text[i]]-1]][0] + ">")
                    i = i + 1
            stringList = ' '.join([str(item) for item in result ])
            return stringList
        
        form = HomeForm(request.POST)
        
        if form.is_valid():
            text = form.cleaned_data['text']
            if 'convert' in request.POST:
                result = string_to_cypher(text)

            form = HomeForm()

        args = {'form': form , 'result': result, 'text':text }
        return render(request, self.template_name, args )


def home(request):
    return render(request,'index.html')