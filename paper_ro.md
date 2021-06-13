
# Abstract

Cu colegul meu am creat jocul Roguelike, **Hopper**, băzată pe mecanici din *Crypt of the Necrodancer*. 
În prima secțiune eu explic de ce am inițiat acest proiect, prin ce cale de dezvoltare am trecut.
Următoarele secțiuni sunt mai tehnice. Acolo eu motivez și ilustrez prin exemple concrete design-ul meu al sistemei, explic cum jocul funcționează intern.
Eu prezint cum am evitat boilerplate-ul și duplicarea codului prin generarea codului cu *Roslyn* și *T4*.

# Introduction

Ideea jocului este inspirată de jocul **Crypt of the Necrodancer** (mai departe voi referi la ea ca simplu *Necrodancer*), care este jocul meu preferat.

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

În acel timp, am ajuns la ideea de a utiliza **chain-urile** pentru implementarea event-urilor.
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
Deci, ideea era să scriu nucleul jocului independent de grafică.
Acest concept are numele *MVC (Model-View-Controller)* sau *MVVM (Model-View-ViewModel)*.
Cu așa sistem, ar fi posibil să creez "scripturi de vizualizare" în orice motor de joc ce suportă C#.

Această idee nu este nimic nou, și de fapt m-am gândit la ea de la început.
Însă, înainte de a începe a utiliza C#, ideea referitor la modul în care comunicare dintre ele trebuia să fie organizată era vagă în mintea mea.
Înainte de tranziția această de la Lua, eu nici nu am încercat să creez un sistem destul de robust pentru a putea dirija acest proces.
Am programat doar un prototip simplu pentru testare și am lăsat așa.

Deci, versiunea jocului pe C# inițială era dezvoltată doar în consola.
Atunci nici nu am știut cum să scriu test automatizate, sau mai bine spus nu m-am apucat de aceasta atunci.
Testele erau manuale, băzate pe inspecție.
Am avut un script care afișa o mulțime de informație referitor la cum obiectele au interacționat în joc, pe când eu aș citi aceste loguri pentru a mă asigura dacă elementul nou a funcționat corect.

În această versiune inițială în C#, eu de fapt am tradus codul din Lua în C# și am îmbunătățit unele idei.
Codul a devenit mai robust, dar nu destul de robust.

Am avut o mulțime de probleme de întreținere care au încetinit programarea și au făcut-o enervantă.
Pe scurt, am folosit fabrici pentru a construi tipurile mele de entități, precum și builder-uri pentru chain-urile lor inițiale.
Problema este că, dacă creați și utilizați fabricile manual, aveți acest cuplaj strâns dintre fabrica și tipul de entititate pe care îl produce.
Deci, când schimbam entitatea, trebuia să mă întorc și să schimb și fabrica.
Când schimba modul în care funcționează chain-urile, trebuia să mă întorc și să văd dacă builder-ul funcționează corect. 

Am avut conceptele de *tinker* și *retoucher* (ambele termeni sunt inventate) care ambele au existat numai pentru a ușura procesul de adăugarea și scoaterea handler-urilor la sau de la chain-urile.
Unica diferența dintre ele era că retoucher-urile se utilizau pentru *tipuri* de entități (pe factori), iar tinker-urile pe *instanțe* de entități.
Au făcut același lucru, fiind diferoți doar în ce container au vizat.
Faptul că ele au făcut același lucru a implicat duplicarea codului și unele probleme de întreținere.
Însă, nu primim nimic dacă le diferențiem, deoarece ele deja fac același lucru.

Într-un fel, am realizat aceasta, însă nu am știut cum să rezolv această problemă.

O altă problemă de întreținere era cod *boilerplate*.

De fapt nicidecum nu puteți evita această problemă în întregime în C# curat.
Știu că există reflexia, însă ea este nesigură și predispusă le erori, în plus foarte lentă.
Am utilizat reflexia pentru a evita boilerplate-ul în unele locuri, de exemplu adăugarea obiectelor de statuturi, care sunt în esența niște structuri cu inturi.

Un alt instrument pe care am încercat să-l utilizez erau interfețe generice.
Acestea lucrez într-o măsură, însă prea mult complic codul.

Pe toate aceste probleme le-am rezolvat în mare parte doar recent, utilizând generarea codului.


### Unity și Godot

Peste niște luni după rescierea proiectului în C#, baza de cod a devenit destul de matură pentru a încerca să fac un *view* pe Unity au Godot.

Inițial, am făcut un demo mic pe [Unity][4].
Demo-ul a prezentat un view care a lucrat cu interfețe și care pe urmă a fost reutilizat pentru același [demo în Godot][5] (nu este veriunea curentă).
Această oară am proiectat un prototip mai robust pentru view, însă oricum unele proprietăți lipseau și nu era plăcut să lucrez cu el.
Deficiențiele lui au fost adresate în versiunea nouă, în mare parte dezvolatată de colegul meu, care o descrie mai detaliat în [lucrarea sa][6].

Mediul concret al motorului video, cum am menționat anterior, nu-mi afectează procesul de lucru într-un mod semnificativ.
Din această cauză voi omite descrierea motoarelor acestea.
Însă colegul meu a lucrat mai apropiat cu motorul de joc, deci vă încurajez să vedeți [lucrarea lui][6] pentru mai multe detalii referitor la motoare de joc.
Partea mea în dezvoltarea a jocului era să derivez API-ul esențial, ce am făcut independent de oarecare motor de joc.
Pentru mine, motorul de joc numai mi-a oferit o modalitate de a vizualiza ce face codul meu.
Acest mod de a vizualiza ce face program uneori poate ajuta în identificarea și înțelegerea unor bug-uri.
Chestia este că oameni înțeleg input-ul vizual mai intuitiv decât log-urile în consola sau stiva de apeluri; uneori problema este mai aparentă dacă o observați în acțiune.


### Generarea codului

Începând cu luna aprilie, am lucrat asupra generării codului pentru a elimina boilerplate-ul și pentru a face procesul de dezvoltare mai puțin strângenitor.

#### Motive pentru generarea codului

Generarea codului este esențială, deoarece ea induce experimentarea.
Când eu văd un pattern care nu poate fi ușor exploatat ușor fără generarea codului, au pot să fac rapid un modul prototip pentru generator de cod care ar exploata ideea.
Dacă văd că este util, îl utilizez în continuare.
Dacă nu, anularea lui poate fi atinsă pur și simplu prin omiterea unui pas în generator de cod.
Eu nu am avea nevoie să frunzăresc zeci de fișieri sau să retrag un git commit.

Generarea codului previne repetarea codului boilerplate în zeci de fișiere, în același timp furnizând orice cod viitor cu unele capacități implicite ??? (out-of-the-box).
Este mai ușor de administrat, deoarece singurul lucru catre trebuie să schimbe pentru a afecta zeci de clase care au utilizat o capacitate particulară a generatorului de cod este doar regulile după care acel cod este construit.
Este mai ușor de adăugat capacitățile noi, din aceeași cauză.
Dă documentarea automată. Imaginați-vă păstrarea documentării la zi în toate acele fișiere.

