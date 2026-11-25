import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, GameSession, Memory, Reminder, CaregiverLog

class MindBloomCoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create Eleanor and Sarah
        self.eleanor = User.objects.create_user(username="eleanor", password="password123", first_name="Eleanor", last_name="Vance")
        self.profile_e = UserProfile.objects.create(
            user=self.eleanor,
            role="elderly",
            preferred_language="en",
            companion_name="Eleanor Vance",
            caregiver_name="Sarah Vance"
        )
        self.sarah = User.objects.create_user(username="sarah", password="password123", first_name="Sarah", last_name="Vance")
        self.profile_s = UserProfile.objects.create(
            user=self.sarah,
            role="caregiver",
            preferred_language="en",
            companion_name="Sarah Vance"
        )
        self.reminder = Reminder.objects.create(
            user=self.eleanor,
            title="Morning Tea",
            time_str="8:30 AM",
            category="tea",
            is_completed=False
        )
        self.memory = Memory.objects.create(
            user=self.eleanor,
            title="Summers in St Ives",
            period="Summer 1968",
            location="Cornwall",
            description="Warm sandy strolls.",
            tag="family",
            image_url="/static/images/stitch/img_b6120a6730fb.jpg"
        )

    def test_all_10_stitch_screens_load(self):
        """Verify all 10 Stitch screen templates render with HTTP 200"""
        endpoints = [
            reverse('home'),
            reverse('games_library'),
            reverse('memory_match'),
            reverse('sequence_game'),
            reverse('picture_recognition'),
            reverse('word_recall'),
            reverse('garden_game'),
            reverse('game_completion'),
            reverse('memories'),
            reverse('caregiver'),
        ]
        for url in endpoints:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"URL {url} failed with status {response.status_code}")
            self.assertContains(response, "MindBloom")

    def test_save_game_api(self):
        """Verify cognitive game results persist in SQLite database via API"""
        payload = {
            "game_type": "memory_match",
            "game_title": "Memory Match: Morning Flora & Familiar Keepsakes",
            "score": 100,
            "moves": 8,
            "mistakes": 2,
            "pairs_found": 6,
            "duration_seconds": 180,
            "stars": 3,
            "notes": "Test play completed perfectly."
        }
        response = self.client.post(
            reverse('save_game_api'),
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('session_id', data)

        # Verify in DB
        session = GameSession.objects.get(id=data['session_id'])
        self.assertEqual(session.score, 100)
        self.assertEqual(session.moves, 8)
        self.assertEqual(session.pairs_found, 6)

    def test_toggle_reminder_api(self):
        """Verify checking and unchecking reminders via AJAX API"""
        self.assertFalse(self.reminder.is_completed)
        response = self.client.post(reverse('toggle_reminder_api', args=[self.reminder.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('is_completed'))

        self.reminder.refresh_from_db()
        self.assertTrue(self.reminder.is_completed)

        # Toggle back
        response2 = self.client.post(reverse('toggle_reminder_api', args=[self.reminder.id]))
        self.assertFalse(response2.json().get('is_completed'))

    def test_language_persistence(self):
        """Verify regional language switching persists in session and translates headers"""
        # Switch to Assamese
        response = self.client.get(reverse('set_language') + "?lang=as&next=/")
        self.assertEqual(response.status_code, 302)

        # Load home page in Assamese
        home_resp = self.client.get(reverse('home'))
        self.assertEqual(home_resp.status_code, 200)
        self.assertEqual(self.client.session.get('language'), 'as')
        # Check Assamese brand or greeting text
        self.assertContains(home_resp, "মৃদু মনৰ খেলসমূহ")

    def test_add_memory(self):
        """Verify creating a new Cherished Memory in SQLite"""
        initial_count = Memory.objects.filter(user=self.eleanor).count()
        response = self.client.post(reverse('add_memory'), {
            'title': 'Bihu Celebration in Tezpur',
            'period': 'Spring 1980',
            'location': 'Tezpur, Assam',
            'description': 'Listening to dhol and pepa under the sunlit mango tree.',
            'tag': 'travel',
            'image_url': '/static/images/stitch/img_6d9f6639cbef.jpg'
        })
        self.assertEqual(response.status_code, 302)
        new_count = Memory.objects.filter(user=self.eleanor).count()
        self.assertEqual(new_count, initial_count + 1)

        mem = Memory.objects.get(title='Bihu Celebration in Tezpur')
        self.assertEqual(mem.location, 'Tezpur, Assam')

    def test_caregiver_log_post(self):
        """Verify caregiver can post a wellness log"""
        response = self.client.post(reverse('caregiver'), {
            'mood': 'Gentle & Content',
            'hydration': '5 of 5 cups water and herbal tea',
            'notes': 'Eleanor was very peaceful today.'
        })
        self.assertEqual(response.status_code, 302)
        log = CaregiverLog.objects.filter(patient=self.eleanor).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.mood, 'Gentle & Content')

    def test_switch_profile(self):
        """Verify seamless switching between Eleanor and Sarah"""
        resp_sarah = self.client.get(reverse('switch_profile', args=['sarah']))
        self.assertEqual(resp_sarah.status_code, 302)
        self.assertIn('caregiver', resp_sarah.url)

        resp_eleanor = self.client.get(reverse('switch_profile', args=['eleanor']))
        self.assertEqual(resp_eleanor.status_code, 302)
        self.assertIn('/', resp_eleanor.url)
