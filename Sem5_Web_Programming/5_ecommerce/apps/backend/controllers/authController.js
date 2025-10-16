const bcrypt = require("bcrypt");

const users = [];

const getUsers = (req, res) => {
  return res.json({
    success: true,
    users: users,
  });
};

const registerUser = async (req, res) => {
  try {
    if (!req.body.password || !req.body.username) {
      return res.status(400).send({
        success: false,
        error: "bad request",
        msg: "missing username/password values",
      });
    }
    for (let existingUser of users) {
      if (existingUser.username === req.body.username) {
        return res.status(409).json({
          success: false,
          error: "username already exists",
          msg: "an account with this username already exists",
        });
      }
    }

    const salt = await bcrypt.genSalt();
    const hashedPassword = await bcrypt.hash(req.body.password, salt);
    const newUser = { username: req.body.username, password: hashedPassword };

    users.push(newUser);
    return res.json({
      success: true,
      user: newUser.username,
    });
  } catch (e) {
    return res.status(500).send({
      success: false,
      error: "something went wrong",
      msg: String(e),
    });
  }
};

const loginUser = async (req, res) => {
  try {
    if (!req.body.password || !req.body.username) {
      return res.status(400).send({
        success: false,
        error: "bad request",
        msg: "missing username/password values",
      });
    }
    const user = users.find((user) => user.username === req.body.username);
    if (!user || !(await bcrypt.compare(req.body.password, user.password))) {
      return res.status(401).json({
        success: false,
        error: "invalid credentials",
        msg: "invalid username or password",
      });
    }
    res.json({
      success: true,
    });
  } catch (e) {
    return res.status(500).send({
      success: false,
      error: "something went wrong",
      msg: String(e),
    });
  }
};

module.exports = { getUsers, registerUser, loginUser };
