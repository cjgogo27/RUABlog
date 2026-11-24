// Use equivalent section anchors when switching languages.
const languageLink = document.querySelector('#lang');
function keepSection() {
  languageLink.hash = location.hash;
}
keepSection();
window.addEventListener('hashchange', keepSection);
