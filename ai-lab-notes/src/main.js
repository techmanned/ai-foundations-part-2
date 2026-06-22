import './styles.css';

const checklistItems = [
  'Install Node.js and npm',
  'Create a Vite project folder',
  'Run npm install',
  'Start the dev server with npm run dev',
  'Open the local URL in a browser',
  'Make a first Git commit',
  'Push the project to GitHub',
  'Deploy the app on Vercel'
];

const commands = [
  {
    group: 'Linux basics',
    items: [
      ['pwd', 'Show the current folder'],
      ['ls', 'List files and folders'],
      ['cd ai-lab-notes', 'Move into the project folder'],
      ['mkdir notes', 'Create a new folder'],
      ['touch README.md', 'Create an empty file']
    ]
  },
  {
    group: 'Git workflow',
    items: [
      ['git status', 'Check changed files'],
      ['git add .', 'Stage all project changes'],
      ['git commit -m "Add AI Lab Notes app"', 'Save a snapshot'],
      ['git branch -M main', 'Rename the branch to main'],
      ['git push -u origin main', 'Push the branch to GitHub']
    ]
  },
  {
    group: 'Vite commands',
    items: [
      ['npm install', 'Install project dependencies'],
      ['npm run dev', 'Start local development'],
      ['npm run build', 'Create a production build'],
      ['npm run preview', 'Preview the production build locally']
    ]
  }
];

const checklistKey = 'ai-lab-notes-checklist';
const noteKey = 'ai-lab-notes-entry';

const defaultNote = {
  title: '',
  date: new Date().toISOString().slice(0, 10),
  model: '',
  prompt: '',
  observation: '',
  nextStep: ''
};

function readJson(key, fallback) {
  try {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : fallback;
  } catch {
    return fallback;
  }
}

function writeJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function renderChecklist() {
  const saved = readJson(checklistKey, {});

  return `
    <section class="panel checklist-panel" aria-labelledby="setup-title">
      <div class="section-heading">
        <p class="eyebrow">Setup</p>
        <h2 id="setup-title">Project Checklist</h2>
      </div>
      <div class="checklist">
        ${checklistItems
          .map((item, index) => {
            const id = `step-${index}`;
            const checked = saved[id] ? 'checked' : '';
            return `
              <label class="check-item" for="${id}">
                <input id="${id}" type="checkbox" data-check-id="${id}" ${checked} />
                <span>${item}</span>
              </label>
            `;
          })
          .join('')}
      </div>
    </section>
  `;
}

function renderCommands() {
  return `
    <section class="panel command-panel" aria-labelledby="commands-title">
      <div class="section-heading">
        <p class="eyebrow">Reference</p>
        <h2 id="commands-title">Linux and Git Cheat Sheet</h2>
      </div>
      <div class="command-groups">
        ${commands
          .map(
            (group) => `
              <article class="command-group">
                <h3>${group.group}</h3>
                <dl>
                  ${group.items
                    .map(
                      ([command, description]) => `
                        <div>
                          <dt><code>${command}</code></dt>
                          <dd>${description}</dd>
                        </div>
                      `
                    )
                    .join('')}
                </dl>
              </article>
            `
          )
          .join('')}
      </div>
    </section>
  `;
}

function renderForm() {
  const note = readJson(noteKey, defaultNote);

  return `
    <section class="panel notes-panel" aria-labelledby="notes-title">
      <div class="section-heading">
        <p class="eyebrow">Local notes</p>
        <h2 id="notes-title">Fictional Lab Entry</h2>
      </div>
      <form id="lab-form" class="lab-form">
        <label>
          <span>Experiment title</span>
          <input name="title" value="${escapeHtml(note.title)}" placeholder="Example: Prompt clarity test" />
        </label>
        <div class="form-row">
          <label>
            <span>Date</span>
            <input name="date" type="date" value="${escapeHtml(note.date)}" />
          </label>
          <label>
            <span>Fictional model name</span>
            <input name="model" value="${escapeHtml(note.model)}" placeholder="Example: LabBot Mini" />
          </label>
        </div>
        <label>
          <span>Test prompt</span>
          <textarea name="prompt" rows="4" placeholder="Write a practice prompt. Do not include private data.">${escapeHtml(note.prompt)}</textarea>
        </label>
        <label>
          <span>Observation</span>
          <textarea name="observation" rows="4" placeholder="What did the fictional system do well or poorly?">${escapeHtml(note.observation)}</textarea>
        </label>
        <label>
          <span>Next step</span>
          <textarea name="nextStep" rows="3" placeholder="What would you try next?">${escapeHtml(note.nextStep)}</textarea>
        </label>
        <div class="form-actions">
          <button type="submit">Save note</button>
          <button type="button" class="secondary" id="clear-note">Clear note</button>
        </div>
        <p id="save-status" class="save-status" role="status" aria-live="polite">Saved notes stay in this browser only.</p>
      </form>
    </section>
  `;
}

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function getFormData(form) {
  const data = new FormData(form);
  return {
    title: data.get('title')?.trim() ?? '',
    date: data.get('date') ?? '',
    model: data.get('model')?.trim() ?? '',
    prompt: data.get('prompt')?.trim() ?? '',
    observation: data.get('observation')?.trim() ?? '',
    nextStep: data.get('nextStep')?.trim() ?? ''
  };
}

function bindEvents() {
  document.querySelectorAll('[data-check-id]').forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
      const saved = readJson(checklistKey, {});
      saved[checkbox.dataset.checkId] = checkbox.checked;
      writeJson(checklistKey, saved);
    });
  });

  const form = document.querySelector('#lab-form');
  const status = document.querySelector('#save-status');

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    writeJson(noteKey, getFormData(form));
    status.textContent = 'Note saved to localStorage.';
  });

  form.addEventListener('input', () => {
    writeJson(noteKey, getFormData(form));
    status.textContent = 'Draft saved locally.';
  });

  document.querySelector('#clear-note').addEventListener('click', () => {
    localStorage.removeItem(noteKey);
    form.reset();
    form.elements.date.value = defaultNote.date;
    status.textContent = 'Note cleared from this browser.';
  });
}

function renderApp() {
  document.querySelector('#app').innerHTML = `
    <main>
      <header class="app-header">
        <div>
          <p class="eyebrow">Beginner Vite project</p>
          <h1>AI Lab Notes</h1>
        </div>
        <p>
          Practice setup steps, keep common commands nearby, and write fictional
          AI experiment notes without sending anything to a server.
        </p>
      </header>
      <div class="dashboard">
        ${renderChecklist()}
        ${renderCommands()}
        ${renderForm()}
      </div>
    </main>
  `;

  bindEvents();
}

renderApp();
