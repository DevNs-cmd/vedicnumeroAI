
document.getElementById("faceForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData();
  const imageFile = document.getElementById("image").files[0];
  formData.append("image", imageFile);

  const res = await fetch("/analyze-face", {
    method: "POST",
    body: formData
  });

  const data = await res.json();

  document.getElementById("result").innerHTML = `
    <h3>🧠 Expression: ${data.expression}</h3>
    <p>🔢 Numerology Trait: ${data.trait}</p>
    <p>🌟 Prediction: ${data.prediction}</p>
  `;
});



