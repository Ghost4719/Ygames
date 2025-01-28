# views.py
import zipfile
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, GameForm
from .models import Game, GamePic, GameFile

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('usat:home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created for ' + user)
                return redirect('usat:log_in')

        context = {'form': form}
        return render(request, 'usat/signup.html', context)

def log_in(request):
    if request.user.is_authenticated:
        return redirect('usat:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('usat:home')
            else:
                messages.info(request, 'Incorrect Username or Password')

        return render(request, 'usat/login.html')

@login_required(login_url='usat:log_in')
def log_out(request):
    logout(request)
    return redirect('usat:log_in')

@login_required(login_url='usat:log_in')
def index(request):
    if request.user.is_authenticated:
        return redirect('usat:home')
    else:
        return render(request, 'usat/login.html')

@login_required(login_url='usat:log_in')
def home(request):
    games = Game.objects.all()
    user_games = Game.objects.filter(user=request.user)
    Action = Game.objects.filter(genre="Action")
    Adventure = Game.objects.filter(genre="Adventure")
    Role_Playing = Game.objects.filter(genre="Role_Playing")
    Simulation = Game.objects.filter(genre="Simulation")
    Strategy = Game.objects.filter(genre="Strategy")
    Sports = Game.objects.filter(genre="Sports")
    Puzzle = Game.objects.filter(genre="Puzzle")
    Racing = Game.objects.filter(genre="Racing")
    Fighting = Game.objects.filter(genre="Fighting")
    Horror = Game.objects.filter(genre="Horror")
    Other = Game.objects.filter(genre="Other")

    # Add print statements for debugging
    print("Action games:", Action.count())
    print("Adventure games:", Adventure.count())
    print("Role_Playing games:", Role_Playing.count())
    # Continue for all genres...

    return render(request, 'usat/home.html', {
        'games': games,
        'user_games': user_games,
        'Action': Action,
        'Adventure': Adventure,
        'Role_Playing': Role_Playing,
        'Simulation': Simulation,
        'Strategy': Strategy,
        'Sports': Sports,
        'Puzzle': Puzzle,
        'Racing': Racing,
        'Fighting': Fighting,
        'Horror': Horror,
        'Other': Other
    })

def about(request):
    if request.user.is_authenticated:
        return redirect('usat:home')
    else:
        return render(request, 'usat/about.html')



from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, GamePic, GameFile, Comment
from django.contrib.auth.decorators import login_required

@login_required(login_url='usat:log_in')
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    game_pics = game.game_pics.all()
    game_files = game.game_file.all()
    comments = game.comments.filter(parent_comment=None)  # Top-level comments

    if request.method == 'POST':
        content = request.POST.get('content')
        parent_comment_id = request.POST.get('parent_comment')

        if content:
            parent_comment = None
            if parent_comment_id:
                parent_comment = get_object_or_404(Comment, id=parent_comment_id)

            Comment.objects.create(
                game=game,
                user=request.user,
                content=content,
                parent_comment=parent_comment
            )
            return redirect('usat:game_detail', game_id=game.id)

    return render(request, 'usat/show.html', {
        'game': game,
        'game_pics': game_pics,
        'game_files': game_files,
        'comments': comments
    })





from django.http import Http404, StreamingHttpResponse

import zipfile
import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import GameForm
from .models import Game, GamePic, GameFile

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import GameForm
from .models import Game, GamePic, GameFile
import os
import zipfile
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required(login_url='usat:log_in')
def create(request, game_id=None):
    # If game_id is provided, we fetch the game instance for editing
    if game_id:
        game = get_object_or_404(Game, id=game_id)
        # Ensure that only the creator of the game can edit it
        if game.user != request.user:
            messages.error(request, "You are not authorized to edit this game.")
            return redirect('usat:home')
    else:
        game = None

    # Handle POST request when submitting the form
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES, instance=game)  # Pass existing game if editing
        if form.is_valid():
            game = form.save(commit=False)  # Save the game without committing to DB yet
            game.user = request.user  # Associate the game with the logged-in user
            game.save()  # Save the game to the DB

            # Save additional pictures and data files
            for f in request.FILES.getlist('pic'):
                GamePic.objects.create(game=game, file=f)
            for g in request.FILES.getlist('deta'):
                GameFile.objects.create(game=game, file=g)

            # Extract the game ZIP file if provided (ensure the model has web_game field)
            game_zip = request.FILES.get('web_game')
            if game_zip:
                # Create directory for the game if it doesn't exist
                game_dir = os.path.join(settings.MEDIA_ROOT, 'web_games', str(game.id))
                os.makedirs(game_dir, exist_ok=True)

                # Extract the ZIP file to the game directory
                with zipfile.ZipFile(game_zip, 'r') as zip_ref:
                    zip_ref.extractall(game_dir)

                messages.success(request, 'Game uploaded and extracted successfully!')

            # Handle theme-related settings
            game.bg_color = request.POST.get('bg_color', game.bg_color)
            game.text_color = request.POST.get('text_color', game.text_color)
            game.link_color = request.POST.get('link_color', game.link_color)
            game.font_family = request.POST.get('font_family', game.font_family)
            game.font_size = request.POST.get('font_size', game.font_size)
            game.banner_image = request.FILES.get('banner_image', game.banner_image)
            game.background_image = request.FILES.get('background_image', game.background_image)
            game.save()  # Save the updated game instance with theme settings

            messages.success(request, 'Game and theme settings saved successfully!')

            return redirect('usat:home')  # Redirect after successful form submission

    else:
        form = GameForm(instance=game)  # Pre-fill the form if editing an existing game

    return render(request, 'usat/create.html', {'form': form, 'game': game})

