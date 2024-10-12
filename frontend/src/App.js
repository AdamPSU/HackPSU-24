import './App.css';

function App() {

  const handleCreateRap = async () => {
    console.log("Create Rap")
    const response = await fetch("http://localhost:8000/")
    console.log(response)
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
