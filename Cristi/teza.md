# Tema: Tehnologii avansate la elaborarea jocurilor pe calculator

## Lista abrevierilor:

MVC: Model - View - Controller
API: application programming interface
ECS: Entity-Component System
POO: Programare orientată pe obiecte

## Introducere

### Actualitatea și importanța temei:

Deși fiind intuitiv apropiate de __programele convenționale__, jocurile video sunt de fapt destul de îndepărtate de acestea. Acestea întâlnesc probleme cardinal diferite și necesită metode specifice pentru a fi dezvoltate cu succes. 

### Scopul şi obiectivele propuse în teză

În cadrul acestei teze vor fi descrise metode de structurare...

### Suportul metodologic și teoretico-ştiinţific al lucrării (metode de cercetare)

## Capitolul 1. Titlul capitolului (analiza situaţiei în domeniul tezei.) (fundamentare teoretică, analiză, sinteze, etc.)

Pentru a crea un joc video este necesar de a dezvolta mai multe componente avansate: renderer 2D/3D, captarea tastelor apăsate pe tastatură/gamepad, simulația fizicii/coliziunilor, audio, animație, management de scenă, etc. Desigur, o asemenea sarcină poate fi extrem de dificil de realizat pentru o echipă mică de programatori neexperimentați. În cazul dat pot fi folosite motoarele de joc: suite de instrumente ce conțin componentele descrise mai sus, lăsând pentru dezvoltatori doar sarcina de creare a programelor specifice jocului (model). 

In primul rănd, pentru a deține un nivel înalt de confort în procesul de dezvoltare a programelor trebuie de ales instrumente corespunzătoare necesităților. Fiecare motor de joc oferă o suită diferită de instrumente, de la doar un API pentru rendering, până la instrumente extrem de complexe de creare rapidă a 3D modele fotorealistice de oameni și import direct a modelelor formate prin fotogrammetrie. În cadrul industriei jocurilor video se observă o axă de suite cu nivel diferit de componente incluse:

Direct3D/OpenGL/Vulkan -> XNA (MonoGame) -> Godot -> Unity -> Unreal Engine

Complexity requirements for different kinds of games: Console/ASCII, 2D, 3D

Pe de altă parte, fiecare joc are nevoie de un set __specific__ de componente pentru a rula. Spre exemplu, jocurile ca Cataclysm: Dark Days Ahead și Dwarf Fortress rulează în consolă, în care fiecare caracter desenat este de fapt un element, fie asta o entitate vie, un perete sau pur și simplu spațiu liber. Asemenea proiecte de fapt nu au nevoie de niciun component din suita motoarelor de joc, pentru că sunt formate doar din din simulare internă (model) și consolă (renderer).

__insert screenshots__

Din acest fapt putem deduce că o suită bogată în instrumente nu e numaidecât cea mai bună alegere __insert more examples__. Spre exemplu, un motor ca Unreal Engine poate fi prea complex și dificil pentru un simplu 2D joc. Deci alegerea trebuie făcută analizând mai mulți factori:

- Cât de complex planificați să fie jocul? Ce componente vor fi necesare pentru întreg jocul?
- Cât de mare și cu experiență este grupul vostru de programatori? Care componente le-ați putea dezvolta singuri și invers, care componente mai bine le-ați folosi din alte suite?
- (opțional) Pentru device-uri cu ce nivel de performanță doriți să creați jocul? (O suită mai avansată poate necesita calculatoare puternice atât pentru dezvoltare, cât și pentru rulare la utilizatorul final).
- Cât de permisivă este licența suitei? Puteți citi sau modifica codul sursă al acestuia?
- Care este costul unei copii de suită? 

