# Saint-Saens
Créé dans le cadre de l'ANR Collabscore (https://anr.fr/Projet-ANR-20-CE27-0014), ce dépôt regroupe les transcriptions électronique de l'ensemble des oeuvres de Camille Saint-Saens (à l'exception des opéras) numérisées par la BnF sur https://gallica.bnf.fr dans l'optique d'être versé sur la plateforme http://neuma.huma-num.fr/.


## Transcriptions

Dans un premier temps, nous réalisons ces transcriptions avec le logiciel de reconnaissance de caractère musicaux (OMR) "PhotoScore & NotateMe Ultimate 2020", mais nous utiliserons à terme l'application développée par notre équipe.

Les informations sur les processus de transcription et le suivi des versions se retrouvent au sein des fichiers MEI.

Les transcriptions feront ultérieurement objet d'une vérification en interne.

Le dossier "Transcription" contient :
+ La numérisation en MEI
+ Une version musicXML
+ Une version musx
+ Une version sib
+ Un fichier JSON 

Le fichier JSON comprend une sélection de métadonnés utilisé par la plateforme "http://neuma.huma-num.fr/". Il comprend:
+ ref = l'identifiant de l'oeuvre transcrite
+ title = son titre
+ composer = son compositeur
+ lyricist = l'auteur des paroles de l'oeuvre transcrite. "lyricist" est laissé vide dans le cas d'une oeuvre instrumentale.
+ date = la date de création de l'oeuvre transcrite.
+ cote = La cote du document ayant servi de source à la numérisation de l'oeuvre transcrite
+ sources = Le lien ark de gallica lié au document indiqué par la cote
 
### Identifiants d'une oeuvre
 
Les numérisations sont cataloguées par un identifiant constitué d'une lettre (R ou C), suivis de trois chiffres, d'un tiret bas "_" et d'un ou deux caractères.

La première lettre donne une indication sur la présence de l'oeuvre dans le catalogue thématique des oeuvres de Camille Saint-Saens réalisé par Sabina Teller Ratner. Si l'oeuvre indentifié est répertorié dans ce catalogue, la première lettre de son identifiant est noté "R" et les trois chiffres suivant correspondent à l'indexation de ce catalogue. 
Dans le cas où l'oeuvre identifié est absent du catalogue de Sabina Teller Ratner, nous lui assignons la lettre "C" et lui attribons un numéro à trois chiffres.
Enfin, après un tiret bas "_", nous indiquons un numéro pour distinguer les différentes versions d'une même œuvre, avec l'adjcontion d'une lettre pour les parties séparés.

Exemple : 

La "Danse macabre" est consigné dans le catalogue de Sabina Teller Ratner au numéro 171. Nous indiquons alors par "R171" les différentes versions de la "Danse Macabre" que nous distinguons ainsi :
- "R171_0" pour la mélodie pour piano et voix.
- "R171_1" pour la mélodie avec orchestre.
- "R171_2" pour la partition orchestrale.
- "R171_3" pour la transcription pour piano et violon.
- "R171_3v" pour la partie séparée du violon.
- "R171_4" pour la transcription pour deux pianos.
- "R171_41" et "R171_42" respectivement pour la partie séparée du premier et du second piano.

### Les metadonnées
Chaque transcription en MEI contient également une série de metadonnées apportant des renseignements sur l'oeuvre transcrite. Nous les récupèrons à partir du site Gallica grace au script "GallicOvuM" que nous avons développé à cette fin.

####identifiant
L'identifiant de l'oeuvre est indiqué dans l'élément mei/meiHead/altId
####title
Le titre de l'oeuvre est indiqué dans les éléments suivants :
+ mei
    └──meiHead
        └──fileDesc
            └──titleStmt
                └──title

+ mei/meiHead/fileDesc/titleStmt/title
+ mei
    └──meiHead
        └──workList
            └──work
                └──title
+ mei
    └──meiHead
        └──manifestationList
            └──manifestation
                └──editionStmt
                    └──title
####compositeur
Le compositeur de l'oeuvre est indiqué dans les éléments suivant :
+ mei/meiHead/fileDesc/titleStmt/composer
+ mei/meiHead/workList/work/composer
+ mei/meiHead/manifestationList/manifestation/editionStmt/composer
####auteur
L'auteur des paroles de l'oeuvre, quand elles existent, est indiqué dans les éléments suivants :
+ mei/meiHead/fileDesc/titleStmt/lyricist
+ mei/meiHead/workList/work/lyricist
+ mei/meiHead/manifestationList/manifestation/editionStmt/lyricist
####edition
Les informations sur l'édition du document qui sert de source à la numérisation sont indiqués dans les éléments suivant :
+ mei/meiHead/fileDesc/editionStmt/respStmt/persName avec comme attribut @role="Editor"
+ mei/meiHead/fileDesc/editionStmt/respStmt/edition
####nombre de pages
Le nombre de pages du document qui sert de source à la numérisation sont indiqués dans les éléments suivant :
+ mei/meiHead/fileDesc/extent avec comme attribut @unit="pages"
+ mei/meiHead/manifestationList/manifestation/physDesc/extent avec comme attribut @unit="pages"
####source & cote
Le lien ark de gallica lié au document ayant servi de source à la numérisation de l'oeuvre transcrite se trouve dans l'attribut @auth.uri de l'élément:
+ mei/meiHead/fileDesc/sourceDesc/source
La cote de ce document se trouve dans les éléments :
+ mei/meiHead/fileDesc/sourceDesc/source/bibl
+ mei/meiHead/manifestationList/manifestation/itemList/item/physLoc/repository
####encodeur & engraveur
L'identité de la personne ayant réalisé l'encodage du document MEI est indiqué dans l'élément :
+ mei/meiHead/fileDesc/titleStmt/respStmt/name juste en dessous de l'élément :
+ mei/meiHead/fileDesc/titleStmt/respStmt/resp="Encoded by"
L'identité de la personne ayant réalisé la gravure du document MEI à l'aide du logiciel OMR est indiqué dans l'élément :
+ mei/meiHead/fileDesc/titleStmt/respStmt/name juste en dessous de l'élément :
+ mei/meiHead/fileDesc/titleStmt/respStmt/resp="Engraved by"
####projet
Le projet ANR Collabscore (https://anr.fr/Projet-ANR-20-CE27-0014) et l'équipe de l'IReMus UMR 8223 rattachée à ce projet (Aurélien Balland Chatignon, Thomas Bottini, Christophe Guillotel-Nothmann, Fabien Guilloux et Simon Raguet) sont identifiés dans l'élément :
+ mei/meiHead/encodingDesc/projectDesc
####gallicovum - Photoscore - Sibelius - Sibmei
Les trois logiciels impliqués dans la constitution des fichiers MEI sont chacun identifié dans un élément :
+ mei/meiHead/encodingDesc/appInfo/application

####date
La date de création du document ayant servi de source à la numérisation de l'oeuvre transcrite se trouve dans les éléments :
+ mei/meiHead/fileDesc/titleStmt/editionStmt/edition/date
+ mei/meiHead/workList/work/creation/date

####genre
L'indication du genre musical de l'oeuvre se trouve dans l'élément :
+ mei/meiHead/manifestationList/manifestation/seriesStmt avec l'attribut @type="Music	Genre"

####revision


##WorkInProgress
Contient simplement les fichiers en cours de traitement avant d'être versé dans "Transcriptions".

## Software
Nous récupérons les métadonnées des numérisations de Gallica avec le script "GallicOvuM".
Nous réalisons les fichiers JSON, contenant des metadonnées utile à la plateforme Neuma avec le script corpus_utils.