import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAuth, 
         GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

// // Your web app's Firebase configuration
// const firebaseConfig = {
//   apiKey: "AIzaSyBPa68RUPQThaVJlExwO6ZWoPp5Uxw13sI",
//   authDomain: "foodfriend-6f24c.firebaseapp.com",
//   projectId: "foodfriend-6f24c",
//   storageBucket: "foodfriend-6f24c.firebasestorage.app",
//   messagingSenderId: "878081467176",
//   appId: "1:878081467176:web:06641146e508525083661d"
//
// };

const firebaseConfig = {
  apiKey: "AIzaSyCiRNR5N7xNoOJcDHaq-k0fEoMCfbhM5p4",
  authDomain: "foodfriend-a774e.firebaseapp.com",
  projectId: "foodfriend-a774e",
  storageBucket: "foodfriend-a774e.firebasestorage.app",
  messagingSenderId: "580311697199",
  appId: "1:580311697199:web:4067c1105229fc05d303da",
};

  // Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const db = getFirestore(app);

export { auth, provider, db };
