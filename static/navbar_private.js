document.addEventListener("DOMContentLoaded", function () {
    const navbar = `
        <div class="navbar">
            <img class="logo-img" src="images/default_logo.png'" />
            <form class="search-form" action="/search" method="GET">
                <input type="text" placeholder="Search..." class="search-input" name="search_query" id="search_query">
                <button type="submit" class="search-button">Search</button>
            </form>
            <span class="hamburger">&#9776;</span>
            <div class="navbar-right" id="navbarRight">
                <span class="closebtn">&times;</span>
                <a href="/dashboard.html">Dashboard</a>
                <a href="/login">Actions</a>
                <div class="dropdown">
                    <a class="dropbtn" id="dropBtn">Account</a>
                    <div class="dropdown-content">
                        <a href="#news1">Profile</a>
                        <a href="#news2">Settings</a>
                        <a id="sign-out-btn" href="#">Logout</a>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.getElementById("navbar").innerHTML = navbar;
});