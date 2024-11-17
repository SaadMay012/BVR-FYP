const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { spawn } = require("child_process");
const fs = require("fs");

const pythonExecutable = "/home/anonymousje/Downloads/backend/backend/venv/bin/python" 

const app = express();
const upload = multer({ dest: "uploads/" }); // Uploaded files will be saved in 'uploads'

app.use(cors());

// Endpoint for file upload
app.post("/upload", upload.single("file"), (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded.");
  }

  const filePath = req.file.path; 
  
  // Call Python script
  const pythonProcess = spawn(pythonExecutable, ["Bird Classification Model.py", filePath]);
  let result = "";
  pythonProcess.stdout.on("data", (data) => {
    result = data.toString();
    
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error("Error from Python script:", data.toString());
  });

  pythonProcess.on("close", (code) => {
    fs.unlinkSync(filePath);
    //console.log(result)

    if (code === 0) {
      res.json({ result: result.trim() });
    } else {
      res.status(500).send("Error processing file.");
    }
  });
});

const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
