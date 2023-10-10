import random
import markdown2

from django.shortcuts import render, redirect
from django.urls import reverse

from . import util, forms

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show(request, title):
    entry = util.get_entry(title)

    if not entry:
        return render(request, "encyclopedia/error.html", {
            "title": "Not Found",
            "message": f"The entry with the title \"{title}\" does not exist"
        })

    return render(request, "encyclopedia/show.html", {
        "title": title.capitalize(),
        "entry": markdown2.markdown(entry)
    })

def search(request):
    if request.method == "POST":
        search_term = request.POST.get("q", "")
        entry = util.get_entry(search_term)

        if not entry:
            entries = util.list_entries()
            filtered_entries = filter(lambda entry: entry.find(search_term) > -1, entries)    
            filtered_entries = list(filtered_entries)

            return render(request, "encyclopedia/search.html", {
                "search_term": search_term.capitalize(),
                "entries": filtered_entries,
                "entries_length": len(filtered_entries)
            })
        return redirect(reverse("show", args=[search_term]))
    
def create(request):
    if request.method == "POST":
        form = forms.PageCreateForm(request.POST)

        if not form.is_valid():
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
        
        if util.get_entry(form.cleaned_data["title"]):
            return render(request, "encyclopedia/error.html", {
                "title": "Duplicate",
                "message": f"The entry with the title \"{form.cleaned_data['title']}\" already exists"
            })
        
        util.save_entry(
            form.cleaned_data["title"],
            form.cleaned_data["content"]
        )

        return redirect(reverse("show", args=[form.cleaned_data["title"]]))

    return render(request, "encyclopedia/create.html", {
        "form": forms.PageCreateForm()
    })

def edit(request, title):
    entry = util.get_entry(title)
    form = forms.PageEditForm(initial={"content": entry})

    if request.method == "POST":
        form = forms.PageEditForm(request.POST)
        if not form.is_valid():
            return render(request, "encyclopedia/edit.html", {
                "form": form,
                "title": title
            })
        
        util.save_entry(title, form.data["content"].strip())

        return redirect(reverse("show", args=[title]))

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })

def show_random(request):
    entries = util.list_entries()
    random_index = random.randint(0, len(entries) - 1)

    return redirect(reverse("show", args=[entries[random_index]]))