#### Instumente în scurt

Utilizez `T4`, scurt pentru `Text Template Transformation Toolkit`, pentru a crea template-uri pentru a genera fișiere sursă adăugătoare.
Utilizez `Roslyn`, pentru analiza codului sursă.
Aș marca clasele mele în codului sursă cu atributuri specifice pentru a permite generarea anumitului cod când generatorul este pornit.

Abordarea mea la analiza codului este una simplistă.
Eu nu monitorizez codul live, printr-o conexiune la language server.
Când generatorul de cod este pornit, el șterge toate fișierile generate anterior și analizează întregul proiect din nou, generând toate fișierile din nou.
Da, această abordare este foarte lentă dar este cu mult mai ușoară de implementat.
Cea mai lentă parte a procesului este citirea și analiza fișierilor sursă, deci precis ar putea fi optimizată cu un language server.

#### Fluxul meu de lucru

Procesul meu de tranformare a docului repetativ în codul generat este aproximativ următorul:
1. Când scriu cod observ un pattern care poate fi exploatat de către generatorul de cod.
2. Dacă pattern-ul nu este destul de clar, aștept până când un pattern asemănător apare într-o altă bucată de cod, până când problema devine destul de clară pentru a propune o soluție generală.
3. Încerc să rezolv problema fără a genera codul, cât mai simplu, printr-o abstracție.
4. Dacă nu pot rezolva astfel, pornesc generarea codului pentru ideea dată.


# Prezentarea generală a sistemei

## Prezentarea generală a mecanicilor jocului

Cum am menționat anterior, mecanicile jocului sunt băzate pe cele din Necrodancer.

Jocul are loc într-o grilă 2d a lumii, și este băzată pe rânduri.
Controlați un caracter poziționat pe o celulă în grilă.
Fiecare rând, puteți face o acțiune, de exemplu, să vă mișcați într-o direcție ortogonală la o celulă adiacentă, să atacați un inamic pe o celulă adiacentă, să săpați un obstacol sau să faceți o acțiune specială, de exemplu ??? (cast a spell).
Încă, este posibil să săriți peste o tură, fără a face nimic.

După ce v-ați luat acțiunea, toți inamicii primesc posibilitatea de a face o acțiune, unu câte unu.
Ce acțiune va fi selectată depinde de IA a lor (algoritm pentru selectarea următoarei acțiuni) și de fapt orice acțiune poate fi selectată, de la ataca sau mișcare simplă până la ??? (casting a spell).

Mai sunt lucruri care au loc după aceasta, însă le vom discuta mai târziu.


### Tipurile de acțiuni

Un concept important care trebuie să-l adresez este faptul că jucătorul poate selecta dintre următoarele două tipuri de acțiuni:
1. *Acțiuni-vector* (`directed actions`), governate de către input-uri direcționale (săgețile). Acestea includ atacarea, mișcarea și săparea într-o direcție specificată.
2. *Acțiuni speciale* (în mare parte `undirected actions`), ca ??? (casting a spell) sau activarea unui item.
Aceste acțiuni sunt executate prin apasarea unei cheie desemnate, fără a necesita un input direcțional simultan (săgeata).
Acele acțiuni speciale care totuși necesită o direcție pentru a lucra corect, ca, de exemplu, aruncarea unei sfere de foc într-o direcție specifică, pot utiliza orientarea curentă a caracterului, sau pot obține direcția într-un alt mod.

Lucrul cel mai important de înțeles este faptul că jucătorul nu poate controla ce acțiune exact va fi executată după furnizarea unui input vectorial.
Mai precis, toate acțiunile posibile vor fi încercate în ordinea și prima acțiune care a reușit să se execute termină procesul de execuție.

De exemplu, dacă jucătorul dă input-ul `sus`, la început caracterul va încerca să atace în direcția sus, pe urmă, dacă atacul nu întâlnește nici un inamic, caracterul va încerca să sape obstacol din sus, pe urmă, dacă nu întâlnește nici un obstacol, caracterul ar mișca sus.

Acest lucru este opus acțiunilor speciale care sunt de obicei mapate direct la un anumit efect sau un anumit item.
De exemlu, zicem, jucătorul furnizează inputul `S` care este mapat la ridicarea scutului.
Deci, apăsarea lui `S` mereu ar executa această acțiune concretă (în general, dar sunt unele excepții).

Ca rezultat acestul model, jucătorul poate executa orice valabilă la moment acțiune în orice moment al timpului prin apăsarea cel mult unei cheie.

### Scopul

Jucătorul se confruntă cu problema de a completa un nivel generat aleator.
Nivelurile consistă dintr-un set de cameri conectate, fiecare cameră conținând inamici.
Există o cameră finală cu o ușă (sau o trapă, sau o scară) la următorul nivel.
Când jucătorul învinge un număr de așa niveluri, el confruntă un bos.
Învingerea bosului ori permite jucătorul să se procede la următorul nivel, sau rezultă într-o victorie generală.

Nivelurile devin progresiv mai complicate. În special, monștri au mai multe puncte de sănătate, apar noi și mai complexi tipuri de monștri, numărul de pericoli, ca ??? (spike) sau iazuri, crește, etc.
În același timp, jucătorul primește itemi când învinge etajul, care dă abilități noi pasive sau active, sporește statuturile.
Deci, jucătorul tot devine mai puternic, progresând.

### Itemii

Inventoriul jucătorului are niște sloturi de itemi, fiecare cu un rol asociat, de exemplu, arma, lopata, ??? (spell) sau o parte de armură, ca cizmele sau casca.
Acele sloturi care pot fi activate sunt mapate la un input, adică furnizând acel input ar activa itemul în slotul corespunzător. 

Jucătorul poate ridica itemi dacă pășește pe ele, astfel ele sunt plasate în slotul desemnat lor automat.
Dacă în acel slot deja este un item, acel item va fi schimbat la cel ridicat și plasat pe podea.

Unii itemi pot să nu aibă un slot asociat.
Așa itemi de obicei sporesc statuturile jucătorului, sau modifică subtil un comportament specific.
De exemplu, ar putea fi un itemm care daunează toți inamicii în jurul inamicului lovit.

Vom presupune, pentru simplitate, că nu pot exista două exact aceiași itemi ridicate de către jucător.

### Inamicii

Fiecare inamic are un comportament clar-definit.
Ei selectează acțiuni după o strategie ușor de înțeles pentru jucător.

De exemplu, un inamic simplu ar putea să aibă următoarea strategie: a sări peste o acțiune, după ce a ataca sau a se mișca în direcția jucătorului.

