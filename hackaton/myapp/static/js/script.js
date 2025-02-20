// Selecting all required elements
const dropArea = document.querySelector(".drag-area"),
dragText = dropArea.querySelector("header"),
button = dropArea.querySelector("button"),
input = dropArea.querySelector("input");
let file; // This is a global variable and we'll use it inside multiple functions

button.onclick = () => {
  input.click(); // If user clicks on the button then the input also gets clicked
};

input.addEventListener("change", function () {
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
