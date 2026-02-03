import axios from "axios";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement } from "chart.js";
import { useState } from "react";

ChartJS.register(CategoryScale, LinearScale, BarElement);


const cardStyle = {
  padding: "12px",
  border: "1px solid #ccc",
  borderRadius: "8px",
  textAlign: "center",
  minWidth: "120px",
  background: "#f9f9f9"
};


function App() {
  const [summary, setSummary] = useState(null);

  const uploadCSV = async (e) => {
    const form = new FormData();
    form.append("file", e.target.files[0]);

    const res = await axios.post("http://127.0.0.1:8000/api/upload/", form);
    setSummary(res.data);
  };

return (
    <div style={{ padding: 20 }}>
      <h2>Chemical Equipment Parameter Visualizer</h2>
      <input type="file" onChange={uploadCSV} />

      {summary && (
  <>
    <div style={{
      display: "flex",
      gap: "15px",
      margin: "20px 0"
    }}>
      <div style={cardStyle}>Total<br />{summary.total_equipment}</div>
      <div style={cardStyle}>Avg Flow<br />{summary.average_flowrate.toFixed(2)}</div>
      <div style={cardStyle}>Avg Pressure<br />{summary.average_pressure.toFixed(2)}</div>
      <div style={cardStyle}>Avg Temp<br />{summary.average_temperature.toFixed(2)}</div>
    </div>

    <Bar
      data={{
        labels: Object.keys(summary.type_distribution),
        datasets: [{
          label: "Equipment Count",
          data: Object.values(summary.type_distribution),
        }]
      }}
    />
    <p style={{ marginTop: 20, fontSize: 12, color: "#666" }}>
  Both Web and Desktop applications use the same Django REST API.
    </p>
  </>
)}
    </div>
  );
}

export default App;
