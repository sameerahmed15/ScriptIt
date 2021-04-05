// Selecting all required elements
const dropArea = document.querySelector(".drag-area"),
    dragText = dropArea.querySelector("header"),
    button = dropArea.querySelector("button"),
    input = dropArea.querySelector("input");
let file; // This is a global variable and we'll use it inside multiple functions

button.onclick = () => {
    input.click(); // If user click on the button then the input also clicked
}

input.addEventListener("change", function() {
    // Getting user select file and [0] this means if user select multiple files then we'll select only the first one
    file = this.files[0];
    dropArea.classList.add("active");
    showFile();
});


// If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event) => {
    event.preventDefault(); // Preventing from default behaviour
    dropArea.classList.add("active");
    dragText.textContent = "Release to Upload File";
});

// If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
});

// If user drop File on DropArea
dropArea.addEventListener("drop", (event) => {
    event.preventDefault(); // Preventing from default behaviour
    // Getting user select file and [0] this means if user select multiple files then we'll select only the first one
    file = event.dataTransfer.files[0];
    showFile(); // Calling function
});

function showFile() {
    let fileType = file.type; // Getting selected file type
    let validExtensions = ["video/mp4"]; // Adding some valid image extensions in array
    let fileName = file.name;

    if (validExtensions.includes(fileType)) { // If user selected file is an image file
        let fileReader = new FileReader(); // Creating new FileReader object
        fileReader.onload = () => {
            let fileURL = fileReader.result; // Passing user file source in fileURL variable
            let imgTag = `<video name="${fileName}" src="${fileURL}" id="uploadVideo" width="320" height="240" controls></video>`; // Creating an img tag and passing user selected file source inside src attribute
            dropArea.innerHTML = imgTag; // Adding that created img tag inside dropArea container
            document.getElementById("confirm-video").disabled = false; // Enable button after video element created
        }
        fileReader.readAsDataURL(file);
    } else {
        alert("This is not a valid video file!");
        dropArea.classList.remove("active");
        dragText.textContent = "Drag & Drop to Upload File";
    }
}