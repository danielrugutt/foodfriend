document.addEventListener("DOMContentLoaded", function () {
    const navbar = `
        <div class="navbar">
            <img class="logo-img" src="images/default_logo.png" />
            <span class="hamburger">&#9776;</span> <!-- Hamburger Icon -->
            <div class="navbar-right" id="navbarRight">
                <span class="closebtn">&times;</span>
                <a href="index.html">Home</a>
                <!-- Dropdown for News -->
                <div class="dropdown">
                </div>
                <a href="login.html">Login</a>
            </div>
        </div>
    `;
    document.getElementById("navbar").innerHTML = navbar;
});