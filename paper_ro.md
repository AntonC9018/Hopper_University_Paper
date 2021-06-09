
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