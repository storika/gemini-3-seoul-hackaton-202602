/**
 * KG Renderer — Cytoscape.js graph with temporal decay visual encoding
 * + node click interactions per entity type
 */
const KGRenderer = (() => {
  let cy = null;
  let currentData = null;
  let selectedNodeId = null;
  let modelGallery = []; // loaded from API
  let folVisible = false;  // FOL layer toggle state

  // Brand colors (soju + beer)
  const BRAND_COLORS = {
    jinro: '#1B5E20',
    chamisul: '#2E7D32',
    chum_churum: '#1565C0',
    saero: '#F57C00',
    goodday: '#AB47BC',
    san: '#6D4C41',
    green: '#66BB6A',
    ipseju: '#EF6C00',
    daesun: '#D84315',
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
    sunhari: '#F48FB1',
    isul_ttokttok: '#80DEEA',
    multi: '#7B1FA2',
    '': '#888',
  };

  const BRAND_LABELS = {
    jinro: '진로', chamisul: '참이슬', chum_churum: '처음처럼',
    saero: '새로', goodday: '좋은데이', san: '산 소주', green: '그린소주',
    ipseju: '잎새주', daesun: '대선',
    terra: '테라', terra_light: '테라 라이트', cass: '카스',
    cass_light: '카스 라이트', kloud: '클라우드', kloud_draft: '클라우드 생드래프트',
    kloud_na: '클라우드 논알콜릭', krush: '크러시', kelly: '켈리',
    hite: '하이트', max: '맥스', ob: 'OB맥주', crown: '크라운맥주',
    sunhari: '순하리', isul_ttokttok: '이슬톡톡', multi: '통합',
  };

  // Node shapes by type
  const NODE_SHAPES = {
    brand: 'diamond',
    product: 'round-rectangle',
    ingredient: 'hexagon',
    person: 'ellipse',
    award: 'star',
    market: 'rectangle',
    event: 'barrel',
    unknown: 'ellipse',
    // FOL layer
    fol_predicate: 'round-triangle',
    fol_rule: 'vee',
    fol_conclusion: 'pentagon',
  };

  // FOL node colors by type
  const FOL_COLORS = {
    fol_predicate: '#FF8A65',
    fol_rule: '#FFD54F',
    fol_conclusion: '#81C784',
  };

  const TYPE_LABELS = {
    brand: 'Brand', product: 'Product', ingredient: 'Ingredient',
    person: 'Person', award: 'Award', market: 'Market', event: 'Event',
  };

  const TYPE_ICONS = {
    brand: '\u{1F3E2}', product: '\u{1F376}', ingredient: '\u{1F9EA}',
    person: '\u{1F464}', award: '\u{1F3C6}', market: '\u{1F4C8}', event: '\u{1F4C5}',
  };

  function getVisualState(weight) {
    if (weight >= 0.80) return { opacity: 1.0, glow: true, pulse: true, state: 'just-occurred' };
    if (weight >= 0.50) return { opacity: 0.85, glow: true, pulse: false, state: 'active' };
    if (weight >= 0.20) return { opacity: 0.65, glow: false, pulse: false, state: 'fading' };
    if (weight >= 0.05) return { opacity: 0.40, glow: false, pulse: false, state: 'nearly-forgotten' };
    return { opacity: 0.20, glow: false, pulse: false, state: 'inactive' };
  }

  function init() {
    cy = cytoscape({
      container: document.getElementById('cy'),
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'font-size': '10px',
            'font-family': 'Inter, sans-serif',
            'color': '#e8e8ec',
            'text-valign': 'bottom',
            'text-margin-y': 6,
            'text-outline-width': 2,
            'text-outline-color': '#0f1117',
            'width': 'data(size)',
            'height': 'data(size)',
            'background-color': 'data(color)',
            'background-opacity': 'data(opacity)',
            'border-width': 'data(borderWidth)',
            'border-color': 'data(color)',
            'border-style': 'data(borderStyle)',
            'shadow-blur': 'data(shadowBlur)',
            'shadow-color': 'data(color)',
            'shadow-opacity': 'data(shadowOpacity)',
            'shape': 'data(shape)',
            'transition-property': 'background-opacity, width, height, shadow-blur',
            'transition-duration': '0.4s',
          }
        },
        {
          selector: 'node.highlighted',
          style: {
            'border-width': 3,
            'border-color': '#fff',
            'shadow-blur': 20,
            'shadow-color': '#fff',
            'shadow-opacity': 0.5,
            'z-index': 999,
          }
        },
        {
          selector: 'node.neighbor',
          style: {
            'border-width': 2,
            'border-color': '#aaa',
          }
        },
        {
          selector: 'node.dimmed',
          style: {
            'background-opacity': 0.15,
            'border-opacity': 0.15,
            'text-opacity': 0.2,
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 1.5,
            'line-color': 'data(color)',
            'line-opacity': 'data(opacity)',
            'line-style': 'data(lineStyle)',
            'target-arrow-color': 'data(color)',
            'target-arrow-shape': 'triangle',
            'arrow-scale': 0.7,
            'curve-style': 'bezier',
            'label': 'data(relation)',
            'font-size': '8px',
            'color': '#555',
            'text-rotation': 'autorotate',
            'text-outline-width': 1,
            'text-outline-color': '#0f1117',
            'transition-property': 'line-opacity',
            'transition-duration': '0.4s',
          }
        },
        {
          selector: 'edge.highlighted',
          style: {
            'line-color': '#fff',
            'line-opacity': 0.9,
            'width': 2.5,
            'target-arrow-color': '#fff',
            'color': '#e8e8ec',
            'font-size': '9px',
          }
        },
        {
          selector: 'edge.dimmed',
          style: {
            'line-opacity': 0.08,
          }
        },
        // FOL layer styles
        {
          selector: 'node.fol-node',
          style: {
            'border-style': 'double',
            'border-width': 2,
            'font-size': '9px',
            'text-valign': 'bottom',
            'text-margin-y': 4,
          }
        },
        {
          selector: 'edge.fol-edge',
          style: {
            'line-style': 'dashed',
            'line-dash-pattern': [6, 3],
            'target-arrow-shape': 'diamond',
            'arrow-scale': 0.6,
          }
        },
        {
          selector: '.fol-hidden',
          style: {
            'display': 'none',
          }
        },
      ],
      layout: { name: 'preset' },
      minZoom: 0.3,
      maxZoom: 3,
      wheelSensitivity: 0.3,
    });

    // Node click handler
    cy.on('tap', 'node', handleNodeClick);

    // Click on background to deselect
    cy.on('tap', function (evt) {
      if (evt.target === cy) {
        clearSelection();
      }
    });

    // Load model gallery for person enrichment
    loadModelGallery();

    // Close popup button
    document.getElementById('node-popup-close').addEventListener('click', clearSelection);

    // FOL toggle button
    const folBtn = document.getElementById('btn-fol-toggle');
    if (folBtn) {
      folBtn.addEventListener('click', () => {
        folVisible = !folVisible;
        folBtn.classList.toggle('active', folVisible);
        toggleFOLLayer();
      });
    }
  }

  function toggleFOLLayer() {
    if (!cy) return;
    cy.elements('.fol-node, .fol-edge').forEach(el => {
      if (folVisible) {
        el.removeClass('fol-hidden');
      } else {
        el.addClass('fol-hidden');
      }
    });
  }

  function isFOLVisible() {
    return folVisible;
  }

  async function loadModelGallery() {
    try {
      const res = await fetch('/api/timeline/models');
      modelGallery = await res.json();
    } catch { /* optional enrichment */ }
  }

  function handleNodeClick(evt) {
    const node = evt.target;
    const nodeId = node.data('id');
    const nodeType = node.data('nodeType');
    const label = node.data('label');
    const brand = node.data('brand');
    const weight = node.data('weight');

    selectedNodeId = nodeId;

    // Visual: highlight node + neighbors, dim others
    cy.elements().removeClass('highlighted neighbor dimmed');
    cy.elements().addClass('dimmed');
    node.removeClass('dimmed').addClass('highlighted');
    const neighborhood = node.neighborhood();
    neighborhood.removeClass('dimmed').addClass('neighbor');
    neighborhood.connectedEdges().removeClass('dimmed').addClass('highlighted');
    node.connectedEdges().removeClass('dimmed').addClass('highlighted');

    // Get connected edges info
    const connections = [];
    node.connectedEdges().forEach(edge => {
      const src = edge.source().data('label');
      const tgt = edge.target().data('label');
      const rel = edge.data('relation');
      const other = edge.source().data('id') === nodeId ? tgt : src;
      const dir = edge.source().data('id') === nodeId ? '→' : '←';
      connections.push({ other, rel, dir });
    });

    // Build popup content by type
    const popup = document.getElementById('node-popup');
    const content = document.getElementById('node-popup-content');

    let html = '';
    switch (nodeType) {
      case 'person':
        html = buildPersonPopup(nodeId, label, brand, weight, connections);
        break;
      case 'brand':
        html = buildBrandPopup(nodeId, label, brand, weight, connections);
        break;
      case 'product':
        html = buildProductPopup(nodeId, label, brand, weight, connections);
        break;
      case 'award':
        html = buildAwardPopup(nodeId, label, brand, weight, connections);
        break;
      case 'market':
        html = buildMarketPopup(nodeId, label, brand, weight, connections);
        break;
      case 'ingredient':
        html = buildIngredientPopup(nodeId, label, brand, weight, connections);
        break;
      case 'fol_predicate':
      case 'fol_rule':
      case 'fol_conclusion':
        html = buildFOLPopup(nodeId, label, nodeType, brand, weight, connections);
        break;
      default:
        html = buildGenericPopup(nodeId, label, nodeType, brand, weight, connections);
    }

    content.innerHTML = html;
    popup.classList.remove('hidden');

    // Position popup near node
    const pos = node.renderedPosition();
    const container = document.getElementById('kg-panel');
    const rect = container.getBoundingClientRect();
    popup.style.left = `${Math.min(Math.max(pos.x - 140, 10), rect.width - 300)}px`;
    popup.style.top = `${Math.min(Math.max(pos.y + 30, 10), rect.height - 200)}px`;
  }

  function clearSelection() {
    selectedNodeId = null;
    if (cy) {
      cy.elements().removeClass('highlighted neighbor dimmed');
    }
    document.getElementById('node-popup').classList.add('hidden');
  }

  // ── Popup builders per entity type ─────────────────────

  function buildPersonPopup(nodeId, label, brand, weight, connections) {
    const brandLabel = BRAND_LABELS[brand] || brand;
    const brandColor = BRAND_COLORS[brand] || '#888';
    const weightBar = buildWeightBar(weight);

    // Find matching model from gallery — prefer entries with real images
    const candidates = modelGallery.filter(m =>
      label.toLowerCase().includes(m.name.toLowerCase().split(' ')[0]) ||
      label.includes(m.name_ko)
    );
    const model = candidates.find(m => m.image_url && m.image_url.includes('/real/')) || candidates[0];

    const portrait = model
      ? `<img src="${model.image_url}" class="popup-portrait" alt="${label}"
             onerror="this.style.display='none'">`
      : '';

    const modelInfo = model
      ? `<div class="popup-model-meta">
           <span style="color:${brandColor}">${getBrandLabel(model.brand)}</span>
           <span>${model.start_year}–${model.end_year}</span>
         </div>
         ${model.era_note ? `<p class="popup-era-note">${model.era_note}</p>` : ''}`
      : '';

    const rels = connections.map(c =>
      `<div class="popup-rel"><span class="rel-dir">${c.dir}</span> <span class="rel-label">${c.rel}</span> ${c.other}</div>`
    ).join('');

    return `
      <div class="popup-header person">
        ${portrait}
        <div>
          <span class="popup-type-badge person">${TYPE_ICONS.person} Person</span>
          <h3>${label}</h3>
          ${modelInfo}
        </div>
      </div>
      ${weightBar}
      <div class="popup-section">
        <h4>Relationships</h4>
        ${rels || '<span class="popup-muted">None</span>'}
      </div>
    `;
  }

  function buildBrandPopup(nodeId, label, brand, weight, connections) {
    const brandColor = BRAND_COLORS[brand] || '#888';
    const weightBar = buildWeightBar(weight);

    // Group connections by type
    const products = connections.filter(c => c.rel === 'PRODUCES');
    const models = connections.filter(c => c.rel === 'ENDORSES' || c.other.includes('Model'));
    const others = connections.filter(c => !products.includes(c) && !models.includes(c));

    const prodHtml = products.length
      ? products.map(c => `<div class="popup-chip product">${c.other}</div>`).join('')
      : '<span class="popup-muted">None</span>';

    const othersHtml = others.map(c =>
      `<div class="popup-rel"><span class="rel-dir">${c.dir}</span> <span class="rel-label">${c.rel}</span> ${c.other}</div>`
    ).join('');

    return `
      <div class="popup-header brand">
        <div class="popup-brand-icon" style="background:${brandColor}">${label.charAt(0)}</div>
        <div>
          <span class="popup-type-badge brand">${TYPE_ICONS.brand} Brand</span>
          <h3>${label}</h3>
        </div>
      </div>
      ${weightBar}
      <div class="popup-section">
        <h4>Products</h4>
        <div class="popup-chips">${prodHtml}</div>
      </div>
      ${othersHtml ? `<div class="popup-section"><h4>Connections</h4>${othersHtml}</div>` : ''}
    `;
  }

  function buildProductPopup(nodeId, label, brand, weight, connections) {
    const brandColor = BRAND_COLORS[brand] || '#888';
    const weightBar = buildWeightBar(weight);

    const ingredients = connections.filter(c => c.rel.includes('INGREDIENT'));
    const brandConn = connections.filter(c => c.rel === 'PRODUCES');
    const competes = connections.filter(c => c.rel === 'COMPETES_WITH');
    const others = connections.filter(c =>
      !ingredients.includes(c) && !brandConn.includes(c) && !competes.includes(c)
    );

    const ingHtml = ingredients.map(c =>
      `<div class="popup-chip ingredient">${c.other}</div>`
    ).join('') || '<span class="popup-muted">None</span>';

    const compHtml = competes.map(c =>
      `<div class="popup-chip compete">${c.other}</div>`
    ).join('');

    return `
      <div class="popup-header product">
        <div class="popup-product-icon" style="border-color:${brandColor}">
          ${TYPE_ICONS.product}
        </div>
        <div>
          <span class="popup-type-badge product">${TYPE_ICONS.product} Product</span>
          <h3>${label}</h3>
          ${brandConn.length ? `<span class="popup-brand-sub" style="color:${brandColor}">${brandConn[0].other}</span>` : ''}
        </div>
      </div>
      ${weightBar}
      <div class="popup-section">
        <h4>Ingredients</h4>
        <div class="popup-chips">${ingHtml}</div>
      </div>
      ${compHtml ? `<div class="popup-section"><h4>Competes With</h4><div class="popup-chips">${compHtml}</div></div>` : ''}
      ${others.length ? `<div class="popup-section"><h4>Other</h4>${others.map(c =>
        `<div class="popup-rel"><span class="rel-dir">${c.dir}</span> <span class="rel-label">${c.rel}</span> ${c.other}</div>`
      ).join('')}</div>` : ''}
    `;
  }

  function buildAwardPopup(nodeId, label, brand, weight, connections) {
    const weightBar = buildWeightBar(weight);
    const rels = connections.map(c =>
      `<div class="popup-rel"><span class="rel-dir">${c.dir}</span> <span class="rel-label">${c.rel}</span> ${c.other}</div>`
    ).join('');

    return `
      <div class="popup-header award">
        <span class="popup-award-icon">${TYPE_ICONS.award}</span>
        <div>
          <span class="popup-type-badge award">${TYPE_ICONS.award} Award</span>
          <h3>${label}</h3>
        </div>
      </div>
      ${weightBar}
      <div class="popup-section">
        <h4>Achieved By</h4>
        ${rels || '<span class="popup-muted">—</span>'}
      </div>
    `;
  }

  function buildMarketPopup(nodeId, label, brand, weight, connections) {
    const weightBar = buildWeightBar(weight);
    const participants = connections.filter(c => c.rel.includes('MARKET') || c.rel === 'INCLUDES');
    const others = connections.filter(c => !participants.includes(c));

    return `
      <div class="popup-header market">
        <span class="popup-market-icon">${TYPE_ICONS.market}</span>
        <div>
          <span class="popup-type-badge market">${TYPE_ICONS.market} Market</span>
          <h3>${label}</h3>
        </div>
      </div>
      ${weightBar}
      <div class="popup-section">
        <h4>Participants</h4>
        <div class="popup-chips">
          ${participants.map(c => `<div class="popup-chip market">${c.other}</div>`).join('') || '<span class="popup-muted">—</span>'}
        </div>
      </div>
      ${others.length ? `<div class="popup-section"><h4>Connections</h4>${others.map(c =>
        `<div class="popup-rel"><span class="rel-dir">${c.dir}</span> <span class="rel-label">${c.rel}</span> ${c.other}</div>`
      ).join('')}</div>` : ''}
    `;
  }

  function buildIngredientPopup(nodeId, label, brand, weight, connections) {
    const weightBar = buildWeightBar(weight);
    const usedBy = connections.filter(c => c.rel.includes('INGREDIENT'));
    const others = connections.filter(c => !usedBy.includes(c));

    return `
      <div class="popup-header ingredient">
        <span class="popup-ingredient-icon">${TYPE_ICONS.ingredient}</span>
        <div>
          <span class="popup-type-badge ingredient">${TYPE_ICONS.ingredient} Ingredient</span>
          <h3>${label}</h3>
        </div>
      </div>
      ${weightBar}
      <div class="popup-section">
        <h4>Used In</h4>
        <div class="popup-chips">
          ${usedBy.map(c => `<div class="popup-chip product">${c.other}</div>`).join('') || '<span class="popup-muted">—</span>'}
        </div>
      </div>
    `;
  }

  function buildFOLPopup(nodeId, label, nodeType, brand, weight, connections) {
    const weightBar = buildWeightBar(weight);
    const brandColor = BRAND_COLORS[brand] || '#888';
    const folColor = FOL_COLORS[nodeType] || '#FFD54F';

    const typeLabels = {
      fol_predicate: 'Predicate (P)',
      fol_rule: 'Rule (P -> Q)',
      fol_conclusion: 'Conclusion (Q)',
    };
    const typeIcons = {
      fol_predicate: '\u{1F4A1}',
      fol_rule: '\u{2192}',
      fol_conclusion: '\u{2714}',
    };

    const supports = connections.filter(c => c.rel === 'SUPPORTS');
    const implies = connections.filter(c => c.rel === 'IMPLIES');
    const explains = connections.filter(c => c.rel === 'EXPLAINS');
    const others = connections.filter(c =>
      !supports.includes(c) && !implies.includes(c) && !explains.includes(c)
    );

    const renderSection = (title, items, chipClass) => {
      if (!items.length) return '';
      return `<div class="popup-section">
        <h4>${title}</h4>
        <div class="popup-chips">
          ${items.map(c => `<div class="popup-chip ${chipClass}">${c.other}</div>`).join('')}
        </div>
      </div>`;
    };

    return `
      <div class="popup-header fol">
        <div class="popup-fol-icon" style="background:${folColor}">
          ${typeIcons[nodeType] || '\u{1F4CB}'}
        </div>
        <div>
          <span class="popup-type-badge fol" style="background:${folColor}20; color:${folColor}">
            FOL ${typeLabels[nodeType] || nodeType}
          </span>
          <h3>${label}</h3>
          <span class="popup-brand-sub" style="color:${brandColor}">
            ${BRAND_LABELS[brand] || brand}
          </span>
        </div>
      </div>
      ${weightBar}
      ${renderSection('Supported By', supports, 'fol-support')}
      ${renderSection('Implies', implies, 'fol-imply')}
      ${renderSection('Explains', explains, 'fol-explain')}
      ${others.length ? `<div class="popup-section"><h4>Links</h4>
        ${others.map(c => `<div class="popup-rel"><span class="rel-dir">${c.dir}</span> <span class="rel-label">${c.rel}</span> ${c.other}</div>`).join('')}
      </div>` : ''}
    `;
  }

  function buildGenericPopup(nodeId, label, nodeType, brand, weight, connections) {
    const weightBar = buildWeightBar(weight);
    const icon = TYPE_ICONS[nodeType] || '\u{1F4CC}';
    const rels = connections.map(c =>
      `<div class="popup-rel"><span class="rel-dir">${c.dir}</span> <span class="rel-label">${c.rel}</span> ${c.other}</div>`
    ).join('');

    return `
      <div class="popup-header">
        <div>
          <span class="popup-type-badge">${icon} ${TYPE_LABELS[nodeType] || nodeType}</span>
          <h3>${label}</h3>
        </div>
      </div>
      ${weightBar}
      <div class="popup-section">
        <h4>Connections</h4>
        ${rels || '<span class="popup-muted">None</span>'}
      </div>
    `;
  }

  function buildWeightBar(weight) {
    const pct = Math.round(weight * 100);
    const vis = getVisualState(weight);
    const stateLabels = {
      'just-occurred': 'Active',
      'active': 'Active',
      'fading': 'Fading',
      'nearly-forgotten': 'Dim',
      'inactive': 'Inactive',
    };
    return `
      <div class="popup-weight">
        <div class="popup-weight-track">
          <div class="popup-weight-fill" style="width:${pct}%"></div>
        </div>
        <span class="popup-weight-label">${stateLabels[vis.state]} (${pct}%)</span>
      </div>
    `;
  }

  function getBrandLabel(brand) {
    return BRAND_LABELS[brand] || brand;
  }

  function update(snapshot) {
    if (!cy) return;
    currentData = snapshot;

    // Clear selection on update
    clearSelection();

    const elements = [];

    snapshot.nodes.forEach(node => {
      const vis = getVisualState(node.temporal_weight);
      const color = BRAND_COLORS[node.brand] || BRAND_COLORS[''];
      const shape = NODE_SHAPES[node.type] || NODE_SHAPES.unknown;
      const baseSize = node.type === 'brand' ? 50 : (node.type === 'person' ? 40 : 30);
      const size = vis.pulse ? baseSize * 1.3 : baseSize;

      elements.push({
        group: 'nodes',
        data: {
          id: node.id,
          label: node.label,
          color: color,
          opacity: vis.opacity,
          shape: shape,
          size: size,
          borderWidth: vis.state === 'inactive' ? 2 : 1,
          borderStyle: vis.state === 'inactive' ? 'dashed' : 'solid',
          shadowBlur: vis.glow ? (vis.pulse ? 18 : 10) : 0,
          shadowOpacity: vis.glow ? 0.6 : 0,
          weight: node.temporal_weight,
          brand: node.brand,
          nodeType: node.type,
        },
      });
    });

    snapshot.edges.forEach(edge => {
      const vis = getVisualState(edge.temporal_weight);
      const color = BRAND_COLORS[edge.brand] || BRAND_COLORS[''];

      elements.push({
        group: 'edges',
        data: {
          id: `${edge.source}-${edge.relation}-${edge.target}`,
          source: edge.source,
          target: edge.target,
          relation: edge.relation,
          color: color,
          opacity: vis.opacity * 0.7,
          lineStyle: vis.state === 'inactive' ? 'dashed' : 'solid',
        },
      });
    });

    // Add FOL layer nodes/edges if present
    if (snapshot.fol_nodes) {
      snapshot.fol_nodes.forEach(node => {
        const vis = getVisualState(node.temporal_weight);
        const folColor = FOL_COLORS[node.type] || '#FFD54F';
        const shape = NODE_SHAPES[node.type] || 'round-triangle';
        const baseSize = node.type === 'fol_rule' ? 32 : (node.type === 'fol_conclusion' ? 36 : 26);

        elements.push({
          group: 'nodes',
          data: {
            id: node.id,
            label: node.label_ko || node.label,
            color: folColor,
            opacity: vis.opacity * 0.9,
            shape: shape,
            size: baseSize,
            borderWidth: 2,
            borderStyle: 'solid',
            shadowBlur: vis.glow ? 8 : 0,
            shadowOpacity: vis.glow ? 0.4 : 0,
            weight: node.temporal_weight,
            brand: node.brand,
            nodeType: node.type,
            layer: 'fol',
          },
          classes: folVisible ? 'fol-node' : 'fol-node fol-hidden',
        });
      });
    }

    if (snapshot.fol_edges) {
      snapshot.fol_edges.forEach(edge => {
        const vis = getVisualState(edge.temporal_weight);
        const relColor = edge.relation === 'SUPPORTS' ? '#FF8A65'
          : edge.relation === 'IMPLIES' ? '#FFD54F'
          : '#81C784'; // EXPLAINS

        elements.push({
          group: 'edges',
          data: {
            id: `fol-${edge.source}-${edge.relation}-${edge.target}`,
            source: edge.source,
            target: edge.target,
            relation: edge.relation,
            color: relColor,
            opacity: vis.opacity * 0.5,
            lineStyle: 'dashed',
            layer: 'fol',
          },
          classes: folVisible ? 'fol-edge' : 'fol-edge fol-hidden',
        });
      });
    }

    cy.elements().remove();
    cy.add(elements);

    if (elements.length > 0) {
      cy.layout({
        name: 'cose',
        animate: true,
        animationDuration: 600,
        nodeRepulsion: () => 6000,
        idealEdgeLength: () => 80,
        gravity: 0.3,
        padding: 30,
        randomize: false,
        componentSpacing: 60,
      }).run();
    }

    const folNodeCount = snapshot.fol_nodes ? snapshot.fol_nodes.length : 0;
    document.getElementById('stat-nodes').textContent = `${snapshot.nodes.length} nodes`;
    document.getElementById('stat-edges').textContent = `${snapshot.edges.length} edges`;
    document.getElementById('stat-events').textContent =
      `${snapshot.stats.active_events} events`;
  }

  function highlightBrand(brand) {
    if (!cy) return;
    if (brand === 'all') {
      cy.nodes().style('opacity', null);
    } else {
      cy.nodes().forEach(n => {
        const nb = n.data('brand');
        n.style('background-opacity', nb === brand ? n.data('opacity') : n.data('opacity') * 0.3);
      });
    }
  }

  function getCy() { return cy; }

  return { init, update, highlightBrand, getCy, isFOLVisible };
})();
