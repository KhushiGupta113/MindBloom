import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone
from .models import UserProfile, GameSession, Memory, Reminder, CaregiverLog
from .translations import SUPPORTED_LANGUAGES, get_text

def get_current_lang(request):
    lang = request.session.get('language')
    if not lang:
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            lang = request.user.profile.preferred_language
        else:
            lang = 'en'
    return lang

def localize_reminders_and_memories(reminders, memories, lang):
    title_map = {
        'Morning Assam Tea & Warm Porridge': 'reminder_tea_title',
        'Gentle Courtyard Walk & Fresh Marigold Care': 'reminder_walk_title',
        'Gentle Mind Games: Memory Match Flora': 'reminder_games_title',
        'Afternoon Chamomile Tea & Soothing Flute Music': 'reminder_flute_title',
        'Video Call with Daughter Sarah & Little Maya': 'reminder_call_title',
        'Evening Garden Sunset & Peaceful Chimes': 'reminder_sunset_title',
    }
    mem_map = {
        'Summers in St Ives, Cornwall': ('memory_stives_title', 'memory_stives_desc', 'memory_stives_loc'),
        'Morning Tea in Tezpur Garden': ('memory_tezpur_title', 'memory_tezpur_desc', 'memory_tezpur_loc'),
        "Maya's 7th Birthday Party": ('memory_birthday_title', 'memory_birthday_desc', 'memory_birthday_loc'),
        'Our Wedding Day in Wiltshire': ('memory_wedding_title', 'memory_wedding_desc', 'memory_wedding_loc'),
        'Traditional Weaving at the Village Fair': ('memory_sualkuchi_title', 'memory_sualkuchi_desc', 'memory_sualkuchi_loc'),
    }
    tag_map = {
        'all': 'all_memories',
        'family': 'family_holidays',
        'garden': 'garden_nature',
        'wedding': 'wedding_romance',
        'travel': 'travel_places',
    }
    if reminders:
        for r in reminders:
            key = title_map.get(r.title.strip())
            r.display_title = get_text(key, lang) if key else r.title

    if memories:
        for m in memories:
            m.display_tag = get_text(tag_map.get(m.tag, 'family_holidays'), lang)
            tup = mem_map.get(m.title.strip())
            if tup:
                m.display_title = get_text(tup[0], lang)
                m.display_description = get_text(tup[1], lang)
                m.display_location = get_text(tup[2], lang) if tup[2] else m.location
            else:
                m.display_title = m.title
                m.display_description = m.description
                m.display_location = m.location

def localize_game_sessions(sessions, lang):
    game_map = {
        'memory_match': 'game_memory_match_title',
        'sequence': 'game_sequence_title',
        'picture_recognition': 'game_picture_rec_title',
        'word_recall': 'game_word_recall_title',
        'gentle_garden': 'game_garden_title',
    }
    if sessions:
        for s in sessions:
            key = game_map.get(s.game_type)
            s.display_title = get_text(key, lang) if key else s.game_title

def get_or_create_default_user():
    """Ensure Eleanor exists as default companion user for ease of evaluation"""
    eleanor, _ = User.objects.get_or_create(username="eleanor", defaults={"first_name": "Eleanor", "last_name": "Vance"})
    if not hasattr(eleanor, 'profile'):
        UserProfile.objects.create(
            user=eleanor,
            role="elderly",
            preferred_language="en",
            companion_name="Eleanor Vance",
            caregiver_name="Sarah Vance (Daughter)",
            avatar_url="/static/images/stitch/img_a3312d477143.jpg"
        )
    return eleanor

def get_active_user(request):
    if request.user.is_authenticated:
        return request.user
    user = get_or_create_default_user()
    login(request, user)
    return user

def home_view(request):
    user = get_active_user(request)
    lang = get_current_lang(request)
    reminders = list(Reminder.objects.filter(user=user))
    pending_reminders = sum(1 for r in reminders if not r.is_completed)
    recent_memories = list(Memory.objects.filter(user=user)[:3])
    memories_count = Memory.objects.filter(user=user).count()

    localize_reminders_and_memories(reminders, recent_memories, lang)

    context = {
        'reminders': reminders,
        'pending_reminders_count': pending_reminders,
        'recent_memories': recent_memories,
        'memories_count': memories_count,
    }
    return render(request, 'home.html', context)

def games_library_view(request):
    get_active_user(request)
    return render(request, 'games_library.html')

def memory_match_view(request):
    get_active_user(request)
    return render(request, 'game_memory_match.html')

def sequence_view(request):
    get_active_user(request)
    return render(request, 'game_sequence.html')

def picture_recognition_view(request):
    get_active_user(request)
    return render(request, 'game_picture_recognition.html')

def word_recall_view(request):
    get_active_user(request)
    return render(request, 'game_word_recall.html')

def garden_view(request):
    get_active_user(request)
    return render(request, 'game_garden.html')

def game_completion_view(request):
    user = get_active_user(request)
    session_id = request.GET.get('session_id')
    game_name = request.GET.get('game', 'memory_match')

    session = None
    if session_id:
        try:
            session = GameSession.objects.get(id=int(session_id))
        except (GameSession.DoesNotExist, ValueError, TypeError):
            pass
    if not session:
        session = GameSession.objects.filter(user=user).first()

    context = {
        'session': session,
        'game_name': game_name,
    }
    return render(request, 'game_completion.html', context)

