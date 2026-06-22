# Calendar Command Center

A client-only Vite app for planning a daily calendar from a command-center style dashboard. It includes a locally generated looping rocket launch video background and stores editable planning data in `localStorage`.

## Features

- Daily agenda with add and delete controls
- Focus protocol fields saved in the browser
- Weekly capacity chart
- Muted autoplay looping WebM background generated locally
- No external APIs, private calendar data, tokens, passwords, or paid services

## Install

```bash
npm install
```

## Run

```bash
npm run dev
```

## Build

```bash
npm run build
```

## GitHub

From the repository root:

```bash
git add calendar-command-center
git commit -m "Add Calendar Command Center app"
git push origin main
```

## Vercel

Deploy from this folder:

```bash
cd calendar-command-center
npx vercel --prod --yes
```

For Git-backed deploys, connect the Vercel project to the GitHub repository and set the project root directory to `calendar-command-center`.
