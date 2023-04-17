# Implementační Dokumentace k 2. úloze do IPP 2022/2023
## Interpret
### Jméno a přijmení: Petr Kolouch
#### Login: xkolou05

# Implementace
## Návrh
### Prvotní návrh
Implementace a samotné rozdělení specifických částí do funkčních celků nebylo snadnou úlohou. Jeden z prvních návrhů implementace byla abstraktní třída *Instructions*, který by definovala abstraktní instrukce pro kontrolu parametrů a spuštění dané instrukce. Tento návrh jsem ovšem vyřadil, protože se mi nelíbilo množství tříd a samotný workflow i v případě statických tříd.
### Finální návrh
Finální návrh rozděluje jednotlivé části do logicky oddělených funkčních celků.
#### Instrukce
Veškerá implementace instrukcí se nachází ve třídě *Instructions*. Každá instrukce je zde představena stejně pojmenovanou funkcí, která danou instrukci vykonává.
#### Program
Jádro celého programu a abstrakce implentace se odehrává ve třídě *Program* Tato třída obsahuje programový čítač, který uchovává pozici programu a jednotlivé rámce nebo zásobník s rámci. Dále jsou zde uloženy návěští, zásobník volání a datový zásobník pro zásobníkové instrukce.

#### Rámce
Rámce jsou implementovány ve třídě *Frame*. V podstatě se jedná o seznam s proměnnými a metodami přistupující a modifikující proměnné právě v tomto seznamu

#### Zásobník
Dále bylo třeba implementovat datovou strukturu typy zásobník, který slouží pro uchovávání jednotlivých lokálních rámců, dále se zásobník užívá pro ukládání hodnot zásobníkových instrukcí. Zásobník je implementován v souboru *stack*

#### Regulární výrazy
Pro kontrolu správnosti specifických hodnot byly použity regulární výrazy. Pro znovupoužitelnost a abstrakci byla vytvořena třída *Regex* se statickými metodami.

#### Zpracování XML
Pro zpracování samotného vstupního XML souboru s kódem byla vytvořena třída *XMLParser*, stará se jak o zpracování kódu který bude využit pro interpret, tak pro kontrolu správnosti vstupního souboru.

#### Interpret
Samotný interpret je definován v souboru *interpret*. Jedná se pouze o *main* funkci, která zpracovává argumenty a volá specifické funkce pro interpretaci kódu.

![UML class diagram](https://github.com/KolouchPetr/IPP_IMG/blob/master/IMG/classes_interpret.png?raw=true)
Obrázek 1: Třídní diagram implementace Interpretu

![Packages](https://github.com/KolouchPetr/IPP_IMG/blob/master/IMG/packages_interpret.png?raw=true)
Obrázek 2: Diagram částí a jejich vzájemné návaznosti
## Co by šlo zlepšit
Některé datové jednotky jsou "Natvrdo" vytvořeny přímo ve funkcích při zpracování xml. Bylo by možné rozdělit a definovat přesný způsob uložení těchto dat ve specifických třídách. Způsob implementace ovšem nebrání možnostím dalšího rozšíření

## Možnost rozšíření
Jelikož bych osobně řekl, že kód je poměrně úspěšně logicky rozdělen na jednotlivé částí, přidání dalších rozšíření nebo třeba instrukcí by nemělo být obtížné. Instrukce mají přes get/set metody přístup k informacím, které potřebují pro fungování a jejich specifické chování stačí doimplementovat do jejich vlastní metody.



