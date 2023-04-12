function toggleImageSource() {
    let uploadImageDiv = document.getElementById("upload-image-div");
    let captureImageDiv = document.getElementById("capture-image-div");
    let uploadImageRadio = document.getElementById("upload-image");
    let captureImageRadio = document.getElementById("capture-image");
    let captureButton = document.getElementById("capture-button");
    let imagePreview = document.getElementById("show-image-div");

    if (uploadImageRadio.checked) {
        uploadImageDiv.style.display = "block";
        captureImageDiv.style.display = "none";
        captureButton.style.display = "none";
        imagePreview.style.display = "none";
    } else {
        uploadImageDiv.style.display = "none";
        captureImageDiv.style.display = "block";
        captureButton.style.display = "block";
        captureButton.removeEventListener('click', captureImage); // remove the event listener
        startWebcam();
    }
}
//   const errorMsgElement = document.getElementById('spanerrorMsg');
  const contraints = {
    audio: true,
    video: {
        width: 1280,
        height: 720
    }
  };
  
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

  let formData = new FormData();
  let captured = false;
  function captureImage() {
    console.log("Capture button clicked");
    let video = document.getElementById("webCam");
    let canvas = document.getElementById("canvas");
    let imageDataInput = document.getElementById("class-image-data");
    let imagePreview = document.getElementById("show-image-div");
    let uploadImageDiv = document.getElementById("upload-image-div");
    let captureImageDiv = document.getElementById("capture-image-div");
    
  
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(function (blob) {
      let file = new File([blob], "class-image.jpg", { type: "image/jpg" });
      imageDataInput.value = "";
      captured = true;

      // create an image element and set the captured image as its source
      let img = document.createElement("img");
      img.src = URL.createObjectURL(blob);
      img.onload = function() {
        URL.revokeObjectURL(this.src);
      let classNameInput = document.getElementsByName("class_name")[0].value;
      formData.append("class_name", classNameInput);
      formData.append("class_image", file);
      };
      captureImageDiv.style.display = "none";
      uploadImageDiv.style.display = "none";
      imagePreview.style.display = "block";
      // append the image to the preview container
      imagePreview.innerHTML = "";
      imagePreview.appendChild(img);
    }, "image/jpg", 0.9);
}

document.getElementById("attendance-form").addEventListener("submit", function(event) {
    event.preventDefault();
    if (document.getElementById("upload-image").checked) {
        this.submit();
    } else {
        if (captured) {
            let xhr = new XMLHttpRequest();
            xhr.open("POST", "/submit-form");
            xhr.setRequestHeader("Content-Type", "multipart/form-data");
            xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            xhr.open("POST", "/attendance");
            xhr.send(formData);
        } else {
            alert("Please capture an image first.");
        }
    }
  });
