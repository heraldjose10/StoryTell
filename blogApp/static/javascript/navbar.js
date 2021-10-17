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
    } 
    else{
        header.style.height = '80px';
        navbar.style.display = 'none';
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
}

function active(e){
    var elems = document.querySelectorAll(".active");
    [].forEach.call(elems, function(el) {
        el.classList.remove("active");
    });
    e.target.classList.add("active");
}

