const app = document.querySelector('#app');

const projects = [
  {title:'Building with AI Agents', meta:'00:42 · Edited today'},
  {title:'On-device AI explained', meta:'01:18 · Yesterday'},
  {title:'Mumbai Tech Walk', meta:'00:31 · 3 days ago'}
];

function shell(content, active='home'){
  return `<div class="app">${content}
    <nav class="nav">
      <button class="${active==='home'?'active':''}" onclick="go('home')">⌂<br>Home</button>
      <button class="${active==='insights'?'active':''}" onclick="go('insights')">◒<br>Insights</button>
      <button class="ai-nav" onclick="go('create')">✦<br>Create</button>
      <button class="${active==='profile'?'active':''}" onclick="go('profile')">●<br>Profile</button>
    </nav>
  </div>`;
}

function home(){
 return shell(`<main class="screen">
   <div class="top"><button class="icon">☰</button><div class="avatar">H</div></div>
   <div class="kicker">Creator AI</div>
   <h1>Good evening,<br>Harsh.</h1>
   <section class="hero media-bg" style="background-image:url('assets/home-hero.jpg')">
     <div>
       <span class="badge">✦ Inspiration for you</span>
       <h2>Turn what you know into something people want to watch.</h2>
       <div class="muted">AI-curated ideas based on your creator profile.</div>
     </div>
   </section>
   <div class="ai-bar"><span>✦</span><input id="quickPrompt" placeholder="What do you want to create?"><button class="ai-send" onclick="openCopilot()">↑</button></div>
   <section class="section">
     <div class="row"><h2>My Projects</h2><span class="muted">See all</span></div>
     <div class="projects">${projects.map((p,i)=>`<article class="project media-bg" style="background-image:url('assets/${['create-edit-video','trend-on-device-ai','create-from-idea'][i]}.jpg')" onclick="go('editor')"><div class="project-content"><div class="project-title">${p.title}</div><div class="project-meta">${p.meta}</div></div></article>`).join('')}</div>
   </section>
   <button class="cta" onclick="go('create')">+ New Project</button>
 </main>`,'home');
}

function insights(){
 return shell(`<main class="screen">
   <div class="top"><div><div class="kicker">Creator Intelligence</div><h1>Know what to<br>create next.</h1></div><button class="icon">⋯</button></div>
   <div class="metric-grid">
     <div class="metric"><span class="muted">Views</span><strong>24.3K</strong><span class="chip ai">+18%</span></div>
     <div class="metric"><span class="muted">Engagement</span><strong>8.4%</strong><span class="chip ai">+2.1%</span></div>
     <div class="metric"><span class="muted">Watch time</span><strong>41m</strong><span class="chip">This week</span></div>
     <div class="metric"><span class="muted">Growth</span><strong>+12%</strong><span class="chip ai">Healthy</span></div>
   </div>
   <section class="section"><div class="row"><h2>Trending in your niche</h2><span class="muted">Live</span></div>
     <div class="cards">
       <article class="card trend media-bg" style="background-image:url('assets/trend-ai-agents.jpg')"><div class="trend-icon">↗</div><div><h3>AI coding agents</h3><p>Rising across developer and AI communities. Strong relevance to your audience.</p><span class="chip ai">High relevance</span><span class="chip">YouTube</span><span class="chip">X</span></div></article>
       <article class="card trend media-bg" style="background-image:url('assets/trend-on-device-ai.jpg')"><div class="trend-icon">◉</div><div><h3>On-device AI</h3><p>Growing interest in local models, private inference and AI phones.</p><span class="chip ai">Very relevant</span></div></article>
     </div>
   </section>
   <section class="section"><div class="row"><h2>Creation opportunity</h2></div>
     <div class="card"><div class="kicker">Recommended for your profile</div><h2 style="margin-top:8px">“Can a phone run a useful AI agent?”</h2><p>Your technology content and on-device AI topics are closely aligned.</p><button class="cta" onclick="go('editor')">Create video ✦</button></div>
   </section>
   <section class="section"><div class="row"><h2>World trends</h2></div>
     <div class="tag-list"><span class="chip">AI agents</span><span class="chip">Creator economy</span><span class="chip">VLMs</span><span class="chip">Robotics</span><span class="chip">Local AI</span></div>
   </section>
 </main>`,'insights');
}

function create(){
 return shell(`<main class="screen">
   <div class="top"><button class="icon" onclick="go('home')">‹</button><div class="kicker">Create</div><div></div></div>
   <h1>What are you<br>making?</h1><p>Start from footage, an idea, or an interactive experience.</p>
   <div class="create-grid">
     <article class="create-card media-bg" style="background-image:url('assets/create-edit-video.jpg')" onclick="go('editor')"><div class="emoji">🎬</div><span class="arrow">→</span><h3>Edit a Video</h3><p>Import footage and let AI understand, cut and reframe it.</p></article>
     <article class="create-card media-bg" style="background-image:url('assets/create-from-idea.jpg')" onclick="go('editor')"><div class="emoji">✦</div><span class="arrow">→</span><h3>Create from an Idea</h3><p>Idea → script → teleprompter → record → edit.</p></article>
     <article class="create-card media-bg" style="background-image:url('assets/create-game-studio.jpg')"><div class="emoji">🎮</div><span class="arrow">→</span><h3>Game Studio</h3><p>Create camera-powered interactive experiences.</p></article>
     <article class="create-card media-bg" style="background-image:url('assets/create-effects-studio.jpg')"><div class="emoji">✨</div><span class="arrow">→</span><h3>Effects Studio</h3><p>Explore effects, assets and camera interactions.</p></article>
   </div>
 </main>`,'create');
}

