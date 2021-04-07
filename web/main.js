function editCustom(nam, val) {
    if (val == "CUSTOM412") {
        document.getElementById(nam).innerHTML = `<input type="text" name="${nam}" onchange="editCustom(this.name, this.value)">`;
    } else {
        var uid = document.getElementById("uid").innerText;
        console.log(nam, ' : ', val)

        eel.change_transcript(uid, nam, val)(function(ret) {});
    }
}


function seekVideo(seekTime) {
    var vid = document.getElementById("uploadVideo");
    vid.currentTime = seekTime;
    vid.play();
}


function loadVideo() {
    document.getElementById("video-status").innerHTML = `<p>Loading...</p>`;

    var event = document.getElementById("uploadVideo");
    var file = event.src;
    var fileName = event.getAttribute("name");
    var uid = Date.now(); // Can use UUID npm module for a better unique id
    // Invoke python function
    eel.add_to_local(file, fileName, uid)(function(ret) {
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
    document.getElementById("video-status").innerHTML = `<p>Generating Transcript...</p>`;
    
    eel.transcribe(uid, fileName)(function(ret) {
        var transcriptStatus = `<p>Transcript generated!<br>ID: <span id="uid">${uid}</span></p>`;
        document.getElementById("video-status").innerHTML = transcriptStatus;
        document.getElementById("interactive-transcript").innerHTML = ret;
    })
}


function editTranscript() {
    var uid = document.getElementById("uid").innerText;
    eel.edit_transcript(uid)(function(ret) {
        document.getElementById("interactive-transcript").innerHTML = ret;
    })
}

function exitEditTranscript() {
    var uid = document.getElementById("uid").innerText;
    eel.generate_interactive_transcript(uid)(function(ret) {
        document.getElementById("interactive-transcript").innerHTML = ret;
    })
}