Acțiunile inamicilor trebuie să fie previzibile pentru jucător pentru a putea evalua repede o situație dată și a fi sigur în ce acțiune el va lua.
Ideal nimic aleator sau neprevizibil nu trebuie să întâmple.

Fiecare inamic încă trebuie să aibă o metodă de a-l învinge, un pattern simplu de mișcări care jucătorul poate să urmărească și să câștige mereu.
Bucuria jocului constă în studierea setului de mișcări al inamicului, ??? (coming up with) pattern-urile și strategiile de a-i învinge, și în evaluarea situației rapid, ??? (coming up with a good action on the fly), în cauza în care inamicii avansează în grupuri.


### Limita de timp

Cum am menționat anterior, cea mai intrigantă idee este faptul că există o limită de timp pentru fiecate acțiune.
Mai specific, acțiunile trebuie să fie selectate după ritmul muzicii (cu o anumită libertate ??? (with some leeway)). 

Această detalie este esențială pentru design-ul jocului.
Eu aș zice această mecanică este cea mai importantă mecanică din Necrodancer.
Însă, ea este relativ independentă de alte mecanici ale jocului, ca deplasarea jucătorui în grilă și sistemul de itemi, și ea nu va figura în această lucrare.
Acestă lucrare concentrează pe întrebările implementării altor părți ale jocului: sistemul de acțiuni, sistemul de grilă, etc. 


### Mai multe idei

Când motorul este completat, va fi ușor să explorăm mai multe idei.

Eu aș dori să încerc să transform jocul acesta într-o PVP arena, sau MOBA, lăsând mecanicii de bază și ideea să facem acțiuni după muzică neschimbate.
Nu știu cât viabil aceasta ar fi, dar ideea îmi pare destul de intrigantă.


## Prezentarea generală a design-ului sistemului.

Mă preocup în mare parte numai de motorul meu, adică cum logic ar funcționa, cum itemii, acțiunile, intelectul artificial al inamicilor vor fi implementate, cu instrumentele de exemplu pentru generarea codului.
Încă, sunt interesat să permit să extindem contentul existent prin moduri.

### Cum să NU scrieți cod

Unul din cele mai importante subiecte în dezvoltarea jocurilor video este cum să arătăm frumos ce se face în joc pe ecran, cu animații, particule și sprite-urile corect arătate utilizatorului.

O metodă de a face acest lucru este să ne referim la codul ce controlează *View*-ul, adică ce se vede pe ecran, direct în codul pentru logică (*Model*). De exemplu, cam așa (pseudocod pentru înțelegere, nu-i codul real din joc):

```C#
void Move(IntVector2 direction)
{
    if (!Grid.HasBlockAt(this.position + direction))
    {
        SetAnimation(Animation.Hopping);
        TranslateSprite(
            to: this.position + direction, 
            timeInMs: 500, 
            callback: () => SetAnimation(Animation.Idle));
        this.position += direction;
    }
}
```

Însă, așa cod are niște defecte asociate cu el:
1. Logica jocului dvs este cuplată strâns cu view-ul. Mixați codul care ar putea fi separat, astfel complicând procesul de a-l citi, înțelege și menține.
2. Codul este foarte instabil.
Imaginați-vă penru un moment că jucătorul după ce s-a mișcat la o poziție nouă, a declanșat o capcană care l-a ucis. Aceasta ar trebuie să decalșe animația de moarte, însă animația inactivității (idle) setată în callback-ul se joacă ??? (is playing). Evident, acest exemplu este prea simplificat, însă deja puteți vedea că setarea callback-urilor în așa mod este ceva inadmisibil. Aveți nevoie de un sistem mai complex pentru a administra aceasta.
3. Ce dacă jucătorul alunecă în loc de a sări? Atunci, o animație diferită trebuie să fie setată, nu `Animation.Hopping`, ci `Animation.Sliding`. Ați adăuga o verificare în funcția `Move()`? Dar ce dacă alunecarea vine dintr-un mod? Atunci, sistemul dvs nu ar fi putut să aibă cunoștințe despre aceasta. Este clar, că așa strategie simplă nu va lucra aici. 

Deci, defectele identificate sunt:
1. Cuplarea strânsă.
2. Probleme de întreținere.
3. Inflexibilitatea.


### Separarea și event-urile este ideea cheie

Voi ilustra cum separarea componentelor și event-urile pot rezolva toate problemele constatate mai sus.

Deci, în primul rând vom adresa problema cuplării strânse. Imaginați-vă două funcții, una responsibilă pentru mișcare, alta pentru animații.

```C#
void Move(IntVector2 direction)
{
    if (!Grid.HasBlockAt(this.position + direction))
    {
       this.position += direction; 
    }
}

void AnimateMove(IntVector2 newPosition)
{
    SetAnimation(Animation.Hopping);
    TranslateSprite(
        to: newPosition, 
        timeInMs: 500, 
        callback: () => SetAnimation(Animation.Idle));
}
```

Codul nu este ideal, din punct de vedere a implementării (callback-urile, etc.), dar aici avem o problemă mai mare.
Curent, nu există o modalitate de a comunica pentru aceste funcții.
Apelarea lui `AnimateMove()` în `Move()` nu lucrează, deoarece aceasta ar însemna că doar am refactorizat codul legat de animație într-o funcție separată, însă ele au rămas cuplate strâns.
Scopul nostru era să separăm codul pentru logică de la codul pentru view. Cum să facem acest lucru?
Event-urile (semnale) la salvare!

Ideea este să definim o coadă de handleri, codul în care să fie executat după ce jucătorul se mișcă.
Această coadă poate fi statică, configurabilă pentru tipuri diferite de entități.
Încă în pseudocod:

```C#
static EventQueue<Handler> moveEvent;

void Move(IntVector2 direction)
{
    if (!Grid.HasBlockAt(this.position + direction))
    {
       moveEvent.Dispatch(this, this.position + direction);
       this.position += direction;
    }
}

void AnimateMove(IntVector2 newPosition)
{
    SetAnimation(Animation.Hopping);
    TranslateSprite(
        to: newPosition, 
        timeInMs: 500, 
        callback: () => SetAnimation(Animation.Idle));
}

void Setup()
{
    moveEvent.AddHandler(AnimateMove);
}
```

Acum, funcția `Move()` nu știe nimic despre view.
Ea doar expediază event-ul fiecare dată când jucătorul se mișcă.

Însă, aceasta nu rezolvă problema cu de exemplu alunecare.
Jucătorul nu alunecă implicit.
Alunecarea este un efect care poate fi aplicat at runtime.
Dacă am dori să animăm alunecarea corect, ar trebui să schimbăm această coadă at runtime.
Deci, vom crea o coadă de event-uri într-o proprietate a instanței jucătorului, nu doar a tipului jucătorului, ca să putem s-o modificăm at runtime.

