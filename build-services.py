# -*- coding: utf-8 -*-
"""messeze 서비스 서브페이지 6종 생성기
실행: python build-services.py  →  services/<slug>.html"""
import os, json, io

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "services")
os.makedirs(OUT, exist_ok=True)

CSS = """
:root{--ink:#0A1930;--navy:#101F3F;--body:#4A5568;--mut:#8B95A7;--cobalt:#2B5CFF;--cobalt-dk:#1E46D9;
--sky:#EAF1FF;--sky-2:#F5F8FD;--mint:#0BBF8C;--amber:#F59F1E;--red:#E2574C;--line:#E5EAF2;--line-2:#D8E0EC;
--sans:'Pretendard',system-ui,-apple-system,sans-serif;--disp:'Poppins',var(--sans);--maxw:1140px;
--sh-sm:0 1px 2px rgba(10,25,48,.05),0 4px 14px rgba(10,25,48,.05);--sh:0 12px 34px rgba(16,31,63,.10);--sh-lg:0 30px 70px rgba(16,31,63,.16)}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--sans);color:var(--ink);background:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
h1,h2,h3,h4{font-weight:800;letter-spacing:-.035em;line-height:1.28;word-break:keep-all}
.co{color:var(--cobalt)}
.sec{padding:88px 0}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:13.5px;font-weight:700;color:var(--cobalt);margin-bottom:14px}
.h2{font-size:clamp(24px,3.2vw,36px)}
.lead{font-size:16px;color:var(--body);line-height:1.7;margin-top:14px}
.shead{max-width:640px;margin-bottom:44px}
.shead.center{margin-left:auto;margin-right:auto;text-align:center}
.btn{font-family:var(--sans);font-weight:700;font-size:15.5px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:8px;border-radius:14px;padding:15px 26px;border:1.5px solid transparent;transition:.18s}
.btn-co{background:var(--cobalt);color:#fff;box-shadow:0 8px 22px rgba(43,92,255,.28)}
.btn-co:hover{background:var(--cobalt-dk);transform:translateY(-2px)}
.btn-gh{background:#fff;color:var(--ink);border-color:var(--line-2)}
.btn-gh:hover{border-color:var(--ink)}
.nav{position:sticky;top:0;z-index:70;background:rgba(255,255,255,.88);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.nav-in{display:flex;align-items:center;height:72px;gap:40px}
.nav .wrap{max-width:1480px;padding:0 clamp(16px,2.5vw,40px)}
.brand{display:flex;align-items:center;gap:9px}
.brand svg{width:25px;height:25px}
.brand .bw{font-family:var(--disp);font-weight:600;font-size:21px;letter-spacing:-.025em}
.nav-menu{display:flex;gap:6px;font-size:15px;font-weight:600;color:var(--body)}
.nav-menu a{padding:9px 13px;border-radius:10px}
.nav-menu a:hover{background:var(--sky-2);color:var(--ink)}
.nav-menu a.on{color:var(--cobalt)}
.nav-r{margin-left:auto}
.nav-cta{font-weight:700;font-size:14.5px;background:var(--ink);color:#fff;padding:12px 20px;border-radius:12px;transition:.18s}
.nav-cta:hover{background:var(--cobalt)}
.nav-burger{display:none;background:none;border:0;cursor:pointer;padding:10px 4px 10px 10px;flex:0 0 auto}
.nav-burger span{display:block;width:22px;height:2.5px;background:var(--ink);border-radius:2px;margin:4.5px 0;transition:.22s}
.nav-burger.on span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.nav-burger.on span:nth-child(2){opacity:0}
.nav-burger.on span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
.mega{position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 30px 60px rgba(16,31,63,.14);opacity:0;visibility:hidden;transform:translateY(-8px);transition:.22s;padding:32px 0 36px;z-index:80}
.mega.on{opacity:1;visibility:visible;transform:none}
.mega-in{display:grid;grid-template-columns:225px 1fr 1fr 1fr;gap:36px;align-items:stretch}
.mega-brand{background:linear-gradient(160deg,#101F3F,#2B5CFF);border-radius:18px;padding:24px 22px;display:flex;flex-direction:column;justify-content:flex-end;min-height:225px;color:#fff;transition:.2s}
.mega-brand:hover{transform:translateY(-3px)}
.mega-brand .bw2{font-family:var(--disp);font-weight:600;font-size:22px}
.mega-brand p{font-size:12.5px;color:#C7D6FF;margin-top:8px;line-height:1.55;font-weight:600}
.mega-col .h5x{font-size:11.5px;color:var(--mut);font-weight:800;letter-spacing:.05em;margin:0 0 8px 12px}
.mega-col .gap{height:20px}
.mega-col a{display:block;padding:9px 12px;border-radius:12px;transition:.15s}
.mega-col a b{font-size:14.2px;display:block;letter-spacing:-.01em}
.mega-col a span{font-size:12.2px;color:var(--mut);display:block;margin-top:1px}
.mega-col a:hover{background:var(--sky-2)}
.mega-col a:hover b{color:var(--cobalt)}
/* hero */
.crumb{font-size:13.5px;font-weight:600;color:var(--mut);padding:30px 0 0;display:flex;gap:8px;align-items:center}
.crumb a:hover{color:var(--cobalt)}
.crumb .cat{color:var(--cobalt);font-weight:700}
.phero{padding:34px 0 64px;background:linear-gradient(180deg,#F4F9FF,#fff)}
.phero-in{display:grid;grid-template-columns:1.02fr .98fr;gap:60px;align-items:center}
.phero .no{font-family:var(--disp);font-weight:700;font-size:15px;color:var(--cobalt)}
.phero h1{font-size:clamp(30px,4.2vw,46px);margin-top:10px}
.phero .sub{font-size:16.5px;color:var(--body);margin-top:18px;line-height:1.68;max-width:480px}
.ai-view{margin-top:22px;background:var(--ink);color:#DDE4F2;border-radius:16px;padding:18px 22px;font-size:14.3px;line-height:1.65;font-weight:600;position:relative;overflow:hidden}
.ai-view::before{content:"";position:absolute;inset:0;background:radial-gradient(300px 140px at 95% 100%,rgba(43,92,255,.4),transparent 60%)}
.ai-view .avl{position:relative;display:block;font-size:11px;font-weight:800;color:#7FA0FF;letter-spacing:.05em;margin-bottom:7px}
.ai-view p{position:relative}
.phero .cta{margin-top:26px;display:flex;gap:12px;flex-wrap:wrap}
/* visuals */
.svc-vis{position:relative;min-height:420px}
.mini-win{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:var(--sh)}
.mw-bar{display:flex;gap:6px;align-items:center;padding:11px 14px;border-bottom:1px solid var(--line);background:#FAFBFD}
.mw-bar i{width:9px;height:9px;border-radius:50%;background:#E3E9F4}
.mw-bar .u{margin-left:8px;flex:1;background:#F1F4FA;border-radius:7px;font-size:11px;color:var(--mut);padding:5px 10px;font-weight:600}
.mw-body{padding:18px 20px 20px}
.sticker{position:absolute;font-weight:800;font-size:13px;padding:8px 16px;border-radius:999px;box-shadow:0 6px 16px rgba(16,31,63,.16);white-space:nowrap;z-index:5}
.sticker.blue{background:var(--cobalt);color:#fff}
.sticker.white{background:#fff;color:var(--navy);border:1px solid var(--line)}
.sticker.dark{background:var(--ink);color:#fff}
.rep{position:absolute;top:50%;left:2%;width:92%;transform:translateY(-50%) rotate(-1.4deg)}
.rep .row{display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid var(--sky-2);font-size:13.5px;font-weight:700}
.rep .row:last-child{border:0}
.rep .row .en{width:96px;color:var(--ink)}
.rep .row .bt{flex:1;height:6px;border-radius:4px;background:#EEF2F9;overflow:hidden}
.rep .row .bt i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--cobalt),#6E93FF)}
.rep .row .st{font-size:11.5px;font-weight:800}
.rep .row .st.ok{color:var(--mint)}
.rep .row .st.no{color:var(--red)}
.rep .gaugerow{display:flex;align-items:center;gap:18px;padding-bottom:14px;margin-bottom:6px;border-bottom:1px dashed var(--line)}
.rep .gaugerow svg{width:88px;height:88px;flex:0 0 auto}
.rep .gaugerow .t b{font-family:var(--disp);font-size:24px;font-weight:700;display:block}
.rep .gaugerow .t span{font-size:12.5px;color:var(--mut);font-weight:600}
.ba .cwb{position:absolute;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}
.ba .cwb.before{top:6px;left:0;width:58%;transform:rotate(-4deg);box-shadow:0 14px 34px rgba(16,31,63,.10);z-index:1}
.ba .cwb.before .mw-body{filter:grayscale(.9);opacity:.85}
.ba .cwb.after{bottom:0;right:0;width:66%;transform:rotate(1.4deg);box-shadow:0 30px 64px rgba(16,31,63,.2);z-index:3;border-color:#C4D4FF}
.tagchips{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.tagchips span{font-size:11px;font-weight:800;border-radius:7px;padding:5px 9px}
.tagchips .bad{background:#FDECEA;color:var(--red)}
.tagchips .good{background:rgba(11,191,140,.12);color:#08916B}
.skl{height:8px;border-radius:4px;background:#EEF2F9;margin:9px 0}
.skl.s{width:76%}
.skl.xs{width:52%}
.skl.dark{background:#DCE3F0;height:11px;width:64%}
.tree{position:absolute;top:50%;left:0;width:100%;transform:translateY(-50%)}
.tree .root{margin:0 auto;width:fit-content;background:var(--ink);color:#fff;font-weight:800;font-size:14px;border-radius:12px;padding:11px 20px;box-shadow:var(--sh)}
.tree .lvl{display:flex;justify-content:center;gap:12px;margin-top:34px;position:relative;flex-wrap:wrap}
.tree .lvl::before{content:"";position:absolute;top:-20px;left:15%;right:15%;height:1.5px;background:var(--line-2)}
.tree .node{background:#fff;border:1px solid var(--line);border-radius:11px;padding:10px 14px;font-size:12.8px;font-weight:700;box-shadow:var(--sh-sm);position:relative}
.tree .node::before{content:"";position:absolute;top:-20px;left:50%;width:1.5px;height:20px;background:var(--line-2)}
.tree .node em{font-style:normal;display:block;font-size:10.5px;color:var(--cobalt);font-weight:800;margin-top:2px}
.tree .node.q{border-color:#C4D4FF;background:var(--sky)}
.artwin{position:absolute;top:50%;left:4%;width:88%;transform:translateY(-50%) rotate(-1.2deg)}
.artwin .ttl{font-size:16.5px;font-weight:800;line-height:1.45}
.artwin .meta{font-size:11.5px;color:var(--mut);font-weight:700;margin:8px 0 12px}
.artwin .ansbox{background:var(--sky-2);border:1px solid var(--line);border-radius:11px;padding:12px 14px;font-size:12.8px;color:var(--body);line-height:1.6}
.artwin .ansbox b{color:var(--ink)}
.cal{position:absolute;right:-2%;bottom:4%;background:#fff;border:1px solid var(--line);border-radius:16px;box-shadow:var(--sh-lg);padding:14px 15px 15px;transform:rotate(2deg);z-index:4;width:176px}
.cal .cl{font-size:11.5px;font-weight:800;color:var(--ink);margin-bottom:11px;display:flex;justify-content:space-between;align-items:center;gap:8px}
.cal .cl em{font-style:normal;font-size:9.5px;font-weight:800;color:var(--cobalt);background:var(--sky);border-radius:6px;padding:2px 7px;white-space:nowrap}
.cal-hd{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;margin-bottom:6px}
.cal-hd span{font-size:9px;font-weight:800;color:var(--mut);text-align:center}
.cal-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:5px}
.cal-grid i{aspect-ratio:1;border-radius:6px;background:#EEF2F9}
.cal-grid i.pub{background:linear-gradient(150deg,#2B5CFF,#6E93FF);box-shadow:0 3px 8px rgba(43,92,255,.32);position:relative}
.cal-grid i.pub::after{content:"";position:absolute;inset:0;margin:auto;width:5px;height:5px;border-radius:50%;background:#fff}
.radial{position:absolute;top:50%;left:0;width:100%;transform:translateY(-50%)}
.radial .hub{margin:0 auto;width:fit-content;background:var(--ink);color:#fff;border-radius:14px;padding:14px 22px;font-weight:800;font-size:14px;box-shadow:var(--sh);position:relative;z-index:2;text-align:center}
.radial .hub em{font-style:normal;display:block;font-size:10.5px;color:#7FA0FF;font-weight:800}
.radial .spokes{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:40px;position:relative}
.radial .spokes::before{content:"";position:absolute;top:-26px;left:16%;right:16%;height:1.5px;background:var(--line-2)}
.radial .ch{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;box-shadow:var(--sh-sm);position:relative;text-align:center}
.radial .ch::before{content:"";position:absolute;top:-26px;left:50%;width:1.5px;height:26px;background:var(--line-2)}
.radial .ch b{font-size:14px;display:block}
.radial .ch em{font-style:normal;font-size:11px;font-weight:800;display:inline-block;margin-top:8px;border-radius:999px;padding:4px 10px}
.radial .ch.nv em{background:rgba(11,191,140,.13);color:#08916B}
.radial .ch.ts em{background:var(--sky);color:var(--cobalt)}
.radial .ch.gb em{background:#FFF3E0;color:#C77700}
.radial .ch span{display:block;font-size:11.8px;color:var(--mut);font-weight:600;margin-top:6px;line-height:1.5}
.clips .clip{position:absolute;background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 20px;box-shadow:var(--sh)}
.clips .clip .pressname{font-size:10.5px;font-weight:800;color:var(--mut);letter-spacing:.06em}
.clips .clip .clip-h{font-size:14.5px;font-weight:800;line-height:1.45;margin-top:7px;letter-spacing:-.01em}
.clips .clip.c1{top:0;left:0;width:52%;transform:rotate(-3.5deg);z-index:1}
.clips .clip.c2{top:16%;right:0;width:55%;transform:rotate(1.6deg);z-index:3;border-color:#C4D4FF;box-shadow:0 26px 56px rgba(16,31,63,.18)}
.clips .clip.c3{top:41%;left:5%;width:52%;transform:rotate(-1.8deg);z-index:2}
.clips .flowrow{position:absolute;bottom:6%;left:4%;right:4%;display:flex;align-items:center;gap:8px;flex-wrap:wrap;font-size:12px;font-weight:800;color:var(--body)}
.clips .flowrow span{background:#fff;border:1px solid var(--line);border-radius:999px;padding:7px 13px;box-shadow:var(--sh-sm)}
.clips .flowrow i{font-style:normal;color:#B9C2D4}
.clips .flowrow span.hl{background:var(--cobalt);color:#fff;border-color:var(--cobalt)}
/* ===== 히어로 비주얼 내부 모션 (게이지·막대·노드 채움/순차 등장) — .svc-vis.in 재생. transition 기반이라 reduced-motion서 자동 즉시표시 ===== */
/* 01 가시성 — 게이지 채움 + 엔진 막대 채움 + 상태 라벨 */
.rep .gaugerow svg circle:nth-child(2){stroke-dashoffset:314}
.svc-vis.in .rep .gaugerow svg circle:nth-child(2){stroke-dashoffset:198;transition:stroke-dashoffset 1.4s .4s cubic-bezier(.3,.8,.3,1)}
.rep .row .bt i{transform-origin:left;transform:scaleX(0)}
.svc-vis.in .rep .row .bt i{transform:scaleX(1);transition:transform .95s cubic-bezier(.3,.9,.3,1)}
.svc-vis.in .rep .row:nth-child(2) .bt i{transition-delay:.55s}
.svc-vis.in .rep .row:nth-child(3) .bt i{transition-delay:.7s}
.svc-vis.in .rep .row:nth-child(4) .bt i{transition-delay:.85s}
.svc-vis.in .rep .row:nth-child(5) .bt i{transition-delay:1s}
.rep .row .st{opacity:0}
.svc-vis.in .rep .row .st{opacity:1;transition:opacity .45s 1.2s}
/* 02 리뉴얼 — After 카드가 뒤이어 팝인 */
.ba .cwb.after{opacity:0;transform:rotate(1.4deg) scale(.9)}
.svc-vis.ba.in .cwb.after{opacity:1;transform:rotate(1.4deg) scale(1);transition:opacity .5s .12s,transform .62s .12s cubic-bezier(.3,1.25,.4,1)}
/* 03 제작 — 루트 → 노드 순차 낙하 */
.tree .root{opacity:0;transform:translateY(-10px)}
.svc-vis.in .tree .root{opacity:1;transform:none;transition:.6s cubic-bezier(.3,1.2,.4,1)}
.tree .lvl .node{opacity:0;transform:translateY(13px)}
.svc-vis.in .tree .lvl .node{opacity:1;transform:none;transition:.55s cubic-bezier(.3,1.2,.4,1)}
.svc-vis.in .tree .lvl .node:nth-child(1){transition-delay:.45s}
.svc-vis.in .tree .lvl .node:nth-child(2){transition-delay:.65s}
.svc-vis.in .tree .lvl .node:nth-child(3){transition-delay:.85s}
.svc-vis.in .tree .lvl .node:nth-child(4){transition-delay:1.05s}
.svc-vis.in .tree .lvl .node:nth-child(5){transition-delay:1.25s}
/* 04 블로그 — 답변 박스 등장 + 캘린더 도트 팝 */
.artwin .ansbox{opacity:0;transform:translateY(9px)}
.svc-vis.in .artwin .ansbox{opacity:1;transform:none;transition:.6s .45s cubic-bezier(.3,1,.4,1)}
.cal-grid i{transform:scale(0)}
.svc-vis.in .cal-grid i{transform:scale(1);transition:transform .4s cubic-bezier(.3,1.6,.4,1) .5s}
/* 05 채널 — 허브 → 스포크 순차 */
.radial .hub{opacity:0;transform:translateY(-9px)}
.svc-vis.in .radial .hub{opacity:1;transform:none;transition:.6s cubic-bezier(.3,1.2,.4,1)}
.radial .spokes .ch{opacity:0;transform:translateY(15px)}
.svc-vis.in .radial .spokes .ch{opacity:1;transform:none;transition:.55s cubic-bezier(.3,1.2,.4,1)}
.svc-vis.in .radial .spokes .ch:nth-child(1){transition-delay:.45s}
.svc-vis.in .radial .spokes .ch:nth-child(2){transition-delay:.7s}
.svc-vis.in .radial .spokes .ch:nth-child(3){transition-delay:.95s}
/* 06 언론 — 클립 팝인 + 플로우 좌→우 순차 */
.clips .clip.c1{opacity:0;transform:rotate(-3.5deg) translateY(15px)}
.clips .clip.c2{opacity:0;transform:rotate(1.6deg) translateY(15px)}
.clips .clip.c3{opacity:0;transform:rotate(-1.8deg) translateY(15px)}
.svc-vis.clips.in .clip.c1{opacity:1;transform:rotate(-3.5deg);transition:opacity .55s .2s,transform .7s .2s cubic-bezier(.3,1.3,.4,1)}
.svc-vis.clips.in .clip.c2{opacity:1;transform:rotate(1.6deg);transition:opacity .55s .45s,transform .7s .45s cubic-bezier(.3,1.3,.4,1)}
.svc-vis.clips.in .clip.c3{opacity:1;transform:rotate(-1.8deg);transition:opacity .55s .7s,transform .7s .7s cubic-bezier(.3,1.3,.4,1)}
.clips .flowrow>span,.clips .flowrow>i{opacity:0;transform:translateY(7px)}
.svc-vis.clips.in .flowrow>span,.svc-vis.clips.in .flowrow>i{opacity:1;transform:none;transition:.45s cubic-bezier(.3,1.2,.4,1)}
.svc-vis.clips.in .flowrow>*:nth-child(1){transition-delay:.7s}
.svc-vis.clips.in .flowrow>*:nth-child(2){transition-delay:.8s}
.svc-vis.clips.in .flowrow>*:nth-child(3){transition-delay:.9s}
.svc-vis.clips.in .flowrow>*:nth-child(4){transition-delay:1s}
.svc-vis.clips.in .flowrow>*:nth-child(5){transition-delay:1.1s}
.svc-vis.clips.in .flowrow>*:nth-child(6){transition-delay:1.2s}
.svc-vis.clips.in .flowrow>*:nth-child(7){transition-delay:1.3s}
.svc-photo{max-width:980px;margin:0 auto 38px;border-radius:22px;overflow:hidden;position:relative;box-shadow:var(--sh);background:#EEF2F9}
.svc-photo img{width:100%;height:auto;display:block;aspect-ratio:16/9;object-fit:cover}
.svc-photo figcaption{position:absolute;left:0;right:0;bottom:0;padding:44px 30px 22px;background:linear-gradient(180deg,transparent,rgba(10,25,48,.86));color:#fff;font-size:15px;font-weight:700}
@media(max-width:640px){.svc-photo figcaption{font-size:13.5px;padding:34px 20px 16px}}
/* 진행 흐름 미니 플로우 */
.hflow-mini{max-width:980px;margin:0 auto 34px;background:#fff;border:1px solid var(--line);border-radius:20px;padding:26px 28px;box-shadow:var(--sh-sm)}
.hflow-mini h4{font-size:14.5px;margin-bottom:4px}
.hflow-mini .hm-sub{font-size:12.5px;color:var(--mut);margin-bottom:20px}
.hm-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;position:relative}
.hm-step{background:var(--sky-2);border:1px solid var(--line);border-radius:14px;padding:16px 15px;position:relative;transition:.25s}
.hm-step:hover{border-color:#C4D4FF;transform:translateY(-3px);background:#fff}
.hm-step .hn{font-family:var(--disp);font-size:11px;font-weight:800;color:var(--cobalt);display:block;margin-bottom:7px}
.hm-step b{font-size:13.5px;display:block;line-height:1.4}
.hm-step span{display:block;font-size:11.5px;color:var(--mut);margin-top:6px;line-height:1.5;font-weight:600}
.hm-step::after{content:"→";position:absolute;right:-11px;top:50%;transform:translateY(-50%);color:#C4D4FF;font-size:14px;font-weight:800;z-index:2}
.hm-step:last-child::after{display:none}
@media(max-width:820px){.hm-row{grid-template-columns:1fr 1fr}.hm-step::after{display:none}}







.dg-rows{max-width:880px;margin:0 auto;border-top:1px solid var(--line)}
.dg-row{display:grid;grid-template-columns:64px 240px 1fr;gap:20px;align-items:baseline;padding:24px 4px;border-bottom:1px solid var(--line)}
.dg-no{font-family:var(--disp);font-size:15px;font-weight:700;color:var(--cobalt)}
.dg-row b{font-size:16.5px;letter-spacing:-.01em;color:var(--ink);word-break:keep-all}
.dg-row p{font-size:14.5px;color:var(--body);line-height:1.66;margin:0;word-break:keep-all}
@media(max-width:820px){.dg-row{grid-template-columns:44px 1fr;gap:8px 14px}.dg-row p{grid-column:2}}

/* detail lists */
.dt-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.dt{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px 26px}
.dt .c{font-size:12px;font-weight:800;color:var(--mint)}
.dt b{font-size:16.5px;display:block;margin-top:8px;letter-spacing:-.01em}
.dt p{font-size:13.8px;color:var(--body);line-height:1.62;margin-top:7px}
/* process */
.proc{background:linear-gradient(180deg,#E4ECFF,#F4F9FF 72%)}
.pr-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;counter-reset:pr}
.pr{background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:24px 22px;position:relative;transition:opacity .6s cubic-bezier(.2,.7,.2,1),transform .6s cubic-bezier(.2,.7,.2,1),border-color .5s ease,box-shadow .5s ease}
.pr .n{font-family:var(--disp);font-weight:700;font-size:14px;color:#fff;background:#AEBBD4;width:34px;height:34px;border-radius:11px;display:grid;place-items:center;margin-bottom:14px;transition:background .5s ease,box-shadow .5s ease,transform .5s cubic-bezier(.3,1.4,.4,1)}
/* 진행 절차 — 화면 고정(핀) + 스크롤에 따라 1→2→3→4 순서대로 채워짐 */
.proc{background:linear-gradient(180deg,#E4ECFF,#F4F9FF 72%);padding:84px 0}
.proc .pr.in{border-color:#B9CCFF;box-shadow:0 18px 44px rgba(43,92,255,.14)}
.proc .pr.in .n{background:linear-gradient(135deg,#2B5CFF,#6E93FF);box-shadow:0 8px 18px rgba(43,92,255,.34);transform:scale(1.06)}
.pr-grid .pr:nth-child(2){transition-delay:.12s}
.pr-grid .pr:nth-child(3){transition-delay:.24s}
.pr-grid .pr:nth-child(4){transition-delay:.36s}
.pr b{font-size:15.5px;display:block}
.pr p{font-size:13px;color:var(--body);line-height:1.58;margin-top:6px}
/* fit + deliv */
.fitrow{display:grid;grid-template-columns:1.05fr .95fr;gap:40px;align-items:start}
.fit-list{border-top:1px solid var(--line)}
.fit-list div{display:flex;gap:12px;padding:16px 4px;border-bottom:1px solid var(--line);font-size:15.5px;font-weight:600}
.fit-list .c{font-size:12px;font-weight:800;color:var(--mint);padding-top:4px}
.dv-card{background:var(--ink);color:#fff;border-radius:20px;padding:30px 28px;position:relative;overflow:hidden}
.dv-card::before{content:"";position:absolute;inset:0;background:radial-gradient(360px 200px at 92% 100%,rgba(43,92,255,.4),transparent 60%)}
.dv-card h3{color:#fff;font-size:19px;position:relative}
.dv-card .chips{position:relative;display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.dv-card .chips span{font-size:13px;font-weight:700;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:8px 15px}
.dv-card .dvl{position:relative;display:flex;flex-direction:column;gap:12px;margin-top:20px}
.dvi{display:flex;gap:14px;align-items:flex-start;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:15px 17px}
.dvi i{font-style:normal;font-family:var(--disp);font-weight:700;font-size:12.5px;color:#8FB0FF;padding-top:2px;flex:0 0 auto}
.dvi b{font-size:14.8px;display:block}
.dvi p{font-size:12.8px;color:#C9D6F5;margin-top:3px;line-height:1.55}
.prcheck{max-width:820px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:20px;box-shadow:var(--sh);padding:30px 32px;display:grid;grid-template-columns:1fr 1.1fr;gap:30px;align-items:center}.prc-score{text-align:center}.prc-gauge{display:inline-flex;align-items:baseline;gap:2px;font-family:var(--disp);color:var(--cobalt)}.prc-gauge b{font-size:52px;font-weight:700;line-height:1}.prc-gauge span{font-size:16px;font-weight:700}.prc-score p{font-size:13px;color:var(--body);margin-top:10px;line-height:1.6}.prc-items{display:flex;flex-direction:column;gap:11px}.prc-i{display:grid;grid-template-columns:82px 1fr 46px;gap:10px;align-items:center;font-size:13px;font-weight:700}.prc-i i{height:8px;border-radius:4px;background:#EEF2F9;overflow:hidden;display:block}.prc-i i em{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--cobalt),#6E93FF)}.prc-i b{text-align:right;font-family:var(--disp);color:var(--mut)}.prc-cta{max-width:820px;margin:22px auto 0;background:var(--ink);color:#fff;border-radius:18px;padding:24px 28px;text-align:center}.prc-cta b{font-size:16px;display:block}.prc-cta span{display:block;font-size:13.5px;color:#AEB9D2;margin:8px 0 16px}@media(max-width:720px){.prcheck{grid-template-columns:1fr;gap:22px}}
/* faq */
.faq{max-width:760px;margin:0 auto}
.qa{border:1px solid var(--line);border-radius:16px;margin-bottom:12px;background:#fff;overflow:hidden;transition:.2s}
.qa.open{border-color:var(--ink);box-shadow:var(--sh-sm)}
.qa button{width:100%;text-align:left;background:none;border:0;cursor:pointer;padding:20px 24px;font-family:var(--sans);font-size:16px;font-weight:700;color:var(--ink);display:flex;justify-content:space-between;align-items:center;gap:16px}
.qa .ico{flex:0 0 26px;height:26px;border-radius:9px;background:var(--sky-2);display:grid;place-items:center;font-size:15px;transition:.2s}
.qa.open .ico{background:var(--ink);color:#fff;transform:rotate(45deg)}
.qa .ans{max-height:0;overflow:hidden;transition:max-height .3s ease;color:var(--body);font-size:14.8px;line-height:1.68}
.qa .ans p{padding:0 24px 20px}
/* related */
.rel-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:760px;margin:0 auto}
.relc{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px 26px;transition:transform .3s cubic-bezier(.34,1.2,.4,1),box-shadow .3s ease,border-color .3s ease;display:block}
.relc:hover{box-shadow:0 22px 48px rgba(20,32,68,.14);transform:translateY(-7px);border-color:#B9CCFF}
.relc .no{transition:color .3s ease}
.relc:hover .no{color:var(--cobalt)}
.relc b{transition:color .3s ease}
.relc:hover b{color:var(--cobalt)}
.relc .no{font-family:var(--disp);font-size:12.5px;font-weight:700;color:var(--cobalt)}
.relc b{font-size:17px;display:block;margin-top:6px}
.relc span{font-size:13px;color:var(--mut);display:block;margin-top:4px}
.svcta{background:linear-gradient(180deg,#0B1533 0%,#101F3F 60%,#0A1224 100%);color:#fff;text-align:center;padding:92px 0;position:relative;overflow:hidden}
.svcta::before{content:"";position:absolute;inset:0;background:radial-gradient(720px 380px at 50% -10%,rgba(43,92,255,.32),transparent 62%),radial-gradient(520px 300px at 85% 110%,rgba(43,92,255,.16),transparent 60%)}
.svcta .wrap{position:relative}
.svcta h2{color:#fff;font-size:clamp(26px,3.6vw,42px);letter-spacing:-.03em;line-height:1.28}
.svcta p{color:#DCE6FF;font-size:16px;margin-top:16px;line-height:1.7}
.svcta .sbtn{display:inline-flex;align-items:center;gap:10px;background:#fff;color:var(--cobalt);font-weight:800;font-size:16px;border-radius:14px;padding:17px 34px;margin-top:32px;box-shadow:0 14px 34px rgba(10,25,48,.24);transition:.2s}
.svcta .sbtn:hover{transform:translateY(-3px);box-shadow:0 20px 44px rgba(10,25,48,.3)}
.svcta-stats{display:flex;justify-content:center;gap:56px;margin-top:52px;flex-wrap:wrap}
.svcta-stats div{text-align:center}
.svcta-stats b{display:block;font-size:19px;font-weight:800;color:#fff;letter-spacing:-.02em}
.svcta-stats span{display:block;font-size:12.5px;color:#BCCCFF;margin-top:6px;font-weight:600}
@media(max-width:640px){.svcta{padding:66px 0}.svcta-stats{gap:28px}}
/* cta foot */
.cta-band{background:var(--ink);border-radius:24px;padding:46px 40px;display:flex;justify-content:space-between;align-items:center;gap:26px;flex-wrap:wrap;color:#fff;position:relative;overflow:hidden;margin:70px auto}
.cta-band::before{content:"";position:absolute;inset:0;background:radial-gradient(520px 280px at 90% 100%,rgba(43,92,255,.4),transparent 60%)}
.cta-band h3{font-size:clamp(20px,2.6vw,27px);color:#fff;position:relative}
.cta-band p{color:#AEB9D2;font-size:14.5px;margin-top:8px;position:relative}
.cta-band .btn{position:relative;background:var(--cobalt);color:#fff}
.cta-band .btn:hover{background:#4270FF}
.reltool{display:flex;align-items:center;justify-content:space-between;gap:24px;background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:26px 30px;margin:40px auto 0;box-shadow:0 1px 2px rgba(10,25,48,.05),0 4px 14px rgba(10,25,48,.05);transition:.2s;flex-wrap:wrap;text-align:left}
.reltool:hover{border-color:#C4D4FF;box-shadow:0 12px 34px rgba(16,31,63,.1);transform:translateY(-3px)}
.reltool .rt-tag{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:800;color:var(--cobalt);margin-bottom:9px}
.reltool .rt-tag::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--cobalt)}
.reltool h3{font-size:20px;letter-spacing:-.02em}
.reltool p{font-size:14px;color:var(--body);margin-top:7px;line-height:1.55;max-width:560px}
.reltool .rt-go{flex:0 0 auto;font-weight:800;font-size:14.5px;color:var(--cobalt);background:var(--sky);border-radius:12px;padding:12px 20px;white-space:nowrap}
.foot{background:#070D1C;color:#7C879D;padding:52px 0 38px}
.foot-in{display:flex;justify-content:space-between;gap:36px;flex-wrap:wrap}
.foot .brand{color:#fff;margin-bottom:14px}
.foot p{font-size:13.5px;line-height:1.7;max-width:320px}
.foot-b{margin-top:38px;padding-top:22px;border-top:1px solid #141C30;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;font-size:12.5px;color:#4E5A73}
.rv{opacity:0;transform:translateY(22px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.rv.in{opacity:1;transform:none}
/* 히어로(1번 섹션) 좌우 미끄러지는 등장 */
.phero-in>.rv{transform:translateX(-34px);transition-duration:.85s}
.phero-in>.svc-vis.rv{transform:translateX(34px);transition-delay:.12s}
.phero-in>.rv.in,.phero-in>.svc-vis.rv.in{transform:none}
/* 히어로 카드 은은하게 떠다니는 모션 (메인 히어로 카드와 동일 톤) — transform 슬라이드와 충돌 안 나게 translate 사용 */
.phero-in>.svc-vis{animation:svcFloat 6.6s 1.7s ease-in-out infinite;will-change:translate}
@keyframes svcFloat{0%,100%{translate:0 0}50%{translate:0 -9px}}
@media(max-width:980px){
  .nav-menu{display:none}.nav-burger{display:block}.mega{max-height:calc(100vh - 72px);overflow:auto}.mega-in{grid-template-columns:1fr;gap:18px}.mega-brand{min-height:auto;padding:18px 20px}
  .phero-in,.fitrow{grid-template-columns:1fr;gap:40px}
  .dt-grid{grid-template-columns:1fr}
  .pr-grid{grid-template-columns:1fr 1fr}
  .rel-grid{grid-template-columns:1fr}
  .svc-vis{min-height:400px}
}

@media(max-width:560px){.sec{padding:64px 0}.pr-grid{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}.rv,.phero-in>.rv,.phero-in>.svc-vis.rv,.proc .pr{opacity:1;transform:none;translate:none}}
"""

