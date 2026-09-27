# Začátečník

Tato kapitola vás provede vytvořením první knihy od úplného začátku až po její vygenerování.

Nebudeme řešit nic, co není pro první knihu potřeba.

# 1. Vytvoření složky knihy

Nejdříve vytvořte novou složku.

Například:

    MojeKniha/

Tato složka bude obsahovat všechno, co ke knize patří.

# 2. Vytvoření základní struktury

Ve složce vytvořte soubor:

    Description.md

a dvě složky:

    Pages/
    Images/

Výsledná struktura bude:

    MojeKniha/
    ├── Description.md
    ├── Pages/
    └── Images/

# 3. Vytvoření Description.md

Soubor `Description.md` obsahuje základní informace o knize.

Otevřete jej v textovém editoru a zapište informace podle struktury, kterou Bindery používá.

Soubor musí mít přesný název:

    Description.md

Je důležité zachovat správný název souboru i jeho umístění v hlavní složce knihy.

# 4. Vytvoření první stránky

Otevřete složku `Pages`.

Do ní vytvořte první Markdown soubor.

Například:

    01.md

Do souboru napište:

    # Moje první kniha

    Toto je moje první kniha vytvořená pomocí Bindery.

    Toto je první odstavec knihy.

Soubor uložte.

# 5. Jak pojmenovávat soubory

Jednotlivé části knihy ukládejte do složky `Pages`.

Například:

    Pages/
    ├── 01.md
    ├── 02.md
    ├── 03.md
    └── 04.md

Číslování umožňuje určit pořadí jednotlivých částí.

Každý soubor obsahuje text jedné části knihy.

# 6. Jak psát text

Bindery používá Markdown.

Markdown umožňuje jednoduchým způsobem určit například nadpisy, tučné písmo, kurzívu nebo seznamy.

## Nadpis

Nadpis vytvoříte pomocí znaku `#`:

    # Hlavní nadpis

Menší nadpis může vypadat například takto:

    ## Podnadpis

## Tučné písmo

    **tučné písmo**

## Kurzíva

    *kurzíva*

## Seznam

    - první položka
    - druhá položka
    - třetí položka

## Odstavce

Jednotlivé odstavce oddělujte prázdným řádkem:

    Toto je první odstavec.

    Toto je druhý odstavec.

Takto lze napsat celý text knihy.

# 7. Přidání obrázků

Obrázky patří do složky:

    Images/

Například:

    Images/
    ├── cover.png
    ├── background.png
    └── obrazek.jpg

Obrázek s názvem `cover` slouží jako obálka knihy.

Obrázek s názvem `background` slouží jako pozadí.

Ostatní obrázky můžete pojmenovat podle jejich obsahu.

Například:

    fotografie.jpg
    obrazek_01.png
    diagram.png

# 8. Vložení obrázku do textu

Obrázek lze vložit přímo do Markdown souboru.

Například:

    ![Popis obrázku](../Images/obrazek.jpg)

Cesta musí odpovídat skutečnému umístění obrázku.

# 9. První kompletní kniha

Po dokončení bude například struktura vypadat takto:

    MojeKniha/
    ├── Description.md
    ├── Pages/
    │   ├── 01.md
    │   └── 02.md
    └── Images/
        ├── cover.png
        └── obrazek.jpg

Nyní máte připravené všechny základní části knihy.

# 10. Vygenerování knihy

Otevřete Bindery a vyberte složku s knihou.

Bindery načte její obsah a připraví knihu k vytvoření.

Spusťte generování.

Bindery zpracuje jednotlivé Markdown soubory, obrázky a informace o knize a vytvoří výslednou knihu.

# 11. Úprava knihy

Pokud chcete něco změnit, upravte příslušný soubor.

Text knihy:

    Pages/

Informace o knize:

    Description.md

Obrázky:

    Images/

Po provedení změn knihu znovu vygenerujte.

Tímto způsobem můžete knihu postupně vytvářet a upravovat, aniž byste museli celý projekt vytvářet znovu.