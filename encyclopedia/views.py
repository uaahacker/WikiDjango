from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
import random

def index(request):
    """
    Renders the index page with a list of all available encyclopedia entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entrypage(request, title):
    """
    Displays an encyclopedia entry. If the entry does not exist, 
    an error page is shown with a message.
    """
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Sorry, the page '{title}' does not exist.",
            "suggestion": "Return to Home or try searching again."
        })
    else:
        return render(request, "encyclopedia/entrypage.html", {
            "entry": markdown2.markdown(entry),
            "title": title
        })

def search(request):
    """
    Searches for an encyclopedia entry.
    - If an exact match is found, redirects to the entry page.
    - If partial matches are found, displays a list of matching entries.
    - If no matches are found, displays an error page.
    """
    query = request.GET.get('q', '')
    
    if not query:
        return redirect('index')

    entries = util.list_entries()
    matching_entries = []

    for entry in entries:
        if query.lower() == entry.lower():  # Exact match (case-insensitive)
            return redirect('entrypage', title=entry)
        elif query.lower() in entry.lower():  # Partial match
            matching_entries.append(entry)

    if matching_entries:
        return render(request, "encyclopedia/search_results.html", {
            "entries": matching_entries, 
            "query": query
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": f"No results found for '{query}'.",
            "suggestion": "Try a different keyword or create a new page."
        })

def newpage(request):
    """
    Handles creating a new encyclopedia page.
    - If the title already exists, shows an error message.
    - Otherwise, saves the new page and redirects to its entry page.
    """
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if util.get_entry(title):  # Check if entry already exists
            return render(request, "encyclopedia/error.html", {
                "message": f"A page with the title '{title}' already exists.",
                "suggestion": "Try a different title or edit the existing page."
            })
        else:
            util.save_entry(title, content)
            return redirect(reverse("entrypage", kwargs={'title': title}))  # Redirect to the new entry's page

    return render(request, "encyclopedia/newpage.html")  # Display form

def edit(request, title):
    """
    Handles editing an existing encyclopedia page.
    - If the page exists, displays the edit form.
    - If the page does not exist, shows an error message.
    """
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)  # Save the updated content
        return redirect(reverse("entrypage", kwargs={'title': title}))

    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Cannot edit '{title}' because it does not exist.",
            "suggestion": "Create a new page instead."
        })

    return render(request, "encyclopedia/editpage.html", {
        "title": title, 
        "content": content
    })

def random_page(request):
    """
    Redirects to a random encyclopedia entry.
    """
    entries = util.list_entries()
    
    if not entries:  # Handle case when there are no entries
        return render(request, "encyclopedia/error.html", {
            "message": "There are no entries available.",
            "suggestion": "Create a new page to get started!"
        })

    random_title = random.choice(entries)  # Choose a random entry
    return redirect('entrypage', title=random_title)

def errorpage(request, message="An error occurred.", suggestion="Try again."):
    """
    Displays a generic error page with a message and suggestion.
    """
    return render(request, "encyclopedia/error.html", {
        "message": message,
        "suggestion": suggestion
    })
