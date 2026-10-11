# Rule-Based Vending Machine

**Origin:** EE 5663 Artificial Intelligence, Assignment 2. Design a rule-based system for a vending machine that sells tea, coffee, and hot chocolate, asks for coins before activating the buttons, and gives change.

## Files

- `vending_machine_DT.m`: the MATLAB function. Run `vending_machine_DT` and answer the prompts.
- `engine.js` and `demo.html`: the same rules in the browser. Open `demo.html` directly.

## The rules

1. **Money Rule 1.** A recognized coin is added to the balance M. Coins are P (1), N (5), D (10), Q (25), F (50) cents.
2. **Error rule.** An unrecognized coin or drink letter is reported. If the shared stock is empty, it is refilled.
3. **Drink dispensary rule 1.** If M is at least the price, dispense and subtract the price. The rest stays as credit.
4. **Drink dispensary rule 2.** If M is less than the price, ask for more coins and check the same drink again.
5. **Change rule.** When the customer is finished, return M as change and reset it.

Prices: tea 25, coffee 50, hot chocolate 30 cents. One shared stock of 20 covers all three drinks.
