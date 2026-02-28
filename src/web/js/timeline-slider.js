/**
 * Timeline Slider — custom scrubber + auto-play for 1924–2026
 */
const TimelineSlider = (() => {
  // Date range: 1924-01-01 to 2026-12-31
  const MIN_DATE = new Date(1924, 0, 1);
  const MAX_DATE = new Date(2026, 11, 31);
  const TOTAL_MS = MAX_DATE.getTime() - MIN_DATE.getTime();

  // Auto-play: advance 180 days every 1.5 seconds (covers 100 years in ~5 min)
  const PLAY_INTERVAL_MS = 1500;
  const PLAY_STEP_DAYS = 180;

  let slider = null;
  let playBtn = null;
  let resetBtn = null;
  let markersEl = null;
  let dateDisplay = null;
  let playTimer = null;
  let isPlaying = false;
  let events = [];
  let onChange = null;
  let onEventHit = null;

  function init({ onDateChange, onEventReached }) {
    slider = document.getElementById('timeline-slider');
    playBtn = document.getElementById('btn-play');
    resetBtn = document.getElementById('btn-reset');
    markersEl = document.getElementById('timeline-markers');
    dateDisplay = document.getElementById('current-date-display');
    onChange = onDateChange;
    onEventHit = onEventReached;

    slider.addEventListener('input', handleSliderInput);
    playBtn.addEventListener('click', togglePlay);
    resetBtn.addEventListener('click', resetTimeline);
  }

  function setEvents(evts) {
    events = evts;
    renderMarkers();
  }

  function renderMarkers() {
    markersEl.innerHTML = '';
    events.forEach(evt => {
      const d = new Date(evt.date);
      const pct = ((d.getTime() - MIN_DATE.getTime()) / TOTAL_MS) * 100;
      const marker = document.createElement('div');
      marker.className = `timeline-marker brand-${evt.brand}`;
      marker.style.left = `${pct}%`;
      marker.title = `${evt.title_ko || evt.title} (${evt.date.slice(0, 7)})`;
      markersEl.appendChild(marker);
    });
  }

  function sliderToDate(val) {
    const ratio = val / 1000;
    const ms = MIN_DATE.getTime() + ratio * TOTAL_MS;
    return new Date(ms);
  }

  function dateToSlider(date) {
    const ratio = (date.getTime() - MIN_DATE.getTime()) / TOTAL_MS;
    return Math.round(ratio * 1000);
  }

  function handleSliderInput() {
    const date = sliderToDate(parseInt(slider.value));
    updateDisplay(date);
    if (onChange) onChange(date);
    checkEventHit(date);
  }

  function updateDisplay(date) {
    const y = date.getFullYear();
    const m = date.getMonth() + 1;
    dateDisplay.textContent = `${y}년 ${m}월`;
    updateMarkers(date);
  }

  function updateMarkers(date) {
    const markers = markersEl.querySelectorAll('.timeline-marker');
    markers.forEach((marker, i) => {
      if (i < events.length) {
        const evtDate = new Date(events[i].date);
        marker.classList.toggle('active', evtDate <= date);
      }
    });
  }

  function checkEventHit(date) {
    let closest = null;
    for (const evt of events) {
      const evtDate = new Date(evt.date);
      if (evtDate <= date) {
        closest = evt;
      }
    }
    if (closest && onEventHit) {
      onEventHit(closest);
    }
  }

  function togglePlay() {
    if (isPlaying) {
      stopPlay();
    } else {
      startPlay();
    }
  }

  function startPlay() {
    isPlaying = true;
    playBtn.classList.add('playing');
    playBtn.innerHTML = '&#9646;&#9646; Pause';
    playTimer = setInterval(() => {
      const current = sliderToDate(parseInt(slider.value));
      const next = new Date(current.getTime() + PLAY_STEP_DAYS * 86400000);
      if (next >= MAX_DATE) {
        stopPlay();
        return;
      }
      slider.value = dateToSlider(next);
      updateDisplay(next);
      if (onChange) onChange(next);
      checkEventHit(next);
    }, PLAY_INTERVAL_MS);
  }

  function stopPlay() {
    isPlaying = false;
    playBtn.classList.remove('playing');
    playBtn.innerHTML = '&#9654; Play';
    if (playTimer) {
      clearInterval(playTimer);
      playTimer = null;
    }
  }

  function resetTimeline() {
    stopPlay();
    slider.value = 0;
    const date = MIN_DATE;
    updateDisplay(date);
    if (onChange) onChange(date);
  }

  function getCurrentDate() {
    return sliderToDate(parseInt(slider.value));
  }

  function jumpToYear(year) {
    const date = new Date(year, 0, 15);
    slider.value = dateToSlider(date);
    updateDisplay(date);
    if (onChange) onChange(date);
    checkEventHit(date);
  }

  return { init, setEvents, getCurrentDate, stopPlay, jumpToYear };
})();
