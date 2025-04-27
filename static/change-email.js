import { auth, provider } from "./firebase-config.js";
import { getAuth, updateEmail } from "https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js";

const emailToChange = document.getElementById("emailChangeInput")
const changeEmailButton = document.getElementById("changeEmail")

const auth = getAuth();
updateEmail(auth.currentUser, "emailChangeInput").then(() => {
     console.log("Email changed to", user);.
}).catch((error) => {
    // An error occurred
    // ...
});
