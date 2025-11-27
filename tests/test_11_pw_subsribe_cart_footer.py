# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 11_TEST CASE: Verify Subscription in Cart page
# TEST REGISTRACE K ODBĚRU NOVINEK ZE ZÁPATÍ DOMOVSKÉ STRÁNKY, I S POTVRZENÍM DOČASNÉ HLÁŠKY
def test_subscribe_cart_footer(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    
    # 4. Click 'Cart' button
    cart_link = page.get_by_role("link", name=" Cart")             # lokátor pro vyhledání linku pro nákupní vozík
    cart_link.click()                                               # kliknutí na link pro přihlášení uživatele

    # 5. Scroll down to footer
    subs_heading = page.get_by_role("heading", name="Subscription") # funkční lokátor nadpisu "SUBSCRIPTION" v zápatí 'cart' stránky
    subs_heading.scroll_into_view_if_needed() # skrolování do zápatí k nadpisu "SUBSCRIPTION"

    # 6. Verify text 'SUBSCRIPTION'
    expect(subs_heading).to_be_visible(timeout=500)  # ověření, že Playwright našel v zápatí požadovaný nadpis (lokátor s kroku 4)

    # 7. Enter email address in input and click arrow button
    ### Zadání emailu pro odběr novinek
    subs_email_input = page.locator("input#susbscribe_email")  # CSS lokátor pole pro zadání emailu k odběru novinek, v HTML mají překlep "susbscribe"
    # get_by_role("textbox", name="Your email address")    # funkční lokátor z Playwright Inspectora
    subs_email = "subscribe_email@test.com" # hard-coded testovací e-mail (bez kontroly duplicit už zadaných emailů pro odběr novinek)
    subs_email_input.fill(subs_email)  # vyplnění pole emailovou adresou

    ### Potvrzení / Odeslání emailu pro odběr novinek (kliknutí na tlačítko s šipkou)
    subs_arrow_btn =  page.locator("button#subscribe.btn.btn-default") # CSS lokátor pole pro šipku, potvrzení emailu k odběru novinek
    subs_arrow_btn.click() # kliknutí na tlačítko s šipkou

    # 8. Verify success message 'You have been successfully subscribed!' is visible
    ###	Po zadání emailu pro odběr novinek a jeho odeslání (klik na šipku vedle emailu) se zobrazí jen krátce hláška o úspěšném odeslání.
    ###	Pro získání CSS selektoru pro danou hlášku z DevTools je nutné po zadání emailu pro odběr novinek provést zastavení běhu na JavaScriptu na události kliknutí.
    ### DevTools - záložka Sources - Event Listener Breakpoints/ Mouse / Click
    ### Pak kliknout na šipku vedle emailu (potvrdit odeslání emailu pro odběr novinek) a šipkou na debugovací liště postupně odkrokovat JS kód do stavu zobrazení hlášky.
    ### V momentu zobrazení hlášky je možné získat už v záložce Elements její CSS lokátor.
    success_subs_msg = page.locator(".alert-success")      # CSS lokátor na dočasnou notifikaci v DOM získaný zastavením běhu na JS na události v DevTools
    expect(success_subs_msg).to_be_visible(timeout=1000)   # vyčkání na zobrazení dočasné hlášky


    
   