Acum, după ce le-am separat, putem rezolva și problemele de întreținere.
Deoarece partea lui view va fi îmbunătățită și va devine un sistem complet și independent, această problemă tot poate fi rezolvată, cu ceva mai mult chibzuit.


### O direcție greșită?

Deci, ideea mea inițială era că modelul va fi separat de la view-ul, dar nu am știut cum să exact fac acest lucru.
Am știut despre event-uri și le-am utilizat, însă realizarea că ele pot fi utilizate pentru comunicarea dintre view-ul și model-ul atunci încă nu a venit la mine până recent.
Pur și simplu am gândit despre problema puțin diferit.
Am gândit că view-ul și modelul sunt aceste două sisteme complet independente, view-ul fiind conectat cu model-ul printr-un pod minuscul.
Aceasta poate lucra, însă nu este tare scalabil.
În loc de această abordare, view-ul trebuie să fie conectat cu modelul într-un set lat de puncte de contact, prin event-uri, unde modelul nu ar cunoaște nimic despre view-ul.

#### Ideea istoriei

Inițial, mi-am imaginat modelul și view-ul să fie conectate prin *istoria*.
Modelul ar împinge actualizările referitor la ce event-uri s-au întâmplat în lume prin această istorie.
De exemplu, când jucătorul ar fi atacat, actualizarea `fiind atacat` ar fi salvată pe istorie.
View-ul și-ar actualiza starea și ar decide ce animații să pornească dupa ce toate event-urile au avut loc.

Deci, mi-am imaginat această în așa mod: avem o mulțime de mașini de stări separate în view-ul jucătorului, toate responsabile pentru detectarea event-urilor diferite.
De exemplu, există o mașină de stări pentru fandare. "Fandare" înseamnă o atacă imediat urmărite de o mișcare.
Mai este o mașini de stări pentru mișcare care constă din doar actualizarea de mișcare.

Deci, după ce s-a procesat încă un tur în model și istoria s-a umplut, view-ul ar primi istoria și ar încerca să pornească toate mașinile de stări pe această istorie.
Deci, după ce jucătorul și a atacat, și a mișcat în același tur, view-ul ar primi istoria cu 2 actualizări: atacul și mișcarea.
Fiecare din aceste mașini de stări ar fi încercate.
Fandarea este atac și mișcare, deci această mașină de stări ar fi satisfăcută.
Mașina de stări care reprezintă mișcare tot ar reuși, deoarece actualizarea de mișcare este prezentă.
Din aceste două view-ul ar selecta pentru animare una mai complexă, adică, fondarea.

Chiar am avut un termen mai intuitiv pentru această: sitele.
Fiecare mașină de stări este o sită care devine blocată când încercați să ciuruiți istoria prin ea.
După ce am trecut istoria prin toate sitele, cea mai complexă blocată sită este selectată și animațiile pentru acea sită sunt ??? (played).


#### Care este problemă dar?

Problema vine când aveți nevoie să transmiteți datele împreună cu actualizările.

Ați putea transmite orice date cu ele, însă atunci nu avem o modalitate clară de a vedea ce event a avut loc fără de a face un cast al datelor într-un tip cunoscut.
Aceasta aduce la `if-else` urâte pentru a determina tipul corect.


```C#
foreach (object update in history)
{
   if (update is AttackingUpdate attackingUpdate)
   {
       // facem ceva cu datele din `attackingUpdate`
       // ...
   }
   else if (update is MovingEvent movingEvent)
   {
       // ați înțeles ideea
   }
}
```

Din cauza că gaură prin care încercați să împingeți aceste actualizări de la model la view-ul este atât de îngustă, aveți nevoie să convertați actualizările într-un tip analog lui `object`, astfel pierzând tipul concret al actualizării în proces.
Acest fenomen poartă numele "ștergerea tipului".

Stop, oare nu putem putem utiliza polimorfizmul în loc de `if-else` pentru a apela funcșiile concrete care trebuie să procesează datele?

Având în vedere faptul că modelul nu știe nimic despre logica view-ului dvs asociată cu actualizaările, însă știe ce datele vor fi în update-urile, nu, aceasta nu este posibil.
Nu puteți da modelului un tip cu acele date pe care el l-ar instanția (ca obiectul să conțină funcțiile pozimorfice dvs).
Adică, *ați putea*, însă nu este tare convenabil si sunt modalități mai simple de a atinge același rezultat.

Ați putea menține un dicționar tipurile actualizărilor mapate la handler-urile, ca mai jos.
Însă acest cod este rău și nu este plăcut să mențineți așa cod.

```C#
void HandleAttack(object update)
{
    // În primul rând, castăm în tipul dorit
    var attackingUpdate = (AttackingUpdate) update;
    // Facem ceva cu datele ...
}

void HandleMove(object update)
{
    // În primul rând, castăm în tipul dorit
    var movingUpdate = (MovingUpdate) update;
    // Facem ceva cu datele ...
}

// Type este type info unei clase date.
// Action<T> este void function care ia T ca argument.
Dictionary<Type, Action<object>> typeErasedHandlers
{
    { typeof(AttackingUpdate), HandleAttack },
    { typeof(MovingUpdate),    HandleMove   }
};

void SieveThroughHistory(History history)
{
    foreach (object update in history)
    {
        typeErasedHandlers[typeof(update)](update);
    }
}
```


#### Soluția

Din fericire, există o modalitate mai bună de a ??? (deal with this).

Ideea este să permitem mai multe puncte de contact între modelul și view-ul.
Astfel, putem sări peste faza istoriei cu totul.
Modelul nu ar trebui să împingă nici o actualizare în istorie.
Al doar ar declanșa un event corespunzător cu toate datele cu care la moment lucrează, păstrate într-un context.
Ca un exemplu simplificat (codul nu este real):

```C#
class AttackingContext
{
    Player player;
    Enemy attackedEnemy;
    IntVector2 direction;
}

class Player
{
    // ...

    EventQueue<AttackingContext> attackEventQueue;

    void Attack(IntVector2 direction)
    {
        var enemy = Grid.GetEnemyAt(this.position + direction);
       
        if (enemy != null)
        {
            var context = new AttackingContext(
                player        : this,
                attackedEnemy : enemy,
                direction     : direction);
            
            attackEventQueue.Dispatch(context);

            enemy.TakeDamage(this.damage);
        }
    }
}

class PlayerView
{
    // ...

    void AttackHandler(AttackingContext context)
    {
        // Facem ceva cu:
        // context.player
        // context.attackedEnemy 
        // context.direction     
    } 

    void Setup(Player playerInstance)
    {
        playerInstance.attackEventQueue.AddHandler(AttackHandler);
    }
}

```

Această idee poate vă pare evidentă după ce am ilustrat-o, însă pentru mine ea nu era evidentă până recent.
Trebuia să sufăr prin toate probelemele istoriei explicate mai sus pentru a ajunge la această revelație.

