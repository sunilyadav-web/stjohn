let width = screen.width;

if (width <= 992)
{
let navitems=document.querySelectorAll('.nav-item')
let firstNav=document.getElementById('first-nav')
firstNav.classList.remove('border-start')
navitems.forEach(e=>{
    e.classList.remove('border-end')
})
console.log('it working nav')
}