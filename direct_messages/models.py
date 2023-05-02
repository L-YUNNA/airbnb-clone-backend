from django.db import models

# Create your models here.
from common.models import CommonModel

class ChattingRoom(CommonModel):  # 채팅방
    """
    Room Model Definition
    """
    users = models.ManyToManyField(
        "users.User",
    )

    def __str__(self):
        return "Chatting Room."    # 추후 채팅방에 있는 유저 수 표시


class Message(CommonModel):
    """
    Message Model Definition
    """
    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.text}"