const express = require("express");
const router = express.Router();
const {
  getUsers,
  registerUser,
  loginUser,
} = require("../controllers/authController");

router.post("/users", getUsers);
router.post("/register", registerUser);
router.post("/login", loginUser);

module.exports = router;
