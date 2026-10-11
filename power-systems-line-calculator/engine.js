// Transmission line models: short, nominal pi, exact (hyperbolic). 3-phase, balanced, per-phase analysis.
const C = {
  add:(a,b)=>({re:a.re+b.re,im:a.im+b.im}), sub:(a,b)=>({re:a.re-b.re,im:a.im-b.im}),
  mul:(a,b)=>({re:a.re*b.re-a.im*b.im,im:a.re*b.im+a.im*b.re}),
  div:(a,b)=>{const d=b.re*b.re+b.im*b.im;return{re:(a.re*b.re+a.im*b.im)/d,im:(a.im*b.re-a.re*b.im)/d};},
  sc:(a,k)=>({re:a.re*k,im:a.im*k}), abs:a=>Math.hypot(a.re,a.im), arg:a=>Math.atan2(a.im,a.re),
  polar:(r,t)=>({re:r*Math.cos(t),im:r*Math.sin(t)}), conj:a=>({re:a.re,im:-a.im}),
  sqrt:a=>{const r=Math.hypot(a.re,a.im),t=Math.atan2(a.im,a.re);return C.polar(Math.sqrt(r),t/2);},
  cosh:a=>({re:Math.cosh(a.re)*Math.cos(a.im),im:Math.sinh(a.re)*Math.sin(a.im)}),
  sinh:a=>({re:Math.sinh(a.re)*Math.cos(a.im),im:Math.cosh(a.re)*Math.sin(a.im)}),
};
function abcd(model, p, len){
  const z = {re:p.r, im:p.x}, y = {re:0, im:p.b*1e-6};      // per km, b in microsiemens
  const Z = C.sc(z, len), Y = C.sc(y, len);
  if (model === "short") return { A:{re:1,im:0}, B:Z, C:{re:0,im:0}, D:{re:1,im:0} };
  if (model === "nominal"){
    const YZ = C.mul(Y, Z);
    const A = {re:1 + YZ.re/2, im:YZ.im/2};
    const Cc = C.mul(Y, {re:1 + YZ.re/4, im:YZ.im/4});
    return { A, B:Z, C:Cc, D:A };
  }
  const Zc = C.sqrt(C.div(z, y));
  const gl = C.sc(C.sqrt(C.mul(z, y)), len);
  const A = C.cosh(gl);
  return { A, B:C.mul(Zc, C.sinh(gl)), C:C.div(C.sinh(gl), Zc), D:A, Zc, gl };
}
function solve(model, p, len){
  const m = abcd(model, p, len);
  const VLL = p.kv * 1e3, VR = {re:VLL/Math.sqrt(3), im:0};
  const mag = p.mw * 1e6 / (Math.sqrt(3) * VLL * p.pf);
  const th = Math.acos(p.pf) * (p.lead ? 1 : -1);
  const IR = C.polar(mag, th);
  const VS = C.add(C.mul(m.A, VR), C.mul(m.B, IR));
  const IS = C.add(C.mul(m.C, VR), C.mul(m.D, IR));
  const SS = C.sc(C.mul(VS, C.conj(IS)), 3), SR = C.sc(C.mul(VR, C.conj(IR)), 3);
  const vrNL = C.abs(VS) / C.abs(m.A);
  return {
    m, VS, IS, IR,
    vsLL: C.abs(VS) * Math.sqrt(3) / 1e3, isA: C.abs(IS),
    vr: (vrNL - C.abs(VR)) / C.abs(VR) * 100,
    ps: SS.re / 1e6, loss: (SS.re - SR.re) / 1e6, eff: SR.re / SS.re * 100,
    delta: C.arg(VS) * 180 / Math.PI,
  };
}
const TL_DEFAULT = { r:0.08, x:0.48, b:3.33, kv:220, mw:250, pf:0.99, lead:false, len:200 };
if (typeof module !== "undefined") module.exports = { solve, abcd, TL_DEFAULT, C };
