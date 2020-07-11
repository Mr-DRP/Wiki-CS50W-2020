from django.shortcuts import render,redirect

from . import util
import markdown2
import random as random_obj


def index(request):
    if request.method == "POST":
        term = request.POST.get("q")
        result = search(term)
        if not result:
            result = None
        title = f"Search result for '{term}'"
    else:
        result = util.list_entries()
        print(result)
        title = "All Pages"
    return render(request, "encyclopedia/index.html", {
        "header": title,
        "entries": result
    })

def content(request,entry):
    content = util.get_entry(entry)
    if content is None:
        content = util.get_entry("404")
        html = markdown2.markdown(content)
        return render(request, "encyclopedia/content.html",{
            "content": html, "title": "No contents"
            })
    html = markdown2.markdown(content)
    return render(request, "encyclopedia/content.html",{
            "content": html, "title": entry
            })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content")
        entries = util.list_entries()
        check = [s for s in entries if title.lower()==s.lower()]
        if not check:
            util.save_entry(title, content)
            return redirect("content", entry=title)
        return render(request, "encyclopedia/create.html",{ "error" : "Title already used" })
    return render(request, "encyclopedia/create.html")

def random(request):
    entries = util.list_entries()
    random_entry = random_obj.choice(entries)
    return redirect("content", entry=random_entry)

def edit(request,title):
    if request.method == "POST":
        content = util.get_entry(title)
        if content is None:
            content = util.get_entry("404")
            html = markdown2.markdown(content)
            return render(request, "encyclopedia/content.html",{
                "content": html, "title": "No contents"
                })
        return render(request, "encyclopedia/create.html",{
                "title_value": title,
                "default_content": content
                    })

def editsave(request,title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("content", entry=title)

def search(term):
    entryList = util.list_entries()
    match = [s for s in entryList if term.lower() in s.lower()]
    return match

