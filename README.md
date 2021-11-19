# Order Display

An order display screen for Odoo. Displays unpicked orders, packed orders, incoming returns, and scheduled runs.

## How to use it

Any open pick orders scheduled between the beginning of the current year and today are  appear in the Pick list.

Any delivery order that is in the "Ready" or "Waiting" state (not "Waiting Another Operation") appear in the Deliveries list.

Any rental return scheduled between the beginning of the current year and today appear in the Returns list.

Any "Local Pickup" or "Local Delivery" activity scheduled on (respectively) a Receipt or Return will appear in the Runs list.

The application reloads every 30 seconds.

## Known bugs

- The application stops loading new orders after a few hours and must be totally reloaded.
- The date range applied to picks and returns is too wide.
- The Django private key is exposed and must be hidden.

## Future development

- Add a new order sound.
- Flag new orders for five minutes after it is confirmed and added.