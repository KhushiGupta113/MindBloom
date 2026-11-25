# MindBloom: AI-Based Cognitive Gaming and Memory Assistance Platform

> **Project Title:** AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in North Eastern Region (NER)  
> **Product Name:** MindBloom  
> **Source Design System:** Google Stitch Project — *MindBloom Calm Warmth Redesign* (ID: `18079229948759559368`)

---

### Important Educational Notice
> **MindBloom is an educational assistance and cognitive engagement platform, not a medical diagnostic tool.**  
> It does not diagnose, prevent, treat, or cure dementia. All game scores, memory activities, and daily rhythm guideposts represent gentle engagement, comfort, and cognitive practice rather than clinical assessments.

---

## 🌸 Key Features Implemented from Stitch

MindBloom faithfully translates all **10 Google Stitch screens** into a functional Django application with the Calm Warmth design language, tailored to North Eastern Region (NER) cultural themes (Assam tea gardens, orchids, brass temple bells, traditional bell metal kahi, and silk looms):

1. **Home Sanctuary (Elderly User Dashboard)** (`/`)
   - Reassuring daily orientation banner ("Good morning, Eleanor. It's lovely to see you.")
   - Date, weather, and gentle affirmation badges
   - Four large 56px action cards: *Gentle Brain Games*, *My Cherished Memories*, *Daily Rhythm & Reminders*, and *My Peaceful Progress*
   - Interactive daily reminder checklist with instant AJAX toggle
   - Voice note player with audio narration

2. **Cognitive Games Library** (`/games/`)
   - 5 cognitive games hub with warm preview cards, estimated times, and gentle tags
   - Calming meadow ambience audio player
   - Sarah's audio walkthrough explanation

3. **Memory Match Game** (`/games/memory-match/`)
   - Tactile 4x3 grid of 12 cards (6 matching pairs of NER flora and keepsakes)
   - Real interactive card flipping, match detection, turns counter, and harmonic Web Audio chimes
   - Automatically saves game session score and duration to SQLite, transitioning to celebration

4. **Remember the Sequence Game** (`/games/sequence/`)
   - 3-step sequence memory game: *Brass Temple Bell*, *Steaming Ceramic Teacup*, and *Fresh Marigold Garland*
   - "Audio Chime Helper" demonstration with harmonic glow
   - Tactile tapping in order, gentle mistake correction, and completion saving

5. **Picture Recognition Game** (`/games/picture-recognition/`)
   - Multi-round recognition challenges (Star Jasmine blossom, Brass temple bell, Traditional silk loom)
   - Read Question Aloud speech synthesis
   - Touch-friendly cards, instant checkmark affirmation, and score persistence

6. **Word and Picture Recall Game** (`/games/word-recall/`)
   - Phase 1: Study phase with clear large text and high-res imagery
   - Phase 2: Recall phase where user selects the 3 studied keepsakes from a grid of 6 items
   - Score calculation and completion celebration

7. **English Garden Blossoms (Mindfulness Garden Game)** (`/games/garden/`)
   - Calming flower pairing (Antique Tea Rose, Sweet Pea, Blue Hydrangea, English Lavender)
   - Gentle garden blossoms found tracker and soft meadow ambience

8. **Game Completion & Celebration** (`/games/completion/`)
   - Non-competitive, compassionate celebration ("A Gentle Morning Well Spent")
   - Summary of gentle turns, unhurried time in calm flow, and mind state
   - Daughter Sarah's voice note player with animated waveform bars
   - "Play Again", "Back to Games Library", and "Home Sanctuary" navigation

9. **Cherished Memories Scrapbook** (`/memories/`)
   - Physical paper scrapbook aesthetics with washi tape details
   - Categorized by: *All Memories*, *Family & Holidays*, *Garden & Nature*, *Wedding & Romance*, *Travel & Places*
   - Working "+ Add a Cherished Memory" modal and form saving new stories to database
   - Per-memory audio player with soothing narration

10. **Family Circle & Caregiver Support Dashboard** (`/caregiver/`)
    - Eleanor's daily mood gauge, hydration comfort tracker, and next gentle reminder
    - Weekly Cognitive Engagement Trend interactive chart powered by Chart.js
    - History table of completed game sessions from SQLite
    - Form to record caregiver observations and daily notes

---

## 🌐 Regional Language Selector (NER Localization)

Located in the global header with persistent session storage:
- **English** (Default)
- **Assamese (অসমীয়া)**
- **Bodo (बड़ो)**
- **Manipuri / Meitei (মৈতৈলোন্)**
- **Khasi (Ka Ktien Khasi)**
- **Garo (A·chik)**
- **Mizo (Mizo ṭawng)**
- **Kokborok (Kokborok)**
- **Nepali (नेपाली)**

Verified translations are provided for primary navigation, controls, buttons, and accessibility prompts, with automatic graceful fallback to English.

---

## 🔊 Accessibility & Dementia-Friendly Design

- **Typography:** Warm serif headlines (*Merriweather*) and clean, legible body text (*Plus Jakarta Sans*).
- **Text Size Adjustment:** Dynamic toggle between Normal, Large, and Extra Large text size.
- **Read Aloud:** Built-in SpeechSynthesis integration reading page instructions softly and clearly.
- **Need a Hand? Modal:** Instant reassurance modal with one-tap calling to caregiver Sarah (555-0192) or companion device.
- **Web Audio API Chimes:** Pure client-side harmonic bell and chime synthesizer without external audio file dependencies.
- **Tactile Click Targets:** All primary buttons are sized at 48px–56px height with high contrast.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.14+, Django 6.1
- **Database:** SQLite (`db.sqlite3`)
- **Frontend:** Django Templates, Tailwind CSS (Stitch Calm Warmth tokens), Google Fonts, Material Symbols Outlined
- **Charts:** Chart.js
- **Audio:** Web Audio API (Synthesized chimes) & Web Speech Synthesis API

---

## 🚀 Running the Project Locally on Windows

### 1. Clone or Open the Workspace
```powershell
cd c:\Users\Khushi\Downloads\MindBloom
```

### 2. Verify / Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Apply Database Migrations
```powershell
python manage.py migrate
```

### 4. (Optional) Seed Sample Data
Populates Eleanor Vance's memories, reminders, past game history, and caregiver notes:
```powershell
python manage.py seed_data
```

### 5. Run the Automated Tests
```powershell
python manage.py test
```

### 6. Start the Development Server
```powershell
python manage.py runserver 127.0.0.1:8000
```

Open your browser at:  
👉 **http://127.0.0.1:8000/**

---

## 👤 Sample Demonstration Accounts

- **Eleanor Vance (Elderly Patient)**: `username: eleanor`, `password: mindbloom123`
- **Sarah Vance (Caregiver)**: `username: sarah`, `password: mindbloom123`

You can switch between Eleanor's view and Sarah's caregiver view at any time by clicking the profile avatar in the top right corner of the header.