Deci, am reușit șă separăm view-ul de la modelul, în același timp având posibilitate de a transmite datele de la model la view fără ștergerea tipurilor și chiar să evităm ca model să cunoască despre existența view-ului, datorită unui astfel de design.

#### Este oare totul?

Mai sunt niște probleme cu așa design.

Una din ele este legată de inconviența unelor lucruri care apar din cauza că design-ul este așa.
Le-am adresat prin generarea codului.

O altă problemă este legată de ordonarea handler-urilor.
Am rezolvat-o prin introducerea priorităților.

Vom discuta ambele pe urmă.


### ECS (Entitate-Component-Sistem)

S-au spus multe lucruri despre ECS-uri.
Însă, eu sunt convins că nu puteți să le înțelegeți integral dacă nu redescoperiți această idee singuri.
Când vedeți o problemă reală și încercați s-o soluționați prin diferite metode, incluzând ECS-ul, iată atunci apare înțelerea profundă.

#### Introducere 

ECS permite să privim spațiul programului printr-o perspectivă diferită.

ECS zice că există o lume și orice obiect în acea lume este o *entitate*.
Toate entitățile încep ca un obiect vid doar cu un identificator.
Ele sunt ca un schelet la care adăugăm componente pentru a le da un comportament sau o proprietate specifică.
Componentele de obicei doar conțin datele.

Toate mecanicile din joc sunt pur și simplu interacțiunile dintre diferite obiecte din lume.
Acestea sunt conceptualizate ca *sisteme*.
Ele operează pe componentente individuale ale entităților, astfel asigurându-le comportament specific.

Ideea după ECS-ul este "entitățile flexibile și dinamice".

#### De ce nu POO?

Dacă vreodată ați încercat să reprezentați tipurile diferite ale entităților într-un mediu dinamic, știți că aceasta nu va lucra.
1. Nu puteți utiliza conceptul de moștenire și ierarhiile cum-se-cade.
2. Tipurile statice sunt prea rigide.

Deci, imaginați-vă pentru un moment că aveți clasa `Player`.
Jucătorul poate face multe lucruri, prin care mișcarea, atacarea și săparea.

Acum, considrați o clasă diferită, `Enemy`.
Puteți observa că inamicul tot poate să se miște și să atace, dar are o schemă de control diferită: jucătorul este controlat de către input-ul utilizatorului, pe când inamicul de o inteligență artificială.

Deci, probabil veți fi tentați să refactorizați lucrurile comune, anume atacarea și mișcare, într-o clasă de bază.
Clasa `Player` atunci ar moșteni acea clasă de bază adăugând abilitatea de a săpa, pe lângă schemei proprii de input, iar clasa `Enemy` ar adăuga iteligența sa artificială.

Acum apare un tip nou de inamic: el poate să atace, să se miște și să sape, având un IA.
Unde să-l punem în ierarhia noastră? Ar trebuie el să moștenească `Enemy`?
Dar atunci ar trebui să adăugăm săparea, care este deja implementată în clasa `Player`.
Să scoatem săparea într-o clasă de bază `DiggingMovingAttackingBase`?
Nu, deoarece atunci nu putem moșteni IA din clasa `Enemy`.
Poate `Enemy` trebuie să moștenească `DiggingMovingAttackingBase`?
Din nou nu, deoarece el nu poate săpa după design.

Deci, chiar cu așa exemplu simplist, ideea tipică lui POO a moștenire nu merge.
Acum imaginați-vă același scenariu dar amplificat în sutele de ori: sunt sutele de proprietăți și comportamente pe care orice entitate poate să le posede.
Aceasta ar fi imposibil de modelat printr-o ierarhie.

Altă ideea este faptul că entitățile, dacă sunt modelate ca instanțe de tipuri statice, nu pot să-și schimbe comportamentul at runtime.
Într-un joc real, jucătorul poate să înceapă fără abilitatea de a săpa, însă, când primește târnăcopul, ar învăța această abilitate nouă.
Însă, nu puteți modifica clasa `Player` să poată sape.
S-o modificați de la început nu are sens, deoarece jucătorul a obținut abilitatea *eventual*.

Încă un exemplu: aveți un monstru de două faze, zicem, un fluture furioas care inițial începe ca o omidă inocentă, deci nici nu poate ataca, însă care poate să se transforme într-un fluture, obține abilitatea de a zbura și de a ataca jucătorul.

Cu POO există doar un mod de a modela această transformare.
Ați avea două clase, una pentru starea de omidă, alta pentru starea de fluture.
Ca să transformați omida în fluture trebuie să distrugeți instanța omidei si să creați un fluture nou.

Cu componentele dinamice aveți două posibilități.
Puteți ori să facem cum am descris mai sus, ori să transformați omida în fluture dându-i comportamentele de `Flying` și de `Attacking`.
În acest sens, a două abordare este mai flexibilă.


#### Compresie

O altă idee este să dați fiecării entități întreaga gama tuturor proprietăților și abilităților posibile însă să nu le dați voie să utilizeze majoritatea lor.
Astfel, ar fi ușor să aprindeți unele abilități mai târziu: puteți pur șă simplu să setați sau să curățați acel flag care indică dacă entitatea poate aplica acea abilitate.

Avem două probleme cu așa abordare:
1. Cât de multe componente și proprietăți aveți în joc, atât de umflate entitățile dvs devin, atât de mult spațiu ele ocupă.
Nu doar una din ele, ci toate. 
2. Așa sistem nu poate fi expandat de moduri, ceea ce-i inacceptabil în cazul meu. Unul din scopuri al proiectului meu este de a permite modarea.

Deci, păstrarea componentelor în constrast lumii unde toate entitățile au toate proprietăți posibile, natural aduce la entități *sparse*, în alte cuvinte, la ideea *compresiei*. 

#### ECS-ul meu

La moment, perspectiva mea la ECS este ceva specială.
- Noțiunea *sistemei* este destul de vagă în codul meu.
- Există distincția dintre *componente cu datele* (sau simplu *componente*) și *comportamente*.
- În codul meu, comportamentele sunt acele care definesc *event-urile* (utilizez *chain-urile*, mai mult ulterior).
Deci, comportamentele în codul meu este o fuziune dintre componente și sisteme.
Cum am descris anterior, event-urile sunt esențiale pentru a lega view-ul și model-ul.
- Există conceptul unui tip.
La moment, tipul este de fapt un template după care entitățile sunt construite la instanțiere.
Tipurile la moment sunt modelate printr-o entitate (un *subiect*) care este copiată la instanțiere pentru a crea o instanță nouă de acel tip.
Instanța atunci devine independentă de subiect și poate să se schimbe at runtime în orice mod, fără a-l afecta pe subiect.
Așadar, tipurile pot fi augmentate cu componente în timpul construcției, la fel ca entitățile at runtime.

