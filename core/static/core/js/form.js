document.addEventListener("submit", function (event) {
  const submittedForm = event.target;

  const submitbtn = submittedForm.querySelector('button[type="submit"]');
  if (submitbtn) {
    const spinner = submitbtn.querySelector("#btn-spinner");
    const btnText = submitbtn.querySelector("#btn-text");

    submitbtn.disabled = true;
    submitbtn.classList.add("cursor-not-allowed");

    if (spinner) spinner.classList.remove("hidden");
    if (btnText) btnText.classList.add("hidden");
  }
});
