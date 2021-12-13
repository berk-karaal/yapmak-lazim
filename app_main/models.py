from django.db import models
from django.contrib.auth import get_user_model


class Todo(models.Model):

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    update_date = models.DateTimeField(auto_now_add=True)
    is_marked = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    COLORS = [
        ("white", "white"),
        ("tomato", "tomato"),
        ("aqua", "aqua"),
        ("skyblue", "skyblue"),
        ("coral", "coral"),
    ]

    color = models.CharField(max_length=20, choices=COLORS, default="white")

    def __str__(self) -> str:
        return self.content[:30] + "..."
