const button = document.querySelector(".documents__button");
const select = document.querySelector(".documents__select");

button.setAttribute("disabled", "disabled");

select.addEventListener("change", () => {
  if (select.value !== "Оберіть посаду") {
    button.removeAttribute("disabled");
  } else {
    button.setAttribute("disabled", "disabled");
  }
});

button.addEventListener("click", e => {
  window.preventAction = true;
  if (select.value == "Оберіть посаду") {
    if (window.preventAction) {
      e.preventDefault();
      alert("Виберіть коректну посаду!");
      return;
    }
  }
  window.preventAction = false;
});
