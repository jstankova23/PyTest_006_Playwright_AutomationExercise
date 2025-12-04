# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 25_TEST CASE: Verify Scroll Up using 'Arrow' button and Scroll Down functionality
# TEST KLASICKÉHO SKROLOVÁNÍ NA HOME PAGE DO ZÁPATÍ STRÁNKY K NADPISU SUBSCRIPTION A RYCHLÉHO SKROLOVÁNÍ PŘES ŠIPKU ZPĚT DO ZÁHLAVÍ STRÁNKY S KONTROLOU 
# NADPISU V CAROUSELU V HERO BANNERU 
def test_subscibe_home_footer(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    

    # 4. Scroll down page to bottom
    subs_heading = page.get_by_role("heading", name="Subscription") # funkční lokátor nadpisu "SUBSCRIPTION" v zápatí domovské stránky
    subs_heading.scroll_into_view_if_needed()                       # skrolování do zápatí k nadpisu "SUBSCRIPTION"


    # 5. Verify 'SUBSCRIPTION' is visible
    expect(subs_heading).to_be_visible(timeout=500)  # ověření, že Playwright našel v zápatí požadovaný nadpis (lokátor z kroku 4)


    # 6. Click on arrow at bottom right side to move upward
    # Scroll Up šipka je generována dynamicky JavaScriptem (jquery.scrollUp) a nachází se v DOMu vždy na konci <body> hned za <footer>. 
    # Není součástí statického HTML. V DevTools není vidět a Playwright Inspector na ní poskytuje velmi křehký funkční lokátor.
    # Má CSS selektor a#scrollUp a href="#top". 
    # Po načtení je display: none, zobrazí se až po scrollu.
    scroll_arrow_btn = page.locator("#scrollUp") # lokátor na scroll up šipku v pravém dolním rohu stránky
    scroll_arrow_btn.click()


    # 7. Verify that page is scrolled up and 'Full-Fledged practice website for Automation Engineers' text is visible on screen
    ### Ověření úspěšného skrolování až do horní sekce Home page proběhne přes potvrzení existence nadpis 'Full-Fledged practice website for Automation Engineers'
    ### v Hero banneru, ve kterém se nachází rotující slider (carousel).
    ### Slider rotuje, v hero banneru se obměňují 3 různé slidy, ale každý obsahuje ten samý nadpis.
    ### V CSS lokátoru nadpisu je nutné použít 2 třídy: .item.active pro výběr právě zobrazeného slidu - vždy je aktivní a viditelný pro uživatele pouze jeden slide.
    ### Bez lokátoru tříd (.item.active) Playwright neví, ze kterých 3 slidů má daný nadpis vybrat.
    ### hero banner = <section id="slider">
    hero_heading = page.locator("section#slider .item.active h2") # lokátor pro nadpis v právě aktivním slidu
    expect(hero_heading).to_contain_text("Full-Fledged practice website")

    


           