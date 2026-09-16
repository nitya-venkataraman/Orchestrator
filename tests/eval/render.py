#!/usr/bin/env python3
"""Render an ideation artifact as one self-contained HTML page.

Both sides of the skill / no-skill comparison go through this file, so any
difference you see between the two pages is a difference in the artifact, not
in the rendering.

    python3 tests/eval/render.py <ideation.json> <out.html> \
        --title "..." --provenance "..." [--strategy <strategy.json>] \
        [--banner "..."]

`--strategy` is for artifacts that keep personas and HMW statements in a
separate upstream file (the pipeline splits them across stages 2 and 3). An
artifact that carries its own `personas` / `hmw_statements` needs no flag.
"""

import argparse
import html
import json
import math
import sys


# ---------------------------------------------------------------- data access

def load(path):
    with open(path) as fh:
        return json.load(fh)


def personas_and_hmws(ideation, strategy):
    """Personas and HMWs live in the ideation artifact or the strategy one."""
    src = strategy if strategy else ideation
    personas = src.get("personas", []) or ideation.get("personas", [])
    hmws = src.get("hmw_statements", []) or ideation.get("hmw_statements", [])
    return personas, hmws


def hmw_label(statement, hmws):
    """Short label for an HMW, from its `derived_from` where one exists."""
    for h in hmws:
        if isinstance(h, dict) and h.get("statement") == statement:
            if h.get("derived_from"):
                return h["derived_from"]
    # No upstream label: fall back to a trimmed form of the statement itself.
    trimmed = statement.rstrip("?")
    for prefix in ("How might we ", "How might we"):
        if trimmed.startswith(prefix):
            trimmed = trimmed[len(prefix):]
            break
    return trimmed[:60] + ("…" if len(trimmed) > 60 else "")


# ------------------------------------------------------------------- fragments

def e(text):
    return html.escape(str(text), quote=True)


