"""
=============================================================================================================================
FIXTURES PRO TESTOVÁNÍ DEMO E-SHOP WEBU (PLAYWRIGHT + PYTEST)
=============================================================================================================================
Autor:                      Jana Staňková
Verze projektu:             0.1.0  
Datum vytvoření:            11. 11. 2025  
Datum poslední aktualizace: 

# Popis:
Projekt zahrnuje dvě fixture, které jsou automaticky spuštěny hned na začátku testu pro celou session - fixture **'accept_gdpr'**
a fixture **'session_user'**. Pokud tester spustí pouze vybraný test, nikoliv celou testovací session, i tak jsou obě fixture
automaticky volány a vykonávají svoji práci. Automaticky spouštěné fixtures (autouse=True) nemusí být uvedeny v parametrech testů.
Automaticky spouštěné fixtures pro celou testovací session či jednotlivý test:
- fixture **'accept_gdpr'** zajistí jednorázové odsouhlasení GDPR podmínek pro celou testovací session.
- fixture **'session_user'** na začátku testovací session založí skupinového uživatele **'Session_User'** a po doběhnutí všech 
  testů (na konci testovací session) tato fixture daného uživatele vymaže. Tzn. fixture 'session_user' vykonává akci na úplném 
  začátku a na úplném konci testovací session či každého indviduálně spuštěného testu.

V projektu jsou předefinovány vestavěné fixtures **'browser'** a **'page'** poskytované pluginem 'pytest-playwright'. 
Důvodem je potřeba mít plnou kontrolu nad parametry spuštění prohlížeče (headless, slow_mo) a nad výchozí URL stránky.

1) Fixture **'accept_gdpr'** je spuštěna automaticky hned na začátku testovací session či jednotlivého testu (autouse=True). 
Zajišťuje odsouhlasení GDPR/CMP dialogu, takže jednotlivé testy už tento krok nemusí řešit. Tato fixture vyžaduje fixture 
'browser_context', proto musí být obě session-scoped.

2) Fixture **'browser_context'** vytváří sdílený prohlížeč a kontext pro všechny testy. Spuštění pro celou session je nutné 
kvůli kopmatibilitě s fixture 'accept_gdpr'. 
Parametry (headless, slow_mo) lze snadno upravit dle potřeby. Do produkčního odevzdání se používá headless=True; pro lokální 
ladění lze nastavit headless=False. Finální verze tohoto projektu bude nastavena s během testu na pozadí (headless = True). 
Tester si může toto nastavení změnit na běh testu s viditelným oknem prohlížeče (headless = False).

3) Fixture **'page'** vytváří novou stránku (tab) pro každý test a automaticky přechází na výchozí URL demo e-shopu 
(https://automationexercise.com/).
Odstraňuje v intervalech reklamní banner v iframe, což při běhu testu na pozadí není nutností a tuto část je možné zakomentovat. 
Fixture předává připravenou stránku každému testu. Po každém testu stránku zavře.

4) Fixture **'temp_user'** vytváří dočasného uživatele **'Temp_User** s dynamicky vygenerovanou mailovou adresou pro každý
jednotlivý test, který ji ve svém běhu volá. Na konci testu je tento uživatel vždy smazán (testem nebo pomocí této fixture). 
Uživatel 'Temp_User' je unikátní pouze pro daný běh testu, není sdílen více testy.

5) Fixture **'session_user'** je spuštěna automaticky hned na začátku testovací session či jednotlivého testu (autouse=True). 
Založí uživatele **'Session_User'** s dynamicky vytvořeným emailem pro celou testovací session. V rámci jedné testovací session
je tento uživatel sdílen vícero testy, které se na něj odvolávají. Po doběhnutí všech testů (na konci celé testovací session) 
fixture tohoto uživatele vymaže.

# Přehled Fixtures

| **FIXTURE**       | **SCOPE** | **AUTOMATICKÉ SPUŠTĚNÍ** | **VÝSLEDEK** |
|-------------------|-----------|--------------------------|--------------|
| `accept_gdpr`     | session   | Ano                      | přijetí GDPR |
| `browser_context` | session   | Ne                       | sdílený prohlížeč a kontext pro všechny testy |
| `page`            | function  | Ne                       | nová stránka s domovskou URL pro každý test |
| `temp_user`       | function  | Ne                       | uživatel **Temp_User** unikátní pro každý test, smazán na konci testu |
| `session_user`    | session   | Ano                      | uživatel **Session_User** pro celou session, smazán na konci všech testů |

"""

