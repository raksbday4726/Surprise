# 💜 A Secret Place — Raksitha's Birthday Universe

## 🚀 How to Deploy
1. Upload this folder to **Vercel** (drag & drop at vercel.com/new) — it goes live instantly, free.
2. Share the link with Raksitha 💜

---

## 🎵 Adding Songs (plays directly — no Spotify redirect)

1. Put your `.mp3` files in `assets/songs/`
   e.g. `assets/songs/perfect.mp3`

2. Open `story.html`, find the `songs` array (around line 190), uncomment the `src` lines:
   ```js
   { title: "Perfect", artist: "Ed Sheeran", emoji: "💜",
     src: "assets/songs/perfect.mp3"   // ← add this
   }
   ```

3. That's it — tap the song row to play instantly in the built-in player bar.

---

## 📸 Adding Photos (gallery between Wishes and Final section)

1. Put photos in `assets/images/`
   e.g. `assets/images/photo1.jpg`, `photo2.jpg` …

2. Open `story.html`, find the `photoGallery` array (around line 200):
   ```js
   { src: "assets/images/photo1.jpg",  caption: "The moment it all began", date: "12 Oct 2023", style: "polaroid", tilt: "-2deg" },
   { src: "assets/images/photo2.jpg",  caption: "You, always",             date: "Our story",   style: "canva"                  },
   ```

3. Style options:
   - `"polaroid"` — white frame, hand-tilted, Dancing Script caption
   - `"canva"`    — tall Canva love template style card
   - `"square"`   — clean square crop

4. Tap any photo to open it in the lightbox fullscreen.

---

## 🔐 Login Dates
| Who | Date |
|-----|------|
| Rahul | 07-09-2005 |
| Raksitha | 04-07-2006 |
| Together since | 12-10-2023 |

Wrong dates → redirect to birthday wishes page (no "wrong password" shown).

---

## 📂 Project Structure
```
raksitha-birthday/
├── index.html          Login page
├── story.html          Full story + all sections
├── wish.html           Birthday wishes form
├── css/style.css       Complete design system
├── js/universe.js      Stars, hearts, particles, clouds
├── firebase/firebase.js Wish storage (localStorage + Firebase)
└── assets/
    ├── images/         ← Drop your photos here
    └── songs/          ← Drop your MP3s here
```