De asemenea, nu excludem și faptul că instrumentele dezvoltate în interiorul studioului și pentru sarcini specifice pot fi mai avantajoase decât instrumentele externe create pentru sarcini generale, avantajul exprimându-se prin efort, timp și bani economisiți. Spre exemplu, dezvoltatorii puzzle-ului "Manifold Garden" au creat un instrument specific pentru a genera arbori corespunzători stilisticei jocului. Ei au putut să folosească instrumentul Speedtree, care se folosește destul de des pentru a genera vegetație, însă acesta este un instrument general care ar fi dificil de folosit pentru a crea arbori în stilistica dată și cu așa flexibilitate, nemaivorbind și de costul pentru produs, deci în cazul dat instrumentul intern oferă mai multe avantaje decât unul extern. Nu excludem și cazul când asemenea instrumente pot nici să nu existe pe piață. Spre exemplu, dezvoltatorii jocului "S.T.A.L.K.E.R. 2: Heart of Chernobyl" au creat un instrument special pentru a genera o dantură unică și irepetabilă pentru fiecare personaj.



__insert screenshots__

### Outsorcing-ul

Următoarea tehnică nu e o tehnologie, ci o practică de afaceri deseori folosită în prezent. Outsorcing-ul implică angajarea unei companii externe pentru a presta servicii care tradițional se făceau în interiorul companiei angajatoare de către lucrători. În cadrul industriei jocurilor video, __include source__ outsorcing-ul se folosește deseori pentru crearea unor asset-uri necritice, dar necesare pentru joc (filler) ca modelele hainelor, personajelor secundare, transportului și obiectelor statice din mediu. De asemenea această practică poate compensa lipsa lucrătorilor sau echipamentului dintr-un domeniu specific necesar jocului. Spre exemplu, echipamentul de motion capture este extrem de scump și necesită lucrători antrenați pentru lucru, însă este necesar pentru a crea animații realistice fără a decurge la animarea manuală, astfel se formează studiouri de motion capture care dețin echipamentul și personalul necesar și prestează serviciile studiourilor de jocuri video. 










## Capitolul 2. Titlul capitolului (aplicare, rezultate cercetări, studii de caz, etc.)

Ca exemplu de cercetare vom analiza proiectul Hopper, creat împreună cu Anton Curmanschii __include more info about hopper__. Hopper este un proiect ce extinde mecanicile jocului Crypt of the NecroDancer, care respectiv este un roguelike rhythm-game, în care jucătorul controlează un caracter pentru a explora o temniță subterană generată în mod procedural. Extinderea mecanicilor se exprimă prin posibilitatea de modificare a jocului, prin adăugarea/schimbarea entităților existente în joc, ce implică o arhitectură de joc slab cuplată și bazată în majoritate pe evenimente, de care fiecare component singur se agață.

De la bun început am decis să folosim câteva pattern-uri de programare pentru proiectul dat: MVC și ECS. Alegerea pattern-urilor prestabilite de dezvoltare aduc multe avantaje în procesul de dezvoltare. În primul rând, un pattern de programare este o arhitectura predefinită ce poate fi folosită pentru rezolvarea unui set de probleme încă la etapa de planificare. De asemenea aceste pattern-uri formează o structură intuitivă pentru cod, astfel un dezvoltator va ști cum să lucreze asupra proiectului, dacă acesta este menținut într-o oarecare __structură__.

Pattern-ul MVC permite separarea direcțiile de dezvoltare (Anton dezvoltă Modelul, până când eu dezvolt View-ul și Controller-ul). Modelul calculează toată logica internă, și nu este nicicum direct legat de interfață grafică și rendering, View-ul reprezintă propriu-zis interfața grafică, iar Controller-ul formează legătura dintre Model și View. Asemenea reguli nu trebuie să fie urmate strict, fără a considera efectul în cadrul programului, ci invers - pot fi modelate pentru a se potrivi problemei. Spre exemplu, în cazul nostru Modelul este o unitate separată, iar View-ul și Controller-ul sunt formate din motorul de joc Godot și suita de scripturi pentru acesta. O asemenea separare permite și separarea rolurilor pentru fiecare programator, astfel fiecare va lucra strict asupra domeniului său, contactând cu alții în caz ideal doar în situația de code review și formare a legăturilor dintre script-uri.

