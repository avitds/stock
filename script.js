async function fetchStockData() {
  const symbol = document.getElementById("stockSymbol").value.trim().toUpperCase();
  if (!symbol) {
    alert("Please enter a stock symbol.");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/api/stock?symbol=${symbol}`);
    const data = await response.json();

    if (data.error) {
      alert("Error: " + data.error);
      return;
    }

    document.getElementById("signal").innerText = 
      data.signal === "BUY" ? "📈 BUY Signal" : "📉 SELL Signal";

    const ctx = document.getElementById("stockChart").getContext("2d");
    if (window.stockChart) window.stockChart.destroy();

    window.stockChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: data.dates,
        datasets: [{
          label: `${data.symbol} Price`,
          data: data.prices,
          borderColor: "#0a66c2",
          backgroundColor: "rgba(10,102,194,0.2)",
          fill: true,
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: false }
        }
      }
    });

  } catch (error) {
    alert("Failed to fetch data.");
    console.error(error);
  }
}
