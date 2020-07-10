from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from random import randrange
from markdown2 import Markdown

from . import util

class NewForm(forms.Form):
    title = forms.CharField(label= "Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

    def clean_title(self):
        data = self.cleaned_data.get("title")
        if data in util.list_entries():
            raise forms.ValidationError("Wiki entry already exists.")
        return data

def index(request):
    return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries
    })            

def wiki(request, title):
    if len(title) == 0:
        entries = util.list_entries()
        title = entries[randrange(len(entries))]
    file = util.get_entry(title)
    if not file:
        return render(request, "encyclopedia/notFound.html")
    else:
        markdowner = Markdown()
        return render(request, "encyclopedia/wiki.html", {
            "title": title.capitalize(),
            "file": markdowner.convert(file)
        })

def new(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            util.save_entry(data["title"], data["content"])
            return redirect('encyclopedia:wiki', title= data["title"])
        else:   
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    return render(request, "encyclopedia/new.html", {
        "form": NewForm()
    })

def edit(request, title):
    if request.method == "POST":
        util.save_entry(title, request.POST['content']) 
        return redirect('encyclopedia:wiki', title= title)
    return render(request, "encyclopedia/edit.html", {
        # "form": NewForm(initial= {'content': util.get_entry(title)}),
        "title": title,
        "content": util.get_entry(title)
    })

def search(request):
    search = request.GET.get("q")
    file = util.get_entry(search)
    if file == None:
        results = list()
        for entry in util.list_entries():
            if entry.lower().find(search.lower()) != -1:
                results.append(entry)
        return render(request, "encyclopedia/results.html", {
            "entries": results
        })
    else:
        return render(request, "encyclopedia/wiki.html", {
            "title": search,
            "file": util.get_entry(search)
        })