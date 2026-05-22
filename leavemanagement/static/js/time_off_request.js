document.addEventListener("submit", function (event) {
  if (event.target && event.target.id === "time-off-request-form") {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    fetch(form.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": formData.get("csrfmiddlewaretoken"), // Include CSRF token for Django
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Time off request submitted successfully!");
          form.reset(); // Reset the form after successful submission
        } else {
          alert("Error submitting time off request: " + data.error);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred while submitting the time off request.");
      });
  }
});
