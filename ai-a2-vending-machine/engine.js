// Port of vending_machine_DT.m (HW2). One shared stock count, running credit, change returned when the customer is done.
const COINS = { P:1, N:5, D:10, Q:25, F:50 };
const DRINKS = { T:{ name:"Tea", price:25 }, C:{ name:"Coffee", price:50 }, H:{ name:"Hot Chocolate", price:30 } };
function newMachine(){ return { M:0, stock:20, pending:null, log:[] }; }
function say(m, rule, text){ m.log.unshift({ rule, text }); }
function usd(c){ return "$" + (c / 100).toFixed(2); }
function recheck(m){
  const d = m.pending;
  if (!d) return;
  if (m.M >= DRINKS[d].price){
    m.M -= DRINKS[d].price; m.stock -= 1; m.pending = null;
    say(m, "Drink dispensary rule 1", `Dispensing ${DRINKS[d].name}. Credit left: ${usd(m.M)}`);
  } else {
    say(m, "Drink dispensary rule 2", "Not enough money. Insert more coins.");
  }
}
function insertCoins(m, chain){
  chain = chain.toUpperCase();
  if (!chain.length) return m;
  for (const c of chain){
    if (COINS[c] !== undefined){ m.M += COINS[c]; }
    else say(m, "Error rule", `"${c}" is not a recognized coin.`);
  }
  say(m, "Money Rule 1", `M = ${usd(m.M)}`);
  recheck(m);
  return m;
}
function selectDrink(m, d){
  d = d.toUpperCase();
  if (!DRINKS[d]){ say(m, "Error rule", "Not a valid drink letter."); return m; }
  if (m.stock <= 0){ say(m, "Error rule", "Out of stock. Refilling..."); m.stock = 20; }
  m.pending = d;
  recheck(m);
  return m;
}
function finish(m){
  m.pending = null;
  if (m.M > 0){ say(m, "Change rule", `Returning ${usd(m.M)} in change.`); m.M = 0; }
  else say(m, "Change rule", "No change to return.");
  return m;
}
if (typeof module !== "undefined") module.exports = { newMachine, insertCoins, selectDrink, finish, COINS, DRINKS };
