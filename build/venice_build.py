import json, os, sys, re, html as H, math, datetime
D = sys.argv[1]; ASSETS = "in-time-assets"
HERE = os.path.dirname(os.path.abspath(__file__)); pool = json.load(open(os.path.join(HERE,'venice_pool.json'))); cases, adds = pool['cases'], pool['adds']
img = json.load(open(os.path.join(HERE,'venice_images.json'))); sel, res = img['sel'], img['results']
stmt = open(f"{D}/In Time - Refined Curatorial Statement (Jane, 16 Sept).md", encoding='utf-8').read()
def section(md, start, end):
    i = md.find(start); j = md.find(end, i+len(start)); return md[i+len(start):j].strip()
EN = section(stmt, "### English\n", "\n---"); CN = section(stmt, "### 中文（草稿，供合作者润色）\n", "\n---")
def paras(t): return "".join(f"<p>{H.escape(p).replace('**','')}</p>" for p in t.split("\n\n") if p.strip())
THEMES = [("Material","材料"),("Ecological","生态"),("Cultural","文化"),("Maintenance","维护"),("Financial","资金"),("Technological","技术")]
TI = {t:i for i,(t,_) in enumerate(THEMES)}
# ---- per-project curatorial data (EN gloss, secondaries, out-of-time-with, status, call) ----
M = {
"1":("Youjiawa Residential Community Centre (former compressor factory), Nanjing",["Cultural","Maintenance"],"Production ended; the structure, workers' memory and aging residents continue.","core",""),
"13":("Xiaohe Park (oil depot to park), Hangzhou",["Ecological","Maintenance"],"Industrial exit has a date; soil remediation and ecology do not — greenery photos prove nothing.","reserve",""),
"A01":("Shenzhen Women & Children's Centre — MVRDV retrofit",["Cultural","Financial","Maintenance"],"24,000 m³ of concrete retained in a year; care institutions take decades to form; a 30-year vacancy.","priority add",""),
"A03":("Jingdezhen Imperial Kiln Museum — Studio Zhu Pei",["Cultural","Maintenance"],"Brick reuse tied to a 2–3-year kiln cycle; the museum expects permanence.","priority add","Prior international exposure (MoMA) — needs fresh craft/operational evidence."),
"12":("Xianfeng Baiwu Bookstore (granary), Huize",["Cultural","Maintenance"],"Wall, roof truss and original use have three different end dates.","background",""),
"15":("Mawei Shipyard Phase 1, Fuzhou",["Maintenance","Cultural","Financial"],"Production stops fast; protection listing is slower; labor memory fades slowest.","background","Top-up: the clearest labor-memory clock in the Material column."),
"30":("Futian Mangrove Ecological Park — continuous operation, Shenzhen",["Maintenance","Financial","Cultural"],"Migration and habitat cross annual budgets; volunteer vs professional continuity.","core",""),
"20":("Yuweizhou Park, Nanchang — Turenscape",["Material","Maintenance"],"Opening is an event; water level, succession and recovery are cycles.","reserve",""),
"19":("Baoshan Waste-to-Energy Centre, Shanghai",["Material","Maintenance","Financial"],"Waste arrives daily; the facility is fixed for decades; reduction targets shift.","reserve",""),
"28":("Erhai Lake Ecological Corridor — demonstration section, Dali",["Cultural","Financial","Maintenance"],"Shoreline project cycle vs lake recovery and residents' lives.","reserve",""),
"A04":("Yan Wang Preston, <i>Forest</i> (2010–17) — longitudinal photography",["Financial","Cultural","Material"],"Instant 'forest city' image vs transplanted-tree biology, mortality and source villages.","priority add","Proposed 2026–27 revisit commission turns the artwork into a longitudinal test."),
"21":("Meishe River Fengxiang Wetland Park, Haikou",["Financial","Maintenance"],"Works finish fast; water quality and sewage governance are long.","background","Top-up: the governance-time case in the Ecological column."),
"4":("Pengyi Estate — demolish and rebuild in place, Shanghai",["Financial","Material","Maintenance"],"Years of transition housing consume a finite old age; return does not restore the neighborhood.","core",""),
"3":("The Retirement Home — a two-elder apartment retrofit, Beijing",["Material","Maintenance"],"Bodily capacity changes yearly; room allocation is fixed for decades.","core","Consent-sensitive: resident-led account required or use as reserve."),
"6":("Xi'an Old Vegetable Market Phase 1",["Material","Financial","Maintenance"],"Daily trade depends on stable stalls; renovation and rent follow another cycle.","core",""),
"A05":("Handshake 302 and the Baishizhou archive, Shenzhen",["Financial","Maintenance","Material"],"A lease clock inside the waiting period before redevelopment.","priority add",""),
"35":("Cao Fei, <i>The Eternal Wave</i> (VR)",["Technological","Material"],"Industrial space disappears; memory and fiction persist non-linearly.","core",""),
"A08":("Chen Qiulin — Three Gorges sequence (2002–07)",["Ecological","Financial"],"River level and demolition vs the finite lifetimes of the displaced.","priority add","Older than the call's preferred range — a 2026–27 return commission solves the eligibility problem."),
"5":("Futian High School, Shenzhen",["Material","Financial"],"A student stays three years; campus and demography move in decades.","reserve","Top-up: the generational clock in the Cultural column."),
"9":("Xiangzili neighbourhood public-space renewal",["Cultural","Financial","Material"],"Designers stayed to operate; each phase was revised by use.","core","SWING CALL: filed Maintenance (from Cultural) — staying-to-operate is the maintenance argument."),
"8":("Xinhua Community Building Centre, Shanghai",["Cultural","Financial"],"One delivery is visible; repeated organizing labor is invisible.","reserve","Swing from Cultural."),
"25":("Ancha (An Tea) Museum Factory",["Ecological","Cultural","Material"],"Tea season and craft time re-scheduled by the tourist's hour.","reserve",""),
"A09":("Infrastructure of the Ordinary — the Shanzhai Trolley, Huaqiangbei",["Cultural","Technological","Financial"],"Manual repeated trips keep a 'real-time' electronics market moving.","priority add","Shown at UABB 2025 — needs a genuinely new Venice iteration; workers as collaborators."),
"B01":("Shanghai Expo Village — afterlife audit (commission)",["Material","Financial","Cultural"],"Event time vs neighborhood upkeep; existing evidence is designer-led.","commission","Enters only through an independent post-occupancy commission."),
"B02":("Shougang Big Air — post-event life (commission)",["Material","Financial","Cultural"],"Does a permanent Olympic facility acquire daily public life?","commission","State-promotional sources dominate — independent operational audit required."),
"7":("Wen'er Vegetable Market Hall A, Hangzhou",["Cultural","Financial"],"Morning market, close and cleaning as three daily time slots.","reserve","Swing from Cultural."),
"10":("Jinsong North community renewal Phase 1, Beijing",["Maintenance","Cultural"],"Three-year support fund vs indefinite upkeep and residents' ability to pay.","core",""),
"24":("Dabu Village Culture & Living Space, Songxi",["Material","Cultural","Maintenance"],"Lease term, repair cycle and family generations do not coincide.","core",""),
"16":("GATE M West Bund Dream Centre, Shanghai — MVRDV",["Material","Cultural"],"Investment interrupted twice; the concrete waited between developers.","background","Swing from Material — the interrupted-capital clock."),
"A02":("Nantou Ancient City regeneration — URBANUS",["Cultural","Maintenance","Material"],"A 2,000-year narrative, festival time, rent turnover and staged renewal.","priority add","SWING CALL: filed Financial (from Cultural) — rent/commercialization is its sharper 时差. High prior biennale exposure."),
"B03":("One break in the Huangpu River 45-km public-space connection (commission)",["Maintenance","Cultural","Ecological"],"One negotiated break out of ~100; upkeep and access since.","commission",""),
"11":("Qingdeng Village Public Art Museum",["Material","Cultural"],"Administrative reorganization ended use before structural life; 'post-occupancy' images are AI-generated.","background","Swing from Material — a funding/administration clock. Top-up."),
"ART_LIUCHUANG":("Liu Chuang, <i>Bitcoin Mining and Field Recordings of Ethnic Minorities</i> (2018)",["Ecological","Technological"],"Hydropower, crypto finance and minority territories on incommensurable clocks.","art longlist","Carries the Financial column's computational-capital case."),
"40":("Digital-twin Dujiangyan — headworks and irrigation dispatch",["Ecological","Maintenance","Cultural"],"Fast dispatch depends on 2,000-year hydraulic knowledge, field seasons and changing inflow.","core","The proposal's best slow-fast case."),
"34":("Huang Rongyuan Hall — digital survey and restoration, Gulangyu",["Material","Maintenance","Cultural"],"A scan freezes a moment; deterioration continues; models need later keepers.","core",""),
"36":("Tencent Gui'an Qixing Data Centre — <b>paired with He Zike, <i>Random Access</i></b>",["Ecological","Material","Maintenance"],"A long-life cavern hosts 3–5-year equipment; the city never sees the mountain.","reserve · Helena's pick","CONDITION: include only with A07 beside it, or it reads as corporate display. Operating data, not Tencent's claims."),
"18":("Spark 761 Digital-Economy AI Data Centre, Beijing — llLab",["Material","Maintenance","Ecological"],"Factory shell serves decades; MEP and compute are replaced fast; service must never stop.","core","SWING CALL: filed Technological (from Material) — compute inside an industrial shell is track six."),
"A06":("Wendi Yan, <i>Biotopy</i> — live bio-digital instrument",["Ecological","Maintenance"],"Microbial growth and game real-time mutually dependent; a six-month live instrument.","priority add","Import, lab safety, daily care and failure protocol are the gates."),
"37":("Hainan Lingshui undersea data centre",["Ecological","Material","Maintenance"],"Chip upgrade, hull inspection, marine change and subsea engineering life all differ.","reserve","Top-up: the marine-maintenance clock."),
"ART_LIAMYOUNG":("Liam Young — new machine-vision commission, or <i>Planet City</i>",["Cultural","Ecological"],"What the city's sensing system cannot see.","Helena's pick","FLAG: avoid <i>Where the City Can't See</i> (its 'Chinese-owned Detroit zone' imagery is an avoidable distraction in a national pavilion). International-contributor rationale to be written early."),
"A17":("Luxelakes CPI Island — vari architects (2022–24), show-homes to commercial island",["Material","Cultural"],"Show-homes are built for a sales window of months, then wait for years; here the wait ended in a second programme.","Helena's pick 09-18","Footnote to GATE M: concrete waiting between programmes, at villa scale."),
"A12":("Xiwusutu Village Centre, Hohhot — Zhang Pengju (Aga Khan Award 2025)",["Cultural","Maintenance"],"Bricks with a first life, a temple site older than the building, a year of use in two seasons.","Jane's recommendation · Helena 09-18",""),
"A13":("Guanzhong After-Harvest Art Festival, Caijiapo — Wu Xiaochuan (2018– )",["Maintenance","Financial","Ecological"],"An event keyed to the wheat harvest, repeated seven years; income arrives in a season, the village must be kept all year.","Jane's recommendation · Helena 09-18",""),
"A14":("Nanshan Hundred Schools Renewal, Shenzhen — Zhou Hongmei, Zhu Jingxiang (2022–25)",["Cultural","Financial"],"Three eight-week summer windows for 143 schools; a pupil stays six years; the mechanism is built for a district.","Jane's recommendation · Helena 09-18","Pairs with the former card 5 logic at maintenance scale; verify the holiday-window timing with Zhu."),
"A15":("Taoxichuan, Jingdezhen — Zhang Jie (2016 / 2022), paired with 川上行 (Vector Architects)",["Financial","Material","Maintenance"],"A kiln that changed fuel three times, a workforce laid off in a year, makers who turn over every season.","Jane's recommendation · Helena 09-18","Second Jingdezhen card; keep distinct from A03."),
"A16":("Liangma River corridor, Beijing — AECOM (2019–23)",["Financial","Cultural","Maintenance"],"A 1980s channel reopened in four years; water and birds on their own time under a nightly commercial clock.","Jane's recommendation · Helena 09-18",""),
"A10":("Beijing Silvermine — Thomas Sauvin's salvaged-negative archive (2009– )",["Material","Financial"],"Negatives priced by the kilo for their silver; the same frames hold twenty years of a city's private time.","collaborator's pick 09-17",""),
"R04":("China's unfinished buildings as stranded assets — Duan, Bai et al., <i>One Earth</i> 2026",["Material","Ecological"],"Finance stopped on a date; steel, cement and buyers' lives kept aging.","collaborator's pick 09-17","Aggregate figures only until the authors clear project-level detail."),
"A11":("Former Kunming Rubber Factory — Kokaistudios (2011–17)",["Cultural","Financial","Maintenance"],"Three brick ages on one site; a workforce of 2,000 that fell to zero; a developer's programme nine years on.","collaborator's pick 09-17","Nine years after completion the afterlife is the exhibit, if the studio has it."),
"R01":("Microbial self-healing concrete — Jing Xu, Tongji",["Technological","Maintenance"],"Cracks open in days; bacteria mineralize over weeks; repair contracts and budgets run on years.","research add · Helena's pick",""),
"R02":("Futian Mangrove Ecological Park — MCF long-term monitoring",["Maintenance","Cultural","Technological"],"Migration, breeding, daily monitoring rounds and annual plans answer to no project schedule.","research add · Helena's pick","Live data during the pavilion — the one card whose time section keeps growing."),
"R03":("Smart Yingxian Wooden Pagoda — Tsinghua digital twin",["Material","Cultural","Maintenance"],"A 970-year structure, a lean measured in decades, scans in seconds — and a model that needs keepers.","research add · Helena's pick","Filed Technological; Maintenance is its strong second (early-warning monitoring is upkeep)."),
}
def weights(k, theme):
    w = [1]*6; w[TI[theme]] = 3
    for s in M[k][1]:
        if s in TI and w[TI[s]] < 2: w[TI[s]] = 2
    return w
