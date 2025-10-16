import { useState } from "react";
import GlassmorphContainer from "./GlassmorphContainer";

const DetailInputCard = ({ nextPage, prevPage, userData, setUserData }) => {
  let [name, setName] = useState("");
  let [dob, setDob] = useState("");

  let handleSubmit = () => {
    if (name && dob) {
      setUserData({
        ...userData,
        name: name,
        dob: dob,
      });
      nextPage();
    }
  };

  return (
    <GlassmorphContainer classNames="flex flex-col justify-around">
      <p className="text-3xl font-bold">Enter Details</p>

      <div className="flex flex-col gap-4">
        <input
          type="text"
          onChange={(e) => setName(e.target.value)}
          placeholder="Name"
          className="border-1 border-white rounded-lg px-3 py-2 outline-none"
        />
        <input
          type="date"
          onChange={(e) => setDob(e.target.value)}
          placeholder="DOB"
          className="border-1 border-white rounded-lg px-3 py-2 outline-none"
        />
      </div>

      <button
        className="w-full py-2 rounded-full bg-white/30 text-white font-bold text-xl
          transition duration-150 border-2 border-transparent hover:border-white
          hover:cursor-pointer active:bg-white/50"
        onClick={() => handleSubmit()}
      >
        Submit
      </button>
    </GlassmorphContainer>
  );
};

export default DetailInputCard;
