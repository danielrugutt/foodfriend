document.addEventListener("DOMContentLoaded", () => {
    const deleteAccountDiv = document.getElementById("delete-account-div");
    const deletionConfirmationDiv = document.getElementById("deletion-confirmation-div");
    const deleteAccountButton = deleteAccountDiv.querySelector("button");
    const cancelButton = document.getElementById("deletion-cancel-btn");

    // Show confirmation div and hide the initial div
    deleteAccountButton.addEventListener("click", () => {
        deleteAccountDiv.style.display = "none";
        deletionConfirmationDiv.style.display = "block";

        // Set a countdown to switch back after 5 seconds
        const timeoutId = setTimeout(() => {
            deletionConfirmationDiv.style.display = "none";
            deleteAccountDiv.style.display = "block";
        }, 5000);

        // Cancel the timeout if the user interacts with the confirmation div
        deletionConfirmationDiv.addEventListener("click", () => {
            clearTimeout(timeoutId);
        }, { once: true });
    });

    // Cancel button to go back to the initial state
    cancelButton.addEventListener("click", (e) => {
        e.preventDefault();
        deletionConfirmationDiv.style.display = "none";
        deleteAccountDiv.style.display = "block";
    });
});