def radar(w, theme, size=120):
    c = size/2; r = size/2 - 14; pts=[]; axes=[]; labels=[]
    for i,(t,cn) in enumerate(THEMES):
        a = -math.pi/2 + i*2*math.pi/6
        x = c + r*math.cos(a); y = c + r*math.sin(a)
        axes.append(f'<line x1="{c}" y1="{c}" x2="{x:.1f}" y2="{y:.1f}" stroke="#d9d2c5" stroke-width="1"/>')
        lx = c + (r+10)*math.cos(a); ly = c + (r+10)*math.sin(a)
        fw = "700" if t==theme else "400"; col = "#8a2b1b" if t==theme else "#6b6459"
        labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="9" text-anchor="middle" dominant-baseline="middle" fill="{col}" font-weight="{fw}">{cn}</text>')
        rr = r * (w[i]/3.0); pts.append(f"{c + rr*math.cos(a):.1f},{c + rr*math.sin(a):.1f}")
    rings = "".join(f'<circle cx="{c}" cy="{c}" r="{r*f:.1f}" fill="none" stroke="#e8e2d6" stroke-width="1"/>' for f in (1/3,2/3,1))
    return (f'<svg class="radar" viewBox="0 0 {size} {size}" width="{size}" height="{size}" aria-label="time-section profile">'
            f'{rings}{"".join(axes)}<polygon points="{" ".join(pts)}" fill="rgba(138,43,27,0.22)" stroke="#8a2b1b" stroke-width="1.6"/>{"".join(labels)}</svg>')