Sunt nelniștit referitor la performanța ECS-ului meu.
Chestia este, ECS-ul meu este, cum se spune, "fake".
Un ECS optimizat de obicei focusează pe stocarea diferitelor componente într-un loc central în memorie pentru a putea itera pe ele în sisteme (iterarea secvențială este cu mult mai rapidă).
Administrarea memoriei manuală îmbunătățește performanța, salvând lucru pentru GC (colector de gunoi).

Eu face aceasta în modul "nu-mi pasă", adică, aloc toate componentele pe memorie dinamică cu operatorul `new`.
Aceasta este, de fapt, modul cel așteptat și cel ușor de a face acest lucru în C#, însă nu este performant deloc.

Să faceți un ECS într-un mod corect este o sarcină extrem de complicată pentru C#.
Structuri și tablouri de structuri este singurul mod în care datele pot fi păstrate direct în memorie dar nu împrăștiate undeva în memorie dinamică.
C# nu dispune de instrumentele necesare pentru a gestiona memoria manual, care există de exemplu în C#, deoarece nu se așteptă de la programator să facă așa ceva în C#.
Am considerat să migrez proiectul în C++, însă C++ tot are problemele sale, de exemplu că modding-ul ar fi mai complicat de implementat, că serializarea este proastă, deci am hotărât să progrezez cu ECS-ul "fake" al meu, în loc de aceasta.
În viitorul apropiat este posibil că voi migra proiectul pe D care este atrăgător pentru mine în special din cauza facilităților sale de metaprogramare.

# Subiectele tehnice

În această secțiune, prezint unele elemente din joc.
Mai specific, explic motivarea lor și cum le-am implementat, cu exemple concrete din codul sursă.

## Grila

Cum am stabilit anterior, lumea este reprezintată printr-o grilă de două dimensiuni cu entitățile.
Întrucât interogările de a afla dacă dacă o entitate se află într-o celulă specifică, dacă există un bloc pe o celulă specifică sunt atât de răspândite, am beneficia dacă am păstra entitățile (mai explicit, *transform-urile* lor) în coordonatele curente, într-un tablou de două dimensiuni.
Aceasta este de fapt cum am decis să modelez grila ([uitați-vă la costructor][7]).

### Celulile

Se presupune că fiecare celulă are mai multe nivele, unde entitățile de la diferite nivele au proprietăți ceva diferite.
De exemplu, în general, ??? (spiked trap) care dăunează jucătorul când acela o calcă, nu poate fi atacată de către jucători sau inamici, dar poate fi exploadată de către bombe.
Aceasta este deoarece nivelul în celulă unde se află capcana este locat pe nivelul `trap`, pe când jucătorul sau inamicii pot viza doar nivelul `real` prin atacii normali.
În orice caz, am modelat astfel ideea.

Înainte de refacere, am avut câte un slot pentru fiecare nivel al celulei, dar aceasta nu era bine, minimum deoarece majoritatea nivelurilor erau vide aproape mereu.
Vedeți, de exemplu, [clasa celulei din codul precedent, în lua][8].

Acest design a avut un minus: poate fi doar o entitate la fiecare nivel în fiecare moment al timpului.
Aceasta face unele lucruri, de exemplu entități care trec prin alți entități, dificil sau imposibil de implementat sau de considerat.

Am relizat că pot păstra entitățile într-o listă, și itera prin această listă, pentru a lua o entitate din nivelul care mă interesează.
Căutarea lineară ar fi de fapt acceptabilă în acel scenariu, deoarece celulele de obicei nu am mai mult decât 1-2 entități.
Cazurile unde ele conțină mai multe entități sunt rare și pot fi neglijate.

Încă un beneficiu de așa abordare este faptul că o entitate poate să-și schimbe nivelul în care ea se află at runtime, fără a actualiza unde ea este păstrată în celulă.

Implementarea curentă a celulii implică moștenirea de la `List<Transform>`.
[Vedeți implementarea curentă.][9]
Eu personal nu văd nimic rău în așa abordare, cu toate că [unii spun multe lucruri răi despre aceasta.][10]
Oamenii deseori ridic tema *compoziție peste moștenire*, cum compoziția este mai flexibilă, însă consider că aici un avem un caz de așa ceva.
Aici mai mult este vorba despre evitarea boilerplate-ului prin faptul că nu scrieți implementarea pentru interfața `IList<Transform>`, prin înaintarea tuturor metodelor la un membru privat de tip `List<Transform>`.
În același timp această abordare poate aduce la erori deoarece utilizatorului îi permitem mai multe lucruri de decât el trebuie să fie conștient. 
De exemplu, dacă castăm celulă în listă, ceea ce putem face în acest caz, putem folosi metoda `Add()` furnizată de către clasa listei, decât de clasa celulei, care mai conțină unele asserturi pentru debug.

Mie personal nu-mi pasă ce zic oameni la această temă.
Eu voi face ceea ce îmi pare admisibil mie.
Implementarea interfeței prin scrierea manuală a metodelor de înaintare la un list-membru nu mă face să mă simt bine.
În același timp, încă nu mi-am dezvoltat stilul meu propriu de programare în C#, și personal nu sunt de acord cu unele sfaturi ce oameni dau.
Poate când progresez profesional, voi înțelege mai bine.

Încă, un test rapid a indicat că dacă de fapt ne moștenim de la `List` codul merge cu aproape 1.5 ori mai rapid.

Să fie notat, țiglele statice nu sunt considerate ca entități și de aceea nu sunt păstrate în grilă.
Aceași se aplică la efectele de particule, care nu au influența asupra mecanicilor din joc.
Modelul este responsabil doar pentru chestiile care sunt legate de logica jocului. 


### Componentele responsabile pentru poziția și mișcare

Evident, abilitatea de a ocupa o poziție în lume și de a putea să-și schimbe poziția at runtime este esențială pentru joc.

Aceste abilități sunt modelate după următoarele componente specializate:
- `Transform`, dând o *poziție în lume*,
- `Displaceable`, dând abilitatea de *a-și schimba poziția în lume*,
- `Moving`, dând abilitatea de *a se mișca volunar*,
- `Pushable`, dând abilitatea de *a fi mișcat involuntar*.

### Transform

Entitățile care pot fi poziționate în lume trebuie să aibă componentul [`Transform`][11].
Conține informația despre poziția curentă în lume, orientarea curentă (în ce direcție se uită) și ce nivel entitatea ocupă.
Fiecare transform mai conține o referență la entitate, pentru a putea accesa entitatea când interogăm grila.

Curent, există conceptul de a fi `directat` care va fi examinată pe urmă.
Este modelată printr-un `tag` (un component fără date), însă recent am adăugat un flag în `Transform` pentru această.
Astfel am putea introduce mai multe flaguri.

`Transform` mai conține metode ajutătoare pentru interacțiunea cu grila.
Acest component este cuplat cu grila.
Aceste metode sunt definite ca metode instanțe pentru transform simplu pentru comoditate.
Ele ar putea fi definite ca metode de extindere, sau ca metode pe `Grid`, deoarece majoritatea lor are analoguri pe `Grid`.

