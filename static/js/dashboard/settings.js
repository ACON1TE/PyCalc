const button = document.querySelector(".settings__form-button");
const select = document.querySelector(".settings__select");

button.setAttribute("disabled", "disabled");

select.addEventListener("change", () => {
  if (select.value !== "-1") {
    button.removeAttribute("disabled");
  } else {
    button.setAttribute("disabled", "disabled");
  }
});

button.addEventListener("click", e => {
  window.preventAction = true;
  if (select.value == "Оберіть формулу") {
    if (window.preventAction) {
      e.preventDefault();
      alert("Виберіть коректну формулу!");
      return;
    }
  }
  window.preventAction = false;
});
