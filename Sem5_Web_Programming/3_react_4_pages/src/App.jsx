import { useState } from "react";
import LoginCard from "./components/LoginCard.jsx";
import DetailInputCard from "./components/DetailInputCard.jsx";
import ShowDetailCard from "./components/ShowDetailCard.jsx";
import AvgMarksCard from "./components/AvgMarksCard.jsx";

const App = () => {
  let [currentPage, setCurrentPage] = useState(0);
  let [userData, setUserData] = useState(null);

  let nextPage = () => {
    if (currentPage !== pages.length - 1) {
      setCurrentPage(currentPage + 1);
    }
  };
  let prevPage = () => {
    if (currentPage !== 0) {
      setCurrentPage(currentPage - 1);
    }
  };
  let pages = [
    <LoginCard
      nextPage={nextPage}
      prevPage={prevPage}
      userData={userData}
      setUserData={setUserData}
    />,
    <DetailInputCard
      nextPage={nextPage}
      prevPage={prevPage}
      userData={userData}
      setUserData={setUserData}
    />,
    <DetailInputCard
      nextPage={nextPage}
      prevPage={prevPage}
      userData={userData}
      setUserData={setUserData}
    />,
    <ShowDetailCard
      nextPage={nextPage}
      prevPage={prevPage}
      userData={userData}
      setUserData={setUserData}
    />,
    <AvgMarksCard
      nextPage={nextPage}
      prevPage={prevPage}
      userData={userData}
      setUserData={setUserData}
    />,
  ];

  return (
    <div className="min-h-screen w-full">
      <div
        className="flex items-center justify-center text-white h-[100vh]
          bg-[url('/src/assets/bg.png')] bg-cover bg-no-repeat bg-center"
      >
        {pages[currentPage]}
      </div>
    </div>
  );
};

export default App;
