function uploadVideo() {
    var input = document.getElementById("uploadVideo");
    var freeder = new FileReader();
    freeder.readAsDataURL(input.files[0]);
    freeder.onload = function() {
        document.getElementById("video").src=freeder.result;
    }
}

function readFile() {
    var event = document.getElementById("uploadVideo");

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
        .then(processVideoContent)
        .catch(function(err) {
            console.log(err);
        });
    }
}

function processVideoContent(data) {
    eel.transcribe(data)(function(ret) {console.log(ret)})
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