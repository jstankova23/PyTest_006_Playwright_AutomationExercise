# 1) SUCCESS MESSAGE BEZ NÁSLEDNÉHO PŘESMĚROVÁNÍ (subscription: TC10, TC11; product review: TC21)
TC10 - pay_subs_msg, success message bez následného přesměrování na jinou URL
# 7. Verify success message 'You have been successfully subscribed!' is visible
###	Po kliknutí na šipku vedle emailu se zobrazí jen krátce hláška o úspěšné registraci emailu k odběru novinek.
###	Pokud se nedaří získat selektor z DevTools během krátkého zobrazení hlášky, pak je nutné těsně před vyvoláním hlášky 
### (tzn. před kliknutím na šipku za emailem) provést v DevTools zastavení běhu na JavaScriptu na události typu 'kliknutí':
### - DevTools - záložka Sources - Event Listener Breakpoints/ Mouse / Click
### - kliknout na šipku vedle emailu (potvrdit odeslání emailu pro odběr novinek)
### - šipkou na debugovací liště postupně krokovat až do momentu zobrazení dané hlášky
### - kliknout na ikonku pro získání selektoru a označit danou hlášku
### - v záložce Elements dle označení pozice elementu v DOM sestavit si ručně CSS lokátor unikátní pro danou stránku
### - třída 'alert-success' není na stránce unikátní, tuto třídu využívá i hláška po úspěšně odeslaném review na produkt (TC21)
success_subs_msg = page.locator("#success-subscribe")  # CSS lokátor na dočasnou hlášku, nutné ID, třída 'alert-success' by nestačila
expect(success_subs_msg).to_be_visible(timeout=1000)   # vyčkání na zobrazení dočasné hlášky

TC11 - pay_subs_msg, success message bez následného přesměrování na jinou URL
success_subs_msg = page.locator("#success-subscribe")  # CSS lokátor na dočasnou hlášku, nutné ID, třída 'alert-success' by nestačila
expect(success_subs_msg).to_be_visible(timeout=1000)   # vyčkání na zobrazení dočasné hlášky



# 2) SUCCESS MESSAGE S NÁSLEDNÝM PŘESMĚROVÁNÍM (potvrzení platby: TC24)
TC24 - pay_success_msg, success message s následným přesměrováním na jinou URL
# 17. Click 'Pay and Confirm Order' button
# 18. Verify success message 'Your order has been placed successfully!'
### Kliknutí na tlačítko 'Pay and Confirm Order' na stránce https://automationexercise.com/payment okamžitě spustí:
### a) zobrazení velmi krátké dočasné hlášky: "Your order has been placed successfully!"
###  b) téměř okamžité přesměrování na URL: https://automationexercise.com/payment_done/0

### Hláška před přesměrováním je tak rychlá, že má Playwright problém ji samostatně zachytit.
### U testů ověřujících jiný typ hlášky (TC10 – odběr novinek, TC11 – odběr novinek, TC21 – recenze produktu) se tento problém neřešil,
### protože tam nedochází k současnému přesměrování.

### Proto je zde použit WITH blok, který:
###   - synchronizuje kliknutí na tlačítko s očekávanou navigací
###   - zároveň umožní zachytit dočasnou hlášku ještě na stránce /payment

pay_and_confirm_btn = page.get_by_role("button", name="Pay and Confirm Order")   # lokátor pro tlačítko 'Pay and Confirm Order'
success_pay_msg = page.locator("#success_message .alert-success")                # lokátor dočasné hlášky před přesměrováním

# WITH blok sváže kliknutí a očekávané přesměrování do jednoho synchronního kroku, aby se Playwright neztratil mezi zobrazením hlášky a změnou URL.
with page.expect_navigation():
    pay_and_confirm_btn.click()

# Ověření, že se dočasná hláška skutečně zobrazila ještě před přesměrováním
expect(success_pay_msg).to_have_text("Your order has been placed successfully!", timeout=2000)


# 3) JAVA SCRIPT ALERT (REGISTRACE HANDLERU S AUTOMATICKÝM SPUŠTĚNÍM V MOMENTU VZNIKU ALERTU)
TC06 - JS Alert
# 8. Click 'Submit' button — POZOR! Nejdříve je nutné zachytit JavaScript alert!
# 9. Click OK button - POZOR! Jedná se o JavaScript alert "Press OK to proceed."
### Po kliknutí na tlačítko 'Submit' se objeví JavaScript alert, ale s krátkým zpožděním.
### Alert blokuje stránku, proto je nutné před samotným kliknutím zaregistrovat handler, 
### který se automaticky spustí v okamžiku, kdy alert skutečně vznikne.
### Kroky 8 a 9 se tedy řeší společně: nejprve registrace handleru, pak kliknutí na 'Submit'.
submit_btn = page.get_by_role("button", name="Submit")      # lokátor pro tlačítko 'Submit'

### Registrace handleru pro JavaScript alert ještě před kliknutím na 'Submit'.
### Handler se provede automaticky při zobrazení alertu a provede jeho potvrzení (OK).
### Když ze alert objeví, Playwright automaticky předá do parametru funkce objekt typu 'Dialog'.
### Objekt 'Dialog' obsahuje informace o alertu (např. text, typ) a metody pro práci s ním.
### 'dialog.message' je atribut/vlastnost objektu 'Dialog', obsahuje text zobrazený v alert okénku ("Press OK to proceed.")
### Tlačítko 'OK': systémové alerty nemají lokátory, nelze na 'OK' tedy kliknout, nutné použít accept() - vestavěnou metodu objektu 'Dialog'. 
### Pozn. Nelze použít expect_event("dialog"), který očekává alert v přesně vymezeném časovém okně, je pouze pro alerty s okamžitým výskytem.
### Zatímco page.once("dialog", handler) registruje jednorázovou obsluhu alertu, která může reagovat kdykoliv později, bez ohledu na zpoždění.
def handle_alert(dialog):             # parametrem je objekt Dialog s info o alertu
    assert "Press" in dialog.message  # kontrola textu "Press" v alertu přes atribut objektu 'Dialog' ('dialog.message')
    dialog.accept()                   # potvrzení alertu metodou accept(), ne kliknutím na 'OK' - nemá lokátor

page.once("dialog", handle_alert)  # handler čeká na alert a spustí se pouze jednou

submit_btn.click(force=True)   # přinucené kliknutí na 'Submit' — alert přijde později, handler ho ale bezpečně odchytí