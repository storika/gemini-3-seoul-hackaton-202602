export const MIN_DATE = new Date(1924, 0, 1);
export const MAX_DATE = new Date(2026, 11, 31);
export const TOTAL_MS = MAX_DATE.getTime() - MIN_DATE.getTime();

export const PLAY_INTERVAL_MS = 1500;
export const PLAY_STEP_DAYS = 180;
export const DEBOUNCE_MS = 80;

export const BRAND_COLORS: Record<string, string> = {
  jinro: "#1B5E20",
  chamisul: "#2E7D32",
  chum_churum: "#1565C0",
  saero: "#F57C00",
  goodday: "#AB47BC",
  san: "#6D4C41",
  green: "#66BB6A",
  ipseju: "#EF6C00",
  daesun: "#D84315",
  terra: "#00897B",
  terra_light: "#26A69A",
  cass: "#1565C0",
  cass_light: "#42A5F5",
  kloud: "#6A1B9A",
  kloud_draft: "#8E24AA",
  kloud_na: "#AB47BC",
  krush: "#D81B60",
  kelly: "#C62828",
  hite: "#0D47A1",
  max: "#BF360C",
  ob: "#1A237E",
  crown: "#4E342E",
  sunhari: "#F48FB1",
  isul_ttokttok: "#80DEEA",
  multi: "#7B1FA2",
  "": "#888",
};

export const BRAND_LABELS: Record<string, string> = {
  jinro: "\uC9C4\uB85C",
  chamisul: "\uCC38\uC774\uC2AC",
  chum_churum: "\uCC98\uC74C\uCC98\uB7FC",
  saero: "\uC0C8\uB85C",
  goodday: "\uC88B\uC740\uB370\uC774",
  san: "\uC0B0 \uC18C\uC8FC",
  green: "\uADF8\uB9B0\uC18C\uC8FC",
  ipseju: "\uC78E\uC0C8\uC8FC",
  daesun: "\uB300\uC120",
  terra: "\uD14C\uB77C",
  terra_light: "\uD14C\uB77C \uB77C\uC774\uD2B8",
  cass: "\uCE74\uC2A4",
  cass_light: "\uCE74\uC2A4 \uB77C\uC774\uD2B8",
  kloud: "\uD074\uB77C\uC6B0\uB4DC",
  kloud_draft: "\uD074\uB77C\uC6B0\uB4DC \uC0DD\uB4DC\uB798\uD504\uD2B8",
  kloud_na: "\uD074\uB77C\uC6B0\uB4DC \uB17C\uC54C\uCF5C\uB9AD",
  krush: "\uD06C\uB7EC\uC2DC",
  kelly: "\uCF08\uB9AC",
  hite: "\uD558\uC774\uD2B8",
  max: "\uB9E5\uC2A4",
  ob: "OB\uB9E5\uC8FC",
  crown: "\uD06C\uB77C\uC6B4\uB9E5\uC8FC",
  sunhari: "\uC21C\uD558\uB9AC",
  isul_ttokttok: "\uC774\uC2AC\uD1A1\uD1A1",
  multi: "\uD1B5\uD569",
};

export const NODE_SHAPES: Record<string, string> = {
  brand: "diamond",
  product: "round-rectangle",
  ingredient: "hexagon",
  person: "ellipse",
  award: "star",
  market: "rectangle",
  event: "barrel",
  unknown: "ellipse",
  fol_predicate: "round-triangle",
  fol_rule: "vee",
  fol_conclusion: "pentagon",
};

export const FOL_COLORS: Record<string, string> = {
  fol_predicate: "#FF8A65",
  fol_rule: "#FFD54F",
  fol_conclusion: "#81C784",
};

export const TYPE_ICONS: Record<string, string> = {
  brand: "\u{1F3E2}",
  product: "\u{1F376}",
  ingredient: "\u{1F9EA}",
  person: "\u{1F464}",
  award: "\u{1F3C6}",
  market: "\u{1F4C8}",
  event: "\u{1F4C5}",
};
