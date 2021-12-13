from functools import total_ordering
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from app_main.models import Todo
from app_main.forms import Create_Todo_Form
from django.http.response import Http404, HttpResponse
from django.urls import reverse
import json


def http404_view(request, exception):
    return render(request, "app_main/http404.html")


def welcome_view(request):
    if request.user.is_authenticated:
        return redirect("todos")

    return render(request, "app_main/welcome.html")


@login_required
def todos_view(request):
    data = {}

    if request.method == "POST":
        form = Create_Todo_Form(request.POST)
        if form.is_valid():
            Todo.objects.create(
                owner=request.user,
                content=form.cleaned_data["content"],
                is_marked=form.cleaned_data["is_marked"],
                color=form.cleaned_data["color"],
            )
            form = Create_Todo_Form()

            # using redirect to prevent form resubmition thing on browsers
            return redirect(
                reverse("todos")
                + "?"
                + (
                    "tamamlananlari_goster=on&"
                    if request.GET.get("tamamlananlari_goster")
                    else ""
                )
                + ("sirala=eski" if request.GET.get("sirala") == "eski" else "")
            )
        else:
            # message atsan (kayit alinamadi diye) olur aslinda
            pass
    else:
        form = Create_Todo_Form()

    data["form"] = form

    return render(request, "app_main/todos.html", data)


@login_required
def get_list(request):

    data = {}

    users_todos = Todo.objects.filter(owner=request.user)

    # filter and sort by given header values
    if not request.headers["show-done"] == "on":
        users_todos = users_todos.filter(is_done=False)

    if request.headers["sort"] == "eski":
        users_todos = users_todos.order_by("update_date")
    else:
        users_todos = users_todos.order_by("-update_date")

    data["marked_todos"] = users_todos.filter(is_marked=True)
    data["unmarked_todos"] = users_todos.filter(is_marked=False)

    return render(request, "app_main/todo_list.html", data)


@login_required
def delete_todo(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))

        try:
            Todo.objects.get(id=body["id"]).delete()
        except:
            raise Http404

        return HttpResponse("deleted")

    else:
        raise Http404


@login_required
def mark_unmark_todo(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))

        try:
            obj = Todo.objects.get(id=body["id"])
            obj.is_marked = not obj.is_marked
            obj.save()
        except:
            raise Http404

        return HttpResponse("mark_unmark_done")

    else:
        raise Http404


@login_required
def done_undone_todo(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))

        try:
            obj = Todo.objects.get(id=body["id"])
            obj.is_done = not obj.is_done
            obj.save()
        except:
            raise Http404

        return HttpResponse("done_undone_successful")

    else:
        raise Http404


@login_required
def update_todo(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))

        try:
            obj = Todo.objects.get(id=body["id"])
            obj.content = body["content"]
            obj.save()

        except:
            raise Http404

        return HttpResponse("content_updated")

    else:
        raise Http404
