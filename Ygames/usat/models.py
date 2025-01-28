# models.py

from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


class Game(models.Model):

    Option0 = 'Action'
    Option1 = 'Adventure'
    Option2 = 'Role_Playing'
    Option3 = 'Simulation'
    Option4 = 'Strategy'
    Option5 = 'Sports'
    Option6 = 'Puzzle'
    Option7 = 'Racing'
    Option8 = 'Fighting'
    Option9 = 'Horror'
    Option10 = 'Other'

    OPTIONS = [
        (Option0, 'Action'),
        (Option1, 'Adventure'),
        (Option2, 'Role_Playing'),
        (Option3, 'Simulation'),
        (Option4, 'Strategy'),
        (Option5, 'Sports'),
        (Option6, 'Puzzle'),
        (Option7, 'Racing'),
        (Option8, 'Fighting'),
        (Option9, 'Horror'),
        (Option10, 'Other'),
    ]
    
    title = models.CharField(max_length=100)
    description = RichTextUploadingField()
    howto = RichTextUploadingField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_images/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    pic = models.FileField(upload_to='game_images/', blank=True, null=True)
    file = models.FileField(upload_to='game_files/', blank=True, null=True)
    genre = models.CharField(max_length=12, choices=OPTIONS,  default=Option0)
    # web_game = models.FileField(upload_to='web_games/', blank=True, null=True)

    # Theme settings
    bg_color = models.CharField(max_length=7, default='#eeeeee')  # Background color
    text_color = models.CharField(max_length=7, default='#222222')  # Text color
    link_color = models.CharField(max_length=7, default='#fa5c5c')  # Link color
    font_family = models.CharField(max_length=255, default='lato')  # Font family
    font_size = models.CharField(max_length=50, default='large')  # Font size
    banner_image = models.ImageField(upload_to='game_banners/', null=True, blank=True)  # Banner image
    background_image = models.ImageField(upload_to='game_backgrounds/', null=True, blank=True)  # Background image
    bg_style = models.ImageField(upload_to='game_stylebgs/', null=True, blank=True)

    def __str__(self):
        return self.title

from django.db import models
from django.conf import settings

class Comment(models.Model):
    game = models.ForeignKey('Game', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.game.title}"

    class Meta:
        ordering = ['created_at']

    


class GamePic(models.Model):
    game = models.ForeignKey(Game, related_name='game_pics', on_delete=models.CASCADE)
    file = models.FileField(upload_to='game_images/')
    
class GameFile(models.Model):
    game = models.ForeignKey(Game, related_name='game_file', on_delete=models.CASCADE)
    file = models.FileField(upload_to='game_files/')
