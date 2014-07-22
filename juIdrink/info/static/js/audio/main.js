/* Copyright 2013 Chris Wilson

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

var audioContext = new AudioContext();
var audioInput = null,
    realAudioInput = null,
    inputPoint = null,
    audioRecorder = null;
var rafID = null;
var analyserContext = null;
var canvasWidth, canvasHeight;
var recIndex = 0;

/* TODO:

- offer mono option
- "Monitor input" switch
*/

function saveAudio() {
    audioRecorder.exportWAV( doneEncoding );
    
    // console.log(sd);
    // could get mono instead by saying
    // audioRecorder.exportMonoWAV( doneEncoding );
}

function drawWave( buffers ) {
    var canvas = document.getElementById( "wavedisplay" );

    drawBuffer( canvas.width, canvas.height, canvas.getContext('2d'), buffers[0] );
}

function doneEncoding( blob ) {
    Recorder.forceDownload( blob, "myRecordFile" + ((recIndex<10)?"0":"") + recIndex + ".wav" );
    recIndex++;

}

function toggleRecording(e,btn,field) {
    if (e.classList.contains("recording")) {
        // stop recording
        audioRecorder.stop();
        $(self_recordbtn).addClass('disabled',false); //disable record btn during uploading file
        e.classList.remove("recording");
        e.classList.remove('btn3d-danger');
        e.classList.add('btn3d-default');
        e.classList.remove('btn-danger');
        e.classList.add('btn-default');
        audioRecorder.getBuffers( drawWave );
        NProgress.start();
        saveAudio();
        if (btn&&field)
            log(btn,field);
        //svae audio & ajax upload function from recorderjs/recorder.js/=>[forceDownload]
    } else {
        // start recording
        if (!audioRecorder)
            return;
        e.classList.add("recording");
        audioRecorder.clear();
        e.classList.remove('btn3d-default');
        e.classList.add('btn3d-danger');
        e.classList.remove('btn-default');
        e.classList.add('btn-danger');
        audioRecorder.record();
        $('button').each(function(index) {
        var s = $(this);
        if (this!=e)
            $(this).attr('disabled',true);
        });
        $('.popwindow').each(function(index) {
            $(this).attr('disabled',true);
        });
    }
}
//suit change btn (using toggleClass)
// function toggleRecording(e) {
//     if (e == 'stop') {
//         // stop recording
//         audioRecorder.stop();
//         audioRecorder.getBuffers( drawWave );
//     } else if (e == 'start'){
//         // start recording
//         if (!audioRecorder)
//             return;
//         audioRecorder.clear();
//         audioRecorder.record();
//     }
// }

function convertToMono( input ) {
    var splitter = audioContext.createChannelSplitter(2);
    var merger = audioContext.createChannelMerger(2);

    input.connect( splitter );
    splitter.connect( merger, 0, 0 );
    splitter.connect( merger, 0, 1 );
    return merger;
}

function cancelAnalyserUpdates() {
    window.cancelAnimationFrame( rafID );
    rafID = null;
}



function toggleMono() {
    if (audioInput != realAudioInput) {
        audioInput.disconnect();
        realAudioInput.disconnect();
        audioInput = realAudioInput;
    } else {
        realAudioInput.disconnect();
        audioInput = convertToMono( realAudioInput );
    }

    audioInput.connect(inputPoint);
}

function gotStream(stream) {
    inputPoint = audioContext.createGain();

    // Create an AudioNode from the stream.
    realAudioInput = audioContext.createMediaStreamSource(stream);
    audioInput = realAudioInput;
    audioInput.connect(inputPoint);

//    audioInput = convertToMono( input );

    analyserNode = audioContext.createAnalyser();
    analyserNode.fftSize = 2048;
    inputPoint.connect( analyserNode );

    audioRecorder = new Recorder( inputPoint );

    zeroGain = audioContext.createGain();
    zeroGain.gain.value = 0.0;
    inputPoint.connect( zeroGain );
    zeroGain.connect( audioContext.destination );
    
}

function initAudio() {
        if (!navigator.getUserMedia)
            navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
        if (!navigator.cancelAnimationFrame)
            navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame || navigator.mozCancelAnimationFrame;
        if (!navigator.requestAnimationFrame)
            navigator.requestAnimationFrame = navigator.webkitRequestAnimationFrame || navigator.mozRequestAnimationFrame;

    navigator.getUserMedia({audio:true}, gotStream, function(e) {
            alert('未取得麥克風錄音權限');
            console.log(e);
        });
}

window.addEventListener('load', initAudio );