Pattern-ul ECS este folosit pentru a obține o flexibilitate mai înaltă la definirea obiectelor. În cadrul acestui pattern, fiecare obiect de joc este o entitate care este formată din componente ce adaugă funcționalitate. Comparativ cu programarea orientată pe obiecte, acest pattern este mult mai ușor de folosit în cazul proiectelor extrem de mari și oferă posibilități de optimizare pe bază de proiectare orientată pe date, ce se bazează pe utilizarea eficientă a cache-ului procesorului. Spre exemplu, în cazul când un grup de entități trebuie să se miște spre un oarecare punct, în cadrul POO procesorul ar trebui să ia obiecte întregi în cache doar ca să-i modifice un singur câmp intern. Din cauza aceasta, cache-ul se umple în totalitate cu un număr mic de obiecte și deci se efectuează numeroase apeluri extrem de lente la memoria RAM ca să le schimbe. Pe de altă parte, în cadrul ECS se iau în cache doar componentele care conțin poziția entității, care de fapt ocupă mai puțin loc decât obiectele întregi din exemplul trecut. Astfel, în cache încap mai multe componente, deci aceeași sarcină se realizează cu mult mai puține apeluri la memoria ram, în final efectuându-se mult mai rapid. 

O regulă pe care am stabilit-o de la început este separarea domeniului modelului de către View și Controller. În caz ideal, modelul nu trebuie să știe nimic despre celelalte componente, ele singure trebuie să se atașeze la evenimentele create și informația transmisă de model. O asemenea decuplare a logicii de interfață permite ca această logică să fie legată de orice altă interfață, fără a modifica codul intern a modelului. Spre exemplu, acest fapt a permis schimbarea de mai multe ori a motorului de joc, până am ajuns la o variantă satisfăcătoare pentru proiect. În final am ales motorul de joc Godot, care ia rolul de renderer și manager a scenei. Acest motor este extrem de compact, rapid și ușor de utilizat pentru dezvoltarea jocurilor 2D, ceea ce total ne răspunde cerințelor. De asemenea el se distribuie sub licența MIT, care permite utilizarea absolut gratuită a motorului și modificarea codului sursă a acestuia, ceea ce permite analiza în detalii a acestuia.  

Deoarece proiectul dat este dezvoltat în baza limbajului de programare C#, am structurat codul jocului într-un mod standart pentru limbaj. Întregul cod este separat în mai multe părți componente (numite proiecte) ce efectuează funcții specifice:

- Core - componentul de bază a jocului, conține simulațiile interne ale acestuia,
- Meta - generator de cod ce automat creează legături și boilerplate, care altfel ar fi trebuit scris manual
...
__add more info__
- View - proiectul de bază pentru motorul de joc Godot, inițiază toate procesele și formează legătura dintre motor și model.

Datorită acestei separări, am putut stabili fiecare parte componentă în directorii separate, pe care respectiv le-am inclus în repozitorii. Toate componentele ce țin de model sunt sincronizate într-un repozitoriu git separat, iar View-ul este salvat într-un git repozitoriu propriu, care însă include modelul ca submodul, astfel la descărcarea repozitoriului cu View automat se va descărca și ultima versiune a modelului. De asemenea obținem și o separare a drepturilor de acces, astfel cei ce lucrează asupra View-ului nu au acces direct la modificarea repozitoriului modelului și invers. De asemenea, deoarece ambele repozitorii sunt hostate public pe GitHub, orice doritor are drept de descărcare a oricărui repozitoriu, astfel oricine poate descărca doar modelul și crea propriul View, sau poate copia View-ul și să-l analizeze sau modifice local pe propriul plac.

