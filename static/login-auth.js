import { auth, provider } from "./firebase-config.js";

import { createUserWithEmailAndPassword,
         signInWithEmailAndPassword,
         signInWithPopup,
         sendPasswordResetEmail,
         onAuthStateChanged,
         signOut,
         updateEmail,
         reauthenticateWithCredential,
         EmailAuthProvider } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js";



/* == UI - Elements == */
const signInWithGoogleButtonEl = document.getElementById("sign-in-with-google-btn")
const signUpWithGoogleButtonEl = document.getElementById("sign-up-with-google-btn")
const emailInputEl = document.getElementById("email-input")
const passwordInputEl = document.getElementById("password-input")
const signInButtonEl = document.getElementById("sign-in-btn")
const signOutButtonEl = document.getElementById("sign-out-btn")
const createAccountButtonEl = document.getElementById("signup-form")
const emailForgotPasswordEl = document.getElementById("email-forgot-password")
const forgotPasswordButtonEl = document.getElementById("forgot-password-btn")

const errorMsgEmail = document.getElementById("email-error-message")
const errorMsgPassword = document.getElementById("password-error-message")
const errorMsgGoogleSignIn = document.getElementById("google-signin-error-message")


/* == UI - Event Listeners == */
signInWithGoogleButtonEl && signInWithGoogleButtonEl.addEventListener("click", authWithGoogle);
signInButtonEl           && signInButtonEl.addEventListener("click", authSignInWithEmail);
signOutButtonEl          && signOutButtonEl.addEventListener('click', logout);
signUpWithGoogleButtonEl && signUpWithGoogleButtonEl.addEventListener("click", authWithGoogle);
forgotPasswordButtonEl   && forgotPasswordButtonEl.addEventListener("click", resetPassword);
createAccountButtonEl    && createAccountButtonEl.addEventListener("submit", (e) => {
    e.preventDefault();
    authCreateAccountWithEmail();
});

/* === URL Variables === */
// URL variables
const url               = window.location.href;
const indexURL          = window.location.origin + '/index';
const forgotPasswordURL = window.location.origin + '/reset-password';
const dashboardURL      = window.location.origin + '/dashboard';
const loginURL          = window.location.origin + '/login';
const signupURL         = window.location.origin + '/signup';
const profileURL        = window.location.origin + '/profile';
const settingsURL       = window.location.origin + '/settings';
const homeURL           = window.location.origin + '/';



/* === Main Code === */

/* = Functions - Firebase - Authentication = */
onAuthStateChanged(auth, (user) => {
    if (user) {
        console.log("User is signed in: ", user.email);

        // Check if the user is on a public page and redirect to the dashboard
        const publicPages = [indexURL, loginURL, forgotPasswordURL, signupURL];
        if (publicPages.includes(url)) {
            // Ensure the backend session is established before redirecting
            user.getIdToken().then(idToken => {
                fetch('/auth', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${idToken}`
                    },
                }).then(response => {
                    if (response.ok) {
                        window.location.href = '/dashboard';
                    } else {
                        console.error('Backend session not established:', response.status);
                    }
                }).catch(error => {
                    console.error('Error establishing backend session:', error);
                });
            });
        }
    } else {
        console.log("User is not signed in");

        // Redirect to login if trying to access a protected page
        const publicPages = [indexURL, loginURL, forgotPasswordURL, signupURL, homeURL];
        if (!publicPages.includes(url)) {
            window.location.replace(loginURL);
        }
    }
});



async function authWithGoogle() {
    provider.setCustomParameters({
        prompt: 'select_account'
    });

    try {
        const result = await signInWithPopup(auth, provider);

        if (!result || !result.user) {
            throw new Error('Authentication failed: No user data returned.');
        }

        const user = result.user;
        const email = user.email;

        if (!email) {
            throw new Error('Authentication failed: No email address returned.');
        }

        const idToken = await user.getIdToken();

        // Log the user in (your app logic)
        loginUser(user, idToken);

    } catch (error) {
        handleLogging(error, 'Error during Google authentication');
    }
}



function authSignInWithEmail() {

    const email = emailInputEl.value
    const password = passwordInputEl.value

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed in 
            const user = userCredential.user;

            user.getIdToken().then(function(idToken) {
                loginUser(user, idToken)
            });

            console.log("User signed in: ", user)
        })
        .catch((error) => {
            const errorCode = error.code;
            console.error("Error code: ", errorCode)
            if (errorCode === "auth/invalid-email") {
                errorMsgEmail.textContent = "Invalid email"
            } else if (errorCode === "auth/invalid-credential") {
                errorMsgPassword.textContent = "Login failed - invalid email or password"
            }
            else
                alert("Error signing in: ", errorCode)
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
        // await addNewUserToFirestore(user);

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



function resetPassword() {
    const emailToReset = emailForgotPasswordEl.value

    clearInputField(emailForgotPasswordEl)

    sendPasswordResetEmail(auth, emailToReset)
    .then(() => {
        // Password reset email sent!
        const resetFormView = document.getElementById("reset-password-view")
        const resetSuccessView = document.getElementById("reset-password-confirmation-page")

        resetFormView.style.display = "none"
        resetSuccessView.style.display = "block"
    })
    .catch((error) => {
        const errorCode = error.code;
        alert("Error sending reset email: ", errorCode);
    });
}


function loginUser(user, idToken) {
    fetch('/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${idToken}`
        },
    }).then(response => {
        if (response.ok) {
            console.log('User authenticated successfully');
            window.location.href = '/dashboard'; // Redirect to dashboard
        } else {
            console.error('Failed to authenticate user:', response.status);
            response.json().then(data => console.error(data));
            alert('Authentication failed. Please try again.');
        }
    }).catch(error => {
        console.error('Error with Fetch operation:', error);
        alert('An error occurred while logging in. Please try again.');
    });
}

function logout(event) {
    event.preventDefault();
    signOut(auth)
    .then(() => {
        // Successfully signed out of Firebase
        window.location.href = '/logout'; // Redirect to Flask logout route
    })
    .catch((error) => {
        console.error('Error signing out:', error);
    });
}

// /* = Functions - UI = */
function clearInputField(field) {
	field.value = ""
}

function clearAuthFields() {
	clearInputField(emailInputEl)
	clearInputField(passwordInputEl)
}


