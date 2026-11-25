from django.urls import path
from . import views

urlpatterns = [
    # Core Screen Routes
    path('', views.home_view, name='home'),
    path('games/', views.games_library_view, name='games_library'),
    path('games/memory-match/', views.memory_match_view, name='memory_match'),
    path('games/sequence/', views.sequence_view, name='sequence_game'),
    path('games/picture-recognition/', views.picture_recognition_view, name='picture_recognition'),
    path('games/word-recall/', views.word_recall_view, name='word_recall'),
    path('games/garden/', views.garden_view, name='garden_game'),
    path('games/completion/', views.game_completion_view, name='game_completion'),

    # Memories & Scrapbook
    path('memories/', views.memories_view, name='memories'),
    path('memories/add/', views.add_memory_view, name='add_memory'),

    # Caregiver Circle
    path('caregiver/', views.caregiver_view, name='caregiver'),

    # APIs & Controls
    path('api/save-game/', views.save_game_api, name='save_game_api'),
    path('api/toggle-reminder/<int:reminder_id>/', views.toggle_reminder_api, name='toggle_reminder_api'),
    path('api/set-language/', views.set_language_api, name='set_language'),
    path('switch-profile/<str:role>/', views.switch_profile_view, name='switch_profile'),

    # Authentication & Role-Based Portal
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
