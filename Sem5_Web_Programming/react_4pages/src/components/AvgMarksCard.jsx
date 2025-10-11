import { useState } from "react";
import GlassmorphContainer from "./GlassmorphContainer";

const AvgMarksCard = ({ nextPage, prevPage, userData, setUserData }) => {
  let [avgMarks, setAvgMarks] = useState(0);
  let [marks, setMarks] = useState([{ name: "maths", score: 0 }]);

  let handleAddMarks = () => {
    let newMarks = [...marks];
    newMarks.push({ name: "new subject", score: 0 });
    setMarks(newMarks);
    calcAvgMarks();
  };

  let handleChangeMarks = (idx, name, score) => {
    let newMarks = [...marks];
    newMarks[idx] = { name: name, score: score };
    setMarks(newMarks);
    calcAvgMarks();
  };

  let handleRemoveMarks = (idx) => {
    let newMarks = [...marks];
    newMarks.splice(idx, 1);
    setMarks(newMarks);
    calcAvgMarks();
  };

  let calcAvgMarks = () => {
    if (marks.length === 0) {
      return 0;
    }
    let avg = 0;
    for (let mark of marks) {
      avg += mark.score;
    }
    setAvgMarks(avg / marks.length);
  };

  return (
    <GlassmorphContainer classNames="flex flex-col justify-around gap-5">
      <p className="text-3xl font-bold">Avg Marks</p>
      <div className="flex flex-col gap-2 text-xl">
        {marks.map((mark, idx) => (
          <div className="flex flex-row gap-2" key={idx}>
            {/* subject name */}
            <input
              type="text"
              onChange={(e) =>
                handleChangeMarks(idx, e.target.value, mark.score)
              }
              value={mark.name}
              placeholder="subject name"
              className="flex-10 border-1 border-white rounded-lg px-2 py-1 outline-none"
            />

            {/* subject marks */}
            <input
              type="number"
              onChange={(e) =>
                handleChangeMarks(idx, mark.name, e.target.value)
              }
              value={mark.score}
              placeholder="subject name"
              className="flex-1 border-1 border-white rounded-lg px-2 py-1 outline-none"
            />

            {/* remove subject btn */}
            <button
              className="aspect-square h-10 border-1 border-red-400 rounded-full
                text-red-400 outline-none cursor-pointer transition duration-150
                hover:bg-red-400/30 hover:cursor-pointer active:bg-red-400/50"
              onClick={() => handleRemoveMarks(idx)}
            >
              ✕
            </button>
          </div>
        ))}
      </div>

      {/* add subject btn */}
      <button
        onClick={() => handleAddMarks()}
        className="w-full py-2 rounded-full bg-white/30 text-white font-bold
          text-xl transition duration-150 border-2 border-transparent hover:border-white
          hover:cursor-pointer active:bg-white/50"
      >
        Add Subject
      </button>

      <p className="text-xl font-bold">Avg Marks = {avgMarks}</p>
    </GlassmorphContainer>
  );
};
export default AvgMarksCard;
