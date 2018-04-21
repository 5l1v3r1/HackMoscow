let canRequest = true, stream, imageCapture, video, canvas, streaming = false, width, frame, time, frameholder, overlay_form, overlay;

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}


function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);
    // var data = canvas.toDataURL('image/png');
    // photo.setAttribute('src', data);
}

function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
      	canvas.width = width;
      	canvas.height = height;
      	context.drawImage(video, 0, 0, width, height);
    } else {
      	clearphoto();
    }
}

function startStream() {
	video = document.getElementsByTagName('video')[0];
	canvas = document.getElementsByTagName('canvas')[0];
	navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(function(stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function(err) {
        console.log("An error occured! " + err);
    });
    video.addEventListener('canplay', function(ev){
     	if (!streaming) {
        	height = video.videoHeight / (video.videoWidth/width);
        	video.setAttribute('width', width);
        	video.setAttribute('height', height);
        	canvas.setAttribute('width', width);
        	canvas.setAttribute('height', height);
        	if (frame) {		
				frame.style.width = width;
				frame.style.height = height;
        	}
        	streaming = true;
    	}
    }, false);
}

function updateData() {
	if (canRequest) {
	   	takepicture();
		canRequest = false;
        var formdata = new FormData();
        var dataURL = canvas.toDataURL("image/png");
        var blobBin = atob(dataURL.split(',')[1]);
        var array = [];
  		for(var i = 0; i < blobBin.length; i++) {
    		array.push(blobBin.charCodeAt(i));
		}
  		var file=new Blob([new Uint8Array(array)], {type: 'image/png'});
        formdata.append("frame", file);
		$.ajax({
            'headers': { "X-CSRFToken": getCookie("csrftoken") },
		   	'url': 'data',
		    'type': 'POST',
        	'data': formdata,
        	'processData': false,
        	'contentType': false,
		    'success': (data) => {
				    document.getElementById('main').innerHTML = data;
			    canRequest = true;
		    }
		});
	}
}

function error(error) {
    console.error('error:', error.message);
}

function index_start() {
	overlay = document.getElementById("overlay");
	overlay_form = document.getElementById("overlay-form");
	width = 720
	try {
		startStream();
	} catch(e) {
		location.reload();
	}
  	setInterval(updateData, 1000);
}