LOGO = """<svg viewBox="0 0 100 100" fill="none"><path d="M38 24 16 71" stroke="currentColor" stroke-width="17" stroke-linecap="round"/><path d="M72 24 51 71" stroke="#2B5CFF" stroke-width="17" stroke-linecap="round"/><circle cx="85" cy="69" r="9" fill="#2B5CFF"/></svg>"""

FONT_LINKS = """<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@1.3.9/dist/web/static/pretendard.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">"""

P = "../"  # depth 1

def mega():
    p = P
    return f"""<div class="mega" id="mega"><div class="wrap mega-in">
<a class="mega-brand" href="{p}index.html"><span class="bw2">messeze</span><p>사람에게만 보이는 홍보에서,<br>AI가 읽는 홍보로</p></a>
<div class="mega-col"><div class="h5x">서비스</div>
<a href="visibility.html"><b>AI 가시성 평가</b><span>AI가 우리 회사를 아는지부터</span></a>
<a href="website-renewal.html"><b>홈페이지 수정·리뉴얼</b><span>AI가 읽는 구조로 정비</span></a>
<a href="website-build.html"><b>홈페이지 제작</b><span>질문이 페이지가 되는 설계</span></a>
<a href="own-blog.html"><b>자사 블로그 운영</b><span>도메인에 쌓이는 전문성</span></a>
<a href="channels.html"><b>외부 채널 운영</b><span>네이버·티스토리·구글 블로거</span></a>
<a href="press.html"><b>언론 배포</b><span>기자 매칭 · 보도자료 · 기사화</span></a></div>
<div class="mega-col"><div class="h5x">무료 도구</div>
<a href="{p}check.html"><b>AI 노출 무료 진단</b><span>URL만 넣으면 30초 진단</span></a>
<a href="{p}tools.html#pr"><b>PR 플랜 추천</b><span>3가지 질문으로 플랜 찾기</span></a>
<div class="gap"></div><div class="h5x">요금</div>
<a href="{p}pricing.html"><b>플랜 비교</b><span>베이직 · 프리미엄 · 엔터프라이즈</span></a>
<a href="{p}pricing.html#faq"><b>요금 FAQ</b><span>약정 · 수량 · 바우처 연계</span></a></div>
<div class="mega-col"><div class="h5x">리소스</div>
<a href="{p}blog/index.html"><b>블로그</b><span>AI 검색 시대의 홍보 인사이트</span></a>
<a href="{p}interview.html"><b>인터뷰</b><span>먼저 시작한 기업들의 이야기</span></a>
<a href="{p}glossary/index.html"><b>용어사전</b><span>SEO·AEO·GEO·PR 용어 102개</span></a></div>
</div></div>"""

