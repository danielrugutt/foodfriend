document.addEventListener("DOMContentLoaded", () => {
    const deleteAccountDiv = document.getElementById("delete-account-div");
    const deletionConfirmationDiv = document.getElementById("deletion-confirmation-div");
    const deleteAccountButton = deleteAccountDiv.querySelector("button");
    const cancelButton = document.getElementById("deletion-cancel-btn");

    // Show confirmation div and hide the initial div
    deleteAccountButton.addEventListener("click", () => {
        deleteAccountDiv.style.display = "none";
        deletionConfirmationDiv.style.display = "block";
    });

    // Cancel button to go back to the initial state
    cancelButton.addEventListener("click", (e) => {
        e.preventDefault();
        deletionConfirmationDiv.style.display = "none";
        deleteAccountDiv.style.display = "block";
    });
});