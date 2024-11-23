const tabs = document.querySelectorAll("[data-tab-target]")
const tabContents = document.querySelectorAll("[data-tab-content]")

tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        const target = document.querySelector(tab.dataset.tabTarget)
        tabContents.forEach(tabContent => {
            tabContent.classList.remove("active")
        })
        tabs.forEach(tab => {
            tab.classList.remove("active")
        })
        tab.classList.add("active")
        target.classList.add("active")
    })
})

document.querySelectorAll(".recordButton").forEach(button => {
    button.addEventListener("click", async () => {
        const parentTab = button.closest("[data-tab-content]");
        const tabName = parentTab ? parentTab.getAttribute("data-tab-name") || "Recording" : "Recording";

        // Check if the button is already recording
        if (button.classList.contains("recording")) {
            // Stop the recording
            mediaRecorder.stop();
            button.classList.remove("recording");
            return;
        }

        // Start a new recording
        button.classList.add("recording");

        // Request a new audio stream for each recording
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const audioChunks = [];
        const mediaRecorder = new MediaRecorder(stream);

        // Collect audio data
        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

        // Save the file when recording stops
        mediaRecorder.onstop = () => {
            const blob = new Blob(audioChunks, { type: "audio/wav" });
            const url = URL.createObjectURL(blob);

            // Suggest a folder name in the filename
            const a = document.createElement("a");
            a.style.display = "none";
            a.href = url;
            a.download = `${tabName}.wav`; // Suggest folder structure in the filename
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        };

        // Start recording
        mediaRecorder.start();

        // Stop the stream and cleanup if the tab changes
        button.addEventListener("click", () => {
            if (mediaRecorder.state === "recording") {
                mediaRecorder.stop();
                button.classList.remove("recording");
            }
            stream.getTracks().forEach(track => track.stop()); // Stop the stream
        }, { once: true });
    });
});

async function sendAudioToBackend(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.mp3");
    
    // Send audio to the backend
    await fetch("/upload_audio", {
        method: "POST",
        body: formData
    });
}
