const video = document.getElementById("video");
const status = document.getElementById("status");

// start webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => video.srcObject = stream)
  .catch(err => status.textContent = "⚠️ Camera access denied");

// every 1.5s, grab a frame and send to server
setInterval(async () => {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth; canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  const imgData = canvas.toDataURL("image/jpeg", 0.7);

  const res = await fetch("/recognize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: imgData })
  });
//const { names } = await res.json();
//status.textContent = names.length
//  ? `✅ Recognized: ${names.join(", ")}`
// : "❓ No recognized faces yet…";
// after you do:
// const { names } = await res.json();
if (!names || names.length === 0) {
  // truly no faces detected
  status.textContent = "❓ No recognized faces yet…";
} else {
  // At least one face was detected, so show whatever names came back—
  // even if it’s just ["Unknown"]
  status.textContent = `✅ Recognized: ${names.join(", ")}`;
}
