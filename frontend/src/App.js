import "./App.css";
import { useState } from "react";
import background_image from "./background_image.png";
import lip from "./lip.gif";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [transcription, setTranscription] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setTranscription("");
  };

  const handleTranscribeAudio = async () => {
    if (!selectedFile) {
      alert("Please select an audio file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);
      const response = await fetch("http://localhost:8000/transcribe-audio/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to transcribe audio");
      }

      const result = await response.json();
      setTranscription(result.transcription); // Store the transcription result
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while transcribing the audio.");
    } finally {
      setLoading(false);
    }
  };
  const handleCreateRap = async () => {
    if (!transcription) {
      alert("No transcription available to create rap!");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/generate-audio/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: transcription }),
      });

      if (!response.ok) {
        const errorDetail = await response.json();
        throw new Error(`Error: ${errorDetail.detail}`);
      }

      const blob = await response.blob();
      const audioURL = URL.createObjectURL(blob);
      const audio = new Audio(audioURL);
      await audio.play();
    } catch (error) {
      console.error("Error generating rap audio:", error);
      alert(`Failed to generate audio: ${error.message}`);
    }
  };

  return (
    <div className="App">
      {/* Background Image */}
      <div className="background-container">
        <img src={background_image} alt="Background" />
      </div>

      <h1 className="page-title">Professor GenZ!</h1>

      {/* Lip GIF Section */}
      <div className="lip-container">
        <img src={lip} alt="Lip" />
      </div>

      {/* Main App Content */}
      <div className="app-container">
        <div className="container">
          <h1>Upload Your Borin Lecture!</h1>
          <input type="file" onChange={handleFileChange} accept="audio/*" />
          <button onClick={handleTranscribeAudio} disabled={loading}>
            {loading ? "Professor Genz is Thinking" : "Slangify"}
          </button>
        </div>

        <div className="container">
          <h1>Hold Up Let Me Cook!</h1>
          <button onClick={handleCreateRap}>Make It Yap</button>
        </div>
        {/* Transcription Output */}
        {transcription && (
          <div className="transcription-container">
            <h2>Transcription Output:</h2>
            <p>{transcription}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
