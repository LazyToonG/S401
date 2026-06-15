document.addEventListener('DOMContentLoaded', () => {
    const profileBtn = document.getElementById('userProfileBtn');
    const profileMenu = document.getElementById('profileMenu');

    if (profileBtn && profileMenu) {
        // Ouvre/Ferme le menu lors du clic sur le bloc profil
        profileBtn.addEventListener('click', (event) => {
            profileMenu.classList.toggle('show');
            event.stopPropagation(); 
        });

        // Ferme le menu si on clique en dehors
        document.addEventListener('click', (event) => {
            if (!profileBtn.contains(event.target)) {
                profileMenu.classList.remove('show');
            }
        });
    }
});