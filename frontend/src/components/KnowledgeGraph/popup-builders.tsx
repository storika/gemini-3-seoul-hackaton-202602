import { BRAND_COLORS, BRAND_LABELS, TYPE_ICONS, FOL_COLORS } from "@/lib/constants";
import type { ModelEntry } from "@/lib/types";

interface Connection {
  other: string;
  rel: string;
  dir: string;
}

function WeightBar({ weight }: { weight: number }) {
  const pct = Math.round(weight * 100);
  const stateLabel =
    weight >= 0.5 ? "Active" : weight >= 0.2 ? "Fading" : weight >= 0.05 ? "Dim" : "Inactive";
  return (
    <div className="popup-weight">
      <div className="popup-weight-track">
        <div className="popup-weight-fill" style={{ width: `${pct}%` }} />
      </div>
      <span className="popup-weight-label">
        {stateLabel} ({pct}%)
      </span>
    </div>
  );
}

function RelList({ connections }: { connections: Connection[] }) {
  if (!connections.length) return <span className="popup-muted">None</span>;
  return (
    <>
      {connections.map((c, i) => (
        <div key={i} className="popup-rel">
          <span className="rel-dir">{c.dir}</span>
          <span className="rel-label">{c.rel}</span> {c.other}
        </div>
      ))}
    </>
  );
}

export function buildPersonPopup(
  label: string,
  brand: string,
  weight: number,
  connections: Connection[],
  modelGallery: ModelEntry[]
) {
  const brandColor = BRAND_COLORS[brand] || "#888";
  const candidates = modelGallery.filter(
    (m) =>
      label.toLowerCase().includes(m.name.toLowerCase().split(" ")[0]) ||
      label.includes(m.name_ko)
  );
  const model =
    candidates.find((m) => m.image_url?.includes("/real/")) || candidates[0];

  return (
    <>
      <div className="popup-header person">
        {model && (
          <img
            src={model.image_url}
            className="popup-portrait"
            alt={label}
            onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
          />
        )}
        <div>
          <span className="popup-type-badge person">{TYPE_ICONS.person} Person</span>
          <h3>{label}</h3>
          {model && (
            <>
              <div className="popup-model-meta">
                <span style={{ color: brandColor }}>
                  {BRAND_LABELS[model.brand] || model.brand}
                </span>
                <span>{model.start_year}&ndash;{model.end_year}</span>
              </div>
              {model.era_note && <p className="popup-era-note">{model.era_note}</p>}
            </>
          )}
        </div>
      </div>
      <WeightBar weight={weight} />
      <div className="popup-section">
        <h4>Relationships</h4>
        <RelList connections={connections} />
      </div>
    </>
  );
}

export function buildBrandPopup(
  label: string,
  brand: string,
  weight: number,
  connections: Connection[]
) {
  const brandColor = BRAND_COLORS[brand] || "#888";
  const products = connections.filter((c) => c.rel === "PRODUCES");
  const others = connections.filter((c) => c.rel !== "PRODUCES");

  return (
    <>
      <div className="popup-header brand">
        <div className="popup-brand-icon" style={{ background: brandColor }}>
          {label.charAt(0)}
        </div>
        <div>
          <span className="popup-type-badge brand">{TYPE_ICONS.brand} Brand</span>
          <h3>{label}</h3>
        </div>
      </div>
      <WeightBar weight={weight} />
      <div className="popup-section">
        <h4>Products</h4>
        <div className="popup-chips">
          {products.length ? (
            products.map((c, i) => (
              <div key={i} className="popup-chip product">{c.other}</div>
            ))
          ) : (
            <span className="popup-muted">None</span>
          )}
        </div>
      </div>
      {others.length > 0 && (
        <div className="popup-section">
          <h4>Connections</h4>
          <RelList connections={others} />
        </div>
      )}
    </>
  );
}

export function buildProductPopup(
  label: string,
  brand: string,
  weight: number,
  connections: Connection[]
) {
  const brandColor = BRAND_COLORS[brand] || "#888";
  const ingredients = connections.filter((c) => c.rel.includes("INGREDIENT"));
  const brandConn = connections.filter((c) => c.rel === "PRODUCES");
  const competes = connections.filter((c) => c.rel === "COMPETES_WITH");
  const others = connections.filter(
    (c) => !ingredients.includes(c) && !brandConn.includes(c) && !competes.includes(c)
  );

  return (
    <>
      <div className="popup-header product">
        <div className="popup-product-icon" style={{ borderColor: brandColor }}>
          {TYPE_ICONS.product}
        </div>
        <div>
          <span className="popup-type-badge product">{TYPE_ICONS.product} Product</span>
          <h3>{label}</h3>
          {brandConn.length > 0 && (
            <span className="popup-brand-sub" style={{ color: brandColor }}>
              {brandConn[0].other}
            </span>
          )}
        </div>
      </div>
      <WeightBar weight={weight} />
      <div className="popup-section">
        <h4>Ingredients</h4>
        <div className="popup-chips">
          {ingredients.length ? (
            ingredients.map((c, i) => (
              <div key={i} className="popup-chip ingredient">{c.other}</div>
            ))
          ) : (
            <span className="popup-muted">None</span>
          )}
        </div>
      </div>
      {competes.length > 0 && (
        <div className="popup-section">
          <h4>Competes With</h4>
          <div className="popup-chips">
            {competes.map((c, i) => (
              <div key={i} className="popup-chip compete">{c.other}</div>
            ))}
          </div>
        </div>
      )}
      {others.length > 0 && (
        <div className="popup-section">
          <h4>Other</h4>
          <RelList connections={others} />
        </div>
      )}
    </>
  );
}

