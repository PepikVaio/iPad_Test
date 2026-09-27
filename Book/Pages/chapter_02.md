# Začínáme

Bindery lze používat několika způsoby:

- jako aplikaci pro Windows,
- jako aplikaci pro macOS,
- prostřednictvím webové verze.

Princip práce s knihou je stejný. Kniha je uložena ve vlastní složce a Bindery z této složky načítá její obsah.

# První spuštění

Po spuštění Bindery je potřeba vybrat nebo vytvořit složku, ve které bude kniha uložena.

Tato složka bude představovat celý projekt knihy.

Je vhodné vytvořit pro každou knihu vlastní složku.

Například:

    MojeKniha/

Do této složky budou postupně přidány jednotlivé soubory knihy.

# Základní princip

Práce s Bindery je jednoduchá:

1. vytvoříte složku knihy,
2. vytvoříte informace o knize,
3. vytvoříte text knihy,
4. přidáte obrázky,
5. spustíte generování,
6. Bindery vytvoří výslednou knihu.

Jednotlivé části knihy jsou uloženy jako běžné soubory. Díky tomu je možné knihu upravovat i bez Bindery například pomocí běžného textového editoru.

# Co je potřeba pro první knihu

Pro první jednoduchou knihu stačí tři základní části:

    MojeKniha/
    ├── Description.md
    ├── Pages/
    └── Images/

`Description.md` obsahuje informace o knize.

`Pages` obsahuje text knihy.

`Images` obsahuje obrázky používané v knize.

Další možnosti Bindery lze přidávat postupně podle toho, co od výsledné knihy potřebujete.