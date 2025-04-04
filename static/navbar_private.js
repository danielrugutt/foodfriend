document.addEventListener("DOMContentLoaded", function () {
    const navbar = `
        <div class="navbar">
            <img class="logo-img" src="images/default_logo.png" />
            <span class="hamburger">&#9776;</span> <!-- Hamburger Icon -->
            <div class="navbar-right" id="navbarRight">
                <span class="closebtn">&times;</span>
                <a href="dashboard.html">Dashboard</a>
                <a href="login.html">Actions</a>
                <div class="dropdown">
                    <a class="dropbtn" id="dropBtn">Account</a>
                    <div class="dropdown-content">
                        <a href="#news1">Profile</a>
                        <a href="#news2">Settings</a>
                        <a id="sign-out-btn" href="#">Logout</a>
                    </div>
                </div>
                <!-- Placeholder for user email -->
                <span id="user-email"></span> 
            </div>
        </div>
    `;
    document.getElementById("navbar").innerHTML = navbar;
});