MEGA_JS = """<script>
(function(){const p=document.getElementById('mega'),t=document.querySelector('.nav-menu'),b=document.getElementById('burger');if(!p)return;let m;const o=()=>{clearTimeout(m);p.classList.add('on')},c=()=>{m=setTimeout(()=>p.classList.remove('on'),140)};if(t){t.addEventListener('mouseenter',o);t.addEventListener('mouseleave',c);t.querySelectorAll('a').forEach(a=>a.addEventListener('mouseenter',o));}if(window.matchMedia('(hover:hover)').matches){p.addEventListener('mouseenter',o);p.addEventListener('mouseleave',c);}if(b){b.addEventListener('click',()=>{const on=p.classList.toggle('on');b.classList.toggle('on',on);});p.addEventListener('click',e=>{if(e.target.closest('a')){p.classList.remove('on');b.classList.remove('on');}});}})();
</script>"""

def nav():
    p = P
    return f"""<header class="nav"><div class="wrap nav-in">
<a class="brand" href="{p}index.html"><img src="{p}assets/logo.png" alt="messeze" style="height:26px;width:auto;display:block"></a>
<nav class="nav-menu">
<a class="on" href="{p}services.html">서비스</a>
<a href="{p}pricing.html">요금</a>
<a href="{p}check.html">AI 노출 진단</a>
<a href="{p}blog/index.html">블로그</a>
<a href="{p}interview.html">인터뷰</a>
<a href="{p}glossary/index.html">용어사전</a>
</nav>
<div class="nav-r"><a class="nav-cta" href="{p}index.html#final">무료 진단 받기</a></div>
<button class="nav-burger" id="burger" aria-label="메뉴 열기"><span></span><span></span><span></span></button>
</div>
{mega()}
</header>
{MEGA_JS}"""

