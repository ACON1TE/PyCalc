const submitButton = document.querySelector(".sections__button");
// Weight inputs
let weightInput_a1 = document.querySelector(".sections__input[name='weight1_a']");
let weightInput_a2 = document.querySelector(".sections__input[name='weight2_a']");
let weightInput_a3 = document.querySelector(".sections__input[name='weight3_a']");
let weightSummary_a = 0;

let weightInput_b1 = document.querySelector(".sections__input[name='weight1_b']");
let weightInput_b2 = document.querySelector(".sections__input[name='weight2_b']");
let weightInput_b3 = document.querySelector(".sections__input[name='weight3_b']");
let weightSummary_b = 0;

let weightInput_c1 = document.querySelector(".sections__input[name='weight1_c']");
let weightInput_c2 = document.querySelector(".sections__input[name='weight2_c']");
let weightInput_c3 = document.querySelector(".sections__input[name='weight3_c']");
let weightSummary_c = 0;

submitButton.addEventListener("click", e => {
  window.preventAction = true;
  let weightInputValue_a1 = Number(weightInput_a1.value);
  let weightInputValue_a2 = Number(weightInput_a2.value);
  let weightInputValue_a3 = Number(weightInput_a3.value);
  let weightSummary_a = weightInputValue_a1 + weightInputValue_a2 + weightInputValue_a3;

  let weightInputValue_b1 = Number(weightInput_b1.value);
  let weightInputValue_b2 = Number(weightInput_b2.value);
  let weightInputValue_b3 = Number(weightInput_b3.value);
  let weightSummary_b = weightInputValue_b1 + weightInputValue_b2 + weightInputValue_b3;

  let weightInputValue_c1 = Number(weightInput_c1.value);
  let weightInputValue_c2 = Number(weightInput_c2.value);
  let weightInputValue_c3 = Number(weightInput_c3.value);
  let weightSummary_c = weightInputValue_c1 + weightInputValue_c2 + weightInputValue_c3;

  if (weightSummary_a < 100 || weightSummary_a > 100) {
    if (window.preventAction) {
      e.preventDefault();
      alert("Сума ваги підрозділів А має бути рівною 100");
    }
  } else if (weightSummary_b < 100 || weightSummary_b > 100) {
    if (window.preventAction) {
      e.preventDefault();
      alert("Сума ваги підрозділів Б має бути рівною 100");
    }
  } else if (weightSummary_c < 100 || weightSummary_c > 100) {
    if (window.preventAction) {
      e.preventDefault();
      alert("Сума ваги підрозділів С має бути рівною 100");
    }
  }
  window.preventAction = false;
});
