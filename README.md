# PyTest_006_Playwright_AutomationExercise
Automatizované UI testy pro demo e‑shop https://automationexercise.com/ pomocí **Playwright + Pytest** (Python)

> Projekt je aktuálně v aktivním vývoji (work in progress).

**Autor:**                      Jana Staňková  
**Verze projektu:**             0.4.3 
**Datum vytvoření:**            11. 11. 2025  
**Datum poslední aktualizace:** 27. 11. 2025 
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
│   └── test_files/
│       └── Sample.docx                      příloha pro test 'test_06_pw_contact_file_alert.py'
├── .gitignore
├── conftest.py                              fixtures
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

Architektura uživatelů je navržena tak, aby byla zajištěna **nezávislost jednotlivých testů**. Testy si vzájemně neovlivňují data a lze je spouštět opakovaně i paralelně.  
Projekt pracuje se třemi typy testovacích uživatelů:

### 1. **Test User**
- Uživatelský účet je vytvořen **přímo v testu** `test_registration_positive` (`test_01_pw_register_positive.py`)
- Email je **dynamicky generován**
- Uživatel je **na konci testu smazán v rámci testu**
- Nepoužívá žádnou fixture
- Slouží výhradně pro **Test Case 1**

### 2. **Temp User**
- Uživatel je vytvořen pomocí fixture **`temp_user`**
- Email je **dynamicky generován**
- Uživatel je **na konci každého testu smazán pomocí stejné fixture**
- Životnost uživatele = **jeden konkrétní test**
- Používán pro testy vyžadující izolovaného uživatele

### 3. **Session User**
- Uživatel je vytvořen pomocí fixture **`session_user`**
- Email je **dynamicky generován**
- Uživatel je **sdílen napříč celou testovací session**
- Smazání probíhá **až po dokončení všech testů**
- Používán pro testy, které vyžadují sdílené přihlášení

---

### Přehledná tabulka uživatelů

| Typ uživatele  | Email        | Vytváří                | Maže                   | Použití     |
|----------------|--------------|------------------------|------------------------|-------------|
| **Test User**   | dynamický   | samotný test           | samotný test           | jen TC01    |
| **Temp User**   | dynamický   | fixture `temp_user`    | fixture `temp_user`    | per-test    |
| **Session User**| dynamický   | fixture `session_user` | fixture `session_user` | celý běh    |

---

### Ošetření selhání registrace uživatele

U všech tří typů uživatelů je používán **dynamicky generovaný email**, což minimalizuje riziko kolizí s cizími testovacími daty na veřejném demo e-shopu.

Přesto jsou:
- všechny **fixtures a test pro Test Case 1 ošetřeny chybovou hláškou** pro případ, že by se i přesto pokusily o registraci s již existujícím emailem,
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




