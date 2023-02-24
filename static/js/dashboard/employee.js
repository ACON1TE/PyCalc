const accordionButtons = document.querySelectorAll(".employees__switcher");
const accordionHiddenContent = document.querySelectorAll(".employees__accordion");

for (let i = 0; i < accordionButtons.length; i++) {
  accordionButtons[i].addEventListener("click", e => {
    e.preventDefault();
    accordionButtons[i].classList.toggle("employees__switcher--active");
    accordionHiddenContent[i].classList.toggle("employees__row--hidden");
  });
}
