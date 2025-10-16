import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

function BandChart({ uniMarks, enteredMarks }) {
  if (!uniMarks) return null;

  const stds = Object.keys(enteredMarks);
  const minMarks = stds.map((std) => uniMarks.marksExpected[std]?.min || 0);
  const maxMarks = stds.map((std) => uniMarks.marksExpected[std]?.max || 0);
  const userMarks = stds.map((std) => enteredMarks[std]);

  const data = {
    labels: stds,
    datasets: [
      {
        label: "Min Expected Marks",
        data: minMarks,
        borderColor: "transparent",
        backgroundColor: "rgba(0,0,0,0)",
      },
      {
        label: "Max Expected Marks",
        data: maxMarks,
        borderColor: "transparent",
        backgroundColor: "rgba(135, 206, 250, 0.5)",
        fill: "-1",
      },
      {
        label: "Your Marks",
        data: userMarks,
        borderColor: "red",
        backgroundColor: "red",
        fill: false,
        tension: 0.3,
        pointRadius: 5,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: { mode: "index" },
    },
    scales: {
      y: {
        beginAtZero: true,
        suggestedMax: 100,
        title: { display: true, text: "Marks" },
      },
      x: {
        title: { display: true, text: "Standards" },
      },
    },
  };

  return <Line data={data} options={options} />;
}

export default BandChart;