def num(value):
    """Render a number without a trailing .0 on whole values."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def persona_cards(personas):
    if not personas:
        return '<p class="empty">This artifact carries no personas.</p>'
    out = []
    for p in personas:
        parts = [f'<article class="card persona">']
        kind = p.get("type", "")
        parts.append('<header><h3>%s</h3>%s</header>' % (
            e(p.get("name", "Unnamed")),
            f'<span class="tag">{e(kind)}</span>' if kind else "",
        ))
        if p.get("context"):
            parts.append(f'<p class="context">{e(p["context"])}</p>')
        if p.get("quote"):
            parts.append(f'<blockquote>{e(p["quote"])}</blockquote>')
        for key, heading in (("goals", "Goals"), ("frustrations", "Frustrations")):
            items = p.get(key) or []
            if items:
                lis = "".join(f"<li>{e(i)}</li>" for i in items)
                parts.append(f"<h4>{heading}</h4><ul>{lis}</ul>")
        parts.append("</article>")
        out.append("".join(parts))
    return '<div class="cards personas">%s</div>' % "".join(out)


def hmw_list(hmws):
    if not hmws:
        return '<p class="empty">This artifact carries no HMW statements.</p>'
    rows = []
    for i, h in enumerate(hmws, 1):
        statement = h.get("statement", "") if isinstance(h, dict) else str(h)
        label = h.get("derived_from", "") if isinstance(h, dict) else ""
        rows.append(
            '<li><span class="hmw-n">HMW%d</span>'
            '<div><p class="hmw-s">%s</p>%s</div></li>' % (
                i, e(statement),
                f'<p class="hmw-d">{e(label)}</p>' if label else "",
            )
        )
    return '<ol class="hmws">%s</ol>' % "".join(rows)


def feature_rows(features, hmws):
    rows = []
    for rank, f in enumerate(features, 1):
        label = hmw_label(f.get("hmw", ""), hmws)
        metric = f.get("success_metric") or {}
        metric_html = ""
        if metric:
            metric_html = (
                '<dl class="metric"><dt>Success metric</dt><dd>%s</dd>'
                '<dt>Baseline</dt><dd>%s</dd><dt>Target</dt><dd>%s</dd></dl>' % (
                    e(metric.get("name", "—")),
                    e(metric.get("baseline", "—")),
                    e(metric.get("target", "—")),
                )
            )
        rows.append(
            '<tr data-hmw="%s" data-rank="%d">'
            '<td class="rank"><span class="dot-n">%d</span></td>'
            '<td class="name"><strong>%s</strong>'
            '<p class="desc">%s</p><p class="addresses">%s</p>%s</td>'
            '<td class="n">%s</td><td class="n">%s</td><td class="n">%s</td>'
            '<td class="n">%s</td><td class="n rice">%s</td></tr>' % (
                e(f.get("hmw", "")), rank, rank,
                e(f.get("name", "Unnamed")),
                e(f.get("description", "")),
                e(label),
                metric_html,
                num(f.get("reach", "—")), num(f.get("impact", "—")),
                num(f.get("confidence", "—")), num(f.get("effort", "—")),
                num(f.get("rice_score", "—")),
            )
        )
    return "".join(rows)


def hmw_options(features, hmws):
    seen, opts = [], ['<option value="">All problems</option>']
    for f in features:
        statement = f.get("hmw", "")
        if statement and statement not in seen:
            seen.append(statement)
            opts.append(f'<option value="{e(statement)}">{e(hmw_label(statement, hmws))}</option>')
    return "".join(opts)


def direction_cards(directions, hmws):
    if not directions:
        return '<p class="empty">This artifact carries no design directions.</p>'
    out = []
    for d in directions:
        addressed = d.get("hmws_addressed") or []
        tags = "".join(
            f'<span class="tag">{e(hmw_label(s, hmws))}</span>' for s in addressed
        )
        out.append(
            '<article class="card direction"><h3>%s</h3>'
            '<p class="summary">%s</p>'
            '<h4>Differentiator</h4><p>%s</p>'
            '<h4 class="cost">Tradeoff</h4><p>%s</p>'
            '%s</article>' % (
                e(d.get("name", "Unnamed")),
                e(d.get("summary", "")),
                e(d.get("differentiator", "—")),
                e(d.get("tradeoff", "—")),
                f'<div class="tags">{tags}</div>' if tags else "",
            )
        )
    return '<div class="cards directions">%s</div>' % "".join(out)


# ------------------------------------------------------------------------ CSS

CSS = """
:root{
  --bg:#f7f7f5; --surface:#ffffff; --sunken:#f0efec;
  --ink:#16181d; --ink-2:#4a4f59; --ink-3:#767d8a;
  --line:#dcdcd6; --line-2:#c6c6be;
  --accent:#1f4f7a; --accent-soft:#e3edf5;
  --warn:#7a4a12; --warn-soft:#f6ecdd;
  --dot:#1f4f7a;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#14161a; --surface:#1c1f25; --sunken:#22262d;
    --ink:#e9eaec; --ink-2:#b0b5be; --ink-3:#858c98;
    --line:#2e333b; --line-2:#3d434d;
    --accent:#7fb2dd; --accent-soft:#1d2c39;
    --warn:#e0b478; --warn-soft:#33271a;
    --dot:#7fb2dd;
  }
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1120px;margin:0 auto;padding:40px 24px 96px}
h1{font-size:28px;line-height:1.2;letter-spacing:-.015em;margin:0 0 6px}
h2{font-size:19px;letter-spacing:-.01em;margin:0 0 4px}
h3{font-size:16px;margin:0 0 6px}
h4{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--ink-3);margin:14px 0 4px}
h4.cost{color:var(--warn)}
p{margin:0 0 8px}
section{margin-top:44px}
.sec-head{border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:20px}
.sec-head p{color:var(--ink-2);font-size:13.5px;margin:0}
.empty{color:var(--ink-3);font-style:italic}

.prov{
  background:var(--surface);border:1px solid var(--line);border-radius:10px;
  padding:18px 20px;margin-top:14px;
}
.prov dl{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;margin:0;font-size:13px}
.prov dt{color:var(--ink-3);text-transform:uppercase;letter-spacing:.06em;font-size:10.5px;padding-top:3px}
.prov dd{margin:0;color:var(--ink-2)}
.banner{
  background:var(--warn-soft);border:1px solid var(--warn);border-left-width:3px;
  border-radius:8px;padding:14px 16px;margin-top:14px;color:var(--warn);font-size:13.5px;
}
.banner strong{color:var(--warn)}

