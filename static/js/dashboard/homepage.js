const accordion = document.querySelectorAll(".homepage__item");
const accordionButtons = document.querySelectorAll(".homepage__switcher");
const accordionHiddenContent = document.querySelectorAll(".homepage__accordion");

for (let i = 0; i < accordion.length; i++) {
  accordion[i].addEventListener("click", () => {
    accordionButtons[i].classList.toggle("homepage__switcher--active");
    accordionHiddenContent[i].classList.toggle("homepage__row--hidden");
  });
}
