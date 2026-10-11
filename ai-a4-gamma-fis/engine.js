// ---- Mamdani FIS engine (min AND, min implication, max aggregation, centroid) ----
function tri(x, a, b, c){
  if (x === b) return 1;
  if (x <= a || x >= c) return 0;
  return x < b ? (x - a) / (b - a) : (c - x) / (c - b);
}
function trap(x, a, b, c, d){
  if (x >= b && x <= c) return 1;
  if (x <= a || x >= d) return 0;
  return x < b ? (x - a) / (b - a) : (d - x) / (d - c);
}
function mf(def, x){
  return def[0] === "tri" ? tri(x, def[1], def[2], def[3]) : trap(x, def[1], def[2], def[3], def[4]);
}
const INPUTS = {
  NTOTAL: { range:[0,1024], note:"sum of normalized counts", terms:{
    Low:["trap",0,0,200,400], Medium:["tri",200,400,600], High:["trap",400,600,1024,1024] } },
  MAX8:   { range:[0,1], note:"peak of the last 800 bins", terms:{
    Low:["trap",0,0,0.3,0.6], Medium:["tri",0.3,0.6,0.9], High:["trap",0.6,0.9,1,1] } },
  BIN05:  { range:[0,1024], note:"bins below 0.5", terms:{
    Low:["trap",0,0,200,450], Medium:["tri",200,450,700], High:["trap",450,700,1024,1024] } },
  BIN08:  { range:[0,1024], note:"bins above 0.8", terms:{
    Low:["trap",0,0,90,180], Medium:["tri",90,180,270], High:["trap",180,270,1024,1024] } },
};
const OUTPUT = { range:[0,100], terms:{
  VeryLow:["tri",0,0,25], Low:["tri",0,25,50], Medium:["tri",25,50,75],
  High:["tri",50,75,100], VeryHigh:["tri",75,100,100] } };
const RULES = [
  [[["MAX8","High"],["BIN08","High"]],"VeryHigh"],
  [[["MAX8","High"],["NTOTAL","High"]],"VeryHigh"],
  [[["MAX8","High"],["BIN05","Low"]],"High"],
  [[["MAX8","High"],["BIN08","Medium"]],"High"],
  [[["MAX8","High"]],"High"],
  [[["MAX8","Medium"],["BIN08","High"]],"High"],
  [[["MAX8","Medium"],["NTOTAL","High"]],"High"],
  [[["MAX8","Medium"],["BIN05","Low"]],"High"],
  [[["MAX8","Medium"],["BIN08","Medium"]],"Medium"],
  [[["MAX8","Medium"],["BIN05","High"]],"Medium"],
  [[["MAX8","Medium"]],"Medium"],
  [[["MAX8","Low"],["BIN08","Medium"]],"Medium"],
  [[["MAX8","Low"],["NTOTAL","High"],["BIN05","Low"]],"Medium"],
  [[["MAX8","Low"],["BIN08","Low"],["BIN05","High"]],"VeryLow"],
  [[["MAX8","Low"],["NTOTAL","Low"],["BIN08","Low"]],"Low"],
  [[["MAX8","Low"]],"Low"],
];
function evaluate(v, n){
  n = n || 1001;
  const memberships = {};
  for (const k in INPUTS){
    memberships[k] = {};
    for (const t in INPUTS[k].terms) memberships[k][t] = mf(INPUTS[k].terms[t], v[k]);
  }
  const strengths = RULES.map(r => Math.min(...r[0].map(([k,t]) => memberships[k][t])));
  const ys = [], agg = [];
  let num = 0, den = 0;
  for (let i = 0; i < n; i++){
    const y = OUTPUT.range[0] + (OUTPUT.range[1] - OUTPUT.range[0]) * i / (n - 1);
    let m = 0;
    RULES.forEach((r, j) => {
      if (strengths[j] > 0) m = Math.max(m, Math.min(mf(OUTPUT.terms[r[1]], y), strengths[j]));
    });
    ys.push(y); agg.push(m); num += y * m; den += m;
  }
  const crisp = den === 0 ? 50 : num / den;
  return { memberships, strengths, ys, agg, crisp };
}
const SCENARIOS = [
  { name:"Scenario 1", v:{ NTOTAL:81.31843575418995, MAX8:0.6480446927374302, BIN05:965, BIN08:15 } },
  { name:"Scenario 2", v:{ NTOTAL:56.784140969163, MAX8:0.4581497797356828, BIN05:998, BIN08:4 } },
  { name:"Scenario 3", v:{ NTOTAL:36.12578616352202, MAX8:0.10062893081761007, BIN05:1005, BIN08:4 } },
  { name:"Scenario 4", v:{ NTOTAL:43.357142857142854, MAX8:0.023809523809523808, BIN05:990, BIN08:8 } },
  { name:"Scenario 5", v:{ NTOTAL:74.5031847133758, MAX8:0.5923566878980892, BIN05:965, BIN08:15 } },
];
if (typeof module !== "undefined") module.exports = { evaluate, SCENARIOS, INPUTS, OUTPUT, RULES };