.cards{display:grid;gap:14px}
.personas{grid-template-columns:repeat(auto-fit,minmax(290px,1fr))}
.directions{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px 20px}
.card header{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.card ul{margin:0;padding-left:17px;color:var(--ink-2);font-size:13.5px}
.card li{margin-bottom:4px}
.context{color:var(--ink-2);font-size:13.5px}
blockquote{
  margin:12px 0;padding:8px 0 8px 14px;border-left:2px solid var(--line-2);
  color:var(--ink-2);font-style:italic;font-size:13.5px;
}
.summary{color:var(--ink-2);font-size:14px}
.direction p{font-size:13.5px;color:var(--ink-2)}
.tag{
  display:inline-block;background:var(--accent-soft);color:var(--accent);
  border-radius:4px;padding:2px 7px;font-size:10.5px;font-weight:600;
  text-transform:uppercase;letter-spacing:.05em;
}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}

.hmws{list-style:none;margin:0;padding:0;counter-reset:none}
.hmws li{display:flex;gap:14px;padding:12px 0;border-bottom:1px solid var(--line)}
.hmws li:last-child{border-bottom:0}
.hmw-n{
  flex:0 0 auto;color:var(--accent);font-weight:700;font-size:11px;
  letter-spacing:.06em;padding-top:3px;font-variant-numeric:tabular-nums;
}
.hmw-s{margin:0;font-size:14.5px}
.hmw-d{margin:2px 0 0;color:var(--ink-3);font-size:12px}

.controls{display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.controls label{font-size:12px;color:var(--ink-3);text-transform:uppercase;letter-spacing:.06em}
select{
  font:inherit;font-size:13px;padding:6px 10px;border:1px solid var(--line-2);
  border-radius:6px;background:var(--surface);color:var(--ink);
}
.count{font-size:12.5px;color:var(--ink-3);margin-left:auto;font-variant-numeric:tabular-nums}

.t-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:720px;font-size:13.5px}
thead th{
  background:var(--sunken);border-bottom:1px solid var(--line-2);
  padding:0;text-align:left;font-size:10.5px;text-transform:uppercase;
  letter-spacing:.07em;color:var(--ink-3);white-space:nowrap;position:sticky;top:0;
}
thead th button{
  all:unset;display:block;width:100%;box-sizing:border-box;padding:10px 12px;
  cursor:pointer;font:inherit;color:inherit;
}
thead th button:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
thead th.n button{text-align:right}
thead th[aria-sort]{color:var(--accent)}
thead th[aria-sort="descending"] button::after{content:" ↓"}
thead th[aria-sort="ascending"] button::after{content:" ↑"}
tbody td{border-bottom:1px solid var(--line);padding:12px;vertical-align:top}
tbody tr:last-child td{border-bottom:0}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;color:var(--ink-2)}
td.rice{font-weight:700;color:var(--ink)}
td.rank{width:34px}
.dot-n{
  display:inline-flex;align-items:center;justify-content:center;
  width:22px;height:22px;border-radius:50%;background:var(--accent-soft);
  color:var(--accent);font-size:11px;font-weight:700;font-variant-numeric:tabular-nums;
}
td.name{max-width:520px}
.desc{color:var(--ink-2);font-size:13px;margin:5px 0 0}
.addresses{color:var(--ink-3);font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;margin:6px 0 0}
.metric{
  margin:10px 0 0;padding-top:8px;border-top:1px dashed var(--line-2);
  display:grid;grid-template-columns:auto 1fr;gap:2px 12px;font-size:12px;
}
.metric dt{color:var(--ink-3);text-transform:uppercase;letter-spacing:.05em;font-size:10px;padding-top:2px}
.metric dd{margin:0;color:var(--ink-2)}

