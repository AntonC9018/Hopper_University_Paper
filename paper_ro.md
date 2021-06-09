
# Abstract

Cu colegul meu am creat jocul Roguelike, **Hopper**, băzată pe mecanici din *Crypt of the Necrodancer*. 
În prima secțiune eu explic de ce am inițiat acest proiect, prin ce cale de dezvoltare am trecut.
Următoarele secțiuni sunt mai tehnice. Acolo eu motivez și ilustrez prin exemple concrete design-ul meu al sistemei, explic cum jocul funcționează intern.
Eu prezint cum am evitat boilerplate-ul și duplicarea codului prin generarea codului cu *Roslyn* și *T4*.

# Introduction

Idea jocului este inspirată de jocul **Crypt of the Necrodancer** (mai departe voi referi la ea ca simplu *Necrodancer*), care este jocul meu preferat.

Jocul a fost planificat să fie open-source și băzat pe aceleași mecanici.

Niciodată nu am planificat și nu aștept acest joc să-mi aducă vreun profit material.
Ea este desemnată satisfacerii personale, și poate comunității online care sper că îl vor găsi și vor dori să-l dezvolte mai departe.

**Problemele lui Necrodancer** care m-au impus să fac un joc similar sunt următoarele:
1. Modarea este în esență imposibilă. Sunt acceptate numai modurile care schimb aspectul vizual al jocului. Adăugarea mecanicilor sau a tipurilor de inamici nu este posibilă.
2. Necrodancer nu este disponibil pe Android. Inițial, am dorit să pot să joc pe mobil.
3. Codul nu este public.

Deci, **scopurile mele pentru proiect** au devenit următoarele:
1. Să fac o joc cu mecanici asemănători cu cele din Necrodancer.
2. Să dezvolt un sistem informatic scalabil cu mai multe proprietăți și un API ușor de utilizat pentru a ușura dezvoltarea modurilor.
3. Să public codul pe github cu o licența permisivă și a invita dezvoltătorii de moduri când API devine destul de matur.
4. Să-l pot porni pe Android.

**În același timp**:
1. Să primesc experiență în dezvoltarea jocurilor.
2. Să primesc experiență în domeniul menținerii proiectelor complexe.
3. Să primesc experiență în colaborarea și comunicarea cu comunitatea, artiștii și alți dezvoltatori.
4. Să adaug mai un proiect în lista proiectelor personale.


### Partea mea în acest job

Eu sunt programator, nu sunt artist sau designer.

Îmi place a programa sisteme complexe și instrumente, însă eu nu am capacitatea de a proiectez jocurile singur, nici nu vreau să fac acest lucru.
Scopurile mele în acest proiect erau să construiez o bază, un *Core* (nucleul) al jocului, librăria sa de bază, bazându-se pe care alții ar putea adăuga mai multe idei.
Nu am ca scop să creez o joc *completă* cu acest proiect, nici să lucrez asupra graficii (desenarea sprite-urilor, crearea animațiilor, iluminației, interfeței de utilizator (UI), etc.).
Aș dori să accentuez faptul că partea mea în acest proiect este să construiez acea bază, acea interfață de interacțiune cu lumea logică și cu caracterele, instrumentele pentru crearea obiectelor și inamicilor noi etc.

Ca o demonstrare, totuți am creat o versiune minimală a jocului.


## Design-ul mecanicilor jocului

Jocul care am vizat să-l dezvolt împrumută mecanicile sale de bază de la **Crypt of the Necrodancer**.

Necrodancer este un *Dungeon Crawler*, *Roguelike*. 
Explorați un donjon generat aleatoriu, combatând inamicii și bosurile în proces.
Este un joc băzat pe rând (turn-based), adică dvs și inamicii dvs pot să facă o acțiune (mișcare, atacă, ??? (cast a magic spell), deschide un cufăr, etc.) doar o singură dată în fiecare rând.

Îmi place conceptul de Roguelike în general — faptul că deveniți mai puternici când progresați mai adânc în donjon. 
Îmi place și să joc jocuri de acest fel. Printre ele: **The Binding of Isaac**, **Into the Breach**, **The Darkest Dungeon**, **Slay the Spire** și **One Step From Eden** sunt cele care mi-au plăcut în special.

Faptul care îl distinge pe Necrodancer este ??? (clever twist on the mechanic), anume faptul că puteți face acțiuni doar după ritmul muzicii.
Datorită acestui fapt, jocul este clasificat ca un joc *Roguelike Rhythm*.

Faptul că aveți timp limitat excepțional distinge jocul de la celelalte.
Tehnic, jocul este bazăt pe rând, însă datorită acestei mecanici este și cu mersul repede.
Cu toate că aveți *ceva* timp să vă calculați acțiunea următoare, este imposibil să luați în considerare totul, cum ați putea face în șah.

Încă, este important să prevedeți consecințele acțiunilor dvs și să planificați aproximativ ce sa va întâmpla în următoarele rânduri, însă având în vedere faptul că timpul dintre bătăile ritmului pentru a se gândi este atât de limitat, reacția joacă un rol mare tot.
Acest joc învață să puteți opri la un anumit moment, și luați o acțiune vrednică care mai degrabă nu va fi cea optimă.
Această idee este într-un mod similară la ideea șahului cronomerat, unde timpul dvs este o resursă de utilizat competent, deocamdată ticăitul ceasului ar putea să vă agite.  
??? Distanța scurtă dintre bătăi uneori se simte, de asemenea, stresantă, dar se simte bine să te apuci uneori de momente atât de intense, în care poți îndepărta o hoardă de dușmani, de ex. cu o vrajă magică bine aruncată sau un leagăn de armă abil.
(The short spacing between beats likewise feels stressful at times, but it feels good to sometimes clutch out such intense moments, where you are able to ward off a horde of enemies e.g. with a well-casted magic spell or a deft weapon swing.) 


