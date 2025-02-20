// Selecting all required elements
const dropArea = document.querySelector(".drag-area"),
  dragText = dropArea.querySelector("header"),
  browseButton = document.getElementById("browseButton"),
  fileInput = document.getElementById("fileInput"),
  uploadForm = document.getElementById("uploadForm"),
  submitButton = document.getElementById("submitButton"),
  resultArea = document.getElementById("result"),
  extractedText = document.getElementById("extractedText");

let file; // This is a global variable and we'll use it inside multiple functions

browseButton.onclick = () => {
  fileInput.click(); // If user clicks on the button then the input also gets clicked
};

fileInput.addEventListener("change", function () {
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); // Calling function
});

// If user drags file over DropArea
dropArea.addEventListener("dragover", (event) => {
  event.preventDefault(); // Preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

// If user leaves dragged file from DropArea
dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});

// If user drops file on DropArea
dropArea.addEventListener("drop", (event) => {
  event.preventDefault(); // Preventing from default behaviour
  file = event.dataTransfer.files[0];
  showFile(); // Calling function
});

function showFile() {
  let fileName = file.name; // Getting selected file name
  let fileExtension = fileName.split(".").pop().toLowerCase(); // Extracting file extension
  if (fileExtension === "p7m") { // Checking if the file is .p7m
    dragText.textContent = `Selected File: ${fileName}`;
  } else {
    alert("Only .p7m files are allowed!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
    file = null;
  }
}

// Submit the form when the "INVIA" button is clicked
submitButton.addEventListener("click", () => {
  if (!file) {
    alert("Please select a file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("csrfmiddlewaretoken", document.querySelector("[name=csrfmiddlewaretoken]").value);

  fetch(uploadForm.action, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Redirect to result.html with the extracted text
        window.location.href = `/result?extracted_text=${encodeURIComponent(data.extracted_text)}`;
      } else {
        alert(data.error || "An error occurred while processing the file.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while uploading the file.");
    });
});