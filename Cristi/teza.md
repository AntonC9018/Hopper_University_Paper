# Tema: Metode de dezvoltare rapida a jocurilor video


Lista abrevierilor:

MVC: Model - View - Controller
API: application programming interface

## Preambula

Pentru a crea un joc video este necesar de a dezvolta mai multe componente avansate: renderer 2D/3D, simulația fizicii/coliziunilor, audio, animație, management de scenă, etc. Desigur, o asemenea sarcină poate fi extrem de dificil de realizat pentru o echipă mică de programatori neexperimentați. În cazul dat putem folosi motoarele de joc: suite de instrumente ce conțin componentele descrise mai sus, lăsând pentru dezvoltatori doar sarcina de creare a programelor specifice jocului (model). 

## Alegerea instrumentelor corespunzatoare pentru dezvoltare
### About convenience of development

In primul rănd, pentru a deține un nivel înalt de confort în procesul de dezvoltare a programelor trebuie de ales instrumente corespunzătoare necesităților. Fiecare motor de joc oferă o suită diferită de instrumente, de la doar un API pentru rendering, până la instrumente extrem de complexe de creare rapidă a 3D modele de oameni și import direct a modelelor formate prin fotogrammetrie. În cadrul industriei jocurilor video se observă o axă de suite cu nivel diferit de componente incluse:

Direct3D/OpenGL/Vulkan -> XNA (MonoGame) -> Godot -> Unity -> Unreal Engine

Complexity requirements for different kinds of games: Console/ASCII, 2D, 3D

Pe de altă parte, fiecare joc are nevoie de un set specific de componente pentru a rula. Spre exemplu, jocurile ca Cataclysm: Dark Days Ahead și Dwarf Fortress rulează în consolă, în care fiecare caracter desenat este de fapt un element, fie asta o entitate vie, un perete sau pur și simplu spațiu liber. Asemenea proiecte de fapt nu au nevoie de niciun component din suita motoarelor de joc, pentru că constă din simulare internă (model) și consolă (renderer).

__insert screenshots__

Din acest fapt putem deduce că o suită bogată în instrumente nu e numaidecât cea mai bună alegere __insert more examples__. Spre exemplu, un motor ca Unreal Engine poate fi prea complex și dificil pentru un simplu 2D joc. Deci alegerea trebuie făcută analizând mai mulți factori:

- Cât de complex planificați să fie jocul? Ce componente vor fi necesare pentru întreg jocul?
- Cât de mare și cu experiență este grupul vostru de programatori? Care componente le-ați putea dezvolta singuri și invers, care componente mai bine le-ați folosi din alte suite?
- (opțional) Pentru device-uri cu ce nivel de performanță doriți să creați jocul? (O suită mai avansată necesită calculatoare puternice atât pentru dezvoltare, cât și pentru rulare la utilizatorul final).

Spre exemplu, în cazul nostru am ales motorul de joc Godot, care va lua rolul de renderer și manager a scenei. Restul componentelor (modelul, animatorul) deja noi singuri le-am creat.

## Alegerea unui pattern prestabilit de dezvoltare și planificare exhaustiva

Alegerea unui pattern prestabilit de dezvoltare aduce mai multe avantaje în procesul de dezvoltare. În primul rând, un pattern de programare este o arhitectura predefinită ce poate fi folosită pentru rezolarea unui set de probleme încă la etapa de planificare. Spre exemplu, în cadrul proiectului nostru folosim pattern-ul MVC pentru a separa direcțiile de dezvoltare (Anton dezvoltă Modelul, până când eu dezvolt View-ul și Controller-ul). Modelul calculează toată logica internă, și nu este nicicum direct legat de interfață grafică și rendering, View-ul reprezintă propriu-zis interfața grafică, iar Controller-ul formează legătura dintre Model și View __(review this)__. Asemenea reguli nu trebuie să fie urmate strict, indiferent de efect în cadrul programului, ci invers - pot fi modelate pentru a se potrivi problemei. Spre exemplu, în cazul nostru Modelul este o unitate separată, View-ul este de fapt motorul de joc Godot, iar Controller-ul este de fapt suita de script-uri rulate în Godot.

O asemenea separare permite și separarea rolurilor pentru fiecare programator, astfel fiecare va lucra strict asupra domeniului său, contactând cu alții doar în caz de code review și legături dintre script-uri (best case scenario).

## Outsourcing-ul 

Outsourcing-ul este practica de afaceri de angajare a unor lucrători externi pentru efectuarea unui serviciu, care de obicei se face în cadrul organizației. În cadrul industriei jocurilor video, __include source__ outsorcing-ul se folosește deseori pentru crearea unor asset-uri necritice, dar necesare pentru joc (filler). Sp

## Simplificarea conceptelor până la nivelul actual pentru joc

Deoarece 