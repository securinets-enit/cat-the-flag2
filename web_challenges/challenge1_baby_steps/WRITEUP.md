# Baby Steps — Writeup

## Summary
The landing page is a decoy. The real clue is visible only in the browser’s Developer Tools. The page dynamically fetches `flag_1337.txt`, which contains the flag.

## Steps
1. Open the site (Docker instructions in README).
2. Open Developer Tools (F12 or Ctrl+Shift+I) → Network tab.
3. Reload the page.
4. Find the request `flag_1337.txt`.
5. Click it to view contents.

## Flag
`SecurinetsENIT{B4BY_ST3PS!}`