def foot():
    p = P
    return f"""<footer class="foot"><style>.foot{{background:#070D1C;color:#7C879D;padding:60px 0 42px;font-size:13.5px}}.foot a{{color:inherit;text-decoration:none}}.foot .wrap{{max-width:1140px;margin:0 auto;padding:0 24px}}.foot-in{{display:flex;justify-content:space-between;gap:40px;flex-wrap:wrap}}.foot .brand{{color:#fff;margin-bottom:16px;display:inline-block}}.foot p{{font-size:13.5px;line-height:1.7;max-width:320px;margin:0}}.foot-info{{font-size:12.5px;line-height:1.7;color:#7C879D;margin-top:14px}}.foot-cols{{display:flex;gap:56px}}.foot-col .h5x{{color:#C3CBDC;font-size:13.5px;margin:0 0 15px;font-weight:800}}.foot-col a{{display:block;font-size:14px;margin-bottom:10px}}.foot-col a:hover{{color:#fff}}.foot-b{{margin-top:46px;padding-top:24px;border-top:1px solid #141C30;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:12.5px;color:#4E5A73}}@media(max-width:720px){{.foot-cols{{gap:32px;flex-wrap:wrap}}}}</style><div class="wrap"><div class="foot-in">
<div><a class="brand" href="{p}index.html"><img src="{p}assets/logo-white.png" alt="messeze" style="height:24px;width:auto;display:block"></a>
<p>AI 시대, 고객이 우리 회사를 발견하도록 만드는 새로운 기업 정보 관리 서비스.</p>
<div class="foot-info">주식회사 메세지 · 주식회사 퍼스트마케팅컴퍼니<br>대구광역시 중구 국채보상로 488, 3층<br>대표번호 1600-9487 · sales@firstmkt.co.kr</div></div>
<div class="foot-cols">
<div class="foot-col"><div class="h5x">서비스</div><a href="{p}services.html">서비스 상세</a><a href="{p}pricing.html">요금</a><a href="{p}check.html">AI 노출 진단</a></div>
<div class="foot-col"><div class="h5x">리소스</div><a href="{p}blog/index.html">블로그</a><a href="{p}interview.html">인터뷰</a><a href="{p}glossary/index.html">용어사전</a><a href="{p}faq.html">FAQ</a></div>
<div class="foot-col"><div class="h5x">회사</div><a href="{p}index.html#final">상담 신청</a><a href="{p}index.html#final">무료 진단</a></div>
</div>
</div><div class="foot-b"><span>© 2026 messeze</span><span>사람에게만 보이는 홍보에서, AI가 읽는 홍보로</span></div></div></footer>"""

