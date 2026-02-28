/**
 * Decay Chart — Chart.js temporal weight curves per node
 */
const DecayChart = (() => {
  let chart = null;

  const BRAND_COLORS = {
    jinro: { line: '#1B5E20', fill: 'rgba(27,94,32,0.1)' },
    chamisul: { line: '#2E7D32', fill: 'rgba(46,125,50,0.1)' },
    chum_churum: { line: '#1565C0', fill: 'rgba(21,101,192,0.1)' },
    saero: { line: '#F57C00', fill: 'rgba(245,124,0,0.1)' },
    multi: { line: '#7B1FA2', fill: 'rgba(123,31,162,0.1)' },
  };

  function init() {
    const ctx = document.getElementById('decay-chart').getContext('2d');
    chart = new Chart(ctx, {
      type: 'line',
      data: { labels: [], datasets: [] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 400 },
        plugins: {
          legend: {
            display: true,
            position: 'right',
            labels: {
              color: '#8b8fa3',
              font: { size: 10, family: 'Inter' },
              boxWidth: 12,
              padding: 8,
            },
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: '#1a1d27',
            borderColor: '#2a2d3a',
            borderWidth: 1,
            titleColor: '#e8e8ec',
            bodyColor: '#8b8fa3',
            titleFont: { size: 11 },
            bodyFont: { size: 10 },
          },
        },
        scales: {
          x: {
            grid: { color: 'rgba(42,45,58,0.5)' },
            ticks: { color: '#8b8fa3', font: { size: 9 }, maxTicksLimit: 12 },
          },
          y: {
            min: 0,
            max: 1,
            grid: { color: 'rgba(42,45,58,0.5)' },
            ticks: {
              color: '#8b8fa3',
              font: { size: 9 },
              callback: v => v.toFixed(1),
            },
            title: {
              display: true,
              text: 'Temporal Weight',
              color: '#8b8fa3',
              font: { size: 10 },
            },
          },
        },
        interaction: { mode: 'nearest', axis: 'x', intersect: false },
      },
    });
  }

  function update(snapshot, currentDate, events) {
    if (!chart) return;

    // Track key nodes: brands, products, and persons (influencers)
    const keyNodes = snapshot.nodes.filter(
      n => n.type === 'brand' || n.type === 'product' || n.type === 'person'
    ).slice(0, 10);

    if (keyNodes.length === 0) {
      chart.data.labels = [];
      chart.data.datasets = [];
      chart.update();
      return;
    }

    // Build time axis: yearly for 100-year span
    const minDate = new Date(1924, 0, 1);
    const maxDate = currentDate;
    const labels = [];
    const timePoints = [];
    const d = new Date(minDate);
    while (d <= maxDate) {
      labels.push(`${d.getFullYear()}`);
      timePoints.push(new Date(d));
      d.setFullYear(d.getFullYear() + 2);  // Every 2 years
    }

    const alpha = 0.0003;

    const datasets = keyNodes.map(node => {
      const addedDate = new Date(node.added_date);
      const brand = node.brand || '';
      const colors = BRAND_COLORS[brand] || { line: '#888', fill: 'rgba(136,136,136,0.1)' };
      const isProduct = node.type === 'product';
      const isPerson = node.type === 'person';

      const data = timePoints.map(t => {
        if (t < addedDate) return null;
        const daysDiff = (t - addedDate) / 86400000;
        return Math.exp(-alpha * daysDiff);
      });

      return {
        label: node.label,
        data: data,
        borderColor: colors.line,
        backgroundColor: colors.fill,
        borderWidth: node.type === 'brand' ? 2 : 1,
        borderDash: isPerson ? [6, 3] : (isProduct ? [4, 2] : []),
        pointRadius: 0,
        fill: false,
        tension: 0.3,
      };
    });

    chart.data.labels = labels;
    chart.data.datasets = datasets;
    chart.update();
  }

  function clear() {
    if (!chart) return;
    chart.data.labels = [];
    chart.data.datasets = [];
    chart.update();
  }

  return { init, update, clear };
})();
