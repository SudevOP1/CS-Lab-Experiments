import express from "express";
import dotenv from "dotenv";
import cors from "cors";

import { getUniData, getAvailableUnis } from "./others/helpers.js";


SERVER_PORT=5000
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(
  cors({
    origin: "http://localhost:5173",
  })
);

app.listen(SERVER_PORT, () => {
  console.log(
    `server listening on http://localhost:${SERVER_PORT}/`
  );
});

app.get("/hello", (req, res) => {
  return res.status(201).json({
    success: true,
    data: "yoo",
  });
});

app.post("/uni-data", (req, res) => {
  const uniName = req.body.uniName;
  if (!uniName) {
    return res.status(400).json({
      success: false,
      error: "bad request (missing fields)",
    });
  }
  const uniData = getUniData(uniName);
  if (uniData) {
    return res.status(201).json({
      success: true,
      data: uniData,
    });
  }
  return res.status(404).json({
    success: false,
    error: `uni ${uniName} not found`,
  });
});

app.get("/available-unis", (req, res) => {
  return res.status(201).json({
    success: true,
    data: getAvailableUnis(),
  });
});
