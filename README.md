# PyTest_006_Playwright_AutomationExercise
Automatizované UI testy pro demo e‑shop https://automationexercise.com/ pomocí **Playwright + Pytest** (Python)

> Projekt je aktuálně v aktivním vývoji (work in progress).

**Autor:**                      Jana Staňková  
**Verze projektu:**             0.7.5 
**Datum vytvoření:**            11. 11. 2025  
**Datum poslední aktualizace:** 2. 12. 2025 
**Python:**                     3.10+  
**Licence:**                    MIT  

---

## Popis projektu

Tento projekt obsahuje automatizované UI testy pro demo e‑shop: https://automationexercise.com

Tento projekt obsahuje sadu 26 testů v Pythonu s využitím **pytest + Playwright** pro demo e‑shop 
[automationexercise.com](https://automationexercise.com/). 
Testy následují oficiální [Test Cases](https://automationexercise.com/test_cases).
Projekt obsahuje pozitivní a negativní testy registrace uživatele, jeho přihlášení a odhlášení, komunikaci s e-shop webem přes kontaktní formulář s odesláním souboru v příloze, vyhledávání produktů, odběr novinek a veškerou manipulaci s objednávkou a fakturou. Testy pracují s produkty,
které jsou na stránkách demo e-shopu koncipovány jako karty zabalené do obalu (wrapper) v mřížce. Pro vložení produktu je nutný hover nad danou
kartou produktu, což vyvolá překrývací overlay vrstvu s nabídkou tlačítek nutných k nákupu. Testy pracují i s modálními okny a JavaScript alertem.

## PyTest + Playwright – AutomationExercise

Testy jsou psány pomocí frameworků **Playwright** a **PyTest** a jsou
navrženy s důrazem na:
- plnou izolaci jednotlivých testů,
- opakovatelnost běhu,
- stabilitu při hromadném spouštění,
- minimalizaci vzájemného ovlivňování testů.
---

## Technologie

- Python
- pytest
- Playwright (sync API)
- pytest‑playwright plugin

---

## GDPR a uložený stav prohlížeče

Projekt využívá soubor **gdpr.json**, který obsahuje uložený stav prohlížeče (cookies + localStorage) po odsouhlasení GDPR a je uložen
v kořenovém adresáři projektu.

Tento stav je při spuštění každého testu načítán do nového browser contextu pomocí fixture `context_gdpr`.

Díky tomu:
- není nutné v jednotlivých testech řešit cookie lištu,
- každý test začíná s jednotným výchozím stavem,
- nedochází k flakiness způsobené modálními okny.

---

## Základní architektura běhu testů

- **browser** – jeden sdílený proces Chromium pro celou testovací session (session scoped)
- **context_gdpr** – nový izolovaný browser context pro každý test (function scoped),
                     session-scoped uživatel 'Session User' si vytváří vlastní context
- **page** – jedna konkrétní stránka (tab) v rámci daného browser contextu (function scoped)

---

## Adresářová struktura projektu (nedokončena, fáze vývoje)
```
PyTest_006_Playwright_AutomationExercise/
├── tests/
│   ├── test_00_pw_gdpr.py
│   ├── test_01_pw_register_positive.py
│   ├── test_02_pw_login_positive.py
│   ├── test_03_pw_login_negative.py
│   ├── test_04_pw_logout.py
│   ├── test_05_pw_register_negative.py
│   ├── test_06_pw_contact_file_alert.py      vyžaduje soubor 'test_files/Sample.docx' (příloha k formuláři)
│   ├── test_07_pw_test_cases_page.py
│   ├── test_08_pw_product_pages.py
│   ├── test_09_pw_product_search.py
│   ├── test_10_pw_subsribe_home_footer.py
│   ├── test_11_pw_subsribe_cart_footer.py
│   ├── test_12_pw_product_cart.py
│   ├── test_13_pw_product_qty.py
│   ├── test_14_pw_order_reg_while_checkout.py
│   ├── test_15_pw_order_reg_before_checkout.py
│   ├── test_16_pw_order_login_before_checkout.py
│   ├── test_17_pw_remove_product_cart.py
│   ├── test_18_pw_filter_categories_home_page.py
│   ├── test_19_pw_filter_brands_products_page.py
│   ├── test_20_pw_login_after_cart.py
│   ├── test_21_pw_product_review.py
│   └── test_files/
│       └── Sample.docx                      příloha pro test 'test_06_pw_contact_file_alert.py'
├── .gitignore
├── conftest.py                              fixtures
├── gdpr.json                                stav prohlížeče pro fixture 'context_gdpr'   
├── README.md
└── requirements.txt

```

---

## Seznam Test Cases podle AutomationExercise.com

Níže je kompletní přepis seznamu Test Cases ze stránky:  
https://automationexercise.com/test_cases

### **Test Case 0:** Accept GDPR (přidáno, není v seznamu Test Cases)
### **Test Case 1:** Register User  
### **Test Case 2:** Login User with correct email and password  
### **Test Case 3:** Login User with incorrect email and password  
### **Test Case 4:** Logout User  
### **Test Case 5:** Register User with existing email  
### **Test Case 6:** Contact Us Form  
### **Test Case 7:** Verify Test Cases Page  
### **Test Case 8:** Verify All Products and product detail page  
### **Test Case 9:** Search Product  
### **Test Case 10:** Verify Subscription in home page  
### **Test Case 11:** Verify Subscription in Cart page  
### **Test Case 12:** Add Products in Cart  
### **Test Case 13:** Verify Product quantity in Cart  
### **Test Case 14:** Place Order: Register while Checkout  
### **Test Case 15:** Place Order: Register before Checkout  
### **Test Case 16:** Place Order: Login before Checkout  
### **Test Case 17:** Remove Products From Cart  
### **Test Case 18:** View Category Products  
### **Test Case 19:** View & Cart Brand Products  
### **Test Case 20:** Search Products and Verify Cart After Login  
### **Test Case 21:** Add review on product  
### **Test Case 22:** Add to cart from Recommended items  
### **Test Case 23:** Verify address details in checkout page  
### **Test Case 24:** Download Invoice after purchase order  
### **Test Case 25:** Verify Scroll Up using ‘Arrow’ button and Scroll Down functionality  
### **Test Case 26:** Verify Scroll Up without ‘Arrow’ button and Scroll Down functionality  

---

## Poznámky k implementaci
- Každý test je psaný jako samostatný soubor v `tests/`.
- Testy využívají lokátory z Playwright Inspectora. V případech nejednoznačné identifikace testy využívají ručně sestavené CSS lokátory.
- Testy jsou navrženy tak, aby byly **stabilní**, **opakovatelně spustitelné** a **nezávislé**.

---

## Strategie uživatelů v testech

Architektura uživatelů je navržena tak, aby byla zajištěna **nezávislost jednotlivých testů**. Testy si vzájemně neovlivňují data a je možné je spouštět **opakovaně i paralelně**.

Všichni uživatelé jsou vytvářeni s **dynamicky generovaným e-mailem** a po dokončení testů jsou mazáni. Výjimkou je uživatel **Session User**, který je mazán až na konci celé testovací session po doběhnutí všech testů. Ostatní uživatelé jsou mazáni vždy v rámci konkrétního testu, pro který byli vytvořeni.

Uživatel **Session User** je sdílen mezi testy TC04 a TC05, které samy nevytvářejí nového uživatele, ale vyžadují přihlášení již existujícího uživatele. Tyto testy tedy využívají společného uživatele, který je automaticky vytvořen na začátku testovací session (i při spuštění jednotlivého testu samostatně) a je odstraněn až po dokončení celé session. Uživatel Session User má životnost celé testovací session (session scoped) 
a používá tak session scoped fixture 'browser', ale nemůže používat function scoped fixture 'context_gdpr'. Z tohoto důvodu fixture 'session_user' vytváří pro tohoto uživatele vlastní kontext.

Ostatní uživatelé jsou **unikátní pro každý test**. Liší se pouze způsobem jejich vytvoření:
- Testy, které mají v rámci scénáře zahrnutou registraci nového uživatele, si svého uživatele vytvářejí samy.
- Testy, které registraci netestují, využívají **specifické fixtures definované v souboru `conftest.py`**.

---

### Přehledná tabulka uživatelů

| Typ uživatele    | Email     | Vytváří                | Maže           | Životnost | Použití    |
|------------------|-----------|------------------------|----------------|-----------|------------|
| **Session User** | dynamický | fixture `session_user` | fixture        | celý běh  | TC04, TC05 |
| **Test 1 User**  | dynamický | samotný test           | test           | per-test  | TC01       |
| **Test 2 User**  | dynamický | fixture `test_2_user`  | test / fixture | per-test  | TC02       |
| **Test 14 User** | dynamický | test                   | test           | per-test  | TC14       |
| **Test 15 User** | dynamický | test                   | test           | per-test  | TC15       |
| **Test 16 User** | dynamický | fixture `test_16_user` | test / fixture | per-test  | TC16       |
| **Test 20 User** | dynamický | fixture `test_20_user` | fixture        | per-test  | TC20       |
| **Test 23 User** | dynamický | test                   | test           | per-test  | TC23       |
| **Test 24 User** | dynamický | test                   | test           | per-test  | TC24       |

---

### Ošetření selhání registrace uživatele

U všech uživatelů je používán **dynamicky generovaný email**, což minimalizuje riziko kolizí s cizími testovacími daty na veřejném demo e-shopu.

Přesto jsou:
- všechny **fixtures a testy s registrací uživatele ošetřeny chybovou hláškou** pro případ, že by se i přesto pokusily o registraci s již existujícím emailem,
- pro ladění je doporučeno spouštění testů s příznaky:

```bash
pytest -s -v

---

## Notifikace

V rámci testů v Playwrightu jsou zpracovávány různé typy notifikací:

1. **JavaScript alert se zpožděným výskytem**  
   Test Case 6 – Contact Us Form  
   `test_06_pw_contact_file_alert.py`

2. **Dočasná notifikační hláška v DOM (flash message / success message)**  
   Test Case 10 – Verify Subscription in home page  
   `test_10_pw_subscribe_footer.py`

---

## Fixtures (conftest.py)

Soubor `tests/conftest.py` obsahuje klíčové fixtures:

| **FIXTURE**       | **SCOPE** | **AUTOMATICKÉ SPUŠTĚNÍ** | **VÝSLEDEK** |
|-------------------|-----------|--------------------------|--------------|
| `browser`         | session   | Ne                       | sdílený prohlížeč |
| `context_gdpr`    | function  | Ne                       | nový izolovaný kontext se zpracovaným GDPR pro každý test |
| `page`            | function  | Ne                       | nová stránka s domovskou URL pro každý test |
| `session_user`    | session   | Ano                      | uživatel **Session User** pro celou session, smazán na konci všech testů |
| `test_2_user`     | function  | Ne                       | uživatel **Test_2 User** unikátní pro TC02, smazán na konci testu |
| `test_16_user`    | function  | Ne                       | uživatel **Test_16 User** unikátní pro TC16, smazán na konci testu |
| `test_20_user`    | function  | Ne                       | uživatel **Test_20 User** unikátní pro TC20, smazán na konci testu |

## Spuštění testů

V kořenovém adresáři projektu:

```bash
pytest -s -v
```

Při lokálním ladění lze přepnout prohlížeč do viditelného režimu:

- v `conftest.py` změnit:

```python
browser = p.chromium.launch(headless=True, slow_mo=300)
```

na

```python
browser = p.chromium.launch(headless=False, slow_mo=300)
```

Tím budou jednotlivé kroky testů v prohlížeči dobře pozorovatelné.




