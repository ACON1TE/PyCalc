// Preloader

(function () {
  const select = (el, all = false) => {
    el = el.trim();
    if (all) {
      return [...document.querySelectorAll(el)];
    } else {
      return document.querySelector(el);
    }
  };

  /**
   * Preloader
   */
  let preloader = select("#preloader");
  if (preloader) {
    window.addEventListener("load", () => {
      setTimeout(() => {
        preloader.classList.add("preloader--hidden");
      }, 1500);
    });
  }
})();
// Simple Validation of passwords
let formButton = document.querySelector("#formButton");

let inputs = document.querySelectorAll(".registration__input");
function validation(form) {
  let inputsArray = Array.prototype.slice.call(inputs);
  let errors = document.querySelectorAll(".registration__error");

  inputs.forEach((element, index) => {
    if (element.dataset.required) {
      if (element.value == "") {
        element.classList.add("registration__input--error");
        errors[index].classList.remove("registration__error--hidden");
        errors[index].innerText = "Заповніть це поле";
      } else if (element.value !== "") {
        element.classList.remove("registration__input--error");
        errors[index].classList.add("registration__error--hidden");
        errors[index].innerText = "";
      }
    }
  });

  return inputsArray.every(element => element.value !== "");
}

const registrationForm = document.querySelector(".registration__form");

registrationForm.addEventListener("submit", event => {
  window.preventAction = true;
  if (validation(this) == false) {
    if (window.preventAction) {
      event.preventDefault();
    }
  }
  console.log(validation(this));
  window.preventAction = false;
});
