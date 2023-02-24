const button = document.querySelector(".documents__button");
const selectedItem = document.querySelector(".documents__select-trigger");

button.setAttribute("disabled", "disabled");

selectedItem.addEventListener("click", () => {
  if (selectedItem.innerText !== "Оберіть посаду") {
    button.removeAttribute("disabled");
  }
});
selectedItem.addEventListener("pointerenter", () => {
  if (selectedItem.innerText !== "Оберіть посаду") {
    button.removeAttribute("disabled");
  }
});
