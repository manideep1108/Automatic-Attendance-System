function toggleImageSource() {
    let uploadImageDiv = document.getElementById("upload-image-div");
    let captureImageDiv = document.getElementById("capture-image-div");
    let uploadImageRadio = document.getElementById("upload-image");
    let captureImageRadio = document.getElementById("capture-image");
    let captureButton = document.getElementById("capture-button");
  
    if (uploadImageRadio.checked) {
      uploadImageDiv.style.display = "block";
      captureImageDiv.style.display = "none";
      captureButton.style.display = "none";
    } else {
      uploadImageDiv.style.display = "none";
      captureImageDiv.style.display = "block";
      captureButton.style.display = "block";
      startWebcam();
    }
  }
  
  function startWebcam() {
    let video = document.getElementById("webCam");
  
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
          video.srcObject = stream;
          video.play();
        });
    }
  }
  
  function captureImage() {
    let video = document.getElementById("webCam");
    let canvas = document.getElementById("canvas");
    let imageDataInput = document.getElementById("class-image-data");
  
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    imageDataInput.value = canvas.toDataURL();
  }
  