def memories_view(request):
    user = get_active_user(request)
    lang = get_current_lang(request)
    active_tag = request.GET.get('tag', 'all')

    if active_tag and active_tag != 'all':
        memories = list(Memory.objects.filter(user=user, tag=active_tag))
    else:
        memories = list(Memory.objects.filter(user=user))

    localize_reminders_and_memories(None, memories, lang)
    all_count = Memory.objects.filter(user=user).count()

    context = {
        'memories': memories,
        'active_tag': active_tag,
        'all_count': all_count,
    }
    return render(request, 'memories.html', context)

@require_POST
def add_memory_view(request):
    user = get_active_user(request)
    title = request.POST.get('title', '').strip()
    period = request.POST.get('period', '').strip()
    location = request.POST.get('location', '').strip()
    description = request.POST.get('description', '').strip()
    tag = request.POST.get('tag', 'family')
    image_url = request.POST.get('image_url', '/static/images/stitch/img_6d9f6639cbef.jpg')

    if title and description:
        Memory.objects.create(
            user=user,
            title=title,
            period=period or 'Cherished Moment',
            location=location or 'Assam, India',
            description=description,
            tag=tag,
            image_url=image_url,
            audio_label="Sarah's family audio note",
            audio_duration="1:10"
        )
    return redirect('memories')

def caregiver_view(request):
    user = get_active_user(request)
    lang = get_current_lang(request)
    sarah, _ = User.objects.get_or_create(username="sarah", defaults={"first_name": "Sarah", "last_name": "Vance"})

    if request.method == 'POST':
        mood = request.POST.get('mood', 'Bright & Peaceful')
        hydration = request.POST.get('hydration', 'Well Hydrated (4 of 5 cups)')
        notes = request.POST.get('notes', '')

        CaregiverLog.objects.create(
            caregiver=sarah,
            patient=user,
            mood=mood,
            hydration_status=hydration,
            notes=notes
        )
        return redirect('caregiver')

    game_sessions = list(GameSession.objects.filter(user=user)[:10])
    localize_game_sessions(game_sessions, lang)
    caregiver_logs = CaregiverLog.objects.filter(patient=user)[:5]
    latest_log = caregiver_logs.first()
    caregiver_logs = list(CaregiverLog.objects.filter(patient=user)[:5])
    
    mood_map = {
        'Bright & Peaceful (Sunny disposition)': 'mood_opt_bright',
        'Gentle & Content': 'mood_opt_gentle',
        'Quiet & Reflective': 'mood_opt_quiet',
        'Restful & Relaxed': 'mood_opt_restful',
    }
    for log in caregiver_logs:
        log.display_mood = get_text(mood_map.get(log.mood), lang) if log.mood in mood_map else log.mood

    latest_log = caregiver_logs[0] if caregiver_logs else None
    if latest_log:
        latest_log.display_hydration = get_text('caregiver_hydration_default', lang)
    memories_count = Memory.objects.filter(user=user).count()
    next_reminder = Reminder.objects.filter(user=user, is_completed=False).first()
    if next_reminder:
        localize_reminders_and_memories([next_reminder], None, lang)

    chart_days = [
        get_text('days_thursday', lang),
        get_text('days_friday', lang),
        get_text('days_saturday', lang),
        get_text('days_sunday', lang),
        get_text('days_monday', lang),
        get_text('days_tuesday', lang),
        get_text('days_today_wednesday', lang),
    ]

    context = {
        'game_sessions': game_sessions,
        'caregiver_logs': caregiver_logs,
        'latest_log': latest_log,
        'memories_count': memories_count,
        'next_reminder': next_reminder,
        'chart_days_json': json.dumps(chart_days, ensure_ascii=False),
    }
    return render(request, 'caregiver.html', context)

# ==========================================
# API ENDPOINTS
# ==========================================

@require_POST
def save_game_api(request):
    try:
        data = json.loads(request.body)
        user = get_active_user(request)

        session = GameSession.objects.create(
            user=user,
            game_type=data.get('game_type', 'memory_match'),
            game_title=data.get('game_title', 'Cognitive Mind Game'),
            score=data.get('score', 100),
            moves=data.get('moves', 0),
            mistakes=data.get('mistakes', 0),
            pairs_found=data.get('pairs_found', 0),
            duration_seconds=data.get('duration_seconds', 60),
            stars=data.get('stars', 3),
            notes=data.get('notes', '')
        )
        return JsonResponse({'success': True, 'session_id': session.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_POST
def toggle_reminder_api(request, reminder_id):
    try:
        user = get_active_user(request)
        reminder = get_object_or_404(Reminder, id=reminder_id, user=user)
        reminder.is_completed = not reminder.is_completed
        reminder.save()
        return JsonResponse({'success': True, 'is_completed': reminder.is_completed})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def set_language_api(request):
    lang = request.GET.get('lang') or request.POST.get('lang') or 'en'
    valid_codes = [c[0] for c in SUPPORTED_LANGUAGES]
    if lang not in valid_codes:
        lang = 'en'

    request.session['language'] = lang

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        request.user.profile.preferred_language = lang
        request.user.profile.save()

    next_url = request.GET.get('next') or request.POST.get('next') or '/'
    return redirect(next_url)

def switch_profile_view(request, role):
    if role == 'sarah':
        sarah, _ = User.objects.get_or_create(username="sarah", defaults={"first_name": "Sarah", "last_name": "Vance"})
        login(request, sarah)
        return redirect('caregiver')
    else:
        eleanor, _ = User.objects.get_or_create(username="eleanor", defaults={"first_name": "Eleanor", "last_name": "Vance"})
        login(request, eleanor)
        return redirect('home')
