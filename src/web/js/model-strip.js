/**
 * Model Strip — horizontal thumbnail gallery of soju/beer models along the timeline.
 * Syncs with timeline slider and detail panel.
 */
const ModelStrip = (() => {
  const MIN_YEAR = 1924;
  const MAX_YEAR = 2026;
  let allModels = [];
  let models = [];   // filtered subset currently displayed
  let currentYear = MIN_YEAR;
  let activeModels = [];
  let currentProductType = 'all';

  const BRAND_BORDERS = {
    chamisul: '#2E7D32',
    chum_churum: '#1565C0',
    saero: '#F57C00',
    jinro_is_back: '#388E3C',
    jinro: '#1B5E20',
    goodday: '#AB47BC',
    san: '#6D4C41',
    green: '#66BB6A',
    ipseju: '#EF6C00',
    daesun: '#D84315',
    // Beer brands
    terra: '#00897B',
    terra_light: '#26A69A',
    cass: '#1565C0',
    cass_light: '#42A5F5',
    kloud: '#6A1B9A',
    kloud_draft: '#8E24AA',
    kloud_na: '#AB47BC',
    krush: '#D81B60',
    kelly: '#C62828',
    hite: '#0D47A1',
    max: '#BF360C',
    ob: '#1A237E',
    crown: '#4E342E',
    // Other
    sunhari: '#F48FB1',
    isul_ttokttok: '#80DEEA',
  };

  async function init() {
    try {
      const res = await fetch('/api/timeline/models');
      allModels = await res.json();
      models = allModels;
      render();
      initTypeTabs();
    } catch (err) {
      console.error('Failed to load models:', err);
    }
  }

  function initTypeTabs() {
    const tabs = document.querySelectorAll('#product-type-tabs .type-tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentProductType = tab.dataset.type;
        filterByProductType(currentProductType);
      });
    });
  }

  function filterByProductType(type) {
    if (type === 'all') {
      models = allModels;
    } else {
      models = allModels.filter(m => m.product_type === type);
    }
    render();
    updateYear(currentYear);
  }

  function render() {
    const container = document.getElementById('model-thumbnails');
    if (!container) return;
    container.innerHTML = '';

    models.forEach(model => {
      const thumb = document.createElement('div');
      thumb.className = 'model-thumb future';
      thumb.dataset.modelId = model.id;
      thumb.dataset.startYear = model.start_year;
      thumb.dataset.endYear = model.end_year;
      thumb.dataset.brand = model.brand;

      const pct = ((model.start_year - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)) * 100;
      thumb.style.left = `${pct}%`;

      const borderColor = BRAND_BORDERS[model.brand] || '#666';
      thumb.style.borderColor = borderColor;

      // Click → jump timeline to this model's era
      thumb.addEventListener('click', () => {
        TimelineSlider.jumpToYear(model.start_year);
      });

      // Image
      const img = document.createElement('img');
      img.alt = model.name_ko;
      img.src = model.image_url;
      img.onerror = () => {
        img.style.display = 'none';
        const initials = document.createElement('span');
        initials.className = 'model-initials';
        initials.textContent = model.name_ko.charAt(0);
        thumb.appendChild(initials);
      };
      thumb.appendChild(img);

      // Tooltip
      const tooltip = document.createElement('div');
      tooltip.className = 'model-tooltip';
      tooltip.innerHTML = `
        <strong>${model.name_ko}</strong>
        ${model.company_ko ? `<span class="model-tooltip-company">${model.company_ko}</span>` : ''}
        <span class="model-tooltip-brand">${getBrandLabel(model.brand)}</span>
        <span class="model-tooltip-years">${model.start_year}–${model.end_year}</span>
        ${model.era_note ? `<span class="model-tooltip-note">${model.era_note}</span>` : ''}
      `;
      thumb.appendChild(tooltip);

      // Duration bar
      const duration = document.createElement('div');
      duration.className = 'model-duration-bar';
      const durationPct = ((model.end_year - model.start_year) / (MAX_YEAR - MIN_YEAR)) * 100;
      duration.style.width = `${Math.max(durationPct, 0.5)}%`;
      duration.style.backgroundColor = borderColor;
      thumb.appendChild(duration);

      container.appendChild(thumb);
    });
  }

  function updateYear(year) {
    currentYear = year;
    activeModels = [];

    const thumbs = document.querySelectorAll('.model-thumb');
    thumbs.forEach((thumb, idx) => {
      const start = parseInt(thumb.dataset.startYear);
      const end = parseInt(thumb.dataset.endYear);
      if (year >= start && year <= end) {
        thumb.classList.add('active');
        thumb.classList.remove('past', 'future');
        if (models[idx]) activeModels.push(models[idx]);
      } else if (year > end) {
        thumb.classList.add('past');
        thumb.classList.remove('active', 'future');
      } else {
        thumb.classList.add('future');
        thumb.classList.remove('active', 'past');
      }
    });

    // Update detail panel with active model info
    renderActiveModels();
  }

  function renderActiveModels() {
    const section = document.getElementById('active-model-section');
    const container = document.getElementById('active-model-cards');
    if (!section || !container) return;

    if (activeModels.length === 0) {
      section.classList.add('hidden');
      return;
    }

    section.classList.remove('hidden');
    container.innerHTML = '';

    activeModels.forEach(model => {
      const card = document.createElement('div');
      card.className = `active-model-card brand-${model.brand}`;

      const borderColor = BRAND_BORDERS[model.brand] || '#666';

      card.innerHTML = `
        <div class="active-model-img-wrap" style="border-color: ${borderColor}">
          <img src="${model.image_url}" alt="${model.name_ko}"
               onerror="this.parentElement.innerHTML='<span>${model.name_ko.charAt(0)}</span>'">
        </div>
        <div class="active-model-info">
          <strong>${model.name_ko}</strong>
          ${model.company_ko ? `<span class="active-model-company">${model.company_ko}</span>` : ''}
          <span class="active-model-brand" style="color:${borderColor}">${getBrandLabel(model.brand)}</span>
          <span class="active-model-years">${model.start_year}–${model.end_year}</span>
          ${model.era_note ? `<p class="active-model-note">${model.era_note}</p>` : ''}
        </div>
      `;
      container.appendChild(card);
    });
  }

  function getActiveModels() {
    return activeModels;
  }

  function getBrandLabel(brand) {
    const labels = {
      chamisul: '참이슬',
      chum_churum: '처음처럼',
      saero: '새로',
      jinro_is_back: '진로이즈백',
      jinro: '진로',
      goodday: '좋은데이',
      san: '산 소주',
      green: '그린소주',
      ipseju: '잎새주',
      daesun: '대선',
      terra: '테라',
      terra_light: '테라 라이트',
      cass: '카스',
      cass_light: '카스 라이트',
      kloud: '클라우드',
      kloud_draft: '클라우드 생드래프트',
      kloud_na: '클라우드 논알콜릭',
      krush: '크러시',
      kelly: '켈리',
      hite: '하이트',
      max: '맥스',
      ob: 'OB맥주',
      crown: '크라운맥주',
      sunhari: '순하리',
      isul_ttokttok: '이슬톡톡',
    };
    return labels[brand] || brand;
  }

  return { init, updateYear, getActiveModels };
})();