def title_of(k):
    if k.isdigit(): c=cases[k]; return c['title'], c['sub'], c['team']
    if k in adds: a=adds[k]; return a['title'], a.get('tracks',''), ''
    return {"ART_LIUCHUANG":"刘窗《比特币矿与少数民族田野录音》","ART_LIAMYOUNG":"Liam Young 委约 / Planet City"}[k], "", ""
def shicha_of(k):
    if k.isdigit(): return cases[k]['shicha'], cases[k]['cond'], cases[k]['exhibit']
    if k in adds: return "", adds[k]['gate'], adds[k]['prop']
    return "", "", ""
def links_of(k):
    if k.isdigit(): return cases[k]['links']
    if k in adds: return adds[k]['links']
    return [(res[k]['url'], "project")] if res.get(k,{}).get('url') else []
def img_tag(k, num):
    fn = res.get(k,{}).get('img')
    if fn and os.path.exists(f"{D}/{ASSETS}/{fn}"):
        src = res[k].get('img_src','')
        return f'<img src="{ASSETS}/{fn}" alt="" loading="lazy"><div class="credit">image: {H.escape(re.sub(r"^https?://([^/]+).*", r"\\1", src))}</div>'
    return (f'<div class="ph"><span class="phnum">{H.escape(num)}</span><span>image pending<br><small>source hotlink-blocked or none found —<br>drop a file at {ASSETS}/{k}.jpg</small></span></div>')