`Transform` curent lucrează cu grila globală, adică, presupune că există *doar o lume în același timp*.
Aceasta am făcut în primul rând pentru comoditate, deoarece anterior toate transform-urile au avut o referință la lumea în care ele se află.
Însă, am schimbat acest lucru în mare parte deoarece aproape toate funcțiile într-un mod referă la grilă și mi-a fost anevoios să transmit manual această referință la toate funcțiile.

Când am adaug posibilitatea pentru mai multe lumi de a exista deodată, cumva voi schimba aceast lucru.
Însă, sper că patch-ul nu va fi unul dificil, având în vedere faptul că codul logicii este de un singur thread, ceea ce înseamnă că am putea să schimb lumea globală când se schimbă lumea curent procesată.

Dacă v-ați uita la cod mai aproape, ați putea să observați că unele câmputi sunt decorate cu atribute.
Această este legat cu generatorul de cod.
În scurt, atributul `Inject` este utilizat pentru a genera un constructor și un constructor de copiere pentru acest component, care ar solicita o valoare pentru acel câmp ca parametru.

Probabil ați observat și apelările la metodele `Grid.TriggerLeave()` și `Grid.TriggerEnter()`.
Cum acestea funcționează va fi explicat mai pe urmă.


#### Displaceable

Schimbarea poziției proprii într-o direcție dată, fie voluntar sau nevoluntar, este conceptualizat ca *deplasare*.
Teleportarea la o poziție nouă nu este considerată ca o deplasare.

Acest comportament permite deplasarea dacă celula unde entitatea se mișcă nu este blocată.
Informația ce nivel să fie considerat ca nivelul de blocare este stocat ca un câmp injectat în acest comportament deci poate fi schimbată at runtime pentru o entitate particulară, dacă necesită.

`Displaceable` este un *comportament* care poate fi adăugat la o entitate pentru a-i da posibilitate de a se deplasa. [Codul sursă][12].
În această clasă puteți vede aproximativ modul în care comportamentele sunt implementate.
[Aici][13] definim niște chain-uri (ca atare event-uri).
Generator de cod reacționează la ele, inițializându-le într-un constructor generat automat, și le copiază în constructorul de copiere generat automat.

Dacă codul extern dorește să adauge handler-uri la aceste chain-uri pe o instanță de entitate (sau pe un tip de entitate, deoarece fabricele sunt modelate print-o instanță de entitate-subiect), ar utiliza atributul `Export`.
Aplicând acest atribut ar autogenera codul pentru alocarea unui număr de prioritate unic pentru acel handler și, opțional, ar genera un învelitor care ar putea fi utilizat pentru a ușura procesul de obținere a chain-ului necesar de pe entitate și de conectare a acelui handler.

[Aici][14] avem un exemplu de așa atribute utilizate pentru a expune o funcție handler la generator de cod.

Diferența dintre chain-urile în comportamentul `Displaceable` este că ele sunt executate în momente diferite ale procesului de deplasare:
- `Check` se face înainte de deplasare, verificând dacă deplasarea trebuie să fie încercată cu totul.
Dacă am chain-ul de verificare până la capăt fără stopare, acțiunea de deplasare se consideră reuțită, cu toate că entitatea ar putea să nu se miște în proces. Acesta este by design.
- `BeforeRemove` reprezintă al doilea verificare pentru a verifica dacă deplasarea trebuie să fie aplicată.
  Diferența dintre aceste două chain-uri este că, dacă `BeforeRemove` ar eșua, adică, un handler ar opri propagarea contextului la restul handler-urilor, mișcarea s-ar fi considerată reușită, cu toate că nu ar fi executată în așa caz.
  Diferența există în mare parte pentru sistemul de acționare, explicată mai pe urmă.
  Însă ideea cheie este că chain-urile `Check` sunt utilizate pentru a verifica *dacă o acțiune trebuie să fie încercată*.
  Dacă deplasarea eșuează la `Check`, de exemplu *atacarea va fi încercată*, însă dacă eșuează mai pe urmă la `BeforeRemove`, acțiunea de mișcare va reuși și *nici o acțiune după mișcare nu ar fi încercată*.
- `BeforeReset` este traversată imediat după ce entitatea a fost eliminat din grilă, dar înainte de a fi *resetată* în grilă.
  Cum ați putea observa, este traversată direct, fără verificare propagării, deci toate handler-urile se execută garantat după ce `_BeforeResetChain.Pass(ctx);` este apelat.
- `After` este traversată după ce entitatea a fost resetată în grilă.

Atât de multe chain-uri sunt necesare pentru a putea să schimbe comportamentul de deplasare într-un mod foarte specific.
De exemplu, funcția particulară după [acest link][14] face așa că când entitatea se deplasează, orientarea lui ar fi schimbată în acea direcție.
Însă v-ați putea imagina ideile foarte complicate implementate datorită acestor chain-uri.
De exemplu, [*alunecarea* utilizează chain-ul `After`][15] pentru a opri alunecarea când entitatea se ciocnește cu peretele sau plece de pe o suprafață alunecoasă.

Eu numesc această idee de aplicarea unor detalii mici la algoritmul de deplasare, *retouching*, ca adăugarea unor detalii sau efecte în Photoshop.


#### Moving

`Moving` este comportamentul responsibil de deplasarea voluntară.

Comportamentul `Moving` este un *comportament direcționat activat*, ceea ce implică că el are o funcție `Activate()` care ia o direcție și returnează un boolean, indicând dacă activarea a reușit.
Așa comportamente pot fi activate de către *sistemul de acționare*.
`Moving` utilizează `Displaceable` pentru a executa deplasarea.

`Moving` este un exemplu de comportament care utilizează *autoactivarea*.
*Autoactivarea* este o modalitate oferită de către generatorul de cod care permite să generăm funcția `Activate()` și 2 chain-uri `Check` și `Do` automat.
Scopul lui `Check` ar fi să verificăm dacă trebuie să traversăm chain-ul `Do`.
Chain-ul `Do` ar conține handler-urile care fac ceea ce ține de mișcare în acest caz.
Aici încă vedem uzul funcției `DefaultPreset()` care ar seta aceste chain-uri inițial, aplicând handler-urile necesare.

Acest pattern este răspândit între comportament, dar este cel mai util pentru *prototipare*.
Strategia unde utilizăm `Check` și `Do` lucrează pentru majoritatea comportamentelor la început, însă eventual deseori realizați că aveți nevoie de mai mult control, de exemplu de chain-urile `Before` sau `After`.
Atunci veți defini toate pe care le aveți nevoie în comportamentele dvs particulare, lăsând autoactivarea în urmă.

De exemplu, `Displaceable` a fost inițial un comportament autoactivat.

