import './App.css';

function App() {
  async function playAudioFromStream(stream) {
    const reader = stream.getReader();
  
    let chunks = [];
  
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
  
      chunks.push(value);
    }
  
    const blob = new Blob(chunks, { type: 'audio/mpeg' }); // Adjust type if needed
    const url = URL.createObjectURL(blob);
  
    const audio = new Audio(url);
    audio.play();
  }
  
  const handleCreateRap = async () => {
    console.log("Create Rap")
    await fetch("http://localhost:8000/generate-audio", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({text: "Hello World"})
    }
    )
    .then(response => {
      playAudioFromStream(response.body)
    })
  }

  return (
    <div className="App">
      <div className="container">
        <h1>Input File Upload</h1>
        <input type="file"/>
      </div>
      <button onClick={handleCreateRap}>Create Rap</button>
    </div>
  );
}

export default App;
