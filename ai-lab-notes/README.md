# AI Lab Notes

A beginner-friendly Vite web app for practicing setup steps, Linux/Git commands, and fictional AI lab notes. The app runs fully in the browser and saves notes with `localStorage`.

## What is included

- Setup checklist with saved checkbox progress
- Linux, Git, and Vite command cheat sheet
- Fictional lab notes form saved locally in the browser
- No external APIs, passwords, tokens, private data, or paid services

## Install

```bash
npm install
```

## Run locally

```bash
npm run dev
```

Open the local URL printed by Vite, usually `http://localhost:5173`.

## Build

```bash
npm run build
```

The production files are created in `dist/`.

## Preview the build

```bash
npm run preview
```

## GitHub steps

From inside the `ai-lab-notes` folder:

```bash
git status
git add .
git commit -m "Add AI Lab Notes Vite app"
git branch -M main
git remote add origin git@github.com:YOUR-USERNAME/ai-lab-notes.git
git push -u origin main
```

If the `origin` remote already exists, check it with:

```bash
git remote -v
```

Update it if needed:

```bash
git remote set-url origin git@github.com:YOUR-USERNAME/ai-lab-notes.git
```

## Vercel deployment steps

1. Push the project to GitHub.
2. Sign in to Vercel.
3. Choose **Add New Project**.
4. Import the `ai-lab-notes` GitHub repository.
5. Keep the framework preset as **Vite**.
6. Use `npm run build` as the build command.
7. Use `dist` as the output directory.
8. Deploy.

This app does not need environment variables because it does not use external services.
