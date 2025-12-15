/*!
* Start Bootstrap - New Age v6.0.7 (https://startbootstrap.com/theme/new-age)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-new-age/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});






document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("download-app-container");
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;

    let buttonHTML = "";

    if (/android/i.test(userAgent)) {
        // Android device
        buttonHTML = `
            <a href="https://play.google.com/store/apps/details?id=your.app.id" 
               class="btn btn-success btn-lg d-flex align-items-center gap-2 justify-content-center">
                <i class="fab fa-android fa-2x"></i>
                <span>Download for Android</span>
            </a>`;
    } else if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
        // iOS device
        buttonHTML = `
            <a href="https://apps.apple.com/app/idYOUR_APP_ID" 
               class="btn btn-dark btn-lg d-flex align-items-center gap-2 justify-content-center">
                <i class="fab fa-apple fa-2x"></i>
                <span>Download for iOS</span>
            </a>`;
    } else if (/Win/i.test(userAgent)) {
        // Windows PC
        buttonHTML = `
            <a href="/downloads/your-desktop-app.exe" 
               class="btn btn-primary btn-lg d-flex align-items-center gap-2 justify-content-center">
                <i class="fas fa-desktop fa-1x"></i>
                <span>Download for Windows</span>
            </a>`;
    } else if (/Mac/i.test(userAgent)) {
        // macOS
        buttonHTML = `
            <a href="/downloads/your-desktop-app.dmg" 
               class="btn btn-primary btn-lg d-flex align-items-center gap-2 justify-content-center">
                <i class="fas fa-desktop fa-2x"></i>
                <span>Download for Mac</span>
            </a>`;
    } else {
        // Unknown device / fallback
        buttonHTML = `
            <a href="#get-started" 
               class="btn btn-secondary btn-lg d-flex align-items-center gap-2 justify-content-center">
                <i class="fas fa-download fa-2x"></i>
                <span>Download App</span>
            </a>`;
    }

    container.innerHTML = buttonHTML;
});