document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('chart-container');
  
  const pricesData = container.dataset.prices || "[]";
  const timesData = container.dataset.times || "[]";

  const prices = JSON.parse(pricesData);
  const times = JSON.parse(timesData);

  console.log(prices, times); // debug: should be arrays

  if (prices.length === 0 || times.length === 0) {
    console.warn("No data to display");
    return;
  }

  const ctx = document.getElementById('priceChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: { labels: times, datasets: [{ label: 'Elpris (SEK/kWh)', data: prices }] }
  });
});

