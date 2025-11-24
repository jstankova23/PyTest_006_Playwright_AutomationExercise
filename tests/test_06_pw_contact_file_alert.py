# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# POZOR - NEDOKONČENÝ TEST, NEFUNGUJE OD KROKU 8 - PROBLÉM S ALERTEM VYVOLANÝM PO KLIKNUTÍ NA TLAČÍTKO SUBMIT, 
# PLAYWRIGHT NEUMÍ U NĚJ KLIKNOUT NA TLAČÍTKO OK (není pak možné přejít ke kroku 10, 11)

# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 06_TEST CASE: Contact Us Form - File Attachment
# PŘIHLÁŠENÍ UŽIVATELE DO DEMO E-SHOP WEBU 'https://automationexercise.com/' - POZITIVNÍ TEST
# test neobsahuje žádné přihlášení uživatele
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
    # vložení přílohy 'Sample.docx' dostupné v podsložce tests/test_files
    # nekliká se na tlačítko 'Vložit soubor', Playwright neumí pracovat s otevřeným dialogem
    file_input = page.locator("input[name='upload_file']")
    file_input.set_input_files("tests/test_files/Sample.docx")

    # 8. Click 'Submit' button — POZOR! Nejdříve je nutné zachytit JavaScript alert!
    # JavaScript alert se objeví po kliknutí na 'Submit' a blokuje stránku, proto je nutné ho zachytit před kliknutím
    submit_btn = page.get_by_role("button", name="Submit")      # lokátor pro tlačítko 'Submit'

    # Zachycení dialogu MUSÍ proběhnout těsně před kliknutím, jinak test zamrzne
    with page.expect_event("dialog") as dialog_info:
        submit_btn.click(force=True)

    # 9. Click OK button - POZOR! JavaScript alert "Press OK to proceed."
    # systémové modální okno prohlížeče: alert("Press OK to proceed!");
    # nenínení v DOM, nelze na něm najít žádný lokátor;
    # u testů s alert() je povinné udělat zachycení dialogu před akcí, která ho vyvolá, jinak se test zasekne, stránka se zablokuje a Playwright pouze čeká
    # Práce s JavaScript alertem (Press OK to proceed.)
    dialog = dialog_info.value          # získání JavaSccipt okna
    assert "Press" in dialog.message    # původní verze: assert dialog.message == "Press OK to proceed."
    dialog.accept()                     # kliknutí na OK

    # 10. Verify success message 'Success! Your details have been submitted successfully.' is visible 
    success_msg = page.get_by_text("Success! Your details have been submitted successfully.")  # lokátor cílového textu / nadpisu
    expect(success_msg).to_be_visible(timeout=1000)                                      # čekání, dokud se nezobrazí očekávaný text / nadpis

    # 11. Click 'Home' button and verify that landed to home page successfully
    page.get_by_role("link", name="Home").click()                       # kliknutí na ikonku 'Home' v záhlaví stránky
    expect(page).to_have_url("https://automationexercise.com/")         # čekání, dokud se nezobrazí domovská stránka

 