[Vedeți codul sursă.][16]


#### Pushable

`Pushable` este asemănător un comportament *autoactivat*, însă nu este *direcționat activat*, deoarece acțiunea asociată cu el nu poate fi executată voluntar.

Codul lui `Pushable` la moment nu este matur, deci nu pot explica mult aici.

[Vedeți codul sursă.][17]


### Bloc

Ideea că o entitate nu poate să se miște la o celulă este conceptualizată spunând că acea celulă este *blocată* de o altă entitate.
Tipic, această entitate ar fi ori de la nivelul *real*, ori de la nivelul *wall*.

Cum am notat anterior, blocarea mișcării este implementată în `Displaceable`.
Blocuri mai pot afecta *sistemul de selectare țelelor*, explicată mai târziu.

#### Entitățile direcționate

Proprietatea de a fi direcționat semnifică că entitatea ar ocupa doar o parte a celulii în care ea se află.
Așa entități direcționate care servesc ca blocuri direcționate sunt numite *bariere*.

Ideea este inspirată de așa blocuri din **Cadence of Hyrule**.
[Unul din teste][18] explică ideea blocurilor direcționale cu ASCII mai clar decât eu aș putea prin text.

Aceasta introduce mai multă complexitate în procesul de detectare dacă o celulă particulară este blocată.

De obicei, pentru blocuri nedirecționate, pur și simplu trebuie să verificăm doar o celulă pentru a determina dacă celula este blocată sau nu.
Dacă celula conține o entitate din nivelul de bloc dvs, da, dacă nu conține, nu.
Cu blocuri direcționate aceasta este mai subtil.

Dacă entitatea din nivelul de bloc dvs este direcționat, trebuie să verificați dacă este la partea corectă a celulei (ce parte ea ocupă este indicată de către orientarea ei).
Partea corectă a celulei este partea din care caracterul dvs o ar intra.
Dacă entitatea potențial bloc ar fi pe orice altă parte a celulei, mișcarea nu ar fi blocată. 

Însă nu-i totul! Mai trebuie să verificați dacă celula de pa care caracterul începe mișcare conține un bloc direcțional pe cealaltă parte a celulei de pe care caracterul o ar ieși.

Am implementat toate acestea în [funcția `HasBlock()`][19] din `Grid`.
Deoarece trebuie să știem din ca parte caracterul ar ieși, luăm ca input direcția pe lângă coordonatelor celulei de interes.


### Event-urile de intrare și de ieșire

Grila mai definește [4 structuri utile][20]:
- `TriggerGrids` normală de `Enter` și `Leave`;
- `TriggerGrids` filtrată de `Enter` și `Leave`;

Acestea încă nu și-au demonstrat valoarea utilă în cod, însă le-am utilizat pentru a implementa efectele de *alunecare, bouncing, fixare* și în *proiectile*.

Esențial, aceste grile permit să adăugați funcții handler care vor fi executate când orice entitate intră (sau iese de pe) celula.
Diferența dintre grilele cele normale și filtrate este faptul că în grilele normale, handler-ul dvs *ar fi eliminat după terminarea turului curent*, ceea ce înseamnă că handler-ul va persista numai până la moment când toate entitățile își termină acțiunile.
În constrast, handler-urile adăugate în grila filtrată decid dacă ei trebuie să fie păstrate sau scoase singuri, returnând true sau false. 
Pentru un exemplu, vedeți [`Leave` handlerul lui bouncing][21].

Remarc că acest API încă nu este complet și am putea să decid să-l schimb în viitor.
Pur și simplu am explorat ideea care mi-a părut utilă.

De exemplu, [acest handler][21] captează entitatea ca primul argument.
Captarea (crearea closure-ilor) ideal am s-o schimb la un lookup pe id al entității pentru a permite entităților să fie "garbage collected" imediat.
Însă, să fac acest lucru manual ar fi anevoios.
Eu aș putea să utilizez iarăși generatorul de cod pentru acest scop în viitor.


## Chain-urile

În secțiunile precedente am apăsat ușor ideea de *chain-uri*.
Acestă secțiune dă o descriere mai detaliată despre ce ele sunt.

### Resposibility chains

*Chain-urile* în codul meu sunt băzate pe ideea unui **lanț de responsibilitate** (responsibility chain).

Un lanț de responsibilitate este o listă de funcții handler care operează cu anumite date.
Datele pot fi simple, ca un număr, dar pot fi și mai complexe, în care caz de obicei sunt numite *context*.

Sensul apelării acestor handleri este de a primi un oarecare rezultat sau de a aplica un oarecare efect.
După ce unul din handler-uri au reușit să-și aplică efectul sau să-și calcula rezultatul, propagarea se termină, adică nici un handler ce urmează nu ar fi executat.

În cazul chain-urilor *din codul meu*, ideea *"reușirii de a-și aplica efectul"* este mai generală.
Oare propagarea trebuie să fie oprită este verificat prin evaluarea proprietății `Propagate` a contextului, care poate or incapsula un câmp boolean ori să utilizeze o funcție pentru a calcula valoarea în dependența de valorile altor câmpuri din context.
Încă, un chain poate fi *trecut fără a verifica propagarea*, adică trecut până la capăt independent de valoare lui `Propagate`.

Vedeți [testele pentru chain-urile][24].

### Prioritatea

Ar putea să fie beneficiar ca handler-urile să aibă o prioritate și să fie sortate după acea prioritate.
Aceasta ar face procesul de fixare a diferitor bug-uri legate de ordonarea execuției a handler-urilor mai ușor, dând mai multe flexibilitate chain-urilor.

Întrebarea este, ce structură de date să utilizăm pentru acest scop?
Avem nevoie de inserții, ștergeri și căutări rapide, dar în același timp să putem itera prin colecția sortată după prioritate.

O idee ar fi să utilizăm o listă și s-o sortăm înainte de fiecare iterare prin ea.
Este o soluție, însă problema este că adăugarea handler-urilor este lentă, și căutarea implică scanarea întregei liste.

O altă idee, care am utilizat-o la un moment, ar fi să utilizăm listele înlănțuite, sortându-le înainte de iterare.
Însă:
- sortarea listelor înlănțuite nu este frumoasă,
- trebuie să avem a doua listă pentru a stoca handler-uri adăugate între iterații, ce ar fi pe urmă adăugate în lista principală.

Curent, utilizez un arbore binar balansat (`SortedSet` în C#).
Ștergerea, inserția și căutarea sunt logaritmuce, și colecția mereu stă sortată.
Încă am făcut ca prioritățile să fie unice pentru toate handler-urile în program, ca orice handler să poată fi identificat prin prioritatea sa.

#### Cum prescriem prioritățile?

Prioritatea este prescrisă în funcția de inițializare generată automat, utilizând registrul pentru a genera numere de prioritate.

Am făcut o clasă specială pentru acest lucru, [priority assigner][25], care mapează