În continuare vom analiza implementarea View-ului din proiectul dat. Inițial am creat un prototip ce include funcționalitatea strict necesară într-un timp scurt, fără mare atenție la optimizare și curățenia codului. Scopul acestui prototip este de a elimina problemele majore în legăturile dintre model și view, a avea o versiune relativ stabilă la care ne putem întoarce în orice moment, și a implementa în model funcționalitatea necesară pentru View care la moment poate să nu existe. Spre exemplu, inițial planificam să avem un punct centralizat ce va forma legătura dintre entitățile logice din model și obiectele din scenă, care va transmite rezultatele simulațiilor în scenă și le va arăta pe ecran. Pentru transmiterea rezultatelor planificam să folosim un obiect numit istorie, care de fapt este un queue de un tip de bază pentru datele transmise. Mai târziu însă am observat că o asemenea planificare nu este eficientă din cauza unei probleme mari. În primul rând, folosirea unei istorii centralizate înseamnă că orice date de tip derivat vor fi ascunse ca obiecte de tip de bază, iar ca să inversăm procesul trebuie să facem multe verificări de tipul `if (data is DerivedData) {...}`. Asemenea puncte în majoritatea cazurilor creează cele mai multe probleme, pur și simplu pentru că ele implică faptul că programatorul știe perfect ce date vor trece și că acesta va actualiza imediat codul în cazul unei modificări în model, __ceea ce evident niciodată nu se va întampla__. Codul trebuie scris într-un asemenea mod, ca cel ce îl va folosi nu va avea nevoie să știe pe de rost niște proprietăți ascunse într-o mulțime de cod în cazul când vrea să folosească vreo funcție. Acestea trebuie ori să fie explicit evidențiate către programator (exemplu: funcții leneșe din Java ce scot în evidență faptul că funcția poate ridica o excepție, și ea trebuie gestionată înafara acesteia), sau în general nu trebuie să existe. În cazul nostru am recurs la includerea obiectului din scenă ca un component a entității logice, astfel entitatea poate acționa asupra obiectului din scenă prin intermediul evenimentelor și fără intermediari centralizați.  

- talk animation stuff
Deoarece Hopper este un joc dinamic (???), ar fi logic să adăugăm animații pentru fiecare acțiune. Până când am adăugat animații pentru atac, mișcare și pentru a fi lovit. Ca și bază am creat o clasă abstractă Animator ce include un timer intern și funcții de start, stop și render al animației, iar restul animațiilor derivă de la această clasă și implementează funcțiile stabilite. Adaugător am mai folosit și funcții de interpolare liniară între 2 puncte pe spațiu bidimensional și pe o parabolă cu punctele (0, 0), (durata/2, vârf), (durata, 0). Spre exemplu, am putut forma animația unui salt prin interpolare liniară a poziției de la punctul de start spre final sumată cu valoarea parabolei pe axa y a poziției, iar animația atacului este de fapt interpolarea inversată a transparenței imaginii prin parabola descrisă mai sus.
__add pics__

- tilemap stuff
Deși la moment putem crea entități prin intermediul codului, această variantă nu este comodă în caz că dorim să creăm manual o scenă cu un număr mare de entități. Pentru aceasta am folosit instrumentul TileMap din motorul de joc Godot. Acest instrument permite setarea ușoară a unui număr mare de imagini în scenă (cu setări de collider etc), ceea ce este perfect pentru filler și generarea unei mape, însă nu e bun în cazul câ vrem să folosim obiecte complexe. Pentru a rezolva această problemă am creat un script ce analizează tilemap-ul necesar și găsește fiecare imagine ce este folosită în cadrul mapei date. Apoi în baza denumirii imaginii găsim clasa de bază a entității, și în sfârșit creăm entitățile necesare pe pozițiile date. În final acest instrument ne permite crearea ușoară a unui număr mare de entități în cadrul motorului, care vor fi activate deja la pornirea jocului.
__add pics__

- outsource
Design-ul grafic al unui joc est tot atât de important cât și codul acestuia. Un design plăcut atrage noi jucători, formează o oarecare istorie pentru entitate și pur și simplu dă mai multă inspirație pentru lucru decât o simplă schiță făcută în 5 minute în Paint. Deoarece nu avem artiști în echipă ce ar putea să se ocupe de design-ul jocului, am decis să angajăm un freelancer pentru acest serviciu. După o serie de discuții am ajuns la înțelegerea ca artistul să creeze imagini pentru inamicii din joc. Pentru crearea imaginilor a fost folosit redactorul de imagini GIMP. După introducerea acestor imagini, jocul arată mai profesional și mai plăcut.
__add pics__


## Concluzii şi recomandări


## Bibliografie
My RustConf 2018 Closing Keynote: Wayyyyyyy too much object orientation - https://kyren.github.io/2018/09/14/rustconf-talk.html
TOOLS PROGRAMMING – TREE GENERATOR - https://williamchyr.com/tools-programming-tree-generator/
S.T.A.L.K.E.R. 2 Dev Highlights (teeth) - https://youtu.be/v4lGSP3Po1Y?t=288
Outsorcing - https://youtu.be/ZsidtVmeFM0?t=352