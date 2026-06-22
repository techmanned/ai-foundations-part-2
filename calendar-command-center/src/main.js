import './styles.css';

const eventKey = 'calendar-command-center-events';
const focusKey = 'calendar-command-center-focus';

const starterEvents = [
  {
    title: 'Morning planning',
    time: '08:45',
    type: 'Focus',
    notes: 'Pick the top three outcomes for today.'
  },
  {
    title: 'Product sync',
    time: '11:00',
    type: 'Meeting',
    notes: 'Review blockers and handoffs.'
  },
  {
    title: 'Deep work block',
    time: '14:00',
    type: 'Focus',
    notes: 'Protect this block from low-priority tasks.'
  }
];

const week = [
  ['Mon', 5],
  ['Tue', 3],
  ['Wed', 6],
  ['Thu', 4],
  ['Fri', 2]
];

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

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function renderEvents(events) {
  return events
    .sort((a, b) => a.time.localeCompare(b.time))
    .map(
      (event, index) => `
        <article class="agenda-item">
          <div class="time">${escapeHtml(event.time)}</div>
          <div>
            <div class="event-line">
              <h3>${escapeHtml(event.title)}</h3>
              <span>${escapeHtml(event.type)}</span>
            </div>
            <p>${escapeHtml(event.notes)}</p>
          </div>
          <button class="icon-button" type="button" data-delete="${index}" aria-label="Delete ${escapeHtml(event.title)}">x</button>
        </article>
      `
    )
    .join('');
}

function renderWeek() {
  return week
    .map(
      ([day, count]) => `
        <div class="day-load">
          <span>${day}</span>
          <div class="load-track" aria-hidden="true">
            <div style="height: ${count * 13}%"></div>
          </div>
          <strong>${count}</strong>
        </div>
      `
    )
    .join('');
}

function renderApp() {
  const events = readJson(eventKey, starterEvents);
  const focus = readJson(focusKey, {
    priority: 'Ship one polished calendar workflow',
    boundary: 'No meetings before 10:00',
    recovery: '20 minute walk after the final call'
  });

  document.querySelector('#app').innerHTML = `
    <video class="launch-video" autoplay muted loop playsinline poster="/rocket-poster.svg">
      <source src="/rocket-launch.webm" type="video/webm" />
    </video>
    <div class="video-scrim"></div>
    <main>
      <header class="hero">
        <p class="eyebrow">Mission control</p>
        <h1>Calendar Command Center</h1>
        <p class="hero-copy">
          Plan the day, protect focus blocks, and capture schedule changes from one local dashboard.
        </p>
      </header>

      <section class="metrics" aria-label="Calendar summary">
        <article>
          <span>Today</span>
          <strong>${events.length}</strong>
          <p>planned blocks</p>
        </article>
        <article>
          <span>Focus</span>
          <strong>${events.filter((event) => event.type === 'Focus').length}</strong>
          <p>protected sessions</p>
        </article>
        <article>
          <span>Load</span>
          <strong>68%</strong>
          <p>weekly capacity</p>
        </article>
      </section>

      <div class="command-grid">
        <section class="panel agenda-panel" aria-labelledby="agenda-title">
          <div class="panel-heading">
            <p class="eyebrow">Timeline</p>
            <h2 id="agenda-title">Today's Agenda</h2>
          </div>
          <div class="agenda-list">${renderEvents(events)}</div>
        </section>

        <section class="panel capture-panel" aria-labelledby="capture-title">
          <div class="panel-heading">
            <p class="eyebrow">Capture</p>
            <h2 id="capture-title">Add Calendar Block</h2>
          </div>
          <form id="event-form" class="event-form">
            <label>
              <span>Title</span>
              <input name="title" placeholder="Design review" required />
            </label>
            <div class="form-row">
              <label>
                <span>Time</span>
                <input name="time" type="time" required />
              </label>
              <label>
                <span>Type</span>
                <select name="type">
                  <option>Focus</option>
                  <option>Meeting</option>
                  <option>Admin</option>
                  <option>Personal</option>
                </select>
              </label>
            </div>
            <label>
              <span>Notes</span>
              <textarea name="notes" rows="4" placeholder="Outcome, prep, or follow-up"></textarea>
            </label>
            <button type="submit">Add block</button>
          </form>
        </section>

        <section class="panel focus-panel" aria-labelledby="focus-title">
          <div class="panel-heading">
            <p class="eyebrow">Priorities</p>
            <h2 id="focus-title">Focus Protocol</h2>
          </div>
          <form id="focus-form" class="focus-form">
            <label>
              <span>Primary outcome</span>
              <input name="priority" value="${escapeHtml(focus.priority)}" />
            </label>
            <label>
              <span>Scheduling boundary</span>
              <input name="boundary" value="${escapeHtml(focus.boundary)}" />
            </label>
            <label>
              <span>Recovery plan</span>
              <input name="recovery" value="${escapeHtml(focus.recovery)}" />
            </label>
          </form>
        </section>

        <section class="panel week-panel" aria-labelledby="week-title">
          <div class="panel-heading">
            <p class="eyebrow">Capacity</p>
            <h2 id="week-title">Week Load</h2>
          </div>
          <div class="week-chart">${renderWeek()}</div>
        </section>
      </div>
    </main>
  `;

  bindEvents();
}

function bindEvents() {
  const eventForm = document.querySelector('#event-form');
  const focusForm = document.querySelector('#focus-form');

  eventForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const form = new FormData(eventForm);
    const events = readJson(eventKey, starterEvents);
    events.push({
      title: form.get('title').trim(),
      time: form.get('time'),
      type: form.get('type'),
      notes: form.get('notes').trim() || 'No notes added.'
    });
    writeJson(eventKey, events);
    renderApp();
  });

  document.querySelectorAll('[data-delete]').forEach((button) => {
    button.addEventListener('click', () => {
      const events = readJson(eventKey, starterEvents);
      events.splice(Number(button.dataset.delete), 1);
      writeJson(eventKey, events);
      renderApp();
    });
  });

  focusForm.addEventListener('input', () => {
    const form = new FormData(focusForm);
    writeJson(focusKey, {
      priority: form.get('priority').trim(),
      boundary: form.get('boundary').trim(),
      recovery: form.get('recovery').trim()
    });
  });
}

renderApp();
