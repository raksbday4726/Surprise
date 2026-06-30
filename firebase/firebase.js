/* =====================================================
   FIREBASE.JS — Wishes Storage
   ===================================================== */

// ─── DEMO MODE (localStorage — no Firebase needed) ───
// Wishes are stored locally in the browser for testing.
// To use real Firebase, replace the functions below with
// the actual Firestore calls shown in the comments.

function saveWishLocal(name, message) {
  try {
    const wishes = JSON.parse(localStorage.getItem('raksitha_wishes') || '[]');
    wishes.unshift({
      id: Date.now(),
      name: name,
      message: message,
      createdAt: new Date().toLocaleDateString('en-IN', {
        day: 'numeric', month: 'long', year: 'numeric'
      })
    });
    localStorage.setItem('raksitha_wishes', JSON.stringify(wishes.slice(0, 200)));
    return true;
  } catch (e) { return false; }
}

function loadWishesLocal() {
  try {
    return JSON.parse(localStorage.getItem('raksitha_wishes') || '[]');
  } catch (e) { return []; }
}

// ─── FIREBASE SETUP (uncomment when ready) ──────────
/*
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

async function saveWishFirebase(name, message) {
  await db.collection('wishes').add({
    name, message,
    timestamp: firebase.firestore.FieldValue.serverTimestamp(),
    createdAt: new Date().toLocaleDateString('en-IN', {day:'numeric',month:'long',year:'numeric'})
  });
}

async function loadWishesFirebase() {
  const snap = await db.collection('wishes').orderBy('timestamp','desc').limit(100).get();
  return snap.docs.map(d => ({id: d.id, ...d.data()}));
}
*/
