from django.urls import path
from app_main.views import (
    done_undone_todo,
    welcome_view,
    todos_view,
    delete_todo,
    mark_unmark_todo,
    get_list,
    update_todo,
)


urlpatterns = [
    path("", welcome_view, name="welcome"),
    path("yapilacaklar/", todos_view, name="todos"),
    path("liste_ver/", get_list, name="get_list"),
    path("todo_sil/", delete_todo, name="delete_todo"),
    path("todo_isaretle/", mark_unmark_todo, name="mark_unmark_todo"),
    path("bitti_bitmedi_todo/", done_undone_todo, name="done_undone_todo"),
    path("todo_guncelle/", update_todo, name="update_todo"),
]
