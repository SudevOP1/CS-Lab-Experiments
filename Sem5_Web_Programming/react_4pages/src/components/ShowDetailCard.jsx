import { useState } from "react";
import GlassmorphContainer from "./GlassmorphContainer";

const ShowDetailCard = ({ nextPage, prevPage, userData, setUserData }) => {
  let getAge = (dob) => {
    let today = new Date();
    let bDate = new Date(dob);
    let age = today.getFullYear() - bDate.getFullYear();
    let monthDiff = today.getMonth() - bDate.getMonth();

    if (
      monthDiff < 0 ||
      (monthDiff === 0 && today.getDate() < bDate.getDate())
    ) {
      age--;
    }
    return age;
  };

  let handleSubmit = () => {
    nextPage();
  };

  return (
    <GlassmorphContainer classNames="flex flex-col justify-around">
      <p className="text-3xl font-bold">Details</p>

      <div className="flex flex-col gap-3">
        <p className="text-xl">Your DOB is {userData.dob}</p>
        <p className="text-xl">Your age is {getAge(userData.dob)}</p>
        <p className="text-xl">
          {" "}
          You are {getAge(userData.dob) < 18 && "not"} eligible to apply for
          driver's license
        </p>
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
export default ShowDetailCard;
