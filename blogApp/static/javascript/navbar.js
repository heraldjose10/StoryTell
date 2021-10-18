function navbarButton(){

    let header = document.getElementsByTagName('header')[0];
    let iconLabel = document.getElementsByClassName("hide")[1];
    let navbar = document.getElementsByTagName('nav')[0];
    let icon = iconLabel.firstElementChild;

    if (document.getElementById('nav-checkbox').checked) {
        header.style.height = '100vh';
        navbar.style.display = 'flex';
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
        document.getElementsByTagName('body')[0].classList.add('stop-scrolling');
    } 
    else{
        header.style.height = '80px';
        navbar.style.display = 'none'; // need to fix 
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
        document.getElementsByTagName('body')[0].classList.remove('stop-scrolling');
    }
}

function makeActive(){
    const currentPage = location.href;
    const navBarLinks = document.getElementsByTagName('nav')[0].querySelectorAll('a');
    navBarLinks.forEach(link => {
        if(link.href === currentPage){
            link.classList.add('active')
        }
    });
}

window.onload = makeActive;

window.addEventListener('resize', function () {
    if(window.innerWidth>900){
        document.getElementsByTagName('nav')[0].style.display = 'flex';
    }
  })
