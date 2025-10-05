# Challenge: Baby Steps — Challenge Summary

## Overview
- **Category**: Web-Exploitation
- **Difficulty**: Easy
- **Points**: 100

## Description
A playful landing page teases the user. The real hint is only visible to those who open Developer Tools. The page loads a hidden resource that contains the flag.

## Player Files
- Served via Docker at `/` (index.html)

## Solution (Organizer)
- Open the site in a browser
- Open DevTools → Network tab
- Reload the page and locate a request to `flag_1337.txt`
- Open it to read the flag

## Flag
`SecurinetsENIT{B4BY_ST3PS!}`

## Build & Run (Docker)
```bash
# From this challenge directory
# Build image
docker build -t baby-steps .

# Run container on port 8080
docker run --rm -p 8080:80 --name baby-steps baby-steps

# Open in browser
# http://localhost:8080/
```

## Updating the Page
```bash
# Rebuild without cache to reflect changes
docker rm -f baby-steps 2>/dev/null || true
docker build --no-cache -t baby-steps .
docker run --rm -p 8080:80 --name baby-steps baby-steps
```

## Troubleshooting
- Changes not showing? Perform a hard refresh (Ctrl+Shift+R) in the browser.
- Confirm the container is running: `docker ps`.
- Check logs if needed: `docker logs baby-steps`.
