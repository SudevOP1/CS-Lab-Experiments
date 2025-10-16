const cors = require("cors");
const express = require("express");
const authRoutes = require("./routes/auth");

SERVER_PORT = 3000;
const app = express();

app.use(express.json());
app.use(cors({ origin: "http://localhost:5173" }));
app.use(express.urlencoded({ extended: true }));

app.use("/auth", authRoutes);
app.listen(SERVER_PORT, () => {
  console.log(`server listening on http://localhost:${SERVER_PORT}/`);
});

app.get("/hello", (req, res) => {
  return res.json({
    success: true,
    msg: "yoo",
  });
});