FAQ_JS = """<script>
const io=new IntersectionObserver(es=>{es.forEach(e=>{e.target.classList.toggle('in',e.isIntersecting)})},{threshold:.1,rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.rv').forEach(el=>io.observe(el));
document.querySelectorAll('.qa button').forEach(btn=>{
  btn.addEventListener('click',()=>{
    const qa=btn.parentElement,ans=qa.querySelector('.ans'),open=qa.classList.contains('open');
    document.querySelectorAll('.qa').forEach(x=>{x.classList.remove('open');x.querySelector('.ans').style.maxHeight=null;});
    if(!open){qa.classList.add('open');ans.style.maxHeight=ans.scrollHeight+'px';}
  });
});
</script>"""

# ---------------- 서비스 데이터 ----------------
S = []
def s(**kw): S.append(kw)

# 서비스별 관련 무료 도구 (slug -> (링크, 이름, 한줄설명))
RELTOOL = {
  "visibility":     ("../check.html",         "AI 가시성 진단",   "URL만 넣으면 우리 회사가 AI 답변에 얼마나 노출되는지 100점으로 확인합니다."),
  "website-build":  ("../tools.html#seo",     "SEO 점수 확인",    "검색 기본기 6가지를 자가 점검해 SEO 준비도를 확인합니다."),
  "press":          ("../tools.html#pr",      "PR 플랜 추천",     "상황·목표·예산 3가지 질문으로 우리에게 맞는 PR 플랜을 추천합니다."),
}

