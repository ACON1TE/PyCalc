// This is the JavaScript code for the custom select
const select = document.querySelector("#original-select"); // Get the original select element
const optionsContainer = document.querySelector(".custom-select-options"); // Get the container for the custom select options
const optionsList = optionsContainer.querySelectorAll(".custom-select-option"); // Get the list of custom select options
const selectTrigger = document.querySelector(".custom-select-trigger"); // Get the trigger for the custom select

// Set the text of the custom select trigger to the currently selected option
selectTrigger.textContent = select.options[select.selectedIndex].textContent;

// Add a click event listener to the custom select trigger
selectTrigger.addEventListener("click", () => {
  // Toggle the visibility of the custom select options container
  optionsContainer.classList.toggle("opened");
  selectTrigger.classList.toggle("active");
});

// Add a click event listener to each custom select option
optionsList.forEach(option => {
  option.addEventListener("click", () => {
    // Get the value of the clicked option
    const value = option.dataset.value;
    // Set the value of the original select element to the value of the clicked option
    select.value = value;
    // Set the text of the custom select trigger to the text of the clicked option
    selectTrigger.textContent = option.textContent;
    // Close the custom select options container
    optionsContainer.classList.remove("opened");
    selectTrigger.classList.remove("active");
  });
});

// Add a click event listener to the document
document.addEventListener("click", event => {
  // If the clicked element is not inside the custom select container, close the custom select options container
  if (!event.target.closest(".custom-select-container")) {
    optionsContainer.classList.remove("opened");
    selectTrigger.classList.remove("active");
  }
});
