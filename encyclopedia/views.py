from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random

from . import util



# import markdown and create new markdown object to convert entries
import markdown
md = markdown.Markdown()


# create form class for new article https://docs.djangoproject.com/en/4.0/topics/forms/
# specify widgets for each field https://docs.djangoproject.com/en/4.0/ref/forms/widgets/
class New_article_post(forms.Form):
    title = forms.CharField(label="Article Title", widget=forms.TextInput())
    content = forms.CharField(widget=forms.Textarea())


# check the new article and see if it already exists if it doesn't then create it.

def add_article(request):
    if request.method == "POST":
        form_article = New_article_post(request.POST)
        if form_article.is_valid():
            title = form_article.cleaned_data["title"]
            content = form_article.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("article", kwargs={'article': title}))
            else:
                return render(request, "encyclopedia/error_exist.html")
        else:
            return render(request, "encyclopedia/error_exist.html")

    return render(request, "encyclopedia/new_page.html", {
        "form": New_article_post()
    })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# use initial to get the original values of the articles
def edit_article(request, article):
    # repeat process from add article but remove the existing article check
    if request.method == "POST":
        edit_article = New_article_post(request.POST)
        if edit_article.is_valid():
            title = edit_article.cleaned_data["title"]
            content = edit_article.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("article", kwargs={'article': title}))
        else:
            return render(request, "encyclopedia/error_try.html")
    # if it's not a post display the article to edit
    else:
        article_to_edit = util.get_entry(article)
        if article_to_edit is None:
            return render(request, "encyclopedia/error.html")
        else:
            edit_form = New_article_post()
            edit_form.fields["title"].initial = article
            edit_form.fields["content"].initial = article_to_edit
            return render(request, "encyclopedia/edit_article.html", {
                "edit_form": edit_form,
                "article_title": edit_form.fields["title"].initial
            })


# add action to form in layout
def search_article(request):
    # get query params https://docs.djangoproject.com/en/4.0/ref/request-response/
    q_params = request.GET.get('q', '')
    # check againt current entries with the get_entry
    if util.get_entry(q_params) is not None:
    # will have to use kwargs for redirect https://django.readthedocs.io/en/stable/ref/urlresolvers.html
        return HttpResponseRedirect(reverse("article", kwargs={'article': q_params}))
    else:
        # create a list to hold the names of the entries if the q_params are in the article title send it to the search list
        search_list = []
        for article in util.list_entries():
            if q_params.lower() in article.lower():
                search_list.append(article)

        # if the search list has something in it then render the list if not throw error.
        if len(search_list) > 0:
            # render a new html for search list using index template as base.
            return render(request, "encyclopedia/search_list.html", {
                "articles": search_list,
                "search": q_params
            })
        else:
            return render(request, "encyclopedia/error.html")


# article will use the get_entry function from util to see if entry exists
# if it does it will be rendered to html from markdown if not error page is rendered
def article(request, article):
    article_page = util.get_entry(article)
    if article_page is None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/article.html", {
            "article_title": article,
            "article": md.convert(article_page)
        })


# takes all articles, using list_entries picks random choice and redirects to article https://www.geeksforgeeks.org/random-numbers-in-python/
def random_article(request):
    num_articles = util.list_entries()
    rand_article = random.choice(num_articles)
    return HttpResponseRedirect(reverse("article", kwargs={'article': rand_article}))



