let button = document.querySelector(".reports__button");
let inputs = document.querySelectorAll(".reports__input");
let inputsArray = Array.prototype.slice.call(inputs);

button.addEventListener("click", e => {
  for (let i = 0; i < inputsArray.length; i++) {
    if (inputsArray[i].value.trim().length === 0) {
      e.preventDefault();
      alert("Заповніть поля даними!");
      break;
    }
  }
});
