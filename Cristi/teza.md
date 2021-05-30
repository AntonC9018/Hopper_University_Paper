# Tema: Metode de dezvoltare rapida a jocurilor video


Lista abrevierilor:

MVC: Model - View - Controller


## Preambula

Pentru a crea un joc video este necsar de a crea mai ...

## Alegerea instrumentelor corespunzatoare pentru dezvoltare
## About convenience of development

In primul rănd, pentru a deține un nivel înalt de confort în procesul de dezvoltare a programelor trebuie de ales instrumente corespunzătoare necesităților. În cadrul industriei jocurilor video se observă o axă

Axis of complexity:

Direct3D/OpenGL/Vulkan -> XNA (MonoGame) -> Godot -> Unity -> Unreal Engine

Complexity requirements for different kinds of games: Console/ASCII, 2D, 3D


## Alegerea unui pattern prestabilit de dezvoltare și planificare exhaustiva

Alegerea unui pattern prestabilit de dezvoltare aduce mai multe avantaje în procesul de dezvoltare. În primul rând, un pattern de programare este o arhitectura predefinită ce poate fi folosită pentru rezolarea unui set de probleme încă la etapa de planificare. Spre exemplu, în cadrul proiectului nostru folosim pattern-ul MVC pentru a separa direcțiile de dezvoltare (Anton dezvoltă Modelul, până când eu dezvolt View-ul și Controller-ul). Modelul calculează toată logica internă, și nu este nicicum direct legat de interfață grafică și rendering, View-ul reprezintă propriu-zis interfața grafică, iar Controller-ul formează legătura dintre Model și View __(review this)__. Asemenea reguli nu trebuie să fie urmate strict, indiferent de efect în cadrul programului, ci invers - pot fi modelate pentru a se potrivi problemei. Spre exemplu, în cazul nostru Modelul este o unitate separată, View-ul este de fapt motorul de joc Godot, iar Controller-ul este de fapt suita de script-uri rulate în Godot.

O asemenea separare permite și separarea rolurilor pentru fiecare programator, astfel fiecare va lucra strict asupra domeniului său, contactând cu alții doar în caz de code review și legături dintre script-uri (best case scenario).