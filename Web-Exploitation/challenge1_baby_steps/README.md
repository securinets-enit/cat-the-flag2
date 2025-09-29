# Challenge: Baby Steps — DevTools or Bust

## Category
Web-Exploitation (Easy)

## Story
You land on a cheeky page that swears there’s “nothing to see here.” The Zodiac likes to hide in plain sight. Maybe your browser knows more than it shows…

## Goal
Find the flag being quietly loaded by the page.

## Run (Docker)
```bash
# Build
docker build -t baby-steps .

# Run
docker run --rm -p 8080:80 baby-steps

# Open
# http://localhost:8080/
```

## Player Hint
Open your browser’s developer tools → Network tab.

## Flag
`SecurinetsENIT{B4BY_ST3PS!}`