VIS_HTML = {
  'visibility': """<div class="svc-vis rv">
<span class="sticker white" style="top:2%;left:6%;transform:rotate(-5deg)">진단 리포트 미리보기</span>
<div class="mini-win rep">
<div class="mw-bar"><i></i><i></i><i></i><span class="u">messeze · AI 가시성 진단</span></div>
<div class="mw-body">
<div class="gaugerow"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="50" fill="none" stroke="#EEF2F9" stroke-width="12"/><circle cx="60" cy="60" r="50" fill="none" stroke="#2B5CFF" stroke-width="12" stroke-linecap="round" stroke-dasharray="314" stroke-dashoffset="198" transform="rotate(-90 60 60)"/><text x="60" y="67" text-anchor="middle" font-family="Poppins" font-size="24" font-weight="700" fill="#0A1930">37</text></svg>
<div class="t"><b>현재 37점</b><span>질문 6개 중 1개만 노출 · 개선 여지 큼</span></div></div>
<div class="row"><span class="en">ChatGPT</span><span class="bt"><i style="width:24%"></i></span><span class="st no">미인식</span></div>
<div class="row"><span class="en">Gemini</span><span class="bt"><i style="width:31%"></i></span><span class="st no">미인식</span></div>
<div class="row"><span class="en">Perplexity</span><span class="bt"><i style="width:58%"></i></span><span class="st ok">부분 인식</span></div>
<div class="row"><span class="en">네이버 검색</span><span class="bt"><i style="width:66%"></i></span><span class="st ok">인식</span></div>
</div></div>
<span class="sticker blue" style="bottom:6%;right:2%;transform:rotate(3deg)">여기서부터 시작합니다</span>
</div>""",
  'website-renewal': """<div class="svc-vis ba rv">
<span class="sticker white" style="top:-2%;left:8%;transform:rotate(-6deg)">Before — 사람만 보는 페이지</span>
<div class="cwb before"><div class="mw-bar"><i></i><i></i><i></i><span class="u">기존 홈페이지</span></div>
<div class="mw-body"><div class="skl dark"></div><div class="skl"></div><div class="skl s"></div><div class="skl xs"></div>
<div class="tagchips"><span class="bad">✕ H1 없음</span><span class="bad">✕ 스키마 없음</span><span class="bad">✕ 이미지 텍스트</span></div></div></div>
<div class="cwb after"><div class="mw-bar"><i></i><i></i><i></i><span class="u">messeze 정비 후</span></div>
<div class="mw-body"><div class="skl dark" style="background:var(--ink);opacity:.9"></div><div class="skl"></div><div class="skl s"></div>
<div class="tagchips"><span class="good">✓ H1·헤딩 위계</span><span class="good">✓ Organization 스키마</span><span class="good">✓ FAQ 페이지</span><span class="good">✓ ALT 완비</span></div></div></div>
<span class="sticker blue" style="bottom:0;right:6%;transform:rotate(2.5deg)">After — AI도 읽는 페이지</span>
</div>""",
  'website-build': """<div class="svc-vis rv">
<span class="sticker white" style="top:0;left:4%;transform:rotate(-4deg)">질문이 곧 페이지가 됩니다</span>
<div class="tree">
<div class="root">🏠 회사 홈</div>
<div class="lvl">
<div class="node">회사 소개<em>Organization</em></div>
<div class="node">제품·서비스<em>Service</em></div>
<div class="node q">"소량 생산 되나요?"<em>FAQPage</em></div>
<div class="node q">"수출 실적 있나요?"<em>FAQPage</em></div>
<div class="node">블로그<em>Article</em></div>
</div></div>
<span class="sticker dark" style="bottom:4%;right:4%;transform:rotate(2deg)">스키마 기본 탑재</span>
</div>""",
  'own-blog': """<div class="svc-vis rv">
<div class="mini-win artwin">
<div class="mw-bar"><i></i><i></i><i></i><span class="u">company.co.kr/blog</span></div>
<div class="mw-body">
<div class="ttl">항공부품 소량 생산, 어디까지 가능할까요?</div>
<div class="meta">전문 칼럼 · FAQPage 스키마 적용</div>
<div class="ansbox"><b>결론부터:</b> 시제품 1개부터 양산 전 단계까지 가능합니다. 판단 기준은 세 가지 — 가공 방식, 소재 수급, 인증 범위입니다…</div>
<div class="tagchips"><span class="good">✓ 질문형 제목</span><span class="good">✓ 첫 문단에 답</span><span class="good">✓ 자사 도메인 축적</span></div>
</div></div>
<div class="cal"><div class="cl">이번 달 발행<em>주 2회</em></div>
<div class="cal-hd"><span>월</span><span>화</span><span>수</span><span>목</span><span>금</span></div>
<div class="cal-grid"><i></i><i class="pub"></i><i></i><i class="pub"></i><i></i><i class="pub"></i><i></i><i></i><i class="pub"></i><i></i><i></i><i class="pub"></i><i></i><i class="pub"></i><i></i><i class="pub"></i><i></i><i></i><i class="pub"></i><i></i></div></div>
</div>""",
  'channels': """<div class="svc-vis rv">
<span class="sticker white" style="top:0;right:6%;transform:rotate(4deg)">출처가 셋이면, 신뢰는 배가</span>
<div class="radial">
<div class="hub"><em>원본</em>자사 블로그 칼럼</div>
<div class="spokes">
<div class="ch nv"><b>네이버 블로그</b><em>네이버 검색</em><span>국내 발주 담당자<br>신뢰 콘텐츠</span></div>
<div class="ch ts"><b>티스토리</b><em>구글 · 다음</em><span>기술·정보성 글<br>구글 유입</span></div>
<div class="ch gb"><b>구글 블로거</b><em>구글 색인</em><span>신규 소식<br>빠른 인덱싱</span></div>
</div></div>
</div>""",
  'press': """<div class="svc-vis clips rv">
<div class="clip c1"><div class="pressname">산업 전문지</div><div class="clip-h">○○정밀, 항공부품 소량 생산 라인 증설… 수출바우처 선정</div></div>
<div class="clip c2"><div class="pressname">경제지</div><div class="clip-h">"베트남 수출 물꼬" ○○정밀, 동남아 인증 획득하고 첫 계약</div>
<div class="tagchips"><span class="good">✓ 제3자 검증 출처</span><span class="good">✓ AI 인용 근거</span></div></div>
<div class="clip c3"><div class="pressname">온라인 뉴스</div><div class="clip-h">○○정밀, 스마트공장 구축으로 정밀부품 납기 30% 단축</div></div>
<div class="flowrow"><span>보도자료</span><i>→</i><span>기자 매칭</span><i>→</i><span>기사 발행</span><i>→</i><span class="hl">AI가 인용</span></div>
</div>""",
}

