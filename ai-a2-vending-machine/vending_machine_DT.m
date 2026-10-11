% HW 2 - David Toure 
% EE 5663 - Artificial Intelligence    
% Design a Rule based system for operating a vending machine.
% The vending machine is able to provide tea, coffee and hot chocolate
% when the appropriate button is pushed. 
% The vending machine asks for coins before activating the buttons, 
% and also is able to provide change

function vending_machine_DT()
% constants
coins  = containers.Map({'P','N','D','Q','F'}, {1,5,10,25,50});   % coin letter, value in CENTS (integers)
names  = containers.Map({'T','C','H'}, {'Tea','Coffee','Hot Chocolate'});  % drink letter, corresponding name
prices = containers.Map({'T','C','H'}, {25,50,30});   % drink letter, price in cents
stock  = 20;   % ONE shared count across all three drinks 

M_cents = 0;       % running balance (M)
running = true;    % keeps serving new customers until they say no

while running
    % ready to serve
    fprintf('\nHello, we make the best drinks, would you like some?\n');
    fprintf('T (Tea, $0.25), C (Coffee, $0.50), or H (Hot Chocolate, $0.30)\n');

    % coin insertion (Money Rule) 
    chain = upper(input('Insert coins as a letter chain (P($0.01) N($0.05) D($0.10) Q($0.25) F($0.50)): ', 's'));  % "QQD" = quarter, quarter, dime
    for i = 1:length(chain)
        c = chain(i);   % one coin letter at a time
        if isKey(coins, c)   % Money Rule 1: recognized coin, add to M
            M_cents = M_cents + coins(c);
        else
            fprintf('"%s" is not a recognized coin.\n', c);  % Error rule: unrecognized letter
        end
    end
    fprintf('M = $%.2f\n', M_cents/100);   % display balance in dollars

    % --- selection loop ---
    done = false;   % becomes true when the customer is finished ordering
    while ~done
        drink = upper(input('Select a drink (T/C/H): ', 's'));

        if ~isKey(names, drink)
            fprintf('Not a valid drink letter.\n');  % Error rule: re-prompt for a new selection
            continue;   % repeat the loop back to "Select a drink" above
        end

        if stock <= 0
            fprintf('Out of stock. Refilling...\n');  % Error rule: shared stock is empty, refill and continue
            stock = 20;
        end

        % keep re-checking THIS drink until it's paid for. 
        % This loop allows the system to recognized when a purchase
        % was correctly made or requires more Money from the customer.
        purchased = false;
        while ~purchased
            if M_cents >= prices(drink)   % Drink dispensary rule 1: enough balance
                M_cents = M_cents - prices(drink);   % Change rule: subtract price, M carries over as credit (no reset)
                stock = stock - 1;   % decrease the shared stock count
                fprintf('Dispensing %s. Credit left: $%.2f\n', names(drink), M_cents/100);
                purchased = true;   % exits this inner loop
            else
                fprintf('Not enough money. Insert more coins.\n');  % Drink dispensary rule 2: insufficient balance
                more = upper(input('Coins: ', 's'));
                for i = 1:length(more)
                    c = more(i);
                    if isKey(coins, c)
                        M_cents = M_cents + coins(c);   % same Money Rule logic as the main insertion above
                    end
                end
                % loop repeats: re-checks the same drink, no re-prompt for the letter
            end
        end

        again = input('Something else? (Y/N): ', 's');
        done = ~strcmpi(again, 'Y');   % 'Y' keeps ordering
    end

    % change rule 
    if M_cents > 0
        fprintf('Returning $%.2f in change.\n', M_cents/100);  % Change rule: only return change once the customer is done
        M_cents = 0;   % reset for the next customer
    end

    cont = input('Another customer? (Y/N): ', 's');
    running = strcmpi(cont, 'Y');   % 'Y' loops the whole machine again to serve a new customer
end
end
