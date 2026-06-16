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


// ==========================================================================
// GESTION DU MODE SOMBRE PERSISTANT (Bordeaux Nocturne)
// ==========================================================================

// 1. FONCTION DE BASCULEMENT (Appelée par ton bouton flottant lune/soleil)
function toggleQuickDarkMode() {
    const body = document.body;
    const toggleBtn = document.getElementById('quick-dark-toggle');
    
    body.classList.toggle('sombre');
    
    if (body.classList.contains('sombre')) {
        localStorage.setItem('theme', 'dark');
        if (toggleBtn) toggleBtn.innerText = '☀️';
    } else {
        localStorage.setItem('theme', 'light');
        if (toggleBtn) toggleBtn.innerText = '🌙';
    }
}

// 2. SCRIPT DE CHARGEMENT IMMÉDIAT (S'exécute de lui-même instantanément)
(function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    
    // ÉTAPE A : On applique la couleur de fond IMMEDIATEMENT sur le body s'il est 'dark'
    if (savedTheme === 'dark') {
        document.body.classList.add('sombre');
    }

    // ÉTAPE B : On attend que le HTML soit totalement lu pour configurer les icônes et boutons
    document.addEventListener('DOMContentLoaded', () => {
        const toggleBtn = document.getElementById('quick-dark-toggle');
        const checkboxMdp = document.getElementById('dark-mode-toggle');
        
        if (localStorage.getItem('theme') === 'dark') {
            if (toggleBtn) toggleBtn.innerText = '☀️';
            if (checkboxMdp) checkboxMdp.checked = true;
        } else {
            if (toggleBtn) toggleBtn.innerText = '🌙';
            if (checkboxMdp) checkboxMdp.checked = false;
        }
    });
})();