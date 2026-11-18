from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
marker = 'const BUY_URL="https://bizzyjo-design.github.io/silentdisconet/buy/donttouch/";'
if marker in text:
    print("DON’T TOUCH purchase CTA already present; no changes needed.")
    raise SystemExit(0)

old = 'const APP_URL="https://bizzyjo-design.github.io/silentdisconet/";'
assert old in text, "APP_URL anchor not found"
text = text.replace(old, old + "\n" + marker, 1)

hook = '''function guestBuyLabel(){
 const labels={nl:"ORGANISEER ZELF EEN RONDE",en:"HOST YOUR OWN ROUND",fr:"ORGANISEZ VOTRE PROPRE PARTIE",de:"STARTE DEINE EIGENE RUNDE",es:"ORGANIZA TU PROPIA RONDA"};
 return labels[language]||labels.en;
}
function addGuestBuyCTA(sectionId){
 const existing=document.getElementById("guestBuyCTA");if(existing)existing.remove();
 if(creator)return;
 const section=$(sectionId);if(!section)return;
 const target=section.querySelector(".stack")||section;
 const a=document.createElement("a");
 a.id="guestBuyCTA";a.className="btn";a.href=BUY_URL;a.rel="noopener";a.textContent=guestBuyLabel();
 a.style.display="block";a.style.textDecoration="none";a.style.marginTop="12px";
 target.appendChild(a);
}
'''
anchor = "function renderGameOver(g){"
assert anchor in text, "renderGameOver anchor not found"
text = text.replace(anchor, hook + anchor, 1)

old_over = 'show("over");document.body.classList.add("alarm");'
assert old_over in text, "game-over show anchor not found"
text = text.replace(old_over, old_over + 'addGuestBuyCTA("over");', 1)

old_success = 'document.body.classList.remove("alarm");show("success");'
assert old_success in text, "success show anchor not found"
text = text.replace(old_success, old_success + 'addGuestBuyCTA("success");', 1)

old_stopped = 'if(wasCreator){creator=true;show("setup")}else{creator=false;show("stopped")}'
assert old_stopped in text, "stopped anchor not found"
text = text.replace(old_stopped, old_stopped + '\n if(!wasCreator)addGuestBuyCTA("stopped");', 1)

old_share = 'const t=T[language],count=Object.keys(roomData?.players||{}).length,text=`DON’T TOUCH — ${t.success} ${count} ${t.players}, ${settings.duration} ${t.minutes}.`;'
new_share = 'const t=T[language],count=Object.keys(roomData?.players||{}).length,text=`DON’T TOUCH — ${t.success} ${count} ${t.players}, ${settings.duration} ${t.minutes}.\\n${BUY_URL}`;'
assert old_share in text, "share-result anchor not found"
text = text.replace(old_share, new_share, 1)

path.write_text(text, encoding="utf-8")
print("Patched DON’T TOUCH guest purchase CTA and share link.")
