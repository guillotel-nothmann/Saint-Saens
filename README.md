# Saint-Saens
Créé dans le cadre de l'ANR Collabscore (https://anr.fr/Projet-ANR-20-CE27-0014), ce dépôt regroupe les transcriptions en fichier MEI de l'ensemble des oeuvres de Camille Saint-Saens (à l'exception des opéras) numérisées par la BnF sur https://gallica.bnf.fr dans l'optique d'être versé sur la plateforme http://neuma.huma-num.fr/.

Dans un premier temps, nous réalisons ces transcriptions avec le logiciel OMR "PhotoScore & NotateMe", mais nous utiliserons à terme l'application développée par notre équipe.

Les informations sur les processus de transcription et le suivi des versions se retrouvent au sein des fichiers MEI.

Les transcriptions feront ultérieurement objet d'une vérification en interne.


## Transcriptions
Le dossier Transcription contient ces numérisations accompagnées de leur version en musicXML, musx, sib. Un fichier JSON comprenant uen sélection de métadonnés pour la plateforme neuma et le PDF de la numérisation sur Gallica accompagne également chaque fichier.
Les numérisations sont cataloguées par un identifiant constitué d'une lettre (R ou C), de trois chiffres, d'un tiret "_" et d'un ou deux caractères.

La première lettre indique si l'oeuvre est consigné ou non dans le catalogue thématique des oeuvres de Camille Saint-Saens réalisé par Sabina Teller Ratner. Si tel est le cas, la première lettre sera noté "R" et les trois chiffres suivant correspondront à l'indexation de ce catalogue.
Dans le cas contraire, nous lui assignerons la lettre "C" et lui attribuerons un numéro à trois chiffres.
Enfin, après le "_", nous indiquons un numéro pour distinguer les différentes versions d'une même œuvre et une lettre pour les parties séparés.

Exemple : 

La "Danse macabre" est consigné dans le catalogue au numéro 171. Nous indiquerons donc par "R171" les différentes versions de la "Danse Macabre" que nous distinguerons comme suit :
- "R171_0" pour la mélodie pour piano et voix.
- "R171_1" pour la mélodie avec orchestre.
- "R171_2" pour la partition orchestrale.
- "R171_3" pour la transcription pour piano et violon.
- "R171_3v" pour la partie séparée du violon.
- "R171_4" pour la transcription pour deux pianos.
- "R171_41" et "R171_42" respectivement pour la partie séparée du premier et du second piano.

##WorkInProgress
Contient simplement les fichiers en cours de traitement avant d'être versé dans "Transcriptions".

## Software
Nous récupérons les métadonnées des numérisations de Gallica avec le script "GallicOvuM".
Nous réalisons les fichiers JSON, contenant des metadonnées utile à la plateforme Neuma avec le script corpus_utils.