# ---- 문구는 data/services.json에서 읽는다 (관리자에서 편집 가능) ----
# vis(시각 목업 HTML)는 디자인 요소라 코드에 유지한다.
_svc_json = os.path.join(ROOT, "data", "services.json")
_VIS = {d["slug"]: d.get("vis", "") for d in S} if S else {}
S.clear()
with io.open(_svc_json, encoding="utf-8") as _f:
    _data = {_x["slug"]: _x for _x in json.load(_f)}
for _slug in ["visibility", "website-renewal", "website-build", "own-blog", "channels", "press"]:
    _d = dict(_data[_slug])
    _d["items"] = [tuple(x) if len(x) < 3 else (x[0], x[1], list(x[2])) for x in _d["items"]]
    _d["proc"] = [tuple(x) for x in _d["proc"]]
    _d["faq"]  = [tuple(x) for x in _d["faq"]]
    _d["vis"]  = VIS_HTML.get(_slug, "")
    s(**_d)

SVCPHOTO = {
 "visibility": ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1000&h=560&fit=crop&q=72&auto=format","진단 리포트로 현재 위치를 숫자로 확인합니다"),
 "website-renewal": ("https://images.unsplash.com/photo-1547658719-da2b51169166?w=1000&h=560&fit=crop&q=72&auto=format","AI가 읽을 수 있는 구조로 홈페이지를 정비합니다"),
 "website-build": ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1000&h=560&fit=crop&q=72&auto=format","질문에서 출발해 페이지 구조를 설계합니다"),
 "own-blog": ("https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1000&h=560&fit=crop&q=72&auto=format","자사 도메인에 전문성이 쌓이도록 매주 발행합니다"),
 "channels": ("https://images.unsplash.com/photo-1522542550221-31fd19575a2d?w=1000&h=560&fit=crop&q=72&auto=format","네이버·티스토리·구글까지 출처를 넓힙니다"),
 "press": ("https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1000&h=560&fit=crop&q=72&auto=format","기자가 검증한 기사로 제3자 신뢰를 만듭니다"),
}
# 서비스별 진행 흐름 (4단계)
FLOWSTEPS = {
 "visibility": [("자료 수집","회사·제품 정보 전달","간단한 질문지 작성"),("AI 질의 테스트","4개 엔진에 질문 실행","답변·인용 출처 기록"),("구조 분석","홈페이지 크롤러 관점 점검","경쟁사 비교 분석"),("리포트 브리핑","진단 결과 미팅 설명","개선 우선순위 전달")],
 "website-renewal": [("범위 확정","진단 결과로 수정/리뉴얼 판정","작업 범위 합의"),("구조 정비","메타·헤딩·콘텐츠 정리","이미지 텍스트 복구"),("스키마 적용","JSON-LD·사이트맵 적용","크롤링 경로 개방"),("전후 검증","점수 비교 리포트","개선 수치 확인")],
 "website-build": [("질문·구조 설계","핵심 질문 정의","사이트 구조(IA) 확정"),("디자인·개발","브랜드 디자인 작업","표준 마크업 개발"),("콘텐츠·스키마","초기 콘텐츠 게재","페이지별 구조화 데이터"),("런칭·색인","서치콘솔 등록","초기 색인 확인")],
 "own-blog": [("글감 캘린더","핵심 질문을 월별 배치","발행 일정 확정"),("초안 작성","전담팀 집필","전문성 인터뷰 반영"),("검수·발행","고객 검수 후 수정","스키마 붙여 발행"),("성과 추적","노출·유입 확인","다음 달 계획 반영")],
 "channels": [("채널 전략","업종별 채널 역할 정의","운영 방향 수립"),("개설·세팅","계정 개설·프로필 정비","카테고리 구성"),("변주 발행","원본을 채널별 재작성","각 채널 성격에 맞게"),("유입 분석","채널별 성과 비교","비중 조정")],
 "press": [("소재 발굴","월간 미팅에서 뉴스거리","보도 가치 판단"),("원고 작성","보도자료·애드버토리얼","리드문 중심 작성"),("기자 매칭 배포","업종별 출입처 선별","맞춤 배포"),("결과 관리","게재 확인·팔로업","기사 자산화")],
}
# 서비스별 "무엇을 하나요" 섹션 제목
WHATHEADS = {
 "visibility": ("무엇을 진단하나요", "이렇게 진단합니다"),
 "website-renewal": ("무엇을 정비하나요", "이렇게 정비합니다"),
 "website-build": ("어떻게 설계하나요", "이렇게 설계하고 짓습니다"),
 "own-blog": ("어떻게 운영하나요", "이렇게 쌓아 올립니다"),
 "channels": ("어떻게 운영하나요", "이렇게 확산시킵니다"),
 "press": ("어떻게 배포하나요", "이렇게 기사로 만듭니다"),
}