import pytest
import uuid                                             # pro fixtures 'temp_user', 'static_session_user'
from playwright.sync_api import sync_playwright, Page, expect

# 1) FIXTURE PRO ODSOUHLASENÍ GDPR
# jednorázové odsouhlasení GDPR dialogového okna pro celou testovací session;
# 'autouse=True' zajistí, že se daná fixture spustí automaticky před prvním testem;
# fixture využívá fixture 'browser_context' (scope=session), protože cookies po odsouhlasení musí zůstat zachovány i pro ostatní testy
@pytest.fixture(scope="session", autouse=True)
def accept_gdpr(browser_context):

    page = browser_context.new_page()
    page.goto("https://automationexercise.com/")
    page.wait_for_timeout(1000)

    consent_frame = None

    # hledání tlačítka v iframe
    for frame in page.frames:
        btn = frame.locator("button.fc-button.fc-cta-consent.fc-primary-button")
        if btn.count() > 0:
            consent_frame = frame
            break

    if consent_frame:
        consent_btn = consent_frame.locator("button.fc-button.fc-cta-consent.fc-primary-button")
        consent_btn.click(force=True)
        page.wait_for_timeout(300)

    page.close()

     
# 2) FIXTURE PRO SPUŠTĚNÍ PROHLÍŽEČE - CHROMIUM
# vestavěná fixture 'browser' a 'context' z pluginu pytest-playwright předefinovaná vlastními parametry; 
# vytváří sdílený browser + context pro celou session;
# paramater 'scope' pro celou session kvůli kompatibilitě scope s fixture 'accept_gdpr', která tuto fixture volá;
# Parametry lze měnit:
# - headless=True  - default pro odevzdání projektu (běh na pozadí);
# - headless=False - viditelné okno prohlížeče při lokálním ladění;
# - slow_mo        - zpomalení akce pro snadné sledování průběhu testů;
# fixture spouští Playwright, otevírá prohlížeč Chromium s uvedenými nastaveními a předává jej testům, po ukončení testu se prohlížeč uzavře
@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        yield context
        browser.close()


# 3) FIXTURE PRO VYTVOŘENÍ VLASTNÍ STRÁNKY (page)
# vytvoří novou stránku pomocí sdíleného browser contextu (fixture browser_context);
# automaticky přejde na domovskou stránku e-shopu;
# otevře v již spuštěném prohlížeči nový tab, přejde na výchozí URL demo e-shopu, odstraní reklamní banner v iframe a předá tuto stránku testu;
# odstranění reklamního banneru v iframe probíhá pomocí page.add_init_script(), které maže všechny iframe reklamy v pravidelných intervalech (2x za sekundu), 
# protože reklama se může znovu objevit během scrollování;
# po dokončení testu se vytvořená stránka (tab) automaticky uzavře
@pytest.fixture()
def page(browser_context):
    page = browser_context.new_page()

    # Odstranění reklamních iframe bannerů (Google Ads) - důležité pouze pro testera/support sledující průběh testu v zobrazeném oknu prohlížeče
    page.add_init_script("""setInterval(() => {document.querySelectorAll("iframe, .google-auto-placed, .adsbygoogle-container")
            .forEach(el => el.remove());}, 100);""")

    page.goto("https://automationexercise.com/")
    page.wait_for_load_state("domcontentloaded")
    yield page
    page.close()


