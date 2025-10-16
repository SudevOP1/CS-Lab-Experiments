import { useState } from "react";
import GlassmorphContainer from "./GlassmorphContainer";

const LoginCard = ({ nextPage, prevPage, userData, setUserData }) => {

  let [username, setUsername] = useState("");
  let [password, setPassword] = useState("");
  let acceptedUsername = "sudev"
  let acceptedPassword = "sudev"

  let handleSubmit = () => {
    if (username === acceptedUsername && password === acceptedPassword) {
      setUserData({
        ...userData,
        "username": username,
        "password": password,
      })
      nextPage();
    }
  }

  return (
    <GlassmorphContainer classNames="flex flex-col justify-around">
      <p className="text-3xl font-bold">Login</p>

      <div className="flex flex-col gap-4">
        <input
          type="text"
          onChange={(e)=>setUsername(e.target.value)}
          placeholder="Username"
          className="border-1 border-white rounded-lg px-3 py-2 outline-none"
        />
        <input
          type="password"
          onChange={(e)=>setPassword(e.target.value)}
          placeholder="Password"
          className="border-1 border-white rounded-lg px-3 py-2 outline-none"
        />
      </div>

      <button
        className="w-full py-2 rounded-full bg-white/30 text-white font-bold text-xl
          transition duration-150 border-2 border-transparent hover:border-white
          hover:cursor-pointer active:bg-white/50"
        onClick={handleSubmit}
      >
        Submit
      </button>
    </GlassmorphContainer>
  );
};

export default LoginCard;