.matrix{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:20px}
.matrix svg{display:block;width:100%;height:auto;overflow:visible}
.ax-line{stroke:var(--line-2);stroke-width:1}
.ax-grid{stroke:var(--line);stroke-width:1;stroke-dasharray:2 4}
.ax-t{fill:var(--ink-3);font-size:11px;font-variant-numeric:tabular-nums}
.ax-lab{fill:var(--ink-3);font-size:10.5px;text-transform:uppercase;letter-spacing:.08em}
.pt{fill:var(--dot);fill-opacity:.18;stroke:var(--dot);stroke-width:1.5}
.pt-n{fill:var(--dot);font-size:11px;font-weight:700;text-anchor:middle;font-variant-numeric:tabular-nums}
.note{color:var(--ink-3);font-size:12.5px;margin-top:12px}
footer{margin-top:56px;padding-top:18px;border-top:1px solid var(--line);color:var(--ink-3);font-size:12px}
"""


# ------------------------------------------------------------------------- JS

JS = """
(function(){
  var data = window.__FEATURES__ || [];
  var table = document.getElementById('rice');
  var tbody = table.querySelector('tbody');
  var filter = document.getElementById('hmw-filter');
  var count = document.getElementById('count');
  var sortKey = 'rice_score', sortDir = -1;

  function visible(){
    var f = filter.value;
    return data.filter(function(d){ return !f || d.hmw === f; });
  }

  function sortRows(){
    var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
    rows.sort(function(a, b){
      if (sortKey === 'rank') {
        return (+a.dataset.rank - +b.dataset.rank) * (sortDir === -1 ? 1 : -1);
      }
      var da = data[+a.dataset.rank - 1], db = data[+b.dataset.rank - 1];
      var va = da[sortKey], vb = db[sortKey];
      if (typeof va === 'string' || typeof vb === 'string') {
        return String(va).localeCompare(String(vb)) * -sortDir;
      }
      return (va - vb) * sortDir;
    });
    rows.forEach(function(r){ tbody.appendChild(r); });
  }

  function applyFilter(){
    var f = filter.value, shown = 0;
    Array.prototype.forEach.call(tbody.querySelectorAll('tr'), function(r){
      var on = !f || r.dataset.hmw === f;
      r.hidden = !on;
      if (on) shown++;
    });
    count.textContent = shown + ' of ' + data.length + ' features';
    drawMatrix();
  }

  // --- impact / effort matrix -------------------------------------------
  // Effort is spaced by its distinct values, not linearly: a 13-point item
  // next to a run of 3s and 5s would otherwise sit alone in the far margin
  // and squash everything else against the axis.
  function drawMatrix(){
    var pts = visible();
    var svg = document.getElementById('matrix-svg');
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    if (!pts.length) return;

    var W = 720, H = 420, L = 58, R = 26, T = 22, B = 52;
    var iw = W - L - R, ih = H - T - B;
    var NS = 'http://www.w3.org/2000/svg';
    function el(n, a){
      var x = document.createElementNS(NS, n);
      for (var k in a) x.setAttribute(k, a[k]);
      return x;
    }
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);

    var efforts = data.map(function(d){ return d.effort; })
                      .filter(function(v, i, a){ return a.indexOf(v) === i; })
                      .sort(function(a, b){ return a - b; });
    var impacts = data.map(function(d){ return d.impact; })
                      .filter(function(v, i, a){ return a.indexOf(v) === i; })
                      .sort(function(a, b){ return a - b; });
    function px(v){
      var i = efforts.indexOf(v);
      return L + (efforts.length < 2 ? iw / 2 : (i / (efforts.length - 1)) * iw);
    }
    function py(v){
      var i = impacts.indexOf(v);
      return T + ih - (impacts.length < 2 ? ih / 2 : (i / (impacts.length - 1)) * ih);
    }
    var maxR = Math.max.apply(null, data.map(function(d){ return d.rice_score; }));
    function pr(v){ return 9 + 17 * Math.sqrt(Math.max(v, 0) / (maxR || 1)); }

    impacts.forEach(function(v){
      var y = py(v);
      svg.appendChild(el('line', {x1:L, y1:y, x2:L+iw, y2:y, 'class':'ax-grid'}));
      var t = el('text', {x:L-12, y:y+4, 'class':'ax-t', 'text-anchor':'end'});
      t.textContent = v; svg.appendChild(t);
    });
    efforts.forEach(function(v){
      var x = px(v);
      var t = el('text', {x:x, y:T+ih+22, 'class':'ax-t', 'text-anchor':'middle'});
      t.textContent = v; svg.appendChild(t);
    });
    svg.appendChild(el('line', {x1:L, y1:T+ih, x2:L+iw, y2:T+ih, 'class':'ax-line'}));
    svg.appendChild(el('line', {x1:L, y1:T, x2:L, y2:T+ih, 'class':'ax-line'}));
    var xl = el('text', {x:L+iw/2, y:T+ih+44, 'class':'ax-lab', 'text-anchor':'middle'});
    xl.textContent = 'Effort →'; svg.appendChild(xl);
    var yl = el('text', {x:0, y:0, 'class':'ax-lab', 'text-anchor':'middle',
                         transform:'translate(16,' + (T+ih/2) + ') rotate(-90)'});
    yl.textContent = 'Impact →'; svg.appendChild(yl);

    // Features that share an impact and an effort land on exactly the same
    // coordinate and hide each other completely. Fan a coincident group out
    // around its shared point instead, by a radius wide enough to clear the
    // biggest bubble in it.
    var groups = {}, offset = {};
    pts.forEach(function(d){
      var k = d.impact + '|' + d.effort;
      (groups[k] = groups[k] || []).push(d);
    });
    Object.keys(groups).forEach(function(k){
      var g = groups[k];
      if (g.length < 2) return;
      var spread = Math.max.apply(null, g.map(function(d){ return pr(d.rice_score); })) * 0.95;
      g.forEach(function(d, i){
        var a = -Math.PI / 2 + (i * 2 * Math.PI / g.length);
        offset[d.rank] = [Math.cos(a) * spread, Math.sin(a) * spread];
      });
    });

    // Biggest first, so a large bubble never hides a small one it overlaps.
    pts.slice().sort(function(a, b){ return b.rice_score - a.rice_score; })
       .forEach(function(d){
      var off = offset[d.rank] || [0, 0];
      var x = px(d.effort) + off[0], y = py(d.impact) + off[1];
      var c = el('circle', {cx:x, cy:y, r:pr(d.rice_score), 'class':'pt'});
      var ttl = document.createElementNS(NS, 'title');
      ttl.textContent = d.rank + '. ' + d.name + ' — RICE ' + d.rice_score +
                        ' (R ' + d.reach + ' · I ' + d.impact +
                        ' · C ' + d.confidence + ' · E ' + d.effort + ')';
      c.appendChild(ttl);
      svg.appendChild(c);
      var n = el('text', {x:x, y:y+4, 'class':'pt-n'});
      n.textContent = d.rank;
      n.appendChild(ttl.cloneNode(true));
      svg.appendChild(n);
    });
  }

  Array.prototype.forEach.call(table.querySelectorAll('thead th[data-key]'), function(th){
    th.querySelector('button').addEventListener('click', function(){
      var key = th.dataset.key;
      sortDir = (key === sortKey) ? -sortDir : (key === 'name' ? 1 : -1);
      sortKey = key;
      Array.prototype.forEach.call(table.querySelectorAll('thead th'), function(o){
        o.removeAttribute('aria-sort');
      });
      th.setAttribute('aria-sort', sortDir === 1 ? 'ascending' : 'descending');
      sortRows();
    });
  });

  filter.addEventListener('change', applyFilter);
  applyFilter();
})();
"""


# ------------------------------------------------------------------------ page

COLUMNS = [
    ("rank", "#", ""),
    ("name", "Feature", ""),
    ("reach", "Reach", "n"),
    ("impact", "Impact", "n"),
    ("confidence", "Conf.", "n"),
    ("effort", "Effort", "n"),
    ("rice_score", "RICE", "n"),
]


def build(ideation, strategy, title, provenance, banner):
    personas, hmws = personas_and_hmws(ideation, strategy)
    features = sorted(
        ideation.get("features", []),
        key=lambda f: f.get("rice_score", 0),
        reverse=True,
    )
    directions = ideation.get("design_directions", [])

    payload = [
        {
            "rank": i,
            "name": f.get("name", ""),
            "hmw": f.get("hmw", ""),
            "reach": f.get("reach", 0),
            "impact": f.get("impact", 0),
            "confidence": f.get("confidence", 0),
            "effort": f.get("effort", 0),
            "rice_score": f.get("rice_score", 0),
        }
        for i, f in enumerate(features, 1)
    ]

    heads = "".join(
        '<th %sclass="%s"%s><button type="button">%s</button></th>' % (
            f'data-key="{key}" ' if key else "",
            cls,
            ' aria-sort="descending"' if key == "rice_score" else "",
            e(label),
        )
        for key, label, cls in COLUMNS
    )

    banner_html = (
        f'<div class="banner" role="note">{banner}</div>' if banner else ""
    )

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<style>{CSS}</style>
</head><body>
<div class="wrap">

<header>
  <h1>{e(title)}</h1>
  <div class="prov">
    <dl>{provenance}</dl>
  </div>
  {banner_html}
</header>

<section>
  <div class="sec-head">
    <h2>Who this is for</h2>
    <p>The people the features below are meant to serve.</p>
  </div>
  {persona_cards(personas)}
</section>

<section>
  <div class="sec-head">
    <h2>Problems worth solving</h2>
    <p>Each feature answers exactly one of these.</p>
  </div>
  {hmw_list(hmws)}
</section>

<section>
  <div class="sec-head">
    <h2>Feature backlog</h2>
    <p>Ranked by RICE. Sort any column; filter to one problem to see what
       competes within it.</p>
  </div>
  <div class="controls">
    <label for="hmw-filter">Filter</label>
    <select id="hmw-filter">{hmw_options(features, hmws)}</select>
    <span class="count" id="count"></span>
  </div>
  <div class="t-wrap">
    <table id="rice">
      <thead><tr>{heads}</tr></thead>
      <tbody>{feature_rows(features, hmws)}</tbody>
    </table>
  </div>
</section>

<section>
  <div class="sec-head">
    <h2>Impact against effort</h2>
    <p>The same features, positioned. Bubble area carries RICE; the number in
       each bubble is its rank in the table above.</p>
  </div>
  <div class="matrix">
    <svg id="matrix-svg" role="img"
         aria-label="Scatter plot of features by impact and effort. The same
                     figures are in the sortable table above."></svg>
    <p class="note">Effort is spaced by its distinct values rather than
      linearly, so a single high-effort item does not squash the rest against
      the axis. Read positions as ordering, not as distance.</p>
  </div>
</section>

<section>
  <div class="sec-head">
    <h2>Design directions</h2>
    <p>Different bets about how to solve the problem, not feature bundles.
       No direction is recommended here — that choice is yours.</p>
  </div>
  {direction_cards(directions, hmws)}
</section>

<footer>
  Rendered by <code>tests/eval/render.py</code>. Both sides of this comparison
  use this same renderer, so any difference between the two pages is a
  difference in the artifact, not in the presentation.
</footer>

</div>
<script>window.__FEATURES__ = {json.dumps(payload)};</script>
<script>{JS}</script>
</body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ideation")
    ap.add_argument("out")
    ap.add_argument("--strategy")
    ap.add_argument("--title", required=True)
    ap.add_argument("--provenance", required=True,
                    help="HTML <dt>/<dd> pairs for the provenance block")
    ap.add_argument("--banner", default="")
    args = ap.parse_args()

    ideation = load(args.ideation)
    strategy = load(args.strategy) if args.strategy else None
    page = build(ideation, strategy, args.title, args.provenance, args.banner)

    with open(args.out, "w") as fh:
        fh.write(page)

    n_f = len(ideation.get("features", []))
    n_d = len(ideation.get("design_directions", []))
    print(f"{args.out}: {n_f} features, {n_d} directions", file=sys.stderr)


if __name__ == "__main__":
    main()
