var counter = 1;
setInterval(function(){
    let radioButton = document.getElementById('radio' + counter);
    if (radioButton) {
        radioButton.checked = true;
    }
    counter = (counter % 4) + 1; // Cycles from 1 to 4
}, 5000);
function toggleMenu() {
    const navbar = document.getElementById('navbar');
    navbar.classList.toggle('show');
    const icon = document.getElementById('hamburger-icon').querySelector('i');
    if (icon) {
        icon.classList.toggle('fas fa-bars');
        icon.classList.toggle('fas fa-times');
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger-icon');
    const navbar = document.getElementById('navbar');
    if (hamburger && navbar) {
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleMenu();
        });
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navbar.contains(e.target) && !hamburger.contains(e.target)) {
                navbar.classList.remove('show');
                const icon = hamburger.querySelector('i');
                if (icon) {
                    icon.classList.remove('fas fa-times');
                    icon.classList.add('fas fa-bars');
                }
            }

        });
    }
});  