from django.contrib.auth.models import User


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm  # Ensure you're using the custom change form

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm  # Use the custom form

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm  # Custom form

def change(request, username):
    user = get_object_or_404(User, username=username)  # Get the existing user
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()  # Save the updated user data (including new password if provided)
            return redirect('usat:home')  # Redirect to the homepage or profile page
        else:
            # Print form errors to debug if the form is invalid
            print(form.errors)
            return render(request, 'usat/change.html', {'form': form})
    
    else:
        form = CustomUserChangeForm(instance=user)  # Pre-fill the form with the current user data
    
    return render(request, 'usat/change.html', {'form': form})




#views.py





# import os
# import re
# from django.http import HttpResponse, Http404
# from django.views.decorators.clickjacking import xframe_options_exempt
# from django.shortcuts import get_object_or_404
# from django.conf import settings
# from django.contrib.auth.decorators import login_required

# from django.http import Http404, HttpResponse
# from django.shortcuts import get_object_or_404
# from django.conf import settings
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.clickjacking import xframe_options_exempt
# import os
# import re
# import mimetypes

# @login_required(login_url='usat:log_in')
# @xframe_options_exempt
# def play_game(request, game_id):
#     game = get_object_or_404(Game, id=game_id)
#     base_game_dir = os.path.join(settings.MEDIA_ROOT, 'web_games', str(game.id))

#     def find_index_html(dir_path):
#         for root, dirs, files in os.walk(dir_path):
#             if 'index.html' in files:
#                 return os.path.join(root, 'index.html')
#         raise Http404("index.html not found in any subdirectory")

#     index_file_path = find_index_html(base_game_dir)
#     index_dir = os.path.dirname(index_file_path)

#     with open(index_file_path, 'r', encoding='utf-8') as f:
#         index_content = f.read()

#     def find_asset_path(filename):
#         for root, dirs, files in os.walk(base_game_dir):
#             if filename in files:
#                 return os.path.join(root, filename)
#         return None

#     def check_script_path(match):
#         old_path = match.group(1) or match.group(2) or match.group(3)

#         if not old_path:
#             return match.group(0)

#         old_path = old_path.strip('"').strip("'")
#         filename = os.path.basename(old_path)
#         found = False

#         for root, dirs, files in os.walk(base_game_dir):
#             if filename in files:
#                 rel_path = os.path.relpath(os.path.join(root, filename), base_game_dir)
#                 new_path = os.path.normpath(rel_path).replace('\\', '/')
#                 found = True
#                 break

#         if found:
#             return f'{match.group(0).split("=")[0]}="/media/web_games/{game.id}/{new_path}"'
#         else:
#             return match.group(0)

#     def check_asset_path(match):
#         old_path = match.group(1) or match.group(2) or match.group(3)

#         if not old_path:
#             return match.group(0)

#         old_path = old_path.strip('"').strip("'")
#         filename = os.path.basename(old_path)
#         asset_path = find_asset_path(filename)

#         if asset_path:
#             rel_path = os.path.relpath(asset_path, base_game_dir)
#             new_path = os.path.normpath(rel_path).replace('\\', '/')
#             return f'{match.group(0).split("=")[0]}="/media/web_games/{game.id}/{new_path}"'
#         else:
#             return match.group(0)

#     script_pattern = re.compile(r'src="([^"]+)"|href="([^"]+)"|url\(([^)]+)\)')
#     asset_pattern = re.compile(r'href="([^"]+)"|url\(([^)]+)\)')
#     index_content = script_pattern.sub(check_script_path, index_content)
#     index_content = asset_pattern.sub(check_asset_path, index_content)
    
#     ext = os.path.splitext(index_file_path)[1]
#     content_type, _ = mimetypes.guess_type(index_file_path)
#     if not content_type:
#         content_type = "text/html"

#     response = HttpResponse(index_content, content_type=content_type)

#     return response
