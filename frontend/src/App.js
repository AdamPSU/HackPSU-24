import "./App.css";
import { useState } from "react";

function App() {
  const [selectedFile, setSelectedFile] = useState(null); // Store the selected file
  const [transcription, setTranscription] = useState(""); // Store the transcription result
  const [loading, setLoading] = useState(false); // Manage loading state

  // Handle file selection for transcription
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setTranscription(""); // Reset transcription when a new file is selected
  };

  // Upload the audio file and get the transcription from the backend
  const handleTranscribeAudio = async () => {
    if (!selectedFile) {
      alert("Please select an audio file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile); // Append file to FormData

    try {
      setLoading(true); // Start loading
      const response = await fetch("http://localhost:8000/transcribe-audio", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to transcribe audio");
      }

      const result = await response.json();
      setTranscription(result.transcription); // Set transcription result
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while transcribing the audio.");
    } finally {
      setLoading(false); // Stop loading
    }
  };

  // Play audio streamed from the backend
  async function playAudioFromStream(stream) {
    const reader = stream.getReader();
    let chunks = [];

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
    }

    const blob = new Blob(chunks, { type: "audio/mpeg" });
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.play();
  }

  // Send a request to generate rap audio from the backend
  const handleCreateRap = async () => {
    console.log("Create Rap");
    await fetch("http://localhost:8000/generate-audio", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: "Hello World" }),
    })
      .then((response) => playAudioFromStream(response.body))
      .catch((error) => console.error("Error:", error));
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Upload Audio File for Transcription</h1>
        <input type="file" onChange={handleFileChange} accept="audio/*" />
        <button onClick={handleTranscribeAudio} disabled={loading}>
          {loading ? "Transcribing..." : "Transcribe Audio"}
        </button>
      </div>

      {transcription && (
        <div className="transcription-result">
          <h2>Transcription:</h2>
          <p>{transcription}</p>
        </div>
      )}

      <div className="container">
        <h1>Create Rap Audio</h1>
        <button onClick={handleCreateRap}>Create Rap</button>
      </div>
    </div>
  );
}

export default App;