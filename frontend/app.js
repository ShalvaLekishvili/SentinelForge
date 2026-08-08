const $ = (id) => document.getElementById(id);
const state = { file: null, result: null, filter: "all", ruleCount: 0 };

const escapeHtml = (value) => String(value ?? "").replace(/[&<>'"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c]));
const basename = (value) => String(value || "").split(/[\\/]/).pop();

function toast(message){
  const el = $("toast"); el.textContent = message; el.classList.add("show");
  clearTimeout(window.__sfToast); window.__sfToast = setTimeout(()=>el.classList.remove("show"), 2200);
}

async function apiStatus(){
  try{
    const res = await fetch("/api/health"); const data = await res.json();
    $("apiState").textContent = "API operational"; $("versionLabel").textContent = data.version; state.ruleCount = data.rules;
    $("ruleCount").textContent = `${data.rules} active detection rules`;
  }catch{ $("apiState").textContent = "API unavailable"; }
}

function setFile(file){
  state.file = file; $("analyzeBtn").disabled = !file;
  $("dropTitle").textContent = file ? file.name : "Choose or drop telemetry";
  $("dropSubtitle").textContent = file ? `${(file.size/1024).toFixed(1)} KB · ready for analysis` : "No file selected";
}

$("fileInput").addEventListener("change", e => setFile(e.target.files[0] || null));
const drop = $("dropZone");
["dragenter","dragover"].forEach(name=>drop.addEventListener(name,e=>{e.preventDefault();drop.classList.add("dragging")}));
["dragleave","drop"].forEach(name=>drop.addEventListener(name,e=>{e.preventDefault();drop.classList.remove("dragging")}));
drop.addEventListener("drop", e=>{const file=e.dataTransfer.files[0]; if(file) setFile(file)});

$("loadDemo").addEventListener("click", async()=>{
  const res = await fetch("/static/sample-incident.json"); const blob = await res.blob();
  setFile(new File([blob], "sentinelforge-demo-incident.json", {type:"application/json"}));
  toast("Synthetic investigation loaded");
});

$("analyzeBtn").addEventListener("click", analyze);
async function analyze(){
  if(!state.file) return;
  const btn=$("analyzeBtn"); btn.disabled=true; btn.innerHTML="Analyzing…";
  try{
    const form=new FormData(); form.append("file",state.file);
    const res=await fetch("/api/analyze",{method:"POST",body:form});
    const data=await res.json();
    if(!res.ok) throw new Error(data.detail || "Analysis failed");
    state.result=data; $("exportBtn").disabled=false; render(data); toast(`Analysis complete · ${data.detection_count} detections`);
  }catch(err){toast(err.message)}finally{btn.disabled=false;btn.innerHTML="Run analysis <span>→</span>"}
}

function render(data){
  $("eventCount").textContent=data.event_count; $("parserName").textContent=`${data.parser} parser · ${data.source}`;
  $("detectionCount").textContent=data.detection_count;
  const c=data.risk.counts||{}; $("criticalCount").textContent=`${c.critical||0} critical / ${c.high||0} high`;
  $("riskScore").textContent=data.risk.score; $("riskLevel").textContent=`${data.risk.level} · ${data.risk.model}`;
  $("riskScore").className=`risk-${String(data.risk.level).toLowerCase()}`;
  $("techniqueCount").textContent=data.mitre_coverage.length;
  renderDetections(); renderAttack(data.mitre_coverage); renderIocs(data.iocs); renderTimeline(data.timeline); renderProcesses(data.process_tree);
}

function renderDetections(){
  if(!state.result) return;
  const rows=state.result.detections.filter(d=>state.filter==="all"||d.severity===state.filter);
  $("detectionRows").innerHTML=rows.length?rows.map(d=>`<tr>
    <td><span class="severity ${escapeHtml(d.severity)}">${escapeHtml(d.severity)}</span></td>
    <td><strong>${escapeHtml(d.title)}</strong><small>${escapeHtml(d.description || d.evidence.join(" · "))}</small></td>
    <td><strong>${escapeHtml(d.host || "Unknown host")}</strong><small>${escapeHtml(basename(d.process) || d.command_line || "No process")}</small></td>
    <td>${d.mitre.map(t=>`<span class="technique">${escapeHtml(t)}</span>`).join("")||"—"}</td>
    <td>${escapeHtml(d.confidence)}</td>
  </tr>`).join(""):`<tr><td colspan="5" class="empty-cell">No ${escapeHtml(state.filter)} detections in this investigation.</td></tr>`;
}

$("severityFilters").addEventListener("click", e=>{
  const btn=e.target.closest("button[data-severity]"); if(!btn)return;
  state.filter=btn.dataset.severity; document.querySelectorAll(".filter").forEach(b=>b.classList.toggle("active",b===btn)); renderDetections();
});

function renderAttack(items){
  if(!items.length){$("attackCoverage").className="attack-list empty-block";$("attackCoverage").textContent="No mapped techniques yet.";return}
  const max=Math.max(...items.map(i=>i.hits)); $("attackCoverage").className="attack-list";
  $("attackCoverage").innerHTML=items.map(i=>`<div class="attack-row"><div class="attack-top"><strong>${escapeHtml(i.technique)}</strong><span>${i.hits} hit${i.hits===1?"":"s"}</span></div><div class="bar"><i style="width:${Math.max(12,(i.hits/max)*100)}%"></i></div></div>`).join("");
}

function renderIocs(iocs){
  const groups=Object.entries(iocs).filter(([,values])=>values.length);
  if(!groups.length){$("iocList").className="ioc-list empty-block";$("iocList").textContent="No indicators extracted yet.";return}
  $("iocList").className="ioc-list"; $("iocList").innerHTML=groups.map(([name,values])=>`<div class="ioc-group"><h3>${escapeHtml(name)} · ${values.length}</h3>${values.slice(0,8).map(v=>`<span class="ioc-chip">${escapeHtml(v)}</span>`).join("")}</div>`).join("");
}

function renderTimeline(events){
  $("timelineMeta").textContent=`${events.length} EVENTS`;
  if(!events.length){$("timelineList").className="timeline empty-block";$("timelineList").textContent="No normalized events.";return}
  $("timelineList").className="timeline"; $("timelineList").innerHTML=events.map(e=>`<div class="timeline-row"><span class="timeline-time">${escapeHtml(e.timestamp||"No timestamp")}</span><span class="timeline-process">${escapeHtml(basename(e.process)||`Event ${e.id}`)}<small>${escapeHtml(e.host||"")} ${e.user?`· ${escapeHtml(e.user)}`:""}</small></span><span class="timeline-command" title="${escapeHtml(e.command_line)}">${escapeHtml(e.command_line||JSON.stringify(e.raw))}</span></div>`).join("");
}

function processNode(node){
  return `<div class="process-node"><div class="process-card"><strong>${escapeHtml(basename(node.name)||"process")}</strong><span>PID ${escapeHtml(node.pid)} · PPID ${escapeHtml(node.parent_pid||"—")}</span><small>${escapeHtml(node.command_line||"")}</small></div>${(node.children||[]).map(processNode).join("")}</div>`;
}
function renderProcesses(roots){
  if(!roots.length){$("processTree").className="process-tree empty-block";$("processTree").textContent="No correlatable PID/PPID relationships in this dataset.";return}
  $("processTree").className="process-tree"; $("processTree").innerHTML=roots.map(processNode).join("");
}

$("exportBtn").addEventListener("click",()=>{
  if(!state.result)return; const blob=new Blob([JSON.stringify(state.result,null,2)],{type:"application/json"});
  const url=URL.createObjectURL(blob); const a=document.createElement("a"); a.href=url; a.download=`${state.result.analysis_id}.json`; a.click(); URL.revokeObjectURL(url); toast("Investigation JSON exported");
});

apiStatus();
