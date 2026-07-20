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
.mega-col h5{font-size:11.5px;color:var(--mut);font-weight:800;letter-spacing:.05em;margin:0 0 8px 12px}
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
.clips .clip h5{font-size:14.5px;font-weight:800;line-height:1.45;margin-top:7px;letter-spacing:-.01em}
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
/* 진행 절차 — 단계별 순차 강조(진한 색감): reveal 시 번호가 코발트로 채워지고 카드가 도드라짐 */
.pr.in{border-color:#B9CCFF;box-shadow:0 18px 44px rgba(43,92,255,.14)}
.pr.in .n{background:linear-gradient(135deg,#2B5CFF,#6E93FF);box-shadow:0 8px 18px rgba(43,92,255,.34);transform:scale(1.06)}
/* 절차 카드: 스크롤 시 1→2→3→4 또렷하게 하나씩 등장 */
.proc .pr.rv{opacity:0;transform:translateY(40px) scale(.965)}
.proc .pr.rv.in{opacity:1;transform:none}
.pr-grid .pr:nth-child(1),.pr-grid .pr:nth-child(1) .n{transition-delay:0s}
.pr-grid .pr:nth-child(2),.pr-grid .pr:nth-child(2) .n{transition-delay:.2s}
.pr-grid .pr:nth-child(3),.pr-grid .pr:nth-child(3) .n{transition-delay:.4s}
.pr-grid .pr:nth-child(4),.pr-grid .pr:nth-child(4) .n{transition-delay:.6s}
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
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}.rv,.phero-in>.rv,.phero-in>.svc-vis.rv{opacity:1;transform:none;translate:none}}
"""

LOGO = """<svg viewBox="0 0 30 30" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4H23a3 3 0 0 1 3 3v12a3 3 0 0 1-3 3H14l-4 4.5V22H7a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3Z"/><line x1="9.5" y1="10" x2="20.5" y2="10"/><line x1="9.5" y1="13.5" x2="20.5" y2="13.5"/><line x1="9.5" y1="17" x2="16.5" y2="17"/></svg>"""

FONT_LINKS = """<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@1.3.9/dist/web/static/pretendard.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">"""

P = "../"  # depth 1

def mega():
    p = P
    return f"""<div class="mega" id="mega"><div class="wrap mega-in">
<a class="mega-brand" href="{p}index.html"><span class="bw2">messeze</span><p>사람에게만 보이는 홍보에서,<br>AI가 읽는 홍보로</p></a>
<div class="mega-col"><h5>서비스</h5>
<a href="../services.html"><b style="color:var(--cobalt)">서비스 전체 보기 →</b><span>6가지 서비스를 한눈에</span></a>
<a href="visibility.html"><b>AI 가시성 평가</b><span>AI가 우리 회사를 아는지부터</span></a>
<a href="website-renewal.html"><b>홈페이지 수정·리뉴얼</b><span>AI가 읽는 구조로 정비</span></a>
<a href="website-build.html"><b>홈페이지 제작</b><span>질문이 페이지가 되는 설계</span></a>
<a href="own-blog.html"><b>자사 블로그 운영</b><span>도메인에 쌓이는 전문성</span></a>
<a href="channels.html"><b>외부 채널 운영</b><span>네이버·티스토리·구글 블로거</span></a>
<a href="press.html"><b>언론 배포</b><span>기자 매칭 · 보도자료 · 기사화</span></a></div>
<div class="mega-col"><h5>무료 도구</h5>
<a href="{p}check.html"><b>AI 가시성 진단</b><span>URL만 넣으면 30초 진단</span></a>
<a href="{p}tools.html#seo"><b>SEO 점수 확인</b><span>검색 기본기 자가 점검</span></a>
<a href="{p}tools.html#pr"><b>PR 플랜 추천</b><span>3가지 질문으로 플랜 찾기</span></a>
<div class="gap"></div><h5>요금</h5>
<a href="{p}pricing.html"><b>플랜 비교</b><span>소상공인형 · 기업형 · 엔터프라이즈</span></a>
<a href="{p}pricing.html#faq"><b>요금 FAQ</b><span>약정 · 수량 · 바우처 연계</span></a></div>
<div class="mega-col"><h5>리소스</h5>
<a href="{p}blog/index.html"><b>블로그</b><span>AI 검색 시대의 홍보 인사이트</span></a>
<a href="{p}glossary/index.html"><b>용어사전</b><span>SEO·AEO·GEO·PR 용어 35개</span></a></div>
</div></div>"""

MEGA_JS = """<script>
(function(){const p=document.getElementById('mega'),t=document.querySelector('.nav-menu'),b=document.getElementById('burger');if(!p)return;let m;const o=()=>{clearTimeout(m);p.classList.add('on')},c=()=>{m=setTimeout(()=>p.classList.remove('on'),140)};if(t){t.addEventListener('mouseenter',o);t.addEventListener('mouseleave',c);t.querySelectorAll('a').forEach(a=>a.addEventListener('mouseenter',o));}if(window.matchMedia('(hover:hover)').matches){p.addEventListener('mouseenter',o);p.addEventListener('mouseleave',c);}if(b){b.addEventListener('click',()=>{const on=p.classList.toggle('on');b.classList.toggle('on',on);});p.addEventListener('click',e=>{if(e.target.closest('a')){p.classList.remove('on');b.classList.remove('on');}});}})();
</script>"""

def nav():
    p = P
    return f"""<header class="nav"><div class="wrap nav-in">
<a class="brand" href="{p}index.html">{LOGO}<span class="bw">messeze</span></a>
<nav class="nav-menu">
<a class="on" href="{p}services.html">서비스</a>
<a href="{p}pricing.html">요금</a>
<a href="{p}check.html">AI 가시성 체크</a>
<a href="{p}blog/index.html">블로그</a>
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
    return f"""<footer class="foot"><div class="wrap"><div class="foot-in">
<div><a class="brand" href="{p}index.html">{LOGO}<span class="bw">messeze</span></a>
<p>기업의 정보를 언론과 AI 검색에 지속적으로 축적하는 구독형 기업 PR 서비스.</p></div>
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

s(slug="visibility", no="01", title="AI 가시성 평가", en="AI Visibility Assessment",
  one="AI에게 우리 회사는 '존재하는 회사'인지, '모르는 이름'인지 — 모든 실행은 이 확인에서 시작합니다.",
  ai="같은 질문을 던져도 AI마다 다른 회사를 추천합니다. 그 차이는 우연이 아니라 '읽을 수 있는 정보의 양과 신뢰도' 차이입니다. 우리가 어디쯤인지부터 정확히 재야 합니다.",
  intro="ChatGPT·Gemini·Perplexity·네이버가 기업을 어떻게 인식하는지, 고객 질문에 우리 회사가 등장하는지, 경쟁사는 어디까지 와 있는지 — 감이 아니라 데이터로 확인하고, 다음 3개월의 실행 순서를 정합니다.",
  items=[("엔진별 인식 상태 점검","주요 AI 검색 4곳에 동일한 질문 세트를 던져 인식·인용 여부와 답변 내용을 기록합니다. '어느 엔진이 우리를 아는가'가 지도에 그려집니다."),
        ("핵심 질문 5~6개 설계","고객이 실제로 물어볼 질문을 온보딩 미팅에서 함께 정의합니다. 이 질문들이 이후 홈페이지·콘텐츠·언론 실행 전체의 뼈대가 됩니다."),
        ("홈페이지 구조 진단","타이틀·헤딩·메타 같은 SEO 기본기부터 구조화 데이터·엔티티 연결까지, AI 크롤러 관점에서 읽히는 상태를 점검합니다."),
        ("경쟁사 비교 분석","같은 질문에서 경쟁사가 어떤 출처 덕분에 답변에 등장하는지 분해합니다. 따라잡을 목록이 그대로 실행 과제가 됩니다."),
        ("개선 우선순위 로드맵","점수를 가장 많이 올릴 항목부터 순서대로. 직접 실행해도 되고, messeze에 맡겨도 되는 형태로 작성합니다."),
        ("기존 콘텐츠·기사 자산 조사","이미 보유한 기사·블로그·자료 중 AI가 활용할 수 있는 자산과 방치된 자산을 구분합니다.")],
  proc=[("사전 정보 수집","회사 소개·주요 제품·고객·목표 시장 자료를 받습니다. 간단한 질문지면 충분합니다."),
        ("AI 질의 테스트","4개 엔진에 질문 세트를 실행하고 답변·인용 출처를 기록합니다."),
        ("구조·출처 분석","홈페이지와 외부 출처를 크롤러 관점에서 분석합니다."),
        ("리포트 브리핑","진단 리포트와 로드맵을 미팅으로 설명드립니다. 여기까지가 평가입니다.")],
  fit=["홍보를 시작하기 전, 현재 위치부터 알고 싶은 기업","경쟁사가 먼저 쌓고 있는지 확인하고 싶은 기업","어디부터 손대야 할지 순서가 필요한 기업"],
  deliv=["AI 가시성 진단 리포트","핵심 질문 설계서","개선 우선순위 로드맵"],
  faq=[("무료 AI 가시성 체크와 뭐가 다른가요?","홈페이지의 무료 체크는 URL 기반 구조 자동 진단입니다. 정식 평가는 실제 AI 질의 테스트, 경쟁사 비교, 핵심 질문 설계까지 전담팀이 수행하고 미팅으로 브리핑합니다."),
       ("진단만 받고 실행은 직접 해도 되나요?","네. 로드맵은 자체 실행이 가능하도록 구체적으로 작성합니다. 실행까지 맡기실 경우 진단 결과가 그대로 운영 계획이 됩니다."),
       ("기간은 얼마나 걸리나요?","기업 규모와 기존 자산에 따라 다르지만 통상 영업일 기준 1~2주입니다."),
       ("어떤 자료를 준비해야 하나요?","회사 소개, 주요 제품·서비스, 홈페이지 주소 정도면 시작할 수 있습니다. 나머지는 저희가 조사합니다.")],
  vis="""<div class="svc-vis rv">
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
  rel=["website-renewal","own-blog"])

s(slug="website-renewal", no="02", title="홈페이지 수정·리뉴얼", en="Website Optimization & Renewal",
  one="예쁜 홈페이지와 AI가 읽는 홈페이지는 다릅니다. 지금 홈페이지를 최대한 살려서, 읽히는 구조로 바꿉니다.",
  ai="화면에는 보이는데 HTML에는 없는 정보, 이미지 안에 갇힌 회사 소개 — AI 크롤러에게는 전부 '없는 정보'입니다. 구조를 바꾸는 것만으로 읽히는 정보량이 몇 배가 됩니다.",
  intro="진단 결과 구조 개선으로 충분하면 수정으로, 뼈대부터 문제라면 리뉴얼로 갑니다. 과잉 제안 없이 필요한 범위만 — 목표는 새 디자인이 아니라 AI와 검색엔진이 읽는 홈페이지입니다.",
  items=[("메타·헤딩 구조 정비","페이지마다 고유한 타이틀과 디스크립션, H1→H2→H3 위계를 바로잡습니다. 검색과 AI가 문서 구조를 즉시 파악하게 됩니다."),
        ("구조화 데이터(JSON-LD) 탑재","Organization·Service·FAQPage 스키마로 발행 주체와 서비스를 기계가 읽는 형식으로 선언합니다. @id·sameAs 연결까지."),
        ("질문-답변형 페이지 신설","설계한 핵심 질문에 정면으로 답하는 페이지를 홈페이지 안에 만듭니다. AI 인용의 착지 지점이 됩니다."),
        ("이미지·텍스트 리커버리","이미지 속에 갇힌 정보를 텍스트로 꺼내고, 모든 이미지에 의미 있는 ALT를 채웁니다."),
        ("크롤링 기반 정비","robots.txt·sitemap.xml·canonical을 정리해 검색엔진과 AI 크롤러의 수집 경로를 엽니다."),
        ("전후 점수 검증","수정 전후를 AI 가시성 체크 점수로 비교해 개선을 숫자로 증명합니다.")],
  proc=[("범위 확정","진단 결과를 바탕으로 수정으로 갈지, 리뉴얼이 필요한지 판정하고 범위를 합의합니다."),
        ("구조 정비 실행","메타·헤딩·콘텐츠·이미지를 순서대로 정비합니다."),
        ("스키마·기술 적용","JSON-LD, 사이트맵, canonical 등 기술 요소를 적용합니다."),
        ("전후 비교 검증","적용 전후 점수와 변화를 리포트로 확인시켜 드립니다.")],
  fit=["홈페이지는 있는데 검색·AI에 안 잡히는 기업","리뉴얼 비용이 부담스러워 미뤄온 기업","이미지 위주로 제작된 구축형 홈페이지를 쓰는 기업"],
  deliv=["수정 전후 비교 리포트","스키마 적용 페이지","질문별 랜딩 페이지"],
  faq=[("수정과 리뉴얼은 어떻게 판단하나요?","진단에서 판단합니다. 콘텐츠와 구조를 살릴 수 있으면 수정으로 충분하고, 프레임 자체가 수정을 막거나(빌더 제약 등) 구조가 무너져 있으면 리뉴얼을 제안합니다."),
       ("홈페이지를 만든 업체가 따로 있는데 가능한가요?","네. 관리 권한이나 업체 협조를 받아 진행하며, 직접 수정이 어려운 환경이면 적용 가이드를 만들어 기존 업체에 전달하는 방식도 가능합니다."),
       ("아임웹·워드프레스 같은 빌더 사이트도 되나요?","대부분 가능합니다. 빌더별로 스키마 삽입·메타 편집 지원 범위가 달라, 제약이 있는 경우 대안(예: 코드 삽입 위젯)을 제시합니다."),
       ("기간은 얼마나 걸리나요?","수정 범위에 따라 다르지만 통상 2~4주입니다. 리뉴얼 판정 시 제작 일정으로 전환됩니다.")],
  vis="""<div class="svc-vis ba rv">
<span class="sticker white" style="top:-2%;left:8%;transform:rotate(-6deg)">Before — 사람만 보는 페이지</span>
<div class="cwb before"><div class="mw-bar"><i></i><i></i><i></i><span class="u">기존 홈페이지</span></div>
<div class="mw-body"><div class="skl dark"></div><div class="skl"></div><div class="skl s"></div><div class="skl xs"></div>
<div class="tagchips"><span class="bad">✕ H1 없음</span><span class="bad">✕ 스키마 없음</span><span class="bad">✕ 이미지 텍스트</span></div></div></div>
<div class="cwb after"><div class="mw-bar"><i></i><i></i><i></i><span class="u">messeze 정비 후</span></div>
<div class="mw-body"><div class="skl dark" style="background:var(--ink);opacity:.9"></div><div class="skl"></div><div class="skl s"></div>
<div class="tagchips"><span class="good">✓ H1·헤딩 위계</span><span class="good">✓ Organization 스키마</span><span class="good">✓ FAQ 페이지</span><span class="good">✓ ALT 완비</span></div></div></div>
<span class="sticker blue" style="bottom:0;right:6%;transform:rotate(2.5deg)">After — AI도 읽는 페이지</span>
</div>""",
  rel=["visibility","website-build"])

s(slug="website-build", no="03", title="홈페이지 제작", en="AEO-first Website Build",
  one="새로 짓는다면 처음부터 AI가 읽는 구조로. 고객의 질문 하나하나가 페이지가 되는 홈페이지를 짓습니다.",
  ai="다 지어놓고 스키마를 덧붙이는 것과, 뼈대부터 질문 중심으로 설계하는 것은 결과가 다릅니다. 페이지가 늘어날수록 AI가 인용할 답이 늘어나는 구조 — 그게 AEO-first 설계입니다.",
  intro="디자인만 예쁜 홈페이지가 아니라, 검색과 AI 양쪽에서 일하는 홈페이지를 짓습니다. 핵심 질문에서 출발한 정보 구조, 표준으로 들어가는 스키마, 운영 단계에서 콘텐츠가 쌓이는 블로그 시스템까지.",
  items=[("질문 기반 정보 구조(IA) 설계","핵심 질문 → 페이지 구조로 변환합니다. 산업·서비스·질문별로 페이지를 계속 늘릴 수 있는 확장형 골격입니다."),
        ("AEO·SEO 기본기 내장","메타·헤딩·구조화 데이터·사이트맵·robots까지, 나중에 고칠 것 없이 처음부터 표준으로 들어갑니다."),
        ("블로그·콘텐츠 시스템 포함","운영 단계에서 칼럼이 쌓일 수 있도록 발행 구조와 템플릿을 함께 짓습니다."),
        ("반응형·속도 최적화","모바일 우선 인덱싱과 사용자 경험 지표(Core Web Vitals)를 기준으로 만듭니다."),
        ("다국어 확장 대비","수출기업이라면 베트남어·영어·중국어 페이지로 확장 가능한 컴포넌트 구조로 설계합니다."),
        ("런칭 후 색인 등록","서치콘솔·네이버 서치어드바이저 등록과 초기 색인 확인까지 마무리합니다.")],
  proc=[("질문·구조 설계","핵심 질문과 사이트 구조(IA)를 확정합니다. 제작의 절반은 여기서 결정됩니다."),
        ("디자인·개발","브랜드에 맞는 디자인과 표준 마크업으로 개발합니다."),
        ("콘텐츠·스키마 적용","초기 콘텐츠를 싣고 페이지별 구조화 데이터를 적용합니다."),
        ("런칭·색인 등록","공개 후 검색엔진 등록과 AI 가시성 체크 점수를 확인합니다.")],
  fit=["홈페이지가 없거나 사실상 새로 시작해야 하는 기업","수출용 다국어 홈페이지가 필요한 기업","진단에서 리뉴얼 판정을 받은 기업"],
  deliv=["신규 홈페이지","구조화 데이터 기본 탑재","운영 가이드"],
  faq=[("제작 기간은 얼마나 걸리나요?","규모에 따라 다르지만 통상 4~8주입니다. 질문·구조 설계가 확정되면 이후 일정은 크게 흔들리지 않습니다."),
       ("비용은 어떻게 되나요?","페이지 규모·다국어 여부에 따라 별도 견적입니다. 구독 플랜과 별도이며, 수출바우처 등 지원사업 활용 방안도 상담에서 안내드립니다."),
       ("제작 후 관리는 어떻게 하나요?","구독 플랜과 연결하면 콘텐츠 발행·점검이 이어집니다. 자체 운영을 원하시면 운영 가이드와 교육을 제공합니다."),
       ("콘텐츠(글·사진)도 만들어 주나요?","네. 초기 페이지 카피는 제작에 포함되며, 촬영·번역이 필요한 경우 범위를 협의해 진행합니다.")],
  vis="""<div class="svc-vis rv">
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
  rel=["website-renewal","own-blog"])

s(slug="own-blog", no="04", title="홈페이지 내 블로그 운영", en="Owned Blog Operation",
  one="같은 글이라도 자사 도메인에 쌓인 글만 '우리 회사의 전문성'으로 계산됩니다.",
  ai="AI는 '이 분야를 아는 회사'를 도메인 단위로 기억합니다. 남의 플랫폼에 쌓은 글은 그 플랫폼의 자산 — 자사 블로그의 축적만이 E-E-A-T가 되어 도메인에 남습니다.",
  intro="설계한 핵심 질문에 답하는 칼럼을 자사 블로그에 매달 발행합니다. 질문형 제목, 첫 문단에 결론, FAQ 스키마 — AI가 인용하기 가장 좋은 형태로 쓰고, 발행 캘린더로 꾸준히 쌓습니다.",
  items=[("질문 기반 칼럼 기획","'고객이 AI에게 물어볼 질문'이 곧 글감입니다. 검색량이 아니라 질문에서 출발해 글감이 고갈되지 않습니다."),
        ("AEO형 구조로 집필","질문형 소제목 → 정면 답변 → 근거 순서. 사람도 AI도 원하는 답을 바로 찾는 구조입니다."),
        ("전문성 소재 인터뷰","현장의 노하우를 짧은 인터뷰·자료로 받아 전문가의 글로 바꿉니다. 쓸 사람이 없어도 됩니다."),
        ("FAQ·Article 스키마 적용","발행 글마다 구조화 데이터를 붙여 리치 결과와 AI 인용 자격을 만듭니다."),
        ("발행 캘린더 운영","월 단위 발행 계획으로 꾸준히. 축적의 리듬이 곧 전략입니다."),
        ("성과 추적","글별 노출·유입과 AI 인용 변화를 월간 리포트에 담습니다.")],
  proc=[("글감 캘린더 수립","핵심 질문을 월별 글감으로 배치합니다."),
        ("초안 작성·검수","전담팀이 작성하고, 원하시면 발행 전 검수를 거칩니다."),
        ("발행·스키마 적용","자사 블로그에 발행하고 구조화 데이터를 붙입니다."),
        ("월간 성과 리포트","노출·유입·AI 반영 변화를 확인하고 다음 달 계획에 반영합니다.")],
  fit=["글 쓸 사람이 없어 블로그가 멈춰 있는 기업","기술력은 있는데 콘텐츠가 없는 제조·B2B 기업","검색량이 적어 블로그 효과를 못 보던 업종"],
  deliv=["월 발행 칼럼","FAQ 스키마 적용","발행 캘린더 · 성과 리포트"],
  faq=[("한 달에 몇 편이나 발행하나요?","플랜과 업종에 따라 확정하며, 수량보다 '질문 커버리지'를 기준으로 계획합니다. 확정 수량은 온보딩에서 함께 정합니다."),
       ("우리 업종의 전문 내용을 어떻게 쓰나요?","짧은 인터뷰와 보유 자료(카탈로그·인증·사례)를 바탕으로 작성합니다. 초안을 검수해 주시면 정확도가 빠르게 올라갑니다."),
       ("발행 전에 검수할 수 있나요?","네. 검수 프로세스를 포함해 운영할 수 있으며, 수정 반영 후 발행합니다."),
       ("기존에 써둔 글도 활용할 수 있나요?","네. 기존 글을 AEO형 구조로 리라이팅하고 스키마를 붙여 재발행하는 것도 효과적인 방법입니다.")],
  vis="""<div class="svc-vis rv">
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
  rel=["channels","website-renewal"])

s(slug="channels", no="05", title="외부 채널 운영", en="External Channel Operation",
  one="AI는 한 곳의 주장보다 여러 출처의 교차 확인을 신뢰합니다. 네이버·티스토리·구글 블로거로 출처를 넓힙니다.",
  ai="자사 블로그 혼자 말하는 회사와, 서로 다른 플랫폼 세 곳에서 같은 사실이 확인되는 회사 — AI의 신뢰는 후자로 기웁니다. 출처의 다양성이 곧 신뢰도입니다.",
  intro="자사 블로그가 원본, 채널은 변주입니다. 같은 메시지를 채널 성격에 맞게 다시 써서 네이버와 구글 양쪽 검색 생태계를 모두 커버하고, 교차 출처를 만듭니다.",
  items=[("네이버 블로그 — 국내 검색","국내 B2B 발주 담당자가 여전히 가장 많이 쓰는 네이버 검색. 신뢰 콘텐츠로 네이버 노출을 잡습니다."),
        ("티스토리 — 구글·다음","구글 검색에 잘 잡히는 플랫폼. 기술·정보성 콘텐츠의 구글 유입을 만듭니다."),
        ("구글 블로거 — 빠른 색인","구글 소유 플랫폼 특유의 빠른 인덱싱. 신규 소식을 구글 생태계에 빠르게 심습니다."),
        ("원본-변주 체계","자사 블로그 원본을 채널별로 다시 씁니다. 복붙 중복이 아니라 서로를 보강하는 교차 출처가 되게."),
        ("채널 개설·세팅 대행","채널이 없다면 개설부터 프로필·카테고리 세팅까지 대행합니다."),
        ("채널별 유입 리포트","채널별 노출·유입을 월간 리포트로 비교해 잘 되는 채널에 힘을 싣습니다.")],
  proc=[("채널 전략 수립","업종·목표에 맞춰 채널별 역할을 정합니다."),
        ("개설·세팅","계정 개설, 프로필·소개·카테고리를 브랜드에 맞게 정비합니다."),
        ("변주 콘텐츠 발행","원본 칼럼을 채널 성격에 맞게 다시 써서 발행합니다."),
        ("유입 분석·조정","채널별 성과를 보고 비중을 조정합니다.")],
  fit=["네이버 검색까지 잡아야 하는 국내 B2B 기업","구글 유입이 필요한 기술 중심 기업","채널 운영할 인력이 없는 기업"],
  deliv=["채널별 월 발행 콘텐츠","채널 개설·세팅","채널별 유입 리포트"],
  faq=[("왜 하필 이 세 채널인가요?","국내 검색(네이버), 구글·다음(티스토리), 구글 빠른 색인(블로거)으로 검색 생태계 커버리지가 가장 넓은 조합이기 때문입니다. 업종에 따라 다른 채널을 추가로 협의할 수 있습니다."),
       ("같은 내용을 여러 곳에 올리면 중복 아닌가요?","그대로 복사하면 중복입니다. 그래서 채널마다 구성과 문장을 다시 쓰는 '변주'로 운영하고, 원본 표시로 출처의 원류를 명확히 합니다."),
       ("기존에 쓰던 회사 블로그 계정을 활용할 수 있나요?","네. 기존 계정의 이력이 자산이 되는 경우가 많아, 살릴 수 있는 계정은 이어서 운영합니다."),
       ("인스타그램·유튜브 같은 채널은 안 하나요?","텍스트 기반 검색·AI 노출에 직접 기여하는 채널을 우선합니다. SNS·영상은 목적이 다른 채널이라 필요시 별도 협의로 진행합니다.")],
  vis="""<div class="svc-vis rv">
<span class="sticker white" style="top:0;right:6%;transform:rotate(4deg)">출처가 셋이면, 신뢰는 배가</span>
<div class="radial">
<div class="hub"><em>원본</em>자사 블로그 칼럼</div>
<div class="spokes">
<div class="ch nv"><b>네이버 블로그</b><em>네이버 검색</em><span>국내 발주 담당자<br>신뢰 콘텐츠</span></div>
<div class="ch ts"><b>티스토리</b><em>구글 · 다음</em><span>기술·정보성 글<br>구글 유입</span></div>
<div class="ch gb"><b>구글 블로거</b><em>구글 색인</em><span>신규 소식<br>빠른 인덱싱</span></div>
</div></div>
</div>""",
  rel=["own-blog","press"])

s(slug="press", no="06", title="언론 배포", en="Press Distribution",
  one="기자가 쓴 한 건의 기사가, 우리가 우리를 소개하는 백 마디보다 AI의 확신을 만듭니다.",
  ai="언론 기사는 제3자의 검증을 거친, AI가 가장 높게 평가하는 출처입니다. AI가 기업을 설명할 때 인용하는 근거의 최상단에 기사가 있습니다.",
  intro="기자가 인용하기 좋은 구조로 보도자료를 쓰고, 업종에 맞는 기자에게 배포합니다. 뉴스 가치가 있으면 보도자료로, 알리고 싶은 메시지는 애드버토리얼로 — 두 방식을 계획적으로 조합합니다.",
  items=[("보도자료 기획·작성","리드문 승부, 검증 가능한 사실 중심. 기사화 가능성과 AI 인용 가능성 두 기준으로 씁니다."),
        ("업종별 기자 매칭","산업 담당 기자 데이터베이스를 기반으로 맞는 출입처에 정확히 배포합니다. 스팸이 아니라 제보가 되게."),
        ("애드버토리얼 발행","게재가 보장되는 기사형 콘텐츠로 원하는 메시지를 원하는 시점에 싣습니다."),
        ("뉴스거리 발굴","신제품·인증·수출·전시회 — 회사 안의 소식에서 기사가 될 이야기를 함께 찾습니다."),
        ("발행 결과 관리","배포·게재 결과를 추적하고, 발행된 기사를 홈페이지·채널과 연결해 자산화합니다."),
        ("해외 언론 확장","수출기업이라면 베트남·중국·미국 등 현지어 보도자료와 현지 매체 배포까지 확장합니다.")],
  proc=[("뉴스거리 발굴","월간 미팅에서 보도 소재를 정리합니다."),
        ("원고 작성·확정","보도자료·애드버토리얼 원고를 작성하고 확정받습니다."),
        ("배포·팔로업","기자 매칭 배포와 게재 팔로업을 진행합니다."),
        ("기사화 리포트","게재 결과와 AI 인용 반영을 리포트로 드립니다.")],
  fit=["신제품·인증·수출 소식이 있는 기업","제3자 신뢰 출처가 필요한 기업","해외 시장에 알릴 일이 생긴 수출기업"],
  deliv=["보도자료 · 애드버토리얼","기자 배포 · 발행 관리","기사화 결과 리포트"],
  faq=[("보도자료를 보내면 기사화가 보장되나요?","보도자료는 기자의 판단을 거치므로 보장되지 않습니다. 그래서 뉴스 가치를 살린 원고와 정확한 기자 매칭으로 확률을 높이고, 반드시 실어야 하는 메시지는 게재가 보장되는 애드버토리얼로 조합합니다."),
       ("어떤 매체에 실리나요?","업종과 소식의 성격에 따라 경제지·산업 전문지·온라인 매체를 조합합니다. 매체 리스트는 배포 전에 공유드립니다."),
       ("한 달에 몇 건이나 진행하나요?","플랜에 따라 다르며, 건수보다 '소식의 뉴스 가치'가 우선입니다. 무리한 대량 송출은 스팸이 되어 오히려 해가 됩니다."),
       ("해외 배포는 어떻게 진행되나요?","목표 국가의 언어로 현지화한 보도자료를 현지 매체·기자에게 배포합니다. 베트남·중국 등 국가별 매체망을 활용하며, 엔터프라이즈 플랜 또는 별도 견적으로 진행합니다.")],
  vis="""<div class="svc-vis clips rv">
<div class="clip c1"><div class="pressname">산업 전문지</div><h5>○○정밀, 항공부품 소량 생산 라인 증설… 수출바우처 선정</h5></div>
<div class="clip c2"><div class="pressname">경제지</div><h5>"베트남 수출 물꼬" ○○정밀, 동남아 인증 획득하고 첫 계약</h5>
<div class="tagchips"><span class="good">✓ 제3자 검증 출처</span><span class="good">✓ AI 인용 근거</span></div></div>
<div class="clip c3"><div class="pressname">온라인 뉴스</div><h5>○○정밀, 스마트공장 구축으로 정밀부품 납기 30% 단축</h5></div>
<div class="flowrow"><span>보도자료</span><i>→</i><span>기자 매칭</span><i>→</i><span>기사 발행</span><i>→</i><span class="hl">AI가 인용</span></div>
</div>""",
  tool="""<section class="sec" style="background:var(--sky-2)"><div class="wrap"><div class="shead center rv"><span class="eyebrow">무료 도구 · 곧 공개</span><h2 class="h2">우리 회사 소식, 기사로 나갈 수 있을까요?</h2><p class="lead">간단한 정보만 입력하면 기사화 가능성과 보완 포인트를 무료로 진단해 드립니다.</p></div><div class="prcheck rv"><div class="prc-score"><div class="prc-gauge"><b>74</b><span>점</span></div><p>현재 소재는 보도자료로 활용할 수 있습니다. 구체적 수치와 시장적 의미를 더하면 기사 채택 가능성이 올라갑니다.</p></div><div class="prc-items"><div class="prc-i"><span>시의성</span><i><em style="width:80%"></em></i><b>16/20</b></div><div class="prc-i"><span>구체성</span><i><em style="width:60%"></em></i><b>12/20</b></div><div class="prc-i"><span>차별성</span><i><em style="width:75%"></em></i><b>15/20</b></div><div class="prc-i"><span>산업적 의미</span><i><em style="width:65%"></em></i><b>13/20</b></div><div class="prc-i"><span>신뢰 근거</span><i><em style="width:90%"></em></i><b>18/20</b></div></div></div><div class="prc-cta rv"><b>기사 가능성은 있지만, 어떻게 써야 할지 막막하신가요?</b><span>messeze가 강점을 기사 관점으로 정리하고 보도자료 작성부터 언론 배포까지 진행해 드립니다.</span><a href="../index.html#final" class="btn btn-co">무료 보도자료 상담받기</a></div></div></section>""",
  rel=["channels","visibility"])

BY_SLUG = {x["slug"]: x for x in S}

def build_page(x):
    rel_cards = ""
    for slug in x["rel"]:
        r = BY_SLUG[slug]
        rel_cards += f"""<a class="relc rv" href="{r['slug']}.html"><span class="no">SERVICE {r['no']}</span><b>{r['title']}</b><span>{r['one'][:38]}…</span></a>"""
    items = "\n".join(f"""<div class="dt rv"><span class="c">POINT {i+1:02d}</span><b>{t}</b><p>{d}</p></div>""" for i,(t,d) in enumerate(x["items"]))
    procs = "\n".join(f"""<div class="pr rv"><span class="n">{i+1}</span><b>{t}</b><p>{d}</p></div>""" for i,(t,d) in enumerate(x["proc"]))
    fits = "\n".join(f"""<div><span class="c">✓</span>{f}</div>""" for f in x["fit"])
    delivs = "".join(f"<span>{d}</span>" for d in x["deliv"])
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
<div class="cta"><a href="../index.html#final" class="btn btn-co">무료 진단으로 시작하기</a><a href="../pricing.html" class="btn btn-gh">요금 보기</a></div>
</div>
{x['vis']}
</div></section>

<section class="sec"><div class="wrap">
<div class="shead rv"><span class="eyebrow">무엇을 하나요</span><h2 class="h2">이 서비스에 포함된 것</h2><p class="lead">{x['intro']}</p></div>
<div class="dt-grid">{items}</div>
{reltool}
</div></section>

{x.get('tool','')}<section class="sec proc"><div class="wrap">
<div class="shead center rv"><span class="eyebrow">진행 절차</span><h2 class="h2">이렇게 진행됩니다</h2></div>
<div class="pr-grid">{procs}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="fitrow">
<div class="rv"><span class="eyebrow">이런 기업에 맞아요</span><h2 class="h2" style="margin-bottom:22px">이런 상황이라면,<br>시작할 때입니다</h2><div class="fit-list">{fits}</div></div>
<div class="dv-card rv"><h3>이렇게 받으세요</h3><div class="chips">{delivs}</div></div>
</div>
</div></section>

<section class="sec" style="background:var(--sky-2)"><div class="wrap">
<div class="shead center rv"><span class="eyebrow">자주 묻는 질문</span><h2 class="h2">{x['title']}, 궁금한 점</h2></div>
<div class="faq rv">{faqs}</div>
</div></section>

<section class="sec" style="padding-top:40px"><div class="wrap">
<div class="shead center rv"><span class="eyebrow">함께 보면 좋은 서비스</span><h2 class="h2">이 서비스와 이어집니다</h2></div>
<div class="rel-grid">{rel_cards}</div>
</div></section>

<div class="wrap"><div class="cta-band rv">
<div><h3>우리 회사에 필요한 조합이 궁금하다면</h3><p>AI 가시성 무료 진단 결과를 보고, 필요한 서비스만 골라 시작하세요.</p></div>
<a class="btn" href="../index.html#final">무료 진단 신청하기</a></div></div>
{foot()}
{FAQ_JS}
</body></html>"""

for x in S:
    with io.open(os.path.join(OUT, x["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(build_page(x))
print("OK:", len(S), "service pages →", OUT)
