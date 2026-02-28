/**
 * Video Panel — event detail display + images + market share + news + inline Veo 3.1 video
 */
const VideoPanel = (() => {
  let currentEvent = null;

  // Brand color mapping for market share bars
  const BRAND_COLORS = {
    '진로': '#1B5E20',
    '진로(참이슬)': '#2E7D32',
    '참이슬': '#2E7D32',
    '처음처럼': '#1565C0',
    '새로': '#F57C00',
    '진로이즈백': '#388E3C',
    '경월소주': '#5D4037',
    '무학': '#616161',
  };

  function init() {
    document.getElementById('btn-generate-video').addEventListener('click', generateVideo);
  }

  function showEvent(event) {
    if (!event) {
      showPlaceholder();
      return;
    }
    if (currentEvent && currentEvent.id === event.id) return;
    currentEvent = event;

    document.getElementById('detail-placeholder').classList.add('hidden');
    const el = document.getElementById('detail-event');
    el.classList.remove('hidden');

    // Category badge
    const badge = document.getElementById('detail-category');
    badge.textContent = event.category.replace(/_/g, ' ');
    badge.className = `category-badge ${event.category}`;

    // Title
    document.getElementById('detail-title').textContent = event.title;
    document.getElementById('detail-title-ko').textContent = event.title_ko;

    // Date
    const d = new Date(event.date);
    document.getElementById('detail-date').textContent =
      `${d.getFullYear()}. ${d.getMonth() + 1}. ${d.getDate()}.`;

    // Hero image — hide first, then load
    const heroContainer = document.getElementById('hero-image-container');
    if (heroContainer) heroContainer.classList.add('hidden');
    loadImage('hero-image-container', 'hero-image', `/images/${event.id}/hero.png`);

    // Market share + sales
    renderMarketShare(event.market_share, event.market_sales);

    // News headlines + news image
    const newsSection = document.getElementById('news-section');
    const newsList = document.getElementById('news-list');
    const newsImgContainer = document.getElementById('news-image-container');
    if (newsImgContainer) newsImgContainer.classList.add('hidden');

    if (event.news_headlines && event.news_headlines.length > 0) {
      newsSection.classList.remove('hidden');
      loadImage('news-image-container', 'news-image', `/images/${event.id}/news.png`);
      newsList.innerHTML = '';
      event.news_headlines.forEach(headline => {
        const li = document.createElement('li');
        li.textContent = headline;
        newsList.appendChild(li);
      });
    } else {
      newsSection.classList.add('hidden');
    }

    // KG mutations
    document.getElementById('detail-mutations').textContent =
      `+${event.kg_mutation_count} mutations`;

    // Description
    document.getElementById('detail-description').textContent = event.description;

    // Video
    resetVideo();
    checkVideoCache(event.id);
  }

  function loadImage(containerId, imgId, src) {
    const container = document.getElementById(containerId);
    const img = document.getElementById(imgId);
    if (!container || !img) return;

    // Create a new Image to avoid lazy-loading issues
    const testImg = new Image();
    testImg.onload = () => {
      img.src = src;
      container.classList.remove('hidden');
    };
    testImg.onerror = () => {
      container.classList.add('hidden');
    };
    testImg.src = src;
  }

  function renderMarketShare(shareData, salesData) {
    const section = document.getElementById('market-share-section');
    const container = document.getElementById('market-share-bars');
    if (!section || !container) return;

    if (!shareData || Object.keys(shareData).length === 0) {
      section.classList.add('hidden');
      return;
    }

    section.classList.remove('hidden');
    container.innerHTML = '';

    // Sort by share descending
    const sorted = Object.entries(shareData).sort((a, b) => b[1] - a[1]);

    sorted.forEach(([brand, share], idx) => {
      const row = document.createElement('div');
      row.className = 'share-bar-row';

      // Rank badge
      const rank = document.createElement('span');
      rank.className = `share-rank${idx === 0 ? ' rank-1' : ''}`;
      rank.textContent = `${idx + 1}`;

      // Brand name
      const label = document.createElement('span');
      label.className = 'share-brand-label';
      label.textContent = brand;

      // Bar track
      const track = document.createElement('div');
      track.className = 'share-bar-track';

      // Bar fill
      const fill = document.createElement('div');
      const colorClass = getBrandColorClass(brand);
      fill.className = `share-bar-fill ${colorClass}`;
      fill.style.width = '0%';
      fill.style.backgroundColor = BRAND_COLORS[brand] || '#666';

      // Share % + sales text
      const pct = document.createElement('span');
      const salesText = (salesData && salesData[brand]) ? ` (${salesData[brand]})` : '';
      pct.textContent = `${share}%${salesText}`;
      fill.appendChild(pct);
      track.appendChild(fill);

      row.appendChild(rank);
      row.appendChild(label);
      row.appendChild(track);
      container.appendChild(row);

      // Animate bar width
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          fill.style.width = `${Math.min(share * 1.5, 100)}%`;
        });
      });
    });
  }

  function getBrandColorClass(brand) {
    if (brand.includes('참이슬') || brand.includes('진로(참이슬)')) return 'chamisul';
    if (brand === '처음처럼') return 'chum_churum';
    if (brand === '새로') return 'saero';
    if (brand.includes('진로')) return 'jinro';
    return '';
  }

  function showPlaceholder() {
    currentEvent = null;
    document.getElementById('detail-placeholder').classList.remove('hidden');
    document.getElementById('detail-event').classList.add('hidden');
  }

  function resetVideo() {
    const video = document.getElementById('event-video');
    const placeholder = document.getElementById('video-placeholder');
    video.style.display = 'none';
    video.src = '';
    placeholder.style.display = 'flex';
  }

  async function checkVideoCache(eventId) {
    try {
      const res = await fetch(`/api/media/video/${eventId}`);
      const data = await res.json();
      if (data.status === 'available') {
        showVideo(data.path);
      }
    } catch { /* Video not available */ }
  }

  function showVideo(src) {
    const video = document.getElementById('event-video');
    const placeholder = document.getElementById('video-placeholder');
    video.src = src;
    video.style.display = 'block';
    placeholder.style.display = 'none';
  }

  async function generateVideo() {
    if (!currentEvent) return;
    const btn = document.getElementById('btn-generate-video');
    btn.textContent = 'Generating...';
    btn.disabled = true;

    try {
      const res = await fetch('/api/media/generate-video', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_id: currentEvent.id,
          prompt: currentEvent.video_prompt,
          aspect_ratio: '16:9',
          duration_seconds: 8,
        }),
      });
      const data = await res.json();
      if (data.status === 'generated' || data.status === 'cached') {
        showVideo(`/videos/${currentEvent.id}.mp4`);
      } else {
        btn.textContent = 'Generation failed — ' + (data.detail || 'unknown error');
      }
    } catch (err) {
      btn.textContent = 'Error: ' + err.message;
    } finally {
      setTimeout(() => {
        btn.disabled = false;
        btn.innerHTML = '<span class="play-icon">&#9654;</span> Generate Veo 3.1 Video';
      }, 5000);
    }
  }

  return { init, showEvent, showPlaceholder };
})();
