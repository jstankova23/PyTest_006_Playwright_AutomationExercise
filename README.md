# PyTest_006_Playwright_AutomationExercise
Automatizované UI testy pro demo e‑shop https://automationexercise.com/ pomocí **Playwright + Pytest** (Python)

> Projekt je aktuálně v aktivním vývoji (work in progress).

**Autor:**                      Jana Staňková  
**Verze projektu:**             0.1.0 
**Datum vytvoření:**            11. 11. 2025  
**Datum poslední aktualizace:** 
**Python:**                     3.10+  
**Licence:**                    MIT  

---

## Popis projektu
Tento projekt obsahuje sadu testů v Pythonu s využitím **pytest + Playwright** pro demo e‑shop 
[automationexercise.com](https://automationexercise.com/). 
Testy následují oficiální [Test Cases](https://automationexercise.com/test_cases).
Projekt obsahuje pozitivní a negativní testy registrace a přihlašování uživatele, komunikaci s e-shop webem přes kontaktní formulář s odesláním souboru v příloze, vyhledávání produktů, odběr novinek a práci s objednávkou a fakturou. 

---

## Technologie

- Python
- pytest
- Playwright (sync API)
- pytest‑playwright plugin

---

## Adresářová struktura projektu
```
PyTest_006_Playwright_AutomationExercise/
│
├── tests/
│   ├── test_00_pw_gdpr.py
│   ├── test_01_pw_register_positive.py
│   ├── test_02_pw_login_positive.py
│   ├── test_03_pw_login_negative.py
│   ├── test_04_pw_logout.py
│   ├── test_05_pw_register_negative.py
│   ├── test_06_pw_contact_file_alert.py
│   ├── test_07_pw_test_cases_page.py
│   ├── test_08_pw_product_pages.py
│   ├── test_09_pw_product_search.py
│   └── test_files/
│       └── Sample.docx
│
├── python.env
├── pytest.ini
└── README.md
```

---

## Seznam Test Cases podle AutomationExercise.com

Níže je kompletní přepis seznamu Test Cases ze stránky:  
https://automationexercise.com/test_cases

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

## Strategie uživatelů a e‑mailů

Architektura uživatelů řeší nezávislost jednotlivých testů. Testy si navzájem neovlivňují data a lze je spouště opakovaně a hromadně ve stejný čas. Koncept zahrnuje 3 typy uživatelů:

1. **Test_User** – unikátní uživatel vygenerovaný testovací funkcí 'test_registration_positive' ze souboru 'test_01_pw_register_positive.py', na závěr testu je uživatel vymazán, k vygenerování uživatele neslouží žádná fixture, email je hardcoded v kódu daného testu
2. **Temp_User** – unikátní uživatel pro každou jednotlivou funkci volající fixture 'temp_user', uživatel je na konci každého testu vymazán přímo v testu nebo pomocí fixture 'temp_user', tzn. životnost uživatele 'Temp_User' je pouze pro jeden test, email uživatele je dynamicky generován
3. **Session_User** – sdílený uživatel pro všechny testy volající fixture 'session_user', uživatel je po doběhnutí všech testů vymazán pomocí fixture 'session_user', tzn. životnost uživatele 'Session_User' je po dobu testování celé session, tento uživatel je vytvořen automaticky vždy hned na začátku spuštění testovací session nebo jakéhokoliv jednotlivého testu, i když daný test uživatele 'Session_User' nepoužívá, email uživatele je dynamicky generován

---

## Fixtures (conftest.py)

Soubor `tests/conftest.py` obsahuje klíčové fixtures:

| **FIXTURE**       | **SCOPE** | **AUTOMATICKÉ SPUŠTĚNÍ** | **VÝSLEDEK** |
|-------------------|-----------|--------------------------|--------------|
| `accept_gdpr`     | session   | Ano                      | přijetí GDPR |
| `browser_context` | session   | Ne                       | sdílený prohlížeč a kontext pro všechny testy |
| `page`            | function  | Ne                       | nová stránka s domovskou URL pro každý test |
| `temp_user`       | function  | Ne                       | uživatel **Temp_User** unikátní pro každý test, smazán na konci testu |
| `session_user`    | session   | Ano                      | uživatel **Session_User** pro celou session, smazán na konci všech testů |


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




