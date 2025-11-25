# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'.
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py.
# Testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases).

from playwright.sync_api import Page, expect

# 06_TEST CASE: Contact Us Form - File Attachment
# TEST KONTAKTNÍHO FORMULÁŘE S ODESLÁNÍM SOUBORU V PŘÍLOZE A S ODKLIKNUTÍM JAVASCRIPT ALERTU
# Test vyžaduje testovací soubor pro přílohu (tests/test_files/Sample.docx).
# Test neobsahuje žádné přihlášení uživatele.
def test_contact_file_alert(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url

    # 4. Click on 'Contact Us' button
    contact_link = page.get_by_role("link", name=" Contact us")     # vyhledání linku v záhlaví stránky pro otevření kontaktního formuláře
    contact_link.click()                                             # kliknutí na link

    # 5. Verify 'GET IN TOUCH' is visible
    contact_heading = page.get_by_role("heading", name="Get In Touch")  # lokátor pro nadpis 'Get In Touch' na nové stránce
    expect(contact_heading).to_be_visible(timeout=1000)                 # ověření přesměrování na stránku s daným nadpisem a zpomalení

    # 6. Enter name, email, subject and message
    name = "Jana Testovací"                    
    email = "test@test.com"                  
    subject = "Automatizovaný test - kontaktní formulář, příloha"                
    message = "PyTest_006_Playwright_AutomationExercise/tests/test_06_pw_contact_form_file.py/test_contact_form_file Vám zasílá přílohu 'Sample.docx'."             

    ### Lokátory
    name_input = page.get_by_role("textbox", name="Name")
    email_input = page.get_by_role("textbox", name="Email", exact=True)
    subject_input = page.get_by_role("textbox", name="Subject")
    message_input = page.get_by_role("textbox", name="Your Message Here")

    ### Vyplnění polí hodnotami proměnných
    name_input.fill(name)                     
    email_input.fill(email)                     
    subject_input.fill(subject)    
    message_input.fill(message)             

    # 7. Upload file
    # Vložení přílohy 'Sample.docx' dostupné v podsložce tests/test_files.
    # Nekliká se na tlačítko 'Vložit soubor', Playwright neumí pracovat s otevřeným dialogem.
    file_input = page.locator("input[name='upload_file']")
    file_input.set_input_files("tests/test_files/Sample.docx")

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


    # 10. Verify success message 'Success! Your details have been submitted successfully.' is visible 
    success_msg = page.locator("#contact-page .alert-success")        # lokátor cílového textu / nadpisu
    expect(success_msg).to_be_visible(timeout=1000)                   # čekání, dokud se nezobrazí očekávaný text / nadpis

    # 11. Click 'Home' button and verify that landed to home page successfully
    # Pozor: Na stránce jsou 2 linky 'Home' se stejným funkčím lokátorem v Playwright Inspectoru (pod hláškou o úspěchu a v záhlaví stránky).
    # page.get_by_role("link", name=" Home") - tento funkční lokátor je na stránce duplicitní.
    # Je třeba jednoznačně identifikovat tlačítko/link pomocí CSS lokátoru.
    home_sucess_btn = page.locator("a.btn.btn-success") # CSS lokátor pro tlačítko/link 'Home' pod hláškou o úspěchu (ne link 'Home' v záhlaví stránky)
    home_sucess_btn.click() # kliknutí na dané tlačítko/link 'Home' 
    expect(page).to_have_url("https://automationexercise.com/")    # čekání, dokud se nezobrazí domovská stránka


