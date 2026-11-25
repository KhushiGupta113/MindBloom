from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('elderly', 'Elderly Patient / User'),
        ('caregiver', 'Caregiver / Family Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='elderly')
    preferred_language = models.CharField(max_length=10, default='en')
    companion_name = models.CharField(max_length=100, default='Eleanor Vance')
    caregiver_name = models.CharField(max_length=100, default='Sarah Vance (Daughter)')
    avatar_url = models.CharField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class GameSession(models.Model):
    GAME_TYPE_CHOICES = [
        ('memory_match', 'Memory Match'),
        ('sequence', 'Remember the Sequence'),
        ('picture_recognition', 'Picture Recognition'),
        ('word_recall', 'Word & Picture Recall'),
        ('gentle_garden', 'English Garden Blossoms'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_sessions')
    game_type = models.CharField(max_length=30, choices=GAME_TYPE_CHOICES)
    game_title = models.CharField(max_length=150)
    score = models.IntegerField(default=100)
    moves = models.IntegerField(default=0)
    mistakes = models.IntegerField(default=0)
    pairs_found = models.IntegerField(default=0)
    duration_seconds = models.IntegerField(default=60)
    stars = models.IntegerField(default=3)
    completed_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username} - {self.game_title} ({self.score} pts on {self.completed_at.strftime('%Y-%m-%d %H:%M')})"


class Memory(models.Model):
    TAG_CHOICES = [
        ('all', 'General'),
        ('family', 'Family & Holidays'),
        ('garden', 'Garden & Nature'),
        ('wedding', 'Wedding & Romance'),
        ('travel', 'Travel & Places'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    title = models.CharField(max_length=200)
    period = models.CharField(max_length=100, help_text="e.g. Summer 1968, Autumn 1974")
    location = models.CharField(max_length=150, blank=True, help_text="e.g. St Ives, Cornwall / Tezpur, Assam")
    description = models.TextField()
    image_url = models.CharField(max_length=500, blank=True)
    tag = models.CharField(max_length=30, choices=TAG_CHOICES, default='family')
    audio_label = models.CharField(max_length=150, blank=True, default="Sarah's audio description")
    audio_duration = models.CharField(max_length=20, blank=True, default="1:15")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.period})"


class Reminder(models.Model):
    CATEGORY_CHOICES = [
        ('tea', 'Tea & Refreshment'),
        ('walk', 'Gentle Walk'),
        ('family', 'Family Call'),
        ('wellness', 'Rest & Relaxation'),
        ('music', 'Music & Chimes'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=200)
    time_str = models.CharField(max_length=50, help_text="e.g. 10:30 AM, 3:00 PM")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='tea')
    icon = models.CharField(max_length=50, default='local_cafe')
    is_completed = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['time_str', 'id']

    def __str__(self):
        return f"{self.time_str} - {self.title} ({'Done' if self.is_completed else 'Pending'})"


class CaregiverLog(models.Model):
    caregiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caregiver_logs')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_logs')
    date = models.DateField(default=timezone.now)
    mood = models.CharField(max_length=100, default='Bright & Calm')
    mood_score = models.IntegerField(default=90)
    hydration_status = models.CharField(max_length=100, default='Well Hydrated (4/5 cups chamomile & warm water)')
    sleep_notes = models.CharField(max_length=200, default='Rested peacefully for 8 hours with soft morning sunlight')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Caregiver Log for {self.patient.username} on {self.date}"