function editor(){
 return shell(`<main class="editor">
   <div class="top" style="padding:14px 6px 0"><button class="icon" onclick="go('home')">‹</button><div style="font-weight:600">Building with AI Agents</div><button class="icon">✓</button></div>
   <div class="video media-bg" style="background-image:url('assets/create-edit-video.jpg')"><button class="play" onclick="this.innerHTML='❚❚'">▶</button></div>
   <div class="row" style="margin-top:12px"><span class="muted">00:06 / 00:42</span><span class="muted">9:16</span></div>
   <div class="timeline"><div class="track"><div class="track-video"></div></div><div class="track"><div class="track-audio"></div></div></div>
   <div class="tools"><button>✂<br>Cut</button><button>♫<br>Audio</button><button>T<br>Text</button><button>✦<br>FX</button><button>◫<br>Crop</button></div>
   <div class="copilot"><div class="copilot-head">✦ Ask Copilot</div><p style="margin:8px 0 0">Tell me what you want to change. I can understand your footage and propose edits.</p><button class="cta" onclick="openCopilot()">Open Copilot</button></div>
 </main>`,'');
}

function profile(){
 return shell(`<main class="screen">
   <div class="top"><div class="kicker">Profile</div><button class="icon">⚙</button></div>
   <div class="profile-cover media-bg" style="background-image:url('assets/creator-setup.jpg')"><span class="badge">Creator DNA · Ready</span></div>
   <div class="profile-main"><div class="big-avatar media-bg" style="background-image:url('assets/creator-avatar.jpg');background-size:cover;color:transparent">H</div><div><h2 style="margin:0">Harsh Jain</h2><span class="muted">Technology · AI · Software</span></div></div>
   <section class="section"><h2>Creator DNA</h2><div class="card"><div class="kicker">Voice</div><p>Technical, conversational, concrete. Prefers strong hooks and minimal fluff.</p><div class="tag-list"><span class="chip ai">AI</span><span class="chip">Software</span><span class="chip">Developer tools</span></div></div></section>
   <section class="section"><h2>Hook patterns</h2><div class="cards"><div class="card">Start with a surprising claim</div><div class="card">Show the result first</div><div class="card">Use a question to open</div></div></section>
   <section class="section"><h2>Connected sources</h2><div class="card">YouTube · LinkedIn · X · Substack</div></section>
 </main>`,'profile');
}

function onboarding(){
 app.innerHTML = `<main class="screen media-bg" style="min-height:100vh;display:flex;flex-direction:column;justify-content:space-between;background-image:url('assets/creator-setup.jpg');background-size:cover;background-position:center;background-blend-mode:soft-light">
   <div><div class="top"><div class="kicker">Creator AI</div><span class="muted">1 / 4</span></div><h1>Let's learn<br>how you create.</h1><p>Your profile helps Copilot make ideas and edits that actually sound like you.</p>
   <div class="cards section">
    <div class="card"><h2>Your niche</h2><div class="tag-list"><span class="chip ai">Technology</span><span class="chip">AI</span><span class="chip">Software</span><span class="chip">Creator tools</span></div></div>
    <div class="card"><h2>Your platforms</h2><div class="tag-list"><span class="chip ai">YouTube</span><span class="chip">Instagram</span><span class="chip">LinkedIn</span></div></div>
    <div class="card"><h2>Existing content</h2><p>Connect channels or upload a few examples so Creator AI can learn your style.</p><button class="cta">Connect content</button></div>
   </div></div>
   <button class="cta" onclick="go('home')">Build my Creator DNA ✦</button>
 </main>`;
}

function openCopilot(){
 const el=document.createElement('div'); el.className='sheet'; el.id='copilotSheet';
 el.innerHTML=`<div class="sheet-inner">
   <div class="row"><div><div class="copilot-head">✦ Copilot</div><div class="muted" style="margin-top:5px">Understands this project</div></div><button class="icon" onclick="closeCopilot()">×</button></div>
   <textarea id="prompt" placeholder="e.g. Make this a 30 second Instagram reel"></textarea>
   <button class="cta" onclick="generateEdit()">Generate ✦</button>
   <div id="result"></div>
 </div>`;
 document.body.appendChild(el);
}
function closeCopilot(){document.getElementById('copilotSheet')?.remove()}
function generateEdit(){
 document.getElementById('result').innerHTML=`<div class="suggestion"><strong>I'll turn this into a social-ready Reel.</strong><br><br>✓ Find strongest moments<br>✓ Remove silence + filler words<br>✓ Reframe to 9:16<br>✓ Add dynamic captions<br>✓ Add subtle zooms<div class="progress"><i></i></div></div><div class="actions"><button onclick="alert('Preview rendered')">Preview</button><button class="primary" onclick="closeCopilot();alert('Edit applied to demo timeline')">Apply</button></div>`;
}
function go(page){
 location.hash=page;
 render();
 window.scrollTo(0,0);
}
function render(){
 const page=location.hash.slice(1)||'home';
 if(page==='home') app.innerHTML=home();
 else if(page==='insights') app.innerHTML=insights();
 else if(page==='create') app.innerHTML=create();
 else if(page==='editor') app.innerHTML=editor();
 else if(page==='profile') app.innerHTML=profile();
 else if(page==='onboarding') onboarding();
}
window.addEventListener('hashchange',render);
render();