## Istoria scurtă a dezvoltării

Am început să lucrez asupra acestui proiect aprope 2 ani în urmă.
Pe parcursul acestor 2 ani, a fost aruncat și rescris, complet sau parțial, de aproape 5 ori.

Aș zice că este greu să știi ce să faci în așa proiect chiar de la început, chiar aș zice imposibil.
Cu sarcini complexe fără cerințe definite în întregime, rar faceți lucrurile bine prima dată.
Codul este rescris, ideile devin mai clare, ariile noi sunt explorate și abandonate.
Să scieți un joc, asemănător, nu este liniar.

Cu toate că am știut de la început conceptul general pe care am vrut să-l urmăresc, și mecanicii de bază deja clare, nu am știut cum să structurez jocul corect, în ceea ce privește codul și design-ul sistemei.
Deci, trebuiam să încerc mai multe chestii pentru a ajunge la acele momente mai insteresante pe care le am astăzi. 

### Încerări inițiale

Inițial, încercam să programez jocul în motorul de joc *Corona*, în limbajul de programare *Lua*.
Permite exportarea pe mobil și pe desktop. Vedeți repertoriul pe github [după acest link][1].

Însă, înțelegerea mea a structurii acestor jocuri, cum ele lucrează pe partea sistemei, era slabă atunci.

Design-ul și realizarea unui joc simplu este cu totul diferit de problema pe care am întâlnit-o eu.
Dacă proiectați un joc care poate să aibă mii de efecte diferite, de mecanici și entități, posibil expandată de către moduri, nu puteți ține cont pentru fiecare interacțiune cu niște if-uri, aveți nevoie de un sistem mai abstract și complex, care permite utilizarea unui oricare fel de polimorfizm.
Nu am realizat acest lucru înaite de acest proiect, însă l-am realizat după această primă încercare.
În secțiunile de mai târziu voi analiza aceasta mai detaliat.

Această încercare inițială la realizarea jocului mi-a adus înțelegerea faptului că jocurile video complexe nu sunt doar o mulțime de if-uri. 
Ele necesită creativitatea și competența.

Codul inițial a fost aruncat și rescris de la început în a doua versiune, încă pe Corona.


### Corona și Lua: etapa 2

Lua este un limbaj de programare foarte simplist: nu există tipurile, modulele sau clasurile.
Dynamic method dispatch, încă, poate fi simulat prin metatable-urile (moștenirea prototipică).
Încă, nu există tablouri: și tablouri și dicționari sunt reprezentate prin așa numite tabele (perechile cheiea-valoare).

Cea mai mare problemă cu Lua este lipsa tipurilor și, ca rezultat, lipsa analizei statice.
Combatați bug-urile proaste, ca o eroarea run-time din cauza unei greșeli în numele variabilei, în fiecare zi. 
Aceste bug-uri sunt dificil de observat.

Am ajuns destul de departe cu Lua, am dezvoltat destul de multe capacități.

În acel timp, am ajuns la idea de a utiliza **chain-urile** pentru implementarea event-urilor.
În scurt, chain-urile în interpretarea mea sunt *responsibility chain-uri* care face ceva cu `context`-ul transmis lor, ca stiva de funcții middleware pe backend care modific în secvența obiectele `request` și `response`.
La orice etapă, propagărea `context`-ului poate fi oprit de către una din funcții (handler), pentru a evita execuția handler-urilor ce urmează. 
În plus, fiecărui handler este asociată o prioritate, după care ele rămân sortate în structura subiacentă a datelor.
Chain-urile vor fi exemplificate mai bine în secțiunile ce urmează.

Această idee a devenit esențială pentru modul în care eu am reușit să administrez mișcarea, atacarea, primirea daunei, etc.

În acest timp, am relizat că, ca sistemul să fie destul de robust, am nevoie de component dinamice.
Mai mult despre ele în secțiunile ce urmează.

Această etapă a proiectului este documentată destul de bine, o valoare esențială, dacă chiar nu aveți tipuri în limbajul dvs.
Am scris niște articole în limba engleză ce descriu unele mecanici din sistem. Le puteți [găsi aici.][2]
Unele idei documentate aici s-au tradus aproape intact în versiunea nouă a codului.


### Rescrierea în C#

În fine, m-am săturat de faptul că Lua nu are tipuri.
Am decis să rescriu întregul proiect în C#.
De ce C#?
Nu-mi păsa ce motor de joc voi utiliza la final, deci m-am concentrat pe partea logică a proiectului, adică dezvoltarea sistemei.
Am știut că există *Unity* și *Godot* care suportă C# ca limbajul său de scripting.
Deci, idea era să scriu nucleul jocului independent de grafică.
Acest concept are numele *MVC (Model-View-Controller)* sau *MVVM (Model-View-ViewModel)*.
Cu așa sistem, ar fi posibil să creez "scripturi de vizualizare" în orice motor de joc ce suportă C#.

Această idee nu este nimic nou, și de fapt m-am gândit la ea de la început.
Însă, înainte de a începe a utiliza C#, idea referitor la modul în care comunicare dintre ele trebuia să fie organizată era vagă în mintea mea.
Înainte de tranziția această de la Lua, eu nici nu am încercat să creez un sistem destul de robust pentru a putea dirija acest proces.
Am programat doar un prototip simplu pentru testare și am lăsat așa.

Deci, versiunea jocului pe C# inițială era dezvoltată doar în consola.
Atunci nici nu am știut cum să scriu test automatizate, sau mai bine spus nu am 
