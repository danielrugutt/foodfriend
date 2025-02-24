// Import the functions you need from the SDKs you need
import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js';
// import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCiRNR5N7xNoOJcDHaq-k0fEoMCfbhM5p4",
  authDomain: "foodfriend-a774e.firebaseapp.com",
  projectId: "foodfriend-a774e",
  storageBucket: "foodfriend-a774e.firebasestorage.app",
  messagingSenderId: "580311697199",
  appId: "1:580311697199:web:7bd462885f6eb46cd303da",
  measurementId: "G-SWSBWK34L3"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);

export default app;
