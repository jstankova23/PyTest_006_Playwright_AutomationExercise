# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page

# 00_PRE-TEST CASE: Accept GDPR
# TEST FUNKČNOSTI FIXTURE PRO PŘIJETÍ GDPR V DEMO E-SHOP WEBU 'https://automationexercise.com/' PRO CELOU TESTOVACÍ SESSION
# oficiální test cases (https://automationexercise.com/test_cases) neobsahují tento krok přijetí GDPR;
# test ověření správné funkcionality fixture 'accept_gdpr' definované v souboru conftest.py;
# fixture 'accept_gdpr' se spouští automaticky ('autouse=True'), není nutno ji uvádět v parametrech;
# tento test pouze ověřuje, že souhlas byl skutečně udělen a GDPR dialog se již nezobrazuje
def test_gdpr_accepted(page: Page):
    page.wait_for_timeout(300)        # přechod na homepage (už se provede ve fixture page), vyčkání na načtení homepage

    # Lokátory
    gdpr_dialog = page.locator(".fc-consent-root")                                  # CSS lokátor (třída) pro GDPR dialogové okno
    consent_btn = page.locator("button.fc-button.fc-cta-consent.fc-primary-button") # CSS lokátor pro tlačítko Consent (přijetí GDPR)

    assert gdpr_dialog.count() == 0, "GDPR dialog is still in the DOM!"                 # GDPR dialog už nesmí být vidět
    assert consent_btn.count() == 0, "Consent button found — GDPR was not accepted!"    # tlačítko 'Consent' v GDPR dialogu už nesmí být vidět