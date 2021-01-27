# AI pro hru Dicewars předmětu SUI

Cílem projektu bylo implementovat umělou inteligenci (dále AI) pro hru Dice Wars. Umělá inteligence by měla být schopna hrát tuto hru, založenou z velké části na náhodě. Její kvalita by
měla následně být hodnocena schopností porážet ostatní umělé inteligence, které již byly ke hře
vytvořeny. **AI neobsahuje žádný prvek strojového učení (z časových důvodů)**. I přes to je ale vysoce výkonná.

## Autoři
 - Jan Chaloupka (`xchalo16`)
 - Michal Krůl (`xkrulm00`)
 - Jan Láncoš (`xlanco00`)
## Vytvořená umělá inteligence
Hráč ovládaný naší AI pracuje na principu algoritmu expectiminimax, který je rozšířený pro hru více hráčů (také označován jako MaxN). Algoritmus je nastavený na prohledávání stavového prostoru do hloubky osmi vrstev. Při počtu čtyř hráčů tedy simuluje dva celé nadcházející tahy hry.

## Výkonnost
AI se umístilo v turnaji všech vytvořených AI (celkem 59 klientů) na 2. místě s úspěšností 41,4 %.

| Pozice | Název AI | Úspěšnost |
|:------:|----------|----------:|
|   1.   | xbartl06 |    45.7 % |
| **2.** |**xchalo16**|**41.1 %**|
|   3.   | xfrejl00 |    40.9 % |
|   4.   | xmrazi00 |    38.8 % |
|   5.   | xpomkl00 |    38.0 % |
|   6.   | xhrivn02 |    37.8 % |
|   7.   | xdacik00 |    37.5 % |
|   8.   | xsedla0v |    35.8 % |
|   9.   | xkotra02 |    35.7 % |
|   10.  | xhrusk25 |    33.5 % |
|        | ...      |           |
