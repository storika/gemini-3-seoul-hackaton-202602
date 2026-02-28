/**
 * App Controller — orchestrates timeline, KG, video, model strip, and decay chart
 */
const App = (() => {
  let allEvents = [];
  let activeBrand = 'all';
  let lastSnapshotDate = null;
  let debounceTimer = null;

  async function init() {
    KGRenderer.init();
    VideoPanel.init();
    DecayChart.init();
    ModelStrip.init();
    TimelineSlider.init({
      onDateChange: handleDateChange,
      onEventReached: handleEventReached,
    });

    await loadEvents();

    // FOL toggle → re-fetch snapshot with FOL data
    const folBtn = document.getElementById('btn-fol-toggle');
    if (folBtn) {
      folBtn.addEventListener('click', () => {
        // KGRenderer already toggled the state; force re-fetch
        lastSnapshotDate = null;
        const date = TimelineSlider.getCurrentDate();
        fetchSnapshot(date);
      });
    }

    // Brand tab listeners
    document.querySelectorAll('.brand-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.brand-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        activeBrand = tab.dataset.brand;
        const filtered = activeBrand === 'all'
          ? allEvents
          : allEvents.filter(e => e.brand === activeBrand || e.brand === 'multi');
        TimelineSlider.setEvents(filtered);
        lastSnapshotDate = null;  // force refresh
        const date = TimelineSlider.getCurrentDate();
        fetchSnapshot(date);
      });
    });

    // Initial state
    handleDateChange(new Date(1924, 0, 1));
  }

  async function loadEvents() {
    try {
      const res = await fetch('/api/timeline/events');
      allEvents = await res.json();
      TimelineSlider.setEvents(allEvents);
    } catch (err) {
      console.error('Failed to load events:', err);
    }
  }

  function handleDateChange(date) {
    // Update model strip immediately (no debounce needed)
    ModelStrip.updateYear(date.getFullYear());

    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      fetchSnapshot(date);
    }, 80);
  }

  function handleEventReached(event) {
    VideoPanel.showEvent(event);
  }

  async function fetchSnapshot(date) {
    const isoDate = date.toISOString().slice(0, 10);
    if (lastSnapshotDate === isoDate) return;
    lastSnapshotDate = isoDate;

    try {
      const brand = activeBrand === 'all' ? 'all' : activeBrand;
      const fol = KGRenderer.isFOLVisible() ? '&include_fol=true' : '';
      const res = await fetch(`/api/kg/snapshot?date=${isoDate}&brand=${brand}${fol}`);
      const snapshot = await res.json();

      KGRenderer.update(snapshot);
      DecayChart.update(snapshot, date, allEvents);

      if (snapshot.current_event) {
        VideoPanel.showEvent(snapshot.current_event);
      } else {
        VideoPanel.showPlaceholder();
      }
    } catch (err) {
      console.error('Failed to fetch KG snapshot:', err);
    }
  }

  document.addEventListener('DOMContentLoaded', init);

  return { init };
})();
