function uploadVideo() {
    var input = document.getElementById("upload");
    var freeder = new FileReader();
    freeder.readAsDataURL(input.files[0]);
    freeder.onload = function() {
        document.getElementById("video").src=freeder.result;
    }
}

function readFile() {
    var event = document.getElementById("upload");

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
        .then(processFileContent)
        .catch(function(err) {
            console.log(err);
        });
    }
}

function processFileContent(data) {
    eel.transcribe(data)(function(ret) {console.log(ret)})
}