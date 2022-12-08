let btn = document.getElementById('btn');
let header = document.querySelector('header');

window.addEventListener("scroll",function(){
    let value = window.scrollY;
    btn.style.marginLeft = value * 2 + 'px';
    header.style.top = value * 0.6 + 'px';
    })