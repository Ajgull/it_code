from django.contrib import admin

from core.models import (
    Category,
    Comment,
    GlobalStopWord,
    Post,
    PostStopWord,
    Tag,
    User,
    Vote,
)

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(GlobalStopWord)
admin.site.register(Post)
admin.site.register(PostStopWord)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Vote)
