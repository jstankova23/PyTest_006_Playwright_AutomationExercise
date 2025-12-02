# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 09_TEST CASE: Search Product
# OVĚŘENÍ PŘESMĚROVÁNÍ Z DOMOVSKÉ STRÁNKY 'https://automationexercise.com/' NA PODSTRÁNKY S PRODUKTY 'https://automationexercise.com/products'
# A VYHLEDÁNÍ / FILTROVÁNÍ PRODUKTŮ PODLE KLÍČOVÉHO SLOVA ZADANÉHO DO VYHLEDAVAČE
def test_product_search(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    
    # 4. Click on 'Products' button
    products_link = page.get_by_role("link", name=" Products")     # vyhledání linku pro 'Products' stránku
    products_link.click()                                           # kliknutí na link 'Products'
    
    # 5. Verify user is navigated to ALL PRODUCTS page successfully (new page)
    all_products_heading = page.get_by_role("heading", name="All Products")   # lokátor pro nadpis 'ALL PRODUCTS' na nové stránce
    expect(all_products_heading).to_be_visible(timeout=5000) # ověření přesměrování na stránku s daným nadpisem a delší zpomalení (problém s heavy load na stránce)

    # 6. Enter product name (TOP) in search input and click search button
    ### test vyhledání všech produktů s klíčovým slovem 'top' zadaným do vyhledavače
    search_field = page.get_by_role("textbox", name="Search Product")
    searched_value = "top"              # s proměnnou 'searched_value' se pracuje v kroku 8
    search_field.fill(searched_value)

    search_btn = page.get_by_role("button", name="")
    search_btn.click()

    # 7. Verify 'SEARCHED PRODUCTS' is visible
    ### ověření, že se zobrazí na stránce nadpis 'SEARCHED PRODUCTS'
    all_products_heading = page.get_by_role("heading", name="Searched Products")   # lokátor pro nadpis 'SEARCHED PRODUCTS' na nové stránce
    expect(all_products_heading).to_be_visible(timeout=1000)       # ověření přesměrování na stránku s daným nadpisem a zpomalení

    # 8. Verify all the products related to search are visible
    ### ověření, že se na stránce s nadpisem 'SEARCHED PRODUCTS' zobrazí všechny produkty obsahující klíčové slovo 'top' ve svém názvu
    product_names = page.locator("div.product-information h2") # obecný CSS lokátor pro názvy produktů na stránce SEARCHED PRODUCTS
    
    count = product_names.count()                              # získání počtu nalezených produktů, lokátor.count()
    for i in range(count):                                     # iterace, projít každý nalezený produkt (1. produkt i = 0)
        result_product_name = product_names.nth(i).text_content().strip().lower() # indexovaný lokátor vrátí každý název produktu samostatně; ořez mezer, převod na malá písmena

        # ověření, že vrácený název produktu obsahuje hledané slovo 'top' uložené v proměnné 'searched_value';
        # proměnná 'searched_value' byla definovaná v kroku 6 při zadávání kritéria pro vyhledávání
        assert searched_value in result_product_name, f"Produkt '{result_product_name}' neobsahuje hledané slovo '{searched_value}'." # ověření, že název obsahuje hledané slovo 'top'

"""
    ### ITERACE JEDNOTLIVÝCH PRVKŮ VE SKUPINĚ - OBECNÉ PRAVIDLO
    count = locator.count()            # počet elementů odpovídajících lokátoru, vrací integer
    for i in range(count):             # for-cyklus procházející všechny elementy podle indexu, generuje indexy od 0 (1. prvek: i = 0)
    result_item = locator.nth(i)       # výsledný element - lokátor na i-tý prvek (umožní pracovat s jedním konkrétním elementem)

"""























