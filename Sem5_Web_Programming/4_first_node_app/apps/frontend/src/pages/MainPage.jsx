import { useEffect, useState } from "react";
import ContainerWithHeading from "../components/ContainerWithHeading.jsx";
import Loader from "../components/Loader.jsx";
import BandChart from "../components/BandChart.jsx";

function MainPage() {
  const stds = ["hsc", "ssc", "sem1", "sem2", "sem3", "sem4"];
  const backendUrl = "http://localhost:5000";
  const testing = {
    uniMarks: {
      name: "University of Oxford",
      marksExpected: {
        ssc: {
          min: 85,
          max: 95,
        },
        hsc: {
          min: 90,
          max: 98,
        },
        sem1: {
          min: 80,
          max: 95,
        },
        sem2: {
          min: 82,
          max: 97,
        },
        sem3: {
          min: 83,
          max: 96,
        },
        sem4: {
          min: 84,
          max: 98,
        },
        sem5: {
          min: 85,
          max: 99,
        },
        sem6: {
          min: 86,
          max: 100,
        },
        sem7: {
          min: 87,
          max: 100,
        },
        sem8: {
          min: 88,
          max: 100,
        },
      },
    },
    enteredMarks: {
      ssc: 80,
      hsc: 85,
      sem1: 85,
      sem2: 81,
      sem3: 88,
      sem4: 99,
    },
  };

  const [fetchingavailableUnis, setFetchingAvailableUnis] = useState(null);
  const [availableUnis, setAvailableUnis] = useState(null);
  const [selectedUni, setSelectedUni] = useState(null);
  const [uniMarks, setUniMarks] = useState(null);
  const [loading, setLoading] = useState(false);
  const [enteredMarks, setEnteredMarks] = useState(
    Object.fromEntries(stds.map((s) => [s, 0]))
  );

  const handleSetEnteredMarks = (std, marks) => {
    setEnteredMarks((prevMarks) => ({
      ...prevMarks,
      [std]: Number(marks),
    }));
  };

  const fetchAvailableUnis = async () => {
    setFetchingAvailableUnis(true);
    try {
      let resp = await fetch(`${backendUrl}/available-unis`);
      if (resp.ok) {
        let respJson = await resp.json();
        if (respJson.success) {
          // console.log(respJson.data);
          setAvailableUnis(respJson.data);
        } else {
          alert(`something went wrong: ${resp.error}`);
        }
      } else {
        alert("some unknown error occured");
      }
    } catch (e) {
      alert(`something went wrong: ${String(e)}`);
    } finally {
      setFetchingAvailableUnis(false);
    }
  };

  const fetchUniMarks = async () => {
    if (!selectedUni) {
      alert("select a uni first");
      return;
    }
    setLoading(true);
    try {
      let resp = await fetch(`${backendUrl}/uni-data`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ uniName: selectedUni }),
      });
      if (resp.ok) {
        let respJson = await resp.json();
        if (respJson.success) {
          console.log(respJson.data);
          setUniMarks(respJson.data);
        } else {
          alert(`something went wrong: ${resp.error}`);
        }
      } else {
        alert("some unknown error occured");
      }
    } catch (e) {
      alert(`something went wrong: ${String(e)}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitMarks = () => {
    setLoading(true);
    fetchUniMarks();
  };

  useEffect(() => {
    fetchAvailableUnis();
  }, []);

  return (
    <div className="flex flex-col align-center text-black m-20 px-14 py-10 border border-1-black rounded-3xl gap-5">
      {/* loader for fetching availableUnis */}
      {fetchingavailableUnis && <Loader />}

      {/* input container */}
      {!fetchingavailableUnis && availableUnis && (
        <ContainerWithHeading
          heading="Input Marks"
          innerDivClassNames="flex flex-col rounded-3xl"
        >
          <div className="flex flex-col gap-3">
            {/* uni select */}
            <div className="flex flex-row gap-4">
              <span className="flex-none text-lg">
                Select target university:
              </span>
              <select
                id="uniOptions"
                className="w-full border-1 border-neutral-400 rounded-md px-2"
                onChange={(e) => setSelectedUni(e.target.value)}
              >
                {availableUnis.map((uni, idx) => (
                  <option value={uni} key={idx}>
                    {uni}
                  </option>
                ))}
              </select>
            </div>

            {/* marks input */}
            {Object.entries(enteredMarks).map(([std, marks], idx) => (
              <div className="flex flex-row gap-4" key={idx}>
                <span className="flex-none text-lg">Enter marks of {std}:</span>
                <input
                  type="number"
                  name={std}
                  id={std}
                  value={marks}
                  onChange={(e) => handleSetEnteredMarks(std, e.target.value)}
                  className="flex-1 border border-1 border-neutral-400 rounded-md px-2"
                />
              </div>
            ))}
            <button
              className="border border-1 border-black rounded-full py-2 cursor-pointer"
              onClick={handleSubmitMarks}
            >
              Submit
            </button>
          </div>
        </ContainerWithHeading>
      )}

      {/* loader for fetching uniMarks */}
      {loading && <Loader />}

      {/* graph container */}
      {!loading && uniMarks && (
        <ContainerWithHeading
          heading="Graphs"
          innerDivClassNames="flex flex-col rounded-3xl"
        >
          <BandChart uniMarks={uniMarks} enteredMarks={enteredMarks} />
        </ContainerWithHeading>
      )}

      {/* testing */}
      {/* <ContainerWithHeading
        heading="Graph"
        innerDivClassNames="flex flex-col rounded-3xl"
      >
        <BandChart
          uniMarks={testing.uniMarks}
          enteredMarks={testing.enteredMarks}
        />
      </ContainerWithHeading> */}
    </div>
  );
}

export default MainPage;