cards=[]; missing=[]; calls=[]
for theme, cn in THEMES:
    items=[]
    for k in sel[theme]:
        en, secs, oot, status, call = M[k]; t, sub, team = title_of(k); sc, cond, exhibit = shicha_of(k)
        facts = adds[k]['body'].split('\n\n',1)[1].strip() if (k in adds and '\n\n' in adds[k]['body']) else ''
        num = k if not k.startswith("ART") else "ART"
        if not (res.get(k,{}).get('img') and os.path.exists(f"{D}/{ASSETS}/{res[k]['img']}")): missing.append((theme,k,t))
        if call: calls.append((theme,k,t,call))
        pair = ""
        if k=="36":
            a7 = adds["A07"]; l7 = a7['links'][0][0] if a7['links'] else "#"
            pair = f'<div class="pair">＋ A07 He Zike, <i>Random Access</i> (2023) — <a href="{H.escape(l7)}" target="_blank" rel="noopener">source</a>. {H.escape(a7["prop"])}</div>'
        lk = "".join(f'<a href="{H.escape(u)}" target="_blank" rel="noopener">{H.escape(lbl or "link")}</a>' for u,lbl in links_of(k)[:3]) or '<span class="muted">link to be supplied</span>'
        secs_txt = " · ".join(secs)
        items.append(f'''
<article class="card" id="p-{k}">
  <div class="media">{img_tag(k,num)}</div>
  <div class="body">
    <div class="kicker"><span class="num">{H.escape(num)}</span><span class="status">{H.escape(status)}</span></div>
    <h3>{H.escape(t)}</h3>
    <div class="en">{en}</div>
    <div class="meta">{H.escape(sub)}{(" · "+H.escape(team)) if team else ""}</div>
    <div class="row">
      <div class="prof">{radar(weights(k,theme), theme)}<div class="proflab">time-section profile · filed under <b>{theme}</b><br><span class="muted">also bulging: {H.escape(secs_txt)}</span></div></div>
      <div class="txt">
        <p class="oot"><b>Out of time with:</b> {H.escape(oot)}</p>
        {("<p class='sc'><b>Facts:</b> "+H.escape(facts)+"</p>") if facts else ""}
        {("<p class='sc'><b>时差 · 策展判断：</b>"+H.escape(sc)+"</p>") if sc else ""}
        {("<p class='ex'><b>拟议展品 / proposition：</b>"+H.escape(exhibit)+"</p>") if exhibit else ""}
        {("<p class='gate'><b>Gate:</b> "+H.escape(cond)+"</p>") if cond else ""}
        {("<p class='call'><b>Curatorial call (Jane):</b> "+call+"</p>") if call else ""}
        {pair}
        <p class="links">{lk}</p>
      </div>
    </div>
  </div>
</article>''')
    cards.append(f'<section class="theme" id="{theme.lower()}"><header><h2><span class="cn">{cn}</span> {theme}</h2><p class="count">{len(sel[theme])} projects</p></header>{"".join(items)}</section>')
