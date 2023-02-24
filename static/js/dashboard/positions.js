function createPosition() {
  let form = document.querySelector("#positions_form");
  // let positionsBlock = document.querySelector(".positions__created");
  // let position = document.querySelector(".positions__block-item");
  let input = document.querySelector(".positions__block-input");
  // let value = "";

  function validation(form) {
    let allPositions = document.querySelectorAll(".positions__block-item");
    let arrayAllPositions = Array.prototype.slice.call(allPositions);
    for (let i = 0; i < arrayAllPositions.length; i++) {
      if (input.value === arrayAllPositions[i].innerText) {
        return false;
      }
    }
    if (input.value.trim().length === 0 || input.value.trim() === "Посад немає") {
      return false;
    }
    return true;
  }

  form.addEventListener("submit", event => {
    window.preventAction = true;
    if (validation(this) == false) {
      if (window.preventAction) {
        event.preventDefault();
        // Проверка по всем элементам-должностям на уникальность имени
        let allPositions = document.querySelectorAll(".positions__block-item");
        let arrayAllPositions = Array.prototype.slice.call(allPositions);
        for (let i = 0; i < arrayAllPositions.length; i++) {
          if (input.value === arrayAllPositions[i].innerText) {
            alert("Введіть унікальну назву посади!");
            input.value = "";
            return;
          }
        }
        if (input.value.trim().length === 0 || input.value.trim() === "Посад немає") {
          alert("Введіть коректну назву посади!");
        }
      }
    }
    window.preventAction = false;
    // else {
    //   if (position.innerText === "Посад немає") {
    //     position.remove();
    //   }
    //   value = input.value;
    //   let newPosition = document.createElement("span");
    //   newPosition.classList.add("positions__block-item");
    //   newPosition.innerText = value;
    //   positionsBlock.appendChild(newPosition);
    //   input.value = "";
    // }
  });
}

createPosition();
