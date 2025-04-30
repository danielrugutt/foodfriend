import { auth, provider } from "./firebase-config.js";
import { getAuth, updateEmail, EmailAuthProvider, reauthenticateWithCredential, sendEmailVerification } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js";

const emailToChange = document.getElementById("emailChangeInput");
const passwordPopup = document.getElementById("passwordPopup");
const confirmPasswordButton = document.getElementById("confirmPasswordButton");
const passwordInput = document.getElementById("passwordInput");


confirmPasswordButton.addEventListener('click', async () => {
    const user = auth.currentUser;

    if (!user) {
        console.error("No user is currently signed in.");
        return;
    }

    const currentPassword = passwordInput.value;
    const newEmail = emailToChange.value;

    if (!newEmail || !currentPassword) {
        alert("Please enter both your new email and current password.");
        return;
    }

    try {
        const credential = EmailAuthProvider.credential(user.email, currentPassword);

        // Reauthenticate the user
        await reauthenticateWithCredential(user, credential);
        console.log("Reauthentication successful.");

        // Update the user's email
        await updateEmail(user, newEmail);
        console.log("Email updated successfully to:", newEmail);
        alert("Email changed to " + newEmail + "!");

        // NOT NEEDED with how firebase is set up right now, if email enumeration is changed this will need to come back
        // Send a verification email to the new address
        // await sendEmailVerification(user);
        // alert("An email has been sent to you informing you of this change. You may click the verification link within it if you wish, but your email has already been changed!");

        // passwordPopup.style.display = 'none';
        passwordPopup.value = '';

    }
    catch (error) {
        if (error.code === 'auth/invalid-credential') {
            alert("Incorrect password. Please try again.");
        } else if (error.code === 'auth/invalid-email') {
            alert("The new email address is invalid. Please try again.");
        } else if (error.code === 'auth/email-already-in-use') {
            alert("This email address is already associated with another account.");
        } else if (error.code === 'auth/requires-recent-login') {
            alert("Please sign in again and retry this action for security reasons.");
        } else {
            alert("An error occurred: " + error.message);
        }
        console.error("Error during email change process:", error);
    }
});
