function checkCookie() {
    console.log("COOKIE CHECK!")
    if (localStorage.getItem("lectureVideoShow") != null) {
        // Remove the two buttons
        var confirmUploadBtn = document.getElementById("confirm-video");
        confirmUploadBtn.remove();

        var videoObj = localStorage["lectureVideoShow"];
        var transcriptExists = localStorage["transcriptExists"];
        var transcriptObj = localStorage["transcriptShow"];
        var uid = localStorage["uid"];
        transcriptExists = (transcriptExists == 'true');

        document.getElementById("load-existing").innerHTML = videoObj;
        document.getElementById("video-status").innerHTML = `ID: <span id="uid">${uid}</span></p>`;

        if (transcriptExists === true) {
            document.getElementById("interactive-transcript").innerHTML = transcriptObj;
            var transcribeBtn = document.getElementById("transcribe-btn");
            transcribeBtn.remove();
        } 
        else {
            document.getElementById("transcribe-btn").disabled = false;
        }

        localStorage.removeItem("lectureVideoShow");
        localStorage.removeItem("transcriptExists");
        localStorage.removeItem("transcriptShow");
    }
}


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
        document.getElementById("confirm-video").disabled = true;
        document.getElementById("transcribe-btn").disabled = false;
    })
}


function transcribeVideo() {
    var event = document.getElementById("uploadVideo");
    console.log(event);
    // var file = event.src;
    var fileName = event.getAttribute("name");
    var uid = document.getElementById("uid").innerText;
    document.getElementById("video-status").innerHTML = `<p>Generating Transcript...</p>`;

    eel.transcribe(uid, fileName)(function(ret) {
        var transcriptStatus = `<p>Transcript generated!<br>ID: <span id="uid">${uid}</span></p>`;
        document.getElementById("video-status").innerHTML = transcriptStatus;
        document.getElementById("interactive-transcript").innerHTML = ret;
        document.getElementById("transcribe-btn").disabled = true;
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


function listVideos() {
    eel.load_videos_dir()(function(ret) {
        document.getElementById("view-dir").innerHTML = ret;
    })
}


function showVideo(uid, time=-10) {
    eel.show_video(uid, time)(function(ret) {
        console.log(ret)
        localStorage["lectureVideoShow"] = ret[0];
        localStorage["transcriptExists"] = ret[1];
        localStorage["transcriptShow"] = ret[2];
        localStorage["uid"] = ret[3];
        window.location.href = "../index.html";
    })
}


function searchWord(word) {
    console.log(word);
    eel.search_word(word)(function(ret) {
        document.getElementById("search-results-div").innerHTML = ret;
    })
}
