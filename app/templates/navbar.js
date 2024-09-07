const navbar = document.getElementById('navbar');
const links = navbar.getElementsByTagName('a');

for (let i = 0; i < links.length; i++) {
  links[i].addEventListener('click', function() {
    const current = document.getElementsByClassName('active');
    current[0].className = current[0].className.replace(' active', '');
    this.className += ' active';
  });
}