n_total = sum(len(v) for v in sel.values()); n_img = sum(1 for th in sel for k in sel[th] if res.get(k,{}).get('img') and os.path.exists(f"{D}/{ASSETS}/{res[k]['img']}"))
dist = ' · '.join(f"{t} {len(sel[t])}" for t,_ in THEMES)
miss_html = "".join(f"<li><b>{H.escape(k)}</b> — {H.escape(t)} <span class='muted'>({th})</span></li>" for th,k,t in missing) or "<li>none</li>"
calls_html = "".join(f"<li><b>{H.escape(k)}</b> {H.escape(t)} <span class='muted'>[{th}]</span> — {c}</li>" for th,k,t,c in calls)
nav = "".join(f'<a href="#{t.lower()}">{cn} {t} <small>{len(sel[t])}</small></a>' for t,cn in THEMES)
today = datetime.date.today().isoformat()
page = f'''<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>In Time / 时差 — {n_total} projects in six temporal dimensions</title>
<style>
:root{{--ink:#1d1a16;--mute:#6b6459;--rule:#e2dccf;--acc:#8a2b1b;--bg:#f6f2ea;--card:#fffdf8}}
*{{box-sizing:border-box}}body{{margin:0;font:15px/1.55 "Noto Serif SC","Songti SC",Georgia,serif;color:var(--ink);background:var(--bg)}}
.wrap{{max-width:1180px;margin:0 auto;padding:32px 28px 80px}}
.hero h1{{font-size:44px;line-height:1.05;margin:0 0 4px;letter-spacing:-.01em}}.hero .sub{{font-size:20px;color:var(--mute);margin:0 0 18px}}
.hero .dash{{display:flex;gap:18px;flex-wrap:wrap;font-size:13px;color:var(--mute);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:10px 0;margin:14px 0 22px}}
.stmt{{display:grid;grid-template-columns:1fr 1fr;gap:34px;margin:10px 0 26px}}.stmt h4{{margin:0 0 8px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}}.stmt p{{margin:0 0 10px;font-size:14.5px;text-align:justify}}
.legend{{background:var(--card);border:1px solid var(--rule);padding:16px 20px;margin:0 0 26px;font-size:14px}}.legend b{{color:var(--acc)}}
nav.themes{{position:sticky;top:0;background:var(--bg);z-index:5;display:flex;gap:6px;flex-wrap:wrap;padding:10px 0;border-bottom:1px solid var(--rule);margin-bottom:28px}}
nav.themes a{{text-decoration:none;color:var(--ink);border:1px solid var(--rule);padding:5px 10px;border-radius:999px;font-size:13px;background:var(--card)}}nav.themes a small{{color:var(--mute);margin-left:4px}}
section.theme{{margin:0 0 44px}}section.theme header{{display:flex;align-items:baseline;gap:14px;border-bottom:2px solid var(--ink);margin-bottom:16px}}section.theme h2{{font-size:28px;margin:0}}section.theme h2 .cn{{color:var(--acc)}}.count{{color:var(--mute);font-size:13px}}
.card{{display:grid;grid-template-columns:300px 1fr;gap:20px;background:var(--card);border:1px solid var(--rule);margin:0 0 14px;padding:16px}}
.media img{{width:100%;height:210px;object-fit:cover;display:block;background:#eee}}.credit{{font-size:10.5px;color:var(--mute);margin-top:4px}}
.ph{{height:210px;border:1px dashed #c9c1b2;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;color:var(--mute);font-size:12px;text-align:center;background:repeating-linear-gradient(45deg,#f3eee4 0 8px,#faf7f1 8px 16px)}}.phnum{{font-size:26px;font-weight:700;color:#b9b0a0}}
.kicker{{display:flex;gap:10px;align-items:center;font-size:12px;color:var(--mute)}}.num{{font-weight:700;color:var(--acc);font-size:13px}}.status{{border:1px solid var(--rule);padding:1px 8px;border-radius:999px}}
h3{{margin:4px 0 2px;font-size:20px;line-height:1.25}}.en{{font-size:14px;color:#3c372f;margin-bottom:2px}}.meta{{font-size:12.5px;color:var(--mute);margin-bottom:10px}}
.row{{display:grid;grid-template-columns:150px 1fr;gap:14px}}.prof{{text-align:center}}.proflab{{font-size:11px;color:var(--mute);line-height:1.35;margin-top:2px}}
.txt p{{margin:0 0 7px;font-size:13.5px}}.oot{{color:var(--acc)}}.gate{{color:#5c4a1e}}.call{{background:#fbf1e6;border-left:3px solid var(--acc);padding:6px 10px}}.pair{{background:#eef2ee;padding:6px 10px;font-size:13px;margin:6px 0}}
.links a{{margin-right:12px;font-size:13px;color:#2c4a7a}}.muted{{color:var(--mute)}}
.appendix{{border-top:2px solid var(--ink);padding-top:18px;margin-top:40px;font-size:14px}}.appendix h2{{font-size:22px}}.appendix li{{margin:0 0 6px}}
@media(max-width:820px){{.card{{grid-template-columns:1fr}}.stmt{{grid-template-columns:1fr}}.row{{grid-template-columns:1fr}}}}
@media print{{nav.themes{{position:static}}.card{{break-inside:avoid}}}}
</style></head><body><div class="wrap">
<header class="hero">
  <h1>In Time <span style="color:var(--acc)">/ 时差</span></h1>
  <p class="sub">Re-timing the Existing City · 重校既有城市的时间 — {n_total} projects across six temporal dimensions</p>
  <div class="stmt"><div><h4>Curatorial statement</h4>{paras(EN)}</div><div><h4>策展陈述（草稿）</h4>{paras(CN)}</div></div>
  <div class="legend"><b>How to read each card.</b> Every project holds all six temporal dimensions — <b>材料 Material · 生态 Ecological · 文化 Cultural · 维护 Maintenance · 资金 Financial · 技术 Technological</b> — in different proportions. The hexagonal <em>time-section profile</em> shows them bulging to different degrees (3 = the dimension the project was commissioned to serve, its filing category; 2 = dimensions it foregrounds; 1 = present but latent). <b>“Out of time with”</b> names the dimension it fails to keep pace with: that gap is the project's 时差. Cards marked <em>Curatorial call</em> are my selection judgments for Helena to keep or flip; <em>Gate</em> lines are the verification conditions before any invitation.</div>
</header>
<nav class="themes">{nav}</nav>
{"".join(cards)}
<section class="appendix" id="appendix">
  <h2>Appendix A — Selection calls made in this pool (for Helena to keep or flip)</h2><ul>{calls_html}</ul>
  <h2>Appendix B — Images still pending ({n_total-n_img})</h2><p class="muted">Sources on gooood.cn (Aliyun OSS) and ArchDaily's CDN block direct download; a browser save into <code>{ASSETS}/&lt;id&gt;.jpg</code> fills any card automatically on rebuild.</p><ul>{miss_html}</ul>
  <h2>Appendix C — Distribution</h2><p>{dist} = {n_total}. The thin native columns (Maintenance 2, Financial 3 in the raw pool) are filled here by swing calls, commissioned afterlife audits, and the art layer — the exhibition's own argument made visible rather than padded.</p>
  <p class="muted">Built from: Time_Differences_40_Project_Dossier (colleagues), In Time – Curatorial Review and Expanded Project Dossier (Chuany), In Time – Six Themes Project Organization (Chuany/Helena), Artwork Longlist. All verification gates from the 12 Sept review still apply.</p>
</section>
</div></body></html>'''
out = sys.argv[2] if len(sys.argv)>2 else f"{D}/In Time - Selected Projects in Six Temporal Dimensions.html"
open(out,'w',encoding='utf-8').write(page)
md = ["# In Time / 时差 — Selection Calls (Jane, 16 Sept 2026)", "",
      f"Companion to *In Time - Selected Projects in Six Temporal Dimensions.html* ({n_total} projects, six categories). Every judgment below is mine, for Helena to keep or flip; nothing is confirmed, invited or cleared.", "",
      "## Distribution", f"{dist} = {n_total}. Base = the proposed 30 (five per theme); top-ups from reserves/additions chosen to give the thin native columns (Maintenance 2, Financial 3) their commissioned audits, swing cases and art layer rather than padding.", "",
      "## Calls (by category)"]
for th,k,t,c in calls: md.append(f"- **{k}** {t} [{th}] — {re.sub(r'<[^>]+>','',c)}")
md += ["", "## Images pending", "Sources on gooood.cn (Aliyun OSS) and ArchDaily's CDN block direct download; a browser save into in-time-assets/<id>.jpg fills the card on rebuild."]
for th,k,t in missing: md.append(f"- {k} — {t} ({th})")
md += ["", "## Selection rule applied", "Filing category = the dimension the project was commissioned to serve (largest bulge on its time-section profile). \"Out of time with\" = the dimension it fails to keep pace with = its 时差. All six dimensions are present in every project to different degrees (Helena, 16 Sept)."]
if len(sys.argv)<=2: open(f"{D}/In Time - Selection Calls (Jane, 16 Sept).md","w",encoding="utf-8").write("\n".join(md))
print("BUILT", out, f"| {n_total} projects | {n_img} images | {len(calls)} calls | {len(missing)} missing")
