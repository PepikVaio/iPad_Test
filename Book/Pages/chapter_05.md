# Expert

Expertní část je určena uživatelům, kteří chtějí pochopit, jak Bindery pracuje uvnitř, a případně upravit samotný proces generování knihy.

## Struktura generování

Bindery pracuje s jednotlivými zdrojovými soubory a postupně je zpracovává.

Základní princip je:

    zdrojové soubory
            ↓
       načtení knihy
            ↓
       zpracování Markdown
            ↓
          HTML
            ↓
      použití stylů
            ↓
      vytvoření výstupu

Výsledný dokument je vytvořen ze zdrojů uložených v projektu.

## Formát stránky

Velikost stránky je možné určit pomocí nastavení knihy.

Bindery podporuje předdefinované formáty, například:

    A4
    A5
    A6
    B5

Je možné použít také vlastní rozměr.

Například zařízení s rozlišením:

    1404x1872px

může mít nastaven vlastní rozměr odpovídající tomuto formátu.

Velikost obálky sama o sobě neurčuje velikost stránky knihy.

## CSS a @page

Velikost stránky výsledného dokumentu může být dále určena pomocí CSS.

Například:

    @page {
        size: 148mm 210mm;
    }

Rozměry jsou zadány jako šířka a výška.

Mezi hodnotami je mezera.

## Templates

Templates určují strukturu výsledného dokumentu.

Pomocí šablon lze ovlivnit například způsob, jakým Bindery skládá jednotlivé části knihy.

Šablony jsou určeny především pro uživatele, kteří chtějí měnit výchozí způsob generování.

## TEMP

Bindery při generování používá pracovní prostor TEMP.

TEMP slouží jako pracovní oblast pro soubory, které vznikají během generování.

Není potřeba do něj běžně zasahovat.

Při řešení problémů nebo při vývoji Bindery však může být obsah TEMP užitečný pro kontrolu toho, co Bindery během generování vytvořil.

## Výstupní formáty

Bindery může zpracovávat knihu pro různé typy výstupu.

Proces může zahrnovat například vytvoření HTML, PDF nebo EPUB.

Každý formát má vlastní požadavky na:

- rozložení stránky,
- písma,
- obrázky,
- CSS,
- strukturu výsledného souboru.

Proto se může stejná kniha v různých výstupních formátech zobrazovat mírně odlišně.

## Úprava celé knihy

Expertní uživatel může upravovat jednotlivé části procesu.

Může například měnit:

- strukturu HTML,
- CSS,
- šablony,
- práci s fonty,
- způsob zpracování obrázků,
- velikost a rozložení stránky,
- způsob vytváření PDF,
- způsob vytváření EPUB.

Tím lze Bindery přizpůsobit konkrétnímu typu knihy.

## Úprava samotného Bindery

Bindery není pouze sada souborů knihy.

Samotný program lze dále upravovat.

Uživatel, který rozumí Pythonu a struktuře projektu, může změnit způsob, jakým Bindery:

- načítá knihu,
- zpracovává Markdown,
- vytváří HTML,
- pracuje s obrázky,
- načítá fonty,
- vytváří PDF,
- vytváří EPUB,
- pracuje s dočasnými soubory,
- vytváří výsledný dokument.

Tím se z Bindery může stát nejen nástroj pro vytváření knih, ale také základ pro vlastní publikační systém.

## Úplná kontrola

Na expertní úrovni už uživatel pouze nevytváří knihu pomocí Bindery.

Může upravovat samotný způsob, kterým Bindery knihu vytváří.

Díky tomu je možné přizpůsobit celý proces od zdrojových Markdown souborů až po výsledný dokument.