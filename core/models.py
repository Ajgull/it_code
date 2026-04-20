from django.db import models

from core.consts import STATUS_CHOICES, VOTE_CHOICES
from core.user import User


class Category(models.Model):
    title = models.CharField(verbose_name="title", max_length=255)

    def __str__(self):
        return f"Category name - {self.title}"


class Tag(models.Model):
    name = models.CharField(verbose_name="name", max_length=50, unique=True)

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(verbose_name="title", max_length=255)
    descripeion = models.TextField(verbose_name="description")
    image = models.ImageField(
        upload_to="posts/",
        verbose_name="post_img",
        blank=True,
        null=True,
    )
    status = models.CharField(choices=STATUS_CHOICES, verbose_name="status")
    deleted = models.DateTimeField(
        verbose_name="date_time_of_delete", null=True, blank=True
    )
    score = models.IntegerField(verbose_name="score", default=0)
    is_hidden_by_score = models.BooleanField(
        default=False, verbose_name="hidden_by_score"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", verbose_name="author"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="category",
    )
    tags = models.ManyToManyField(
        Tag, related_name="posts", blank=True, verbose_name="tegs"
    )

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return f"post {self.title}, author {self.author.username}, description {self.descripeion}, category of post {self.category}"


class Comment(models.Model):
    content = models.TextField(verbose_name="content")
    depth_level = models.IntegerField(default=0, verbose_name="level_of_depth")
    parent_comment_id = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",  # ответы
        verbose_name="parent_comment",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", verbose_name="author"
    )
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="post"
    )
    tags = models.ManyToManyField(
        Tag, verbose_name="tags", related_name="comments", blank=True
    )

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"user {self.author} write the comment {self.content[:20]}"

    def clean(self):
        if self.parent_comment:
            if self.parent_comment.depth_level < 2:
                self.depth_level = self.parent_comment.depth_level + 1
        else:
            self.depth_level = 0

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Vote(models.Model):  # голоса
    vote_type = models.CharField(choices=VOTE_CHOICES)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="votes", verbose_name="user"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="votes",
        verbose_name="post",
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="votes",
        verbose_name="comment",
    )

    class Meta:
        verbose_name = "vote"
        verbose_name_plural = "votes"


class GlobalStopWord(models.Model):
    word = models.CharField(max_length=100, unique=True, verbose_name="word")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="date_of_creation"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="global_stop_words",
        verbose_name="user",
    )

    class Meta:
        verbose_name = "global_stop_word"
        verbose_name_plural = "global_stop_words"

    def __str__(self):
        return self.word


class PostStopWord(models.Model):
    word = models.CharField(verbose_name="word", max_length=100)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="stop_words", verbose_name="Пост"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="post_stop_words",
        verbose_name="user",
    )

    class Meta:
        verbose_name = "post_stop_word"
        verbose_name_plural = "post_stop_words"

    def __str__(self):
        return f"{self.word} post {self.post_id}"
