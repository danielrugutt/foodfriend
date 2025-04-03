import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js";
import { getAuth, 
         GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyCiRNR5N7xNoOJcDHaq-k0fEoMCfbhM5p4",
  authDomain: "foodfriend-a774e.firebaseapp.com",
  projectId: "foodfriend-a774e",
  storageBucket: "foodfriend-a774e.firebasestorage.app",
  messagingSenderId: "580311697199",
  appId: "1:580311697199:web:4067c1105229fc05d303da",
  measurementId: "G-6DL6V70QM3"
};

  // Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const db = getFirestore(app);

export { auth, provider, db };
