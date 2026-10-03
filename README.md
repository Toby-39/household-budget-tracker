A desktop expense-tracking application built with Python and Tkinter, designed to help users log and monitor household spending in real time.

Features
- Add expenses across 5 categories: Food, Transport, Entertainment, Utilities, Other
- Real-time running totals as expenses are added
- Input validation on 3 fields (category, amount, description) such as catches empty, non-numeric, and non-positive entries before they're saved
- Confirmation dialog before resetting all data, to prevent accidental loss
 What I Learned
Building this reinforced how much of good software is defensive validating input before it ever reaches the data layer, and confirming destructive actions before they happen. These are habits I now carry into how I think about testing.
