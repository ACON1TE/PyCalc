// Animation of scrolling
const anchors = document.querySelectorAll('a[href*="#"]');

for (let anchor of anchors) {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();

    const blockID = anchor.getAttribute("href").substr(1);

    document.getElementById(blockID).scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });
}
// Simple Validation of passwords
let formButton = document.querySelector("#formButton");
function validation(form) {
  let inputs = document.querySelectorAll(".login__input");
  let inputsArray = Array.prototype.slice.call(inputs);
  let errors = document.querySelectorAll(".login__error");

  inputs.forEach((element, index) => {
    if (element.value == "") {
      element.classList.add("login__input--error");
      errors[index].classList.remove("login__error--hidden");
      errors[index].innerText = "Заповніть це поле";
    } else if (element.value !== "") {
      element.classList.remove("login__input--error");
      errors[index].classList.add("login__error--hidden");
      errors[index].innerText = "";
    }
  });
  return inputsArray.every(element => element.value !== "");
}

const loginForm = document.querySelector(".login__form");

loginForm.addEventListener("submit", event => {
  window.preventAction = true;
  if (validation(this) == false) {
    if (window.preventAction) {
      event.preventDefault();
    }
  }
  console.log(validation(this));
  window.preventAction = false;
});

const surprise = document.querySelector("#a12397389213");
const photo = document.querySelector(".calc__nothing-important-block-about-project-photo");
let surpriseSum = 0;

function surpriseFunc(surprise, photo) {
  surprise.addEventListener("click", () => {
    surpriseSum++;
    if (surpriseSum >= 5) {
      photo.classList.add("calc__nothing-important-block-about-project-photo--active");
      document.querySelector(".container").classList.add("container--hidden");
    }
  });
}
surpriseFunc(surprise, photo);
