% HW 3 - David Toure
% EE 5663 - Artificial Intelligence
% In lecture 4 (slides 11-18) the movement of a robot
% within an area of obstacles and objects was discussed.
% Please create the same table for a different path.
% PROVIDE THE TABLE WITH CYCLES as in the example in class.
function roboToure()
clc;
% -- scenario --
x = 9; y = 7;             % robot_at(9,7)
dir = 'n';                 % oriented (north)
obstacles = [9 8; 9 1];    % obstacle at position (9,8) and (9,1)
objX = 3; objY = 7;        % object_at(3,7)
order = {'n','w','s','e'}; % order used for the deterministic "random" pick
tried = {};                 % (rule + cell + direction) combos already fired
count = 0;                  % how many random picks we've made so far initialized
rows = struct('Cycle', {}, 'WM', {}, 'Conflicts', {}, 'Strategy', {}, 'Fired', {});
for cyc = 1:30
    wm = wmString(x, y, dir, obstacles, objX, objY, order);
% which move/avoid rule goes with the direction we're facing
switch dir
case 'n', nx = x;   ny = y+1; mRule = 4; mName = 'move_north'; aRule = 8; aName = 'avoid_obstacle_north';
case 's', nx = x;   ny = y-1; mRule = 5; mName = 'move_south'; aRule = 6; aName = 'avoid_obstacle_south';
case 'w', nx = x-1; ny = y;   mRule = 2; mName = 'move_west';  aRule = 7; aName = 'avoid_obstacle_west';
case 'e', nx = x+1; ny = y;   mRule = 3; mName = 'move_east';  aRule = 9; aName = 'avoid_obstacle_east';
end
    onGoal = (x == objX) && (y == objY);
    blocked = ismember([nx ny], obstacles, 'rows');
% conflict set for the table: move rule, plus rule 1 if on the goal,
% plus all 4 ND versions of the avoid rule if blocked
    conf = {sprintf('%d', mRule)};
if onGoal
        conf{end+1} = '1';
end
if blocked
for k = 1:4
            conf{end+1} = sprintf('%d (ND=%s)', aRule, order{k});
end
end
    confStr = ['{' strjoin(conf, ', ') '}'];
if onGoal
% rule 1 wins immediately once it's triggered
        strat = 'Goal priority (rule 1 adopted convention)';
        fired = '1:detect_object';
        done = true;
elseif blocked
% avoid rule already wins specificity, so the real choice is
% just which of the 4 directions to turn to
        strat = {'Specificity'};
        keys = cell(1,4);
for k = 1:4
            keys{k} = sprintf('%d,%d,%d,%d,%d,%s', aRule, x, y, nx, ny, order{k});
end
        untried = ~ismember(keys, tried);
        opts = order;
        optKeys = keys;
if any(untried)
if ~all(untried)
                strat{end+1} = 'Refractoriness';
end
            opts = order(untried);
            optKeys = keys(untried);
end
% if we've somehow tried all 4 already just keep the full set
if numel(opts) > 1
            strat{end+1} = 'Random';
            pick = mod(count, numel(opts)) + 1;
            count = count + 1;
else
            pick = 1;
end
        newDir = opts{pick};
        tried{end+1} = optKeys{pick};
        dir = newDir;
        strat = strjoin(strat, ', ');
        fired = sprintf('%d:%s(ND=%s)', aRule, aName, newDir);
        done = false;
else
% only the move rule matched, nothing to resolve
        strat = '-';
        fired = sprintf('%d:%s', mRule, mName);
        x = nx; y = ny;
        done = false;
end
    rows(cyc) = struct('Cycle', cyc, 'WM', {wm}, 'Conflicts', {confStr}, 'Strategy', {strat}, 'Fired', {fired});
if done
break;
end
end
% print the table
fprintf('\n%-6s %-46s %-44s %s\n', 'Cycle', 'Conflicts', 'Strategy', 'Fired Rule');
fprintf('%s\n', repmat('-', 1, 130));
for i = 1:numel(rows)
    fprintf('%-6d %-46s %-44s %s\n', rows(i).Cycle, rows(i).Conflicts, rows(i).Strategy, rows(i).Fired);
    fprintf('       WM: %s\n\n', rows(i).WM);
end
end
function s = wmString(x, y, dir, obstacles, objX, objY, order)
    parts = {sprintf('robot_at(%d,%d)', x, y), sprintf('direction(%s)', dir)};
for i = 1:numel(order)
        parts{end+1} = sprintf('choice(%s)', order{i}); 
end
    obs = sortrows(obstacles);
for i = 1:size(obs,1)
        parts{end+1} = sprintf('obstacle_at(%d,%d)', obs(i,1), obs(i,2)); 
end
    parts{end+1} = sprintf('object_at(%d,%d)', objX, objY);
    s = strjoin(parts, ', ');
end
