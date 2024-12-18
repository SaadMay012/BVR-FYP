import axios from "axios";
import React, { useState } from "react";

export default function AudioUploader() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResult(response.data.result);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div>
      <input type="file" accept="audio/mp3" onChange={handleFileChange} />
      <button onClick={handleSubmit}>Upload MP3</button>
      {result && <div><strong>Classification Result:</strong> {result}</div>}
    </div>
  );
}