BY_SLUG = {x["slug"]: x for x in S}

def photo_html(slug):
    p = SVCPHOTO.get(slug)
    if not p: return ""
    url, cap = p
    return f'<figure class="svc-photo rv"><img src="{url}" alt="" loading="lazy" referrerpolicy="no-referrer"><figcaption>{cap}</figcaption></figure>'

def flow_html(slug):
    steps = FLOWSTEPS.get(slug)
    if not steps: return ""
    cells = "".join(f'<div class="hm-step"><span class="hn">STEP {i+1:02d}</span><b>{a}</b><span>{b}<br>{c}</span></div>' for i,(a,b,c) in enumerate(steps))
    return f'<div class="hflow-mini rv"><h4>진행 흐름 한눈에 보기</h4><p class="hm-sub">문의부터 결과 전달까지, 이 순서로 진행됩니다.</p><div class="hm-row">{cells}</div></div>'

# 포인트별 채널 로고 타일 (slug -> {item_index: (logo_url, tile_bg)})
ITEMLOGOS = {
  "channels": {
    0: ("../assets/logos/ch-naver.svg", "#E8F7EE"),
    1: ("../assets/logos/ch-tistory.png", "#FFF2EA"),
    2: ("../assets/logos/ch-blogger.png", "#FFF4E5"),
  },
}

def build_page(x):
    rel_cards = ""
    for slug in x["rel"]:
        r = BY_SLUG[slug]
        rel_cards += f"""<a class="relc rv" href="{r['slug']}.html"><span class="no">SERVICE {r['no']}</span><b>{r['title']}</b><span>{r['one'][:38]}…</span></a>"""
    _logos = ITEMLOGOS.get(x["slug"], {})
    def _pt(i, t, d, tg):
        lg = _logos.get(i)
        badge = (f'<img class="ptc-ico" src="{lg[0]}" alt="" loading="lazy">' if lg
                 else f'<span class="ptc-no">{i+1:02d}</span>')
        tags = "".join("<span>"+g+"</span>" for g in tg)
        return f'<div class="dg-row rv"><span class="dg-no">{i+1:02d}</span><b>{t}</b><p>{d}</p></div>'
    items = "\n".join(_pt(i, t, d, (rest[0] if rest else [])) for i,(t,d,*rest) in enumerate(x["items"]))
    procs = "\n".join(f"""<div class="pr rv"><span class="n">{i+1}</span><b>{t}</b><p>{d}</p></div>""" for i,(t,d,*_) in enumerate(x["proc"]))
    fits = "\n".join(f"""<div><span class="c">✓</span>{f}</div>""" for f in x["fit"])
    delivs = "".join(
        f'<div class="dvi"><i>{i+1:02d}</i><div><b>{d[0]}</b><p>{d[1]}</p></div></div>' if isinstance(d, (list, tuple))
        else f"<span>{d}</span>"
        for i, d in enumerate(x["deliv"]))
    faqs = "\n".join(f"""<div class="qa"><button>{q}<span class="ico">+</span></button><div class="ans"><p>{a}</p></div></div>""" for q,a in x["faq"])
    _rt = RELTOOL.get(x["slug"])
    reltool = (f"""<a class="reltool rv" href="{_rt[0]}"><div><span class="rt-tag">관련 무료 도구</span><h3>{_rt[1]}</h3><p>{_rt[2]}</p></div><span class="rt-go">바로 써보기 →</span></a>""" if _rt else "")
    ld = json.dumps({
      "@context":"https://schema.org","@graph":[
        {"@type":"Service","name":x["title"],"alternateName":x["en"],"description":x["one"],
         "provider":{"@type":"Organization","name":"messeze"},"serviceType":"기업 PR · AI 가시성 관리"},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in x["faq"]]},
        {"@type":"BreadcrumbList","itemListElement":[
          {"@type":"ListItem","position":1,"name":"서비스","item":"../services.html"},
          {"@type":"ListItem","position":2,"name":x["title"]}]}
      ]}, ensure_ascii=False)
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{x['title']} | messeze 서비스 — AI가 보는 PR</title>
<meta name="description" content="{x['one']}">
{FONT_LINKS}
<script type="application/ld+json">{ld}</script>
<style>{CSS}</style></head><body id="top">
{nav()}
<div class="wrap crumb"><a href="../services.html">서비스</a><span>›</span><span class="cat">SERVICE {x['no']}</span></div>
<section class="phero"><div class="wrap phero-in">
<div class="rv">
<span class="no">SERVICE {x['no']} · {x['en']}</span>
<h1>{x['title']}</h1>
<p class="sub">{x['one']}</p>
<div class="ai-view"><span class="avl">AI의 눈으로 보면</span><p>{x['ai']}</p></div>
<div class="cta"><a href="../check.html" class="btn btn-co">AI 노출 무료 진단</a><a href="../pricing.html" class="btn btn-gh">요금 보기</a></div>
</div>
{x['vis']}
</div></section>

<section class="sec"><div class="wrap">
<div class="shead rv"><span class="eyebrow">{WHATHEADS.get(x['slug'],("무엇을 하나요","이 서비스에 포함된 것"))[0]}</span><h2 class="h2">{WHATHEADS.get(x['slug'],("무엇을 하나요","이 서비스에 포함된 것"))[1]}</h2><p class="lead">{x['intro']}</p></div>
<div class="dg-rows">{items}</div>
{reltool}
</div></section>

{x.get('tool','')}<section class="proc"><div class="wrap">
<div class="shead center rv" style="margin-bottom:40px"><span class="eyebrow">진행 절차</span><h2 class="h2">이렇게 진행됩니다</h2></div>
<div class="pr-grid">{procs}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="fitrow">
<div class="rv"><span class="eyebrow">이런 기업에 맞아요</span><h2 class="h2" style="margin-bottom:22px">이런 상황이라면,<br>시작할 때입니다</h2><div class="fit-list">{fits}</div></div>
<div class="dv-card rv"><h3>산출물</h3><div class="dvl">{delivs}</div></div>
</div>
</div></section>

<section class="svcta"><div class="wrap">
<h2>{x['title']}, 혼자 고민하지 마세요</h2>
<p>전담 매니저가 우리 회사를 깊이 이해하고, AI가 추천하는 기업이 될 때까지 함께합니다.<br>첫 진단은 무료입니다.</p>
<a class="sbtn" href="../index.html#final">무료 상담 신청</a>
<div class="svcta-stats"><div><b>4개 엔진</b><span>ChatGPT·Gemini·Perplexity·네이버</span></div><div><b>월 60만원~</b><span>구독형 운영 · 약정 없음</span></div><div><b>3개월</b><span>AI 반영 기준선</span></div></div>
</div></section>

<section class="sec" style="background:var(--sky-2)"><div class="wrap">
<div class="shead center rv"><span class="eyebrow">자주 묻는 질문</span><h2 class="h2">{x['title']}, 궁금한 점</h2></div>
<div class="faq rv">{faqs}</div>
</div></section>
{foot()}
{FAQ_JS}
</body></html>"""

for x in S:
    with io.open(os.path.join(OUT, x["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(build_page(x))
print("OK:", len(S), "service pages →", OUT)
