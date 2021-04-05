function loadVideo() {
    document.getElementById("video-status").innerHTML = `<p>Loading...</p>`;

    var event = document.getElementById("uploadVideo");
    var file = event.src;
    var fileName = event.getAttribute("name");
    var uid = Date.now(); // Can use UUID npm module for a better unique id
    // Invoke python function
    eel.addToLocal(file, fileName, uid)(function(ret) {
        var videoStatus = `<p>Video added to database!<br>ID: <span id="uid">${ret}</span></p>`;
        document.getElementById("video-status").innerHTML = videoStatus;
        document.getElementById("transcribe").disabled = false;
    })
}


function transcribeVideo() {
    var event = document.getElementById("uploadVideo");
    // var file = event.src;
    var fileName = event.getAttribute("name");
    var uid = document.getElementById("uid").innerText;
    
    eel.transcribe(uid, fileName)(function(ret) {document.getElementById("output").innerHTML = JSON.stringify(ret);})
}


function readPdf() {
    var event = document.getElementById("uploadPdf");

    var file = event.files[0];
    if (file) {
        new Promise(function(resolve, reject) {
            var reader = new FileReader();
            reader.onload = function (evt) {
                resolve(evt.target.result);
            };
            reader.readAsDataURL(file);
            reader.onerror = reject;
        })
        .then(processPdfContent)
        .catch(function(err) {
            console.log(err);
        });
    }
}

function processPdfContent(data) {
    eel.extractText(data)(function(ret) { })
}
