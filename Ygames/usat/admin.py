from django.contrib import admin
from .models import Game, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # Do not create any empty forms
    fields = ('user', 'content', 'parent_comment', 'created_at')  # The fields you want to display for each comment
    readonly_fields = ('created_at',)  # Make 'created_at' read-only
    can_delete = True  # Allow deletion of existing comments
    show_change_link = True  # Show a link to edit the comment if necessary

class GameAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'cover_image', 'uploaded_at', 'genre', 'file', 'howto', 'bg_style')
    inlines = [CommentInline]  # Include the CommentInline to display comments in the Game admin

admin.site.register(Game, GameAdmin)
