/*License (MIT)

Copyright 穢 2013 Matt Diamond

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.
*/

(function(window){

  var WORKER_PATH = '../../static/js/audio/recorderjs/recorderWorker.js';

  var Recorder = function(source, cfg){
    var config = cfg || {};
    var bufferLen = config.bufferLen || 4096;
    this.context = source.context;
    if(!this.context.createScriptProcessor){
       this.node = this.context.createJavaScriptNode(bufferLen, 2, 2);
    } else {
       this.node = this.context.createScriptProcessor(bufferLen, 2, 2);
    }
   
    var worker = new Worker(config.workerPath || WORKER_PATH);
    worker.postMessage({
      command: 'init',
      config: {
        sampleRate: this.context.sampleRate
      }
    });
    var recording = false,
      currCallback;

    this.node.onaudioprocess = function(e){
      if (!recording) return;
      worker.postMessage({
        command: 'record',
        buffer: [
          e.inputBuffer.getChannelData(0),
          e.inputBuffer.getChannelData(1)
        ]
      });
    }

    this.configure = function(cfg){
      for (var prop in cfg){
        if (cfg.hasOwnProperty(prop)){
          config[prop] = cfg[prop];
        }
      }
    }

    this.record = function(){
      recording = true;
    }

    this.stop = function(){
      recording = false;
    }

    this.clear = function(){
      worker.postMessage({ command: 'clear' });
    }

    this.getBuffers = function(cb) {
      currCallback = cb || config.callback;
      worker.postMessage({ command: 'getBuffers' })
    }

    this.exportWAV = function(cb, type){
      currCallback = cb || config.callback;
      type = type || config.type || 'audio/wav';
      if (!currCallback) throw new Error('Callback not set');
      worker.postMessage({
        command: 'exportWAV',
        type: type
      });

    }

    this.exportMonoWAV = function(cb, type){
      currCallback = cb || config.callback;
      type = type || config.type || 'audio/wav';
      if (!currCallback) throw new Error('Callback not set');
      worker.postMessage({
        command: 'exportMonoWAV',
        type: type
      });
    }

    worker.onmessage = function(e){
      var blob = e.data;
      currCallback(blob);
    }

    source.connect(this.node);
    this.node.connect(this.context.destination);   // if the script node is not connected to an output the "onaudioprocess" event is not triggered in chrome.
  };

  Recorder.forceDownload = function(blob, filename){
    var url = (window.URL || window.webkitURL).createObjectURL(blob);
    //this is file stream , using it to upload
    //-------------------------------------------
    //----
    //----upload
    //----        forceDownload
    //----                      audio
    //----
    //----------------------------------------------------
    var link = window.document.createElement('a');
    link.href = url;
    link.download = filename || 'output.wav';
    link.click = filename || 'output.wav';
    
    var st_audio = $('#student_audio').siblings('input').val();
    st_audio = st_audio.replace('/media/std_answer/','');
    st_audio = st_audio.replace('.wav','');
    ____data____.append('upfile', blob); //____data____ from caller
    ____data____.append('st_audio_path', st_audio); //____data____ from caller
    // alert(blobFile_global_Variable);
    // ____data____.append('upfile', blob); from recorder.js
    $.ajax({
      url: "question/ajax_up_fb" , 
      type: 'POST',
      data: ____data____,
      contentType: false,
      processData: false,
      success: function(fileUrl) {
        $(self_recordbtn).removeClass('disabled'); //recover record_btn at the uploading file end
        if (fileUrl){
            fileUrl = '/media/feedback/'+fileUrl;
            $('#play_btn').siblings('input').val(fileUrl);
            $('#play_btn').removeClass('hidden');
        }
        $('button').each(function(index) {
            $(this).attr('disabled',false);
        });
        NProgress.done();
      },
      error: function(msg) {
        NProgress.done();
        alert(msg);
      
      }
    });
  }
  window.Recorder = Recorder;

})(window);