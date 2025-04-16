document.addEventListener("DOMContentLoaded", () => {
    const deleteAccountDiv = document.getElementById("delete-account-div");
    const deletionConfirmationDiv = document.getElementById("deletion-confirmation-div");
    const deleteAccountButton = deleteAccountDiv.querySelector("button");
    const cancelButton = document.getElementById("deletion-cancel-btn");
    const confirmDeleteButton = document.getElementById("confirm-delete-btn");

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

    // Confirm delete button to send a POST request to the server
    confirmDeleteButton.addEventListener("click", async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("/delete-account", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (response.ok) {
                window.location.href = "/login"; // Redirect to login page
            } else {
                console.error("Failed to delete account");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    });
});