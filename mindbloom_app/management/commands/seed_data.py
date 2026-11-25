from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from mindbloom_app.models import UserProfile, GameSession, Memory, Reminder, CaregiverLog

class Command(BaseCommand):
    help = "Seeds initial sample data for MindBloom (Eleanor & Sarah)"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding MindBloom sample data...")

        # Create or update Eleanor (Elderly Patient)
        eleanor, created = User.objects.get_or_create(username="eleanor", defaults={"email": "eleanor@mindbloom.org", "first_name": "Eleanor", "last_name": "Vance"})
        if created:
            eleanor.set_password("mindbloom123")
            eleanor.save()

        profile_e, _ = UserProfile.objects.get_or_create(
            user=eleanor,
            defaults={
                "role": "elderly",
                "preferred_language": "en",
                "companion_name": "Eleanor Vance",
                "caregiver_name": "Sarah Vance (Daughter)",
                "avatar_url": "/static/images/stitch/img_a3312d477143.jpg"
            }
        )

        # Create or update Sarah (Caregiver)
        sarah, created = User.objects.get_or_create(username="sarah", defaults={"email": "sarah@mindbloom.org", "first_name": "Sarah", "last_name": "Vance"})
        if created:
            sarah.set_password("mindbloom123")
            sarah.save()

        profile_s, _ = UserProfile.objects.get_or_create(
            user=sarah,
            defaults={
                "role": "caregiver",
                "preferred_language": "en",
                "companion_name": "Sarah Vance",
                "caregiver_name": "Sarah Vance",
                "avatar_url": "/static/images/stitch/img_570dff029353.jpg"
            }
        )

        # Create Initial Memories
        memories_data = [
            {
                "title": "Summers in St Ives, Cornwall",
                "period": "Summer 1968",
                "location": "St Ives Harbour, Cornwall",
                "description": "Walking along the warm sandy quay with David, watching the blue fishing boats bob gently in the tide. We shared warm Cornish saffron buns by the sea wall as the gulls glided across the afternoon breeze.",
                "image_url": "/static/images/stitch/img_3e85e15af82d.jpg",
                "tag": "family",
                "audio_label": "Sarah's audio description: The St Ives summer trip",
                "audio_duration": "1:24"
            },
            {
                "title": "Morning Tea in Tezpur Garden",
                "period": "Autumn 1974",
                "location": "Tezpur, Assam",
                "description": "Sitting on the cane planter chairs on the veranda surrounded by blossoming pink orchids. The gentle aroma of fresh autumn flush black tea and marigold flowers filled the crisp Brahmaputra morning breeze.",
                "image_url": "/static/images/stitch/img_6d9f6639cbef.jpg",
                "tag": "garden",
                "audio_label": "Sarah reads Eleanor's tea garden journal entry",
                "audio_duration": "1:05"
            },
            {
                "title": "Maya's 7th Birthday Party",
                "period": "Spring 1986",
                "location": "Family Home Courtyard",
                "description": "A sunny garden gathering with ribbon bunting in the apple trees. Maya blew out seven candles on her strawberry sponge cake while little Oliver tried to catch soap bubbles on the lawn.",
                "image_url": "/static/images/stitch/img_5fbd5f53370d.jpg",
                "tag": "family",
                "audio_label": "Maya's sweet voice note remembering her birthday cake",
                "audio_duration": "0:48"
            },
            {
                "title": "Our Wedding Day in Wiltshire",
                "period": "June 1964",
                "location": "St Mary's Church, Wiltshire",
                "description": "A warm June morning under stone arches. The bells chimed across the village as we walked out into the sunshine together, showered with rose petals by our dearest family and neighbours.",
                "image_url": "/static/images/stitch/img_28b47bd11b77.jpg",
                "tag": "wedding",
                "audio_label": "Recorded chime of Wiltshire bells with David's note",
                "audio_duration": "1:45"
            },
            {
                "title": "Traditional Weaving at the Village Fair",
                "period": "Winter 1979",
                "location": "Sualkuchi, Assam",
                "description": "Watching the skilled artisans weave golden Muga silk on traditional wooden looms (Taat Xaal). The rhythmic clacking of the shuttle and laughter of weavers left an indelible peaceful memory.",
                "image_url": "/static/images/stitch/img_3f33aedd8b33.jpg",
                "tag": "travel",
                "audio_label": "Rhythmic loom sound with flute melody",
                "audio_duration": "1:15"
            }
        ]

        for m_data in memories_data:
            Memory.objects.get_or_create(
                user=eleanor,
                title=m_data["title"],
                defaults=m_data
            )

        # Create Initial Reminders
        reminders_data = [
            {
                "title": "Morning Assam Tea & Warm Porridge",
                "time_str": "8:30 AM",
                "category": "tea",
                "icon": "local_cafe",
                "is_completed": True
            },
            {
                "title": "Gentle Courtyard Walk & Fresh Marigold Care",
                "time_str": "10:30 AM",
                "category": "walk",
                "icon": "nature",
                "is_completed": True
            },
            {
                "title": "Gentle Mind Games: Memory Match Flora",
                "time_str": "11:45 AM",
                "category": "wellness",
                "icon": "spa",
                "is_completed": True
            },
            {
                "title": "Afternoon Chamomile Tea & Soothing Flute Music",
                "time_str": "3:00 PM",
                "category": "tea",
                "icon": "local_cafe",
                "is_completed": False
            },
            {
                "title": "Video Call with Daughter Sarah & Little Maya",
                "time_str": "4:30 PM",
                "category": "family",
                "icon": "call",
                "is_completed": False
            },
            {
                "title": "Evening Garden Sunset & Peaceful Chimes",
                "time_str": "6:15 PM",
                "category": "wellness",
                "icon": "wb_twilight",
                "is_completed": False
            }
        ]

        for r_data in reminders_data:
            Reminder.objects.get_or_create(
                user=eleanor,
                title=r_data["title"],
                defaults=r_data
            )

        # Create Past Game Sessions (for Eleanor's history and Chart.js caregiver view)
        games_data = [
            {
                "game_type": "memory_match",
                "game_title": "Memory Match: Morning Flora & Keepsakes",
                "score": 100,
                "moves": 8,
                "mistakes": 2,
                "pairs_found": 6,
                "duration_seconds": 210,
                "stars": 3,
                "completed_at": timezone.now() - timedelta(hours=3),
                "notes": "Completed smoothly with calm breathing and great recognition of orchids."
            },
            {
                "game_type": "sequence",
                "game_title": "Remember the Sequence: Morning Chimes",
                "score": 95,
                "moves": 6,
                "mistakes": 1,
                "pairs_found": 3,
                "duration_seconds": 180,
                "stars": 3,
                "completed_at": timezone.now() - timedelta(days=1),
                "notes": "Followed the 3-step chimes rhythm with joy."
            },
            {
                "game_type": "picture_recognition",
                "game_title": "Picture Recognition: Familiar Comforts",
                "score": 90,
                "moves": 4,
                "mistakes": 1,
                "pairs_found": 4,
                "duration_seconds": 150,
                "stars": 3,
                "completed_at": timezone.now() - timedelta(days=2),
                "notes": "Recognised Jasmine blossom and terracotta teacup instantly."
            },
            {
                "game_type": "word_recall",
                "game_title": "Word & Picture Recall: Treasures of Home",
                "score": 85,
                "moves": 5,
                "mistakes": 2,
                "pairs_found": 3,
                "duration_seconds": 240,
                "stars": 2,
                "completed_at": timezone.now() - timedelta(days=3),
                "notes": "Engaged warmly with silk loom and bell metal bowl cards."
            },
            {
                "game_type": "gentle_garden",
                "game_title": "English Garden Blossoms: Relaxing Memory Pair",
                "score": 100,
                "moves": 7,
                "mistakes": 0,
                "pairs_found": 5,
                "duration_seconds": 195,
                "stars": 3,
                "completed_at": timezone.now() - timedelta(days=4),
                "notes": "Calm, continuous pairing of hydrangeas and roses."
            }
        ]

        for g in games_data:
            GameSession.objects.get_or_create(
                user=eleanor,
                game_type=g["game_type"],
                completed_at=g["completed_at"],
                defaults=g
            )

        # Create Caregiver Daily Log
        CaregiverLog.objects.get_or_create(
            caregiver=sarah,
            patient=eleanor,
            date=timezone.now().date(),
            defaults={
                "mood": "Bright & Peaceful (Sunny disposition)",
                "mood_score": 92,
                "hydration_status": "Well Hydrated (4 of 5 cups chamomile & warm ginger water)",
                "sleep_notes": "Rested peacefully for 8.2 hours with soft morning sunlight.",
                "notes": "Eleanor had a delightful morning playing Memory Match. She recalled her memories in Tezpur and was very cheerful during lunch."
            }
        )

        self.stdout.write(self.style.SUCCESS("MindBloom sample data successfully seeded!"))