# 4) FIXTURE PRO VYTVOŘENÍ DOČASNÉHO UŽIVATELE `Temp_User`
# fixture vyžaduje import uuid;
# fixture vytvoří unikátního dynamického uživatele pro každý test, který vyžaduje již existujícího uživatele;
# po dokončení testu uživatele smaže, pokud ho nesmazal test
@pytest.fixture
def temp_user(page: Page):
    # Generování unikátních dynamických údajů
    email = f"tempuser_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123"

    # Vytoření dočasného uživatele (kompletní registrace)
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name=" Signup / Login").click()

    page.get_by_role("textbox", name="Name").fill("Temp_User")
    page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address").fill(email)
    page.get_by_role("button", name="Signup").click()

    expect(page.get_by_text("Enter Account Information")).to_be_visible() # čekání na stránku s textem "Enter Account Information"

    # Vyplnění povinných údajů
    page.check("#id_gender1")
    page.fill("#password", password)
    page.select_option("#days", "10")
    page.select_option("#months", "5")
    page.select_option("#years", "1990")
    page.fill("#first_name", "Temp")
    page.fill("#last_name", "User")
    page.fill("#address1", "123 Test Street")
    page.fill("#state", "Florida")
    page.fill("#city", "Sarasota")
    page.fill("#zipcode", "34201")
    page.fill("#mobile_number", "+19415550123")

    # Dokončení registrace
    page.get_by_role("button", name="Create Account").click()
    expect(page.get_by_text("Account Created!")).to_be_visible()   # Vyčkání na potvrzení o úspěšně vytvořeném uživateli
    page.get_by_role("link", name="Continue").click()

    # Odhlášení (logout) uživatele - testy si samy provádějí přihlášení
    logout_link = page.get_by_role("link").filter(has_text="Logout")
    if logout_link.is_visible():
        logout_link.click()

    # Vrácení stránky do defaultního stavu
    page.goto("https://automationexercise.com/")

    # Vrácení údajů (email, heslo) testům
    yield {
        "email": email,
        "password": password,
    }

    # Cleanup – pokud test nezmazal uživatele, smaže ho fixture, mazání dočasného uživatele po každém testu
    page.goto("https://automationexercise.com/delete_account")
    # Někdy se zobrazí potvrzovací stránka
    if page.get_by_text("Account Deleted!").is_visible():
        page.get_by_role("link", name="Continue").click()


# 5) FIXTURE PRO VYTVOŘENÍ JEDNOHO UŽIVATELE `Session_User` PRO CELOU TESTOVACÍ SESSION
# fixture vyžaduje import uuid;
# 'autouse=True' zajistí, že se daná fixture spustí automaticky před prvním testem;
# fixture 'session_user' vytvoří uživatele pro celou statickou session, 
# (na rozdíl od fixture 'temp_user', která vytváří unikátního dočasného uživatele 'Temp:User' pro každou funkci);
# po dokončení všech testů se uživatel SessionUser na závěr přihlásí a vymaže
@pytest.fixture(scope="session", autouse=True)
def session_user(browser_context):
    page = browser_context.new_page() # vytvoření vlastní session page uvnitř existujícího browser_contextu

    # Dynamické vygenerování unikátního emailu
    email = f"sessionuser_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123"
    name = "Session_User"

    # Registrace uživatele SessionUser
    page.goto("https://automationexercise.com/")
    page.get_by_role("link", name=" Signup / Login").click()

    page.get_by_role("textbox", name="Name").fill(name)
    page.locator("form").filter(has_text="Signup").get_by_placeholder("Email Address").fill(email)
    page.get_by_role("button", name="Signup").click()


    expect(page.get_by_text("Enter Account Information")).to_be_visible() # čekání na stránku s textem "Enter Account Information"

    # Vyplnění povinných údajů
    page.check("#id_gender1")
    page.fill("#password", password)
    page.select_option("#days", "10")
    page.select_option("#months", "5")
    page.select_option("#years", "1990")
    page.fill("#first_name", "Session")
    page.fill("#last_name", "User")
    page.fill("#address1", "123 Test Street")
    page.fill("#state", "Florida")
    page.fill("#city", "Sarasota")
    page.fill("#zipcode", "34201")
    page.fill("#mobile_number", "+19415550123")

    # Dokončení registrace
    page.get_by_role("button", name="Create Account").click()
    expect(page.get_by_text("Account Created!")).to_be_visible()   # Vyčkání na potvrzení o úspěšně vytvořeném uživateli
    page.get_by_role("link", name="Continue").click()

    # Odhlášení uživatele – v případě, že je stále přihlášen; testy provádí přihlášení samy
    logout_link = page.get_by_role("link").filter(has_text="Logout")
    if logout_link.is_visible():
        logout_link.click()
    
    # Vrácení stránky do defaultního stavu
    page.goto("https://automationexercise.com/")

    # Vrácení údajů (email, heslo) testům
    yield {
        "email": email,
        "password": password,
    }

    # Cleanup – smazání uživatele po doběhnutí všech testů v session
    page.goto("https://automationexercise.com/login")

    # Přihlášení před mazáním
    page.locator("form").filter(has_text="Login").get_by_placeholder("Email Address").fill(email)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Login").click()

    expect(page.get_by_text("Logged in as")).to_be_visible() # čekání, dokud se v záhlaví stránky neobjeví text "příhlášen jako"

    # Smazání uživatele SessionUser
    page.goto("https://automationexercise.com/delete_account")
    expect(page.get_by_text("Account Deleted!")).to_be_visible()
    page.get_by_role("link", name="Continue").click()

    # Zavření contextu
    page.close()