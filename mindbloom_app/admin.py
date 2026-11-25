from django.contrib import admin
from .models import UserProfile, GameSession, Memory, Reminder, CaregiverLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'preferred_language', 'companion_name', 'caregiver_name')
    list_filter = ('role', 'preferred_language')

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_type', 'score', 'moves', 'duration_seconds', 'stars', 'completed_at')
    list_filter = ('game_type', 'completed_at')

@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'period', 'location', 'tag', 'created_at')
    list_filter = ('tag', 'user')

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('time_str', 'title', 'user', 'category', 'is_completed')
    list_filter = ('is_completed', 'category')

@admin.register(CaregiverLog)
class CaregiverLogAdmin(admin.ModelAdmin):
    list_display = ('patient', 'caregiver', 'date', 'mood')
