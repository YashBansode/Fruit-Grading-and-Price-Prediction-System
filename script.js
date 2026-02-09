document.addEventListener("DOMContentLoaded", () => {
  const uploadButton = document.getElementById("uploadButton");
  const gifBlock = document.querySelector(".gif");
  const centerContainer = document.getElementById("centerContainer");
  emailjs.init("2R7c91SoW7MGbRIEj");

  uploadButton.addEventListener("click", () => {
    if (gifBlock) {
      gifBlock.style.display = "none";
    }

    if (centerContainer) {
      centerContainer.style.display = "flex";
      centerContainer.style.justifyContent = "center";
      centerContainer.style.alignItems = "center";
      centerContainer.style.height = "auto";
    }

    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "image/*";
    fileInput.style.display = "none";

    document.body.appendChild(fileInput);
    fileInput.click();

    fileInput.addEventListener("change", () => {
      const file = fileInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const previewContainer = document.getElementById("previewContainer");
          const previewImage = document.getElementById("imagePreview");
          const imageInfo = document.getElementById("imageInfo");

          imageInfo.style.display = "block";
          previewContainer.style.display = "flex";
          previewImage.innerHTML = "";

          const image = document.createElement("img");
          image.src = e.target.result;
          image.style.maxWidth = "300px";
          image.style.height = "auto";
          image.className = "img-thumbnail";
          previewImage.appendChild(image);
        };
        reader.readAsDataURL(file);

        // Upload the file
        uploadImage(file);
      }
      document.body.removeChild(fileInput);
    });
  });

  function uploadImage(file) {
    const formData = new FormData();
    formData.append("file", file);

    fetch("http://138.199.209.238:5000/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Response:", data);

        if (data.quality && data.rate) {
          document.getElementById(
            "fileName"
          ).textContent = `Quality: ${data.quality}`;
          document.getElementById(
            "fileSize"
          ).textContent = `Rate: ${data.rate}`;
        } else {
          alert("Unexpected response format!");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Not A fruit Image!");
      });
  }

  // Capture Feedback Form Submission
  const feedbackForm = document.querySelector(".feedback form");
  if (feedbackForm) {
    feedbackForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const feedbackInput =
        feedbackForm.querySelector("input[type='text']").value;

      const templateParams = {
        name: "User",
        email: "No email provided",
        message: feedbackInput,
      };

      emailjs
        .send("service_0vfo8vp", "template_vnq188c", templateParams)
        .then((response) => {
          console.log("Feedback sent successfully:", response);
          alert("Thank you for your feedback!");
          feedbackForm.reset();
        })
        .catch((error) => {
          console.error("Error sending feedback:", error);
          alert("Failed to send feedback.");
        });
    });
  }

  // Capture Contact Form Submission
  const contactForm = document.querySelector(".contact form");
  if (contactForm) {
    contactForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const email = contactForm.querySelector(
        "input[placeholder='Enter Email']"
      ).value;
      const phone = contactForm.querySelector(
        "input[placeholder='Enter Phone']"
      ).value;
      const website = contactForm.querySelector(
        "input[placeholder='Enter Website Link']"
      ).value;

      const templateParams = {
        name: "User",
        email: email,
        message: `Phone: ${phone}\nWebsite: ${website}\nEmail: ${email}`,
      };

      emailjs
        .send("service_0vfo8vp", "template_vnq188c", templateParams)
        .then((response) => {
          console.log("Contact form sent successfully:", response);
          alert("Your message has been sent!");
          contactForm.reset();
        })
        .catch((error) => {
          console.error("Error sending contact form:", error);
          alert("Failed to send message.");
        });
    });
  }
});
