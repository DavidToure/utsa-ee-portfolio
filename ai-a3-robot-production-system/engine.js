// Port of roboToure.m (HW3): rule-based robot navigation with conflict resolution.
function runRobot(cfg){
  let x = cfg.x, y = cfg.y, dir = cfg.dir;
  const obstacles = cfg.obstacles, objX = cfg.objX, objY = cfg.objY;
  const order = ["n","w","s","e"];
  const tried = new Set();
  let count = 0;
  const rows = [];
  const isObs = (a, b) => obstacles.some(o => o[0] === a && o[1] === b);
  const maxCycles = cfg.maxCycles || 30;
  let reached = false;
  for (let cyc = 1; cyc <= maxCycles; cyc++){
    const wm = [`robot_at(${x},${y})`, `direction(${dir})`]
      .concat(order.map(o => `choice(${o})`))
      .concat(obstacles.slice().sort((p, q) => p[0] - q[0] || p[1] - q[1]).map(o => `obstacle_at(${o[0]},${o[1]})`))
      .concat([`object_at(${objX},${objY})`]).join(", ");
    let nx, ny, mRule, mName, aRule, aName;
    if (dir === "n"){ nx = x; ny = y + 1; mRule = 4; mName = "move_north"; aRule = 8; aName = "avoid_obstacle_north"; }
    else if (dir === "s"){ nx = x; ny = y - 1; mRule = 5; mName = "move_south"; aRule = 6; aName = "avoid_obstacle_south"; }
    else if (dir === "w"){ nx = x - 1; ny = y; mRule = 2; mName = "move_west"; aRule = 7; aName = "avoid_obstacle_west"; }
    else { nx = x + 1; ny = y; mRule = 3; mName = "move_east"; aRule = 9; aName = "avoid_obstacle_east"; }
    const onGoal = x === objX && y === objY;
    const blocked = isObs(nx, ny);
    const conf = [String(mRule)];
    if (onGoal) conf.push("1");
    if (blocked) order.forEach(o => conf.push(`${aRule} (ND=${o})`));
    const row = { cycle: cyc, x, y, dir, wm, conflicts: "{" + conf.join(", ") + "}" };
    if (onGoal){
      row.strategy = "Goal priority (rule 1 adopted convention)";
      row.fired = "1:detect_object"; row.kind = "goal"; rows.push(row); reached = true; break;
    } else if (blocked){
      const strat = ["Specificity"];
      const keys = order.map(o => `${aRule},${x},${y},${nx},${ny},${o}`);
      const untried = keys.map(k => !tried.has(k));
      let opts = order.slice(), optKeys = keys.slice();
      if (untried.some(Boolean)){
        if (!untried.every(Boolean)) strat.push("Refractoriness");
        opts = order.filter((_, i) => untried[i]);
        optKeys = keys.filter((_, i) => untried[i]);
      }
      let pick;
      if (opts.length > 1){ strat.push("Random"); pick = count % opts.length; count++; } else pick = 0;
      const newDir = opts[pick];
      tried.add(optKeys[pick]);
      dir = newDir;
      row.strategy = strat.join(", ");
      row.fired = `${aRule}:${aName}(ND=${newDir})`; row.kind = "turn";
      row.newDir = newDir;
    } else {
      row.strategy = "-";
      row.fired = `${mRule}:${mName}`; row.kind = "move";
      x = nx; y = ny;
    }
    row.after = { x, y, dir };
    rows.push(row);
  }
  return { rows, reached };
}
const ROBOT_DEFAULT = { x:9, y:7, dir:"n", obstacles:[[9,8],[9,1]], objX:3, objY:7 };
if (typeof module !== "undefined") module.exports = { runRobot, ROBOT_DEFAULT };