export function buildAwardPopup(
  label: string,
  weight: number,
  connections: Connection[]
) {
  return (
    <>
      <div className="popup-header award">
        <span className="popup-award-icon">{TYPE_ICONS.award}</span>
        <div>
          <span className="popup-type-badge award">{TYPE_ICONS.award} Award</span>
          <h3>{label}</h3>
        </div>
      </div>
      <WeightBar weight={weight} />
      <div className="popup-section">
        <h4>Achieved By</h4>
        <RelList connections={connections} />
      </div>
    </>
  );
}

export function buildMarketPopup(
  label: string,
  weight: number,
  connections: Connection[]
) {
  const participants = connections.filter(
    (c) => c.rel.includes("MARKET") || c.rel === "INCLUDES"
  );
  const others = connections.filter((c) => !participants.includes(c));

  return (
    <>
      <div className="popup-header market">
        <span className="popup-market-icon">{TYPE_ICONS.market}</span>
        <div>
          <span className="popup-type-badge market">{TYPE_ICONS.market} Market</span>
          <h3>{label}</h3>
        </div>
      </div>
      <WeightBar weight={weight} />
      <div className="popup-section">
        <h4>Participants</h4>
        <div className="popup-chips">
          {participants.length ? (
            participants.map((c, i) => (
              <div key={i} className="popup-chip market">{c.other}</div>
            ))
          ) : (
            <span className="popup-muted">&mdash;</span>
          )}
        </div>
      </div>
      {others.length > 0 && (
        <div className="popup-section">
          <h4>Connections</h4>
          <RelList connections={others} />
        </div>
      )}
    </>
  );
}

export function buildIngredientPopup(
  label: string,
  weight: number,
  connections: Connection[]
) {
  const usedBy = connections.filter((c) => c.rel.includes("INGREDIENT"));
  return (
    <>
      <div className="popup-header ingredient">
        <span className="popup-ingredient-icon">{TYPE_ICONS.ingredient}</span>
        <div>
          <span className="popup-type-badge ingredient">{TYPE_ICONS.ingredient} Ingredient</span>
          <h3>{label}</h3>
        </div>
      </div>
      <WeightBar weight={weight} />
      <div className="popup-section">
        <h4>Used In</h4>
        <div className="popup-chips">
          {usedBy.length ? (
            usedBy.map((c, i) => (
              <div key={i} className="popup-chip product">{c.other}</div>
            ))
          ) : (
            <span className="popup-muted">&mdash;</span>
          )}
        </div>
      </div>
    </>
  );
}

export function buildFOLPopup(
  label: string,
  nodeType: string,
  brand: string,
  weight: number,
  connections: Connection[]
) {
  const brandColor = BRAND_COLORS[brand] || "#888";
  const folColor = FOL_COLORS[nodeType] || "#FFD54F";
  const typeLabels: Record<string, string> = {
    fol_predicate: "Predicate (P)",
    fol_rule: "Rule (P -> Q)",
    fol_conclusion: "Conclusion (Q)",
  };
  const typeIcons: Record<string, string> = {
    fol_predicate: "\u{1F4A1}",
    fol_rule: "\u2192",
    fol_conclusion: "\u2714",
  };

  const supports = connections.filter((c) => c.rel === "SUPPORTS");
  const implies = connections.filter((c) => c.rel === "IMPLIES");
  const explains = connections.filter((c) => c.rel === "EXPLAINS");
  const others = connections.filter(
    (c) => !supports.includes(c) && !implies.includes(c) && !explains.includes(c)
  );

  return (
    <>
      <div className="popup-header fol">
        <div className="popup-fol-icon" style={{ background: folColor }}>
          {typeIcons[nodeType] || "\u{1F4CB}"}
        </div>
        <div>
          <span
            className="popup-type-badge fol"
            style={{ background: `${folColor}20`, color: folColor }}
          >
            {typeLabels[nodeType] || nodeType}
          </span>
          <h3>{label}</h3>
          <span className="popup-brand-sub" style={{ color: brandColor }}>
            {BRAND_LABELS[brand] || brand}
          </span>
        </div>
      </div>
      <WeightBar weight={weight} />
      {supports.length > 0 && (
        <div className="popup-section">
          <h4>Supported By</h4>
          <div className="popup-chips">
            {supports.map((c, i) => (
              <div key={i} className="popup-chip fol-support">{c.other}</div>
            ))}
          </div>
        </div>
      )}
      {implies.length > 0 && (
        <div className="popup-section">
          <h4>Implies</h4>
          <div className="popup-chips">
            {implies.map((c, i) => (
              <div key={i} className="popup-chip fol-imply">{c.other}</div>
            ))}
          </div>
        </div>
      )}
      {explains.length > 0 && (
        <div className="popup-section">
          <h4>Explains</h4>
          <div className="popup-chips">
            {explains.map((c, i) => (
              <div key={i} className="popup-chip fol-explain">{c.other}</div>
            ))}
          </div>
        </div>
      )}
      {others.length > 0 && (
        <div className="popup-section">
          <h4>Links</h4>
          <RelList connections={others} />
        </div>
      )}
    </>
  );
}

export function buildGenericPopup(
  label: string,
  nodeType: string,
  weight: number,
  connections: Connection[]
) {
  const icon = TYPE_ICONS[nodeType] || "\u{1F4CC}";
  return (
    <>
      <div className="popup-header">
        <div>
          <span className="popup-type-badge">{icon} {nodeType}</span>
          <h3>{label}</h3>
        </div>
      </div>
      <WeightBar weight={weight} />
      <div className="popup-section">
        <h4>Connections</h4>
        <RelList connections={connections} />
      </div>
    </>
  );
}
