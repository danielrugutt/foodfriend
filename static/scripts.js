document.addEventListener("DOMContentLoaded", function() {
    // Toggles the hamburger menu with click
    const hamburger = document.querySelector('.hamburger');
    const navRight = document.getElementById('navbarRight');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            // Toggle navbar visibility
            if (navRight.style.left === "0px" || navRight.style.left === "0") {
                navRight.style.left = "-100%"; // Slide out
            } else {
                navRight.style.left = "0"; // Slide in
            }
        });
    }

    // Close the navbar when the close button is clicked
    const closebtn = document.querySelector('.closebtn');
    if (closebtn) {
        closebtn.addEventListener('click', function() {
            navRight.style.left = "-100%"; // Slide out
        });
    }

    // Toggles the dropdown menu with click
    const dropBtn = document.getElementById('dropBtn');
    if (dropBtn) { // Check if the element actually exists
        const dropdownContent = document.querySelector('.dropdown-content');
    
        dropBtn.addEventListener('click', function() {
            console.log('clicked');
            if (dropdownContent.style.display === "none" || dropdownContent.style.display === "") {
                dropdownContent.style.display = "block";
            } else {
                dropdownContent.style.display = "none";
            }
            console.log(dropdownContent);
        });
    }
});
