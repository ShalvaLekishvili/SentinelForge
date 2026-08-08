let selectedFile = null;
const $ = (id) => document.getElementById(id);

$("file").addEventListener("change", (event) => {
  selectedFile = event.target.files[0] || null;
  $("filename").textContent = selectedFile ? selectedFile.name : "No file selected";
});

$("sample").addEventListener("click", async () => {
  const response = await fetch("/static/sample-incident.json");
  const blob = await response.blob();
  selectedFile = new File([blob], "sample-incident.json", {type: "application/json"});
  $("filename").textContent = "sample-incident.json · built-in demo";
});

$("analyze").addEventListener("click", async () => {
  if (!selectedFile) { alert("Choose a log file or load the demo first."); return; }
  $("analyze").disabled = true; $("analyze").textContent = "Analyzing…";
  const form = new FormData(); form.append("file", selectedFile);
  try {
    const response = await fetch("/api/analyze", { method: "POST", body: form });
    if (!response.ok) throw new Error(await response.text());
    render(await response.json());
  } catch (error) { alert(`Analysis failed: ${error.message}`); }
  finally { $("analyze").disabled = false; $("analyze").textContent = "Analyze"; }
});

function esc(value){return String(value ?? "").replace(/[&<>\"']/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));}
function render(data){
  $("risk").textContent = data.risk.score;
  $("riskLevel").textContent = `${data.risk.level} risk`;
  $("events").textContent = data.event_count;
  $("detectionCount").textContent = data.detection_count;
  $("analysisId").textContent = data.analysis_id;
  const iocCount = Object.values(data.iocs).reduce((n,a)=>n+a.length,0); $("iocCount").textContent = iocCount;
  $("detectionList").innerHTML = data.detections.length ? data.detections.map(d=>`<div class="finding"><div class="finding-top"><span class="sev ${esc(d.severity)}">${esc(d.severity)}</span><strong>${esc(d.title)}</strong><span class="mitre">${esc(d.mitre)}</span></div><p>${esc(d.command_line || d.process || "Matched telemetry event")}</p></div>`).join("") : `<div class="empty">No rule matches in this dataset.</div>`;
  $("iocList").innerHTML = Object.entries(data.iocs).filter(([,v])=>v.length).map(([k,v])=>`<div class="ioc-group"><h3>${esc(k)}</h3>${v.map(x=>`<span class="chip">${esc(x)}</span>`).join("")}</div>`).join("") || `<div class="empty">No indicators found.</div>`;
  $("timelineList").innerHTML = data.timeline.length ? data.timeline.map(e=>`<div class="timeline-row"><span>${esc(e.timestamp || "No timestamp")}</span><strong>${esc(e.process || `Event ${e.id}`)}</strong><p>${esc(e.command_line || JSON.stringify(e.raw))}</p></div>`).join("") : `<div class="empty">No normalized events.</div>`;
}
