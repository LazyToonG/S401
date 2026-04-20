document.addEventListener('DOMContentLoaded', () => {
    const themeSauvegarde = localStorage.getItem('theme');
        if (themeSauvegarde === 'sombre') {
        activerModeSombre();
    }
});

const boutonMode = document.getElementById('bouton');
if (boutonMode) {
    boutonMode.addEventListener('click', chgt_mode);
}

function chgt_mode(event) {
    let bouton = event.target;
    
    if (bouton.classList.contains('mode-sombre')) {
        activerModeSombre();
        localStorage.setItem('theme', 'sombre');
    } 
    else {
        activerModeClair();
        localStorage.setItem('theme', 'clair');
    }
}

function activerModeSombre() {
    let bouton = document.getElementById('bouton');
    let body = document.querySelector('body');
    let nav = document.querySelector('.nav');
    let fin_nav = document.getElementById('fin_nav');
    let presentation = document.querySelector('.presentation');
    let equipe = document.querySelector('.equipe');
    let btnLogout = document.getElementById('logout');
    let control_bar = document.querySelector('.controls-bar');
    let planning = document.querySelector('.planning-container');
    let day_column = document.querySelector('.day-column');

    if(body) body.classList.add('sombre');
    if(nav) nav.classList.add('sombre');
    if(fin_nav) fin_nav.classList.add('sombre');
    if(presentation) presentation.classList.add('sombre');
    if(equipe) equipe.classList.add('sombre');
    if(control_bar) control_bar.classList.add('sombre');
    if(planning) planning.classList.add('sombre');
    if(day_column) day_column.classList.add('sombre');
    let cards = document.querySelectorAll('.card'); 
    cards.forEach(card => {
        card.classList.add('sombre');
    });
    let day_columns = document.querySelectorAll('.day-column');
    day_columns.forEach(day_column => {
        day_column.classList.add('sombre');
    });
    let drops = document.querySelectorAll('.drop-zone');
    drops.forEach(drop => {
        drop.classList.add('sombre');
    });
    let modals = document.querySelectorAll('.modal-content'); 
    modals.forEach(modal => {
        modal.classList.add('sombre');
    });
    let ajouts = document.querySelectorAll('.add-music-btn'); 
    ajouts.forEach(ajout => {
        ajout.classList.add('sombre');
    });
    let days = document.querySelectorAll('.day-header'); 
    days.forEach(day => {
        day.classList.add('sombre');
    });

    if (bouton) {
        bouton.classList.remove('mode-sombre');
        bouton.classList.add('mode-clair');
        bouton.value = "☀️";
    }

    if (btnLogout) {
        btnLogout.classList.remove('btn-logout');
        btnLogout.classList.add('btn-logout-sombre');
    }
}

function activerModeClair() {
    let bouton = document.getElementById('bouton');
    let body = document.querySelector('body');
    let nav = document.querySelector('.nav');
    let fin_nav = document.getElementById('fin_nav');
    let presentation = document.querySelector('.presentation');
    let equipe = document.querySelector('.equipe');
    let btnLogout = document.getElementById('logout');
    let control_bar = document.querySelector('.controls-bar');
    let planning = document.querySelector('.planning-container');

    if(body) body.classList.remove('sombre');
    if(nav) nav.classList.remove('sombre');
    if(fin_nav) fin_nav.classList.remove('sombre');
    if(presentation) presentation.classList.remove('sombre');
    if(equipe) equipe.classList.remove('sombre');
    if(control_bar) control_bar.classList.remove('sombre');
    if(planning) planning.classList.remove('sombre');
    let cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.classList.remove('sombre');
    });
    let day_columns = document.querySelectorAll('.day-column');
    day_columns.forEach(day_column => {
        day_column.classList.remove('sombre');
    });
    let drops = document.querySelectorAll('.drop-zone');
    drops.forEach(drop => {
        drop.classList.remove('sombre');
    });
    let modals = document.querySelectorAll('.modal-content'); 
    modals.forEach(modal => {
        modal.classList.remove('sombre');
    });
    let ajouts = document.querySelectorAll('.add-music-btn'); 
    ajouts.forEach(ajout => {
        ajout.classList.remove('sombre');
    });
    let days = document.querySelectorAll('.day-header'); 
    days.forEach(day => {
        day.classList.remove('sombre');
    });

    if (bouton) {
        bouton.classList.remove('mode-clair');
        bouton.classList.add('mode-sombre');
        bouton.value = "🌒";
    }

    if (btnLogout) {
        btnLogout.classList.remove('btn-logout-sombre');
        btnLogout.classList.add('btn-logout');
    }
}

const selectLangue = document.getElementById('select-langue');
if (selectLangue) {
    selectLangue.addEventListener('change', function() {
        const langue = this.value;
        window.location.search = '?lang=' + langue;
    });
}

const btnLogout = document.getElementById('logout');
if(btnLogout) {
    btnLogout.addEventListener('click', function(){
        window.location.href = "/logout";
    });
}

function create(){
    document.querySelector('.create').createElement('form').classList.add('form');
}
let btnCreate = document.getElementById('create');
if (btnCreate) {
    btnCreate.addEventListener('click', create)
}

let role_nav = document.querySelector('.role_nav')
if(role_nav.textContent==='admin'){
    role_nav.addEventListener('mouseover',function(){
        role_nav.style.backgroundColor='red';
    });
    role_nav.addEventListener('mouseout', function() {
        role_nav.style.backgroundColor = ""; 
    });
    role_nav.addEventListener('click',function(){
        window.location.href = "/admin";
    });
};