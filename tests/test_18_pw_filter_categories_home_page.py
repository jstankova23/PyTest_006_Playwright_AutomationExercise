# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 18_TEST CASE: View Category Products
# TEST FILTRACE PRODUKTŮ Z HOME PAGE DLE KATEGORIE
def test_filter_categories_home_page(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url

    
    # 3. Verify that categories are visible on left side bar
    #### Levý svislý postranní panel slouží k filtraci produktů
    categories_heading = page.get_by_role("heading", name="Category") # vyhledání nadpisu 'CATEGORIES' na domovské stránce
    expect(categories_heading).to_be_visible()

    # 4. Click on 'Women' category
    #### Kliknutím kdekoliv na řádek s nadpisem WOMEN se rozbalí roletové menu
    women_rolet_menu = page.get_by_role("link", name=" Women")       # vyhledání nadpisu 'WOMEN' v sekci 'CATEGORIES'
    women_rolet_menu.click()                                    


    # 5. Click on Dress category link under 'Women' category
    #### výběr z podnabídky produktů, výběr z roletového menu pro kategorii Women / Ženy
    women_dress_link = page.get_by_role("link", name="Dress") # vyhledání nadpisu / linku 'Dress' v podsekci 'WOMEN' v hl. sekci 'CATEGORIES'
    women_dress_link.click()                                  # kliknutí na link


    # 6. Verify that category page is displayed and confirm text 'WOMEN - DRESS PRODUCTS'
    women_dress_products_heading = page.get_by_role("heading", name="Women - Dress Products")
    expect(women_dress_products_heading).to_be_visible(timeout=1000) 


    # 7. On left side bar, click on any sub-category link of 'Men' category
    #### Kliknutím kdekoliv na řádek s nadpisem MEN se rozbalí roletové menu
    men_rolet_menu = page.get_by_role("link", name=" Men")        # vyhledání nadpisu 'MEN' v sekci 'CATEGORIES'
    men_rolet_menu.click()                                    

    #### Kliknutí na Jeans kategorii v roletovém menu MEN
    men_jeans_link = page.get_by_role("link", name="Jeans")
    men_jeans_link.click()


    # 8. Verify that user is navigated to that category page
    men_jeans_products_heading = page.get_by_role("heading", name="Men - Jeans Products")
    expect(men_jeans_products_heading).to_be_visible(timeout=1000) 
