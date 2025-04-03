import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, 
         signInWithEmailAndPassword, signOut, 
         onAuthStateChanged, sendPasswordResetEmail,
         GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js";
import { getFirestore, collection, addDoc } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-firestore.js";


const firebaseConfig = {
  apiKey: "AIzaSyCiRNR5N7xNoOJcDHaq-k0fEoMCfbhM5p4",
  authDomain: "foodfriend-a774e.firebaseapp.com",
  projectId: "foodfriend-a774e",
  storageBucket: "foodfriend-a774e.firebasestorage.app",
  messagingSenderId: "580311697199",
  appId: "1:580311697199:web:4067c1105229fc05d303da",
  measurementId: "G-6DL6V70QM3"
};

document.addEventListener("DOMContentLoaded", function() {


  // Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const db = getFirestore(app);


// URL variables
const url               = window.location.href;
const indexURL          = window.location.origin + '/index.html';
const forgotPasswordURL = window.location.origin + '/forgot_password.html';
const dashboardURL      = window.location.origin + '/dashboard.html';
const loginURL          = window.location.origin + '/login.html';
const signupURL         = window.location.origin + '/signup.html';



// Session Handling
onAuthStateChanged(auth, (user) => {
    if (user) {
        // redirect to dashboard when logged in, but in a signin/ signup location
        if (url == loginURL || url == forgotPasswordURL || url == signupURL)
            window.location.replace(dashboardURL);


    }
    else {
        // disallow privileged access to users that aren't signed in
        if (url != indexURL && url != loginURL && url != forgotPasswordURL && url != signupURL )
            window.location.replace(indexURL);
    }
});

/* == UI - Elements == */
const signInWithGoogleButtonEl = document.getElementById("sign-in-with-google-btn")
const signUpWithGoogleButtonEl = document.getElementById("sign-up-with-google-btn")
const emailInputEl             = document.getElementById("email-input")
const passwordInputEl          = document.getElementById("password-input")
const signInButtonEl           = document.getElementById("sign-in-btn")
const signOutButtonEl          = document.getElementById("sign-out-btn");
const createAccountButtonEl    = document.getElementById("create-account-btn")
const emailForgotPasswordEl    = document.getElementById("email-forgot-password")
const forgotPasswordButtonEl   = document.getElementById("forgot-password-btn")

const errorMsgEmail            = document.getElementById("email-error-message")
const errorMsgPassword         = document.getElementById("password-error-message")
const errorMsgGoogleSignIn     = document.getElementById("google-signin-error-message")


/* == UI - Event Listeners == */
signInWithGoogleButtonEl && signInWithGoogleButtonEl.addEventListener("click", authSignInWithGoogle);
signUpWithGoogleButtonEl && signUpWithGoogleButtonEl.addEventListener("click", authSignInWithGoogle);
signInButtonEl           && signInButtonEl.addEventListener("click", authSignInWithEmail);
createAccountButtonEl    && createAccountButtonEl.addEventListener("click", authCreateAccountWithEmail);
forgotPasswordButtonEl   && forgotPasswordButtonEl.addEventListener("click", resetPassword);
signOutButtonEl          && signOutButtonEl.addEventListener('click', logout);


/* === Main Code === */

/* = Functions - Firebase - Authentication = */

function authSignInWithEmail() {

    const email = emailInputEl.value
    const password = passwordInputEl.value

    signInWithEmailAndPassword(auth, email, password)
    .then(() => {
        // Signed in 
        window.location.replace(dashboardURL);
    })
    .catch((error) => {
        const errorCode = error.code;
        console.error("Error code: ", errorCode)
        if (errorCode === "auth/invalid-email") {
            errorMsgEmail.textContent = "Invalid email"
        } 
        else if (errorCode === "auth/invalid-credential") {
            errorMsgPassword.textContent = "Login failed - invalid email or password"
        } 
        else {
            // unhandled errors
            alert(errorCode, error.message);
        }
    });
}

// Function to sign in with Google authentication
async function authSignInWithGoogle() {
    // Configure Google Auth provider with custom parameters
    provider.setCustomParameters({
        'prompt': 'select_account'  // Forces the user to select an account every time
    });

    try {
        // Attempt to sign in with a popup and retrieve user data
        const result = await signInWithPopup(auth, provider);

        // Check if result.user exists
        const user = result.user;
        if (!user) {
            throw new Error('Authentication failed: No user data returned.');
        }

        const email = user.email;
        if (!email) {
            throw new Error('Authentication failed: No email address returned.');
        }

        // should redirect automatically with onAuthStateChange trigger
    } catch (error) {
        // Handle errors, such as user denial or network failure
        console.error('Error during sign-in with Google:', error.message);
        
        // Optionally display an error message to the user
        alert('Sign-in failed: ' + error.message);
    }
}



function logout() {
    signOut(auth).then(() => {
        // logout successful
    })
    .catch((error) => {
        // there was an error
        const errorCode    = error.code;
        const errorMessage = error.message;
        alert(errorCode, errorMessage);
    });
}


function resetPassword() {
    
    const email = emailForgotPasswordEl.value;

    clearInputField(email);
  
    sendPasswordResetEmail(auth, email)
    .then(() => {
        // Password reset email sent!
        const resetFormView = document.getElementById("reset-password-view")
        const resetSuccessView = document.getElementById("reset-password-confirmation-page")

        resetFormView.style.display = "none"
        resetSuccessView.style.display = "block"
    })
    .catch((error) => {
        // Handle errors
        alert("Error sending password reset email:" + error.code);
    });
}


async function authCreateAccountWithEmail() {
    try {
        const email = emailInputEl.value;
        const password = passwordInputEl.value;

        // Create user and wait for Firebase to complete the operation
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        // Add user to Firestore (wait for it to finish)
        await addNewUserToFirestore(user);

        console.log("User successfully created and logged in:", user);

    } catch (error) {
        // Handle errors properly
        if (error.code === "auth/invalid-email") {
            errorMsgEmail.textContent = "Invalid email";
        } else if (error.code === "auth/weak-password") {
            errorMsgPassword.textContent = "Password must be at least 6 characters";
        } else if (error.code === "auth/email-already-in-use") {
            errorMsgEmail.textContent = "An account already exists for this email.";
        } else {
            console.error("Error:", error.message);
            alert(error.message);
        }
    }
}



// /* = Functions - UI = */
function clearInputField(field) {
	field.value = ""
}

function clearAuthFields() {
	clearInputField(emailInputEl)
	clearInputField(passwordInputEl)
}


/* === Firestore Function === */

async function addNewUserToFirestore(user) {
    try {
        const docRef = await addDoc(collection(db, "users"), {
            uid: user.uid,
            email: user.email,
            createdAt: new Date(),
        });
        console.log("Document written with ID: ", docRef.id);
    } catch (e) {
        console.error("Error adding document: ", e);
    }
}
// end of DOM event listener
});