import app from "../src/config.js";
import { getAuth, signInWithEmailAndPassword } from 'https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js';

const auth = getAuth(app);



console.log("Firebase running: ", app);


// Log in function
function loginWithEmailPassword(email, password) {
    signInWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        // Signed in
        const user = userCredential.user;
        console.log("Logged in successfully: ", user);

        document.getElementById("message").textContent = "Logged in as " + email;
        // You can now redirect to a dashboard or home page
      })
      .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.log("Error: ", errorCode, errorMessage);
        // You can show an error message to the user here
      });
}

document.getElementById("login-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    loginWithEmailPassword(email, password);
});