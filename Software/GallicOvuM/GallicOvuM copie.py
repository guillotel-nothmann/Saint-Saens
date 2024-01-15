from document_api import Document
import os
import json
import lxml
import lxml.etree as ET
import tkinter as tk
from tkinter.filedialog import askopenfilename
import csv
import datetime

ns = {"mei": "http://www.music-encoding.org/ns/mei",
       "xml": "http://www.w3.org/XML/1998/namespace"}
utfx = "utf-8"

#liste_ark=



def file_creator(content):
    root = ET.Element("mei", xmlns="http://www.music-encoding.org/ns/mei", meiversion="5.0")
    music = ET.SubElement(root, "music")
    tree = ET.ElementTree(root)

    with open("mei_vierge_test.mei", 'w', encoding='utf-8') as fichier:
        fichier.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fichier.write('<?xml-model href="https://music-encoding.org/schema/5.0/mei-all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n')
        fichier.write('<?xml-model href="https://music-encoding.org/schema/5.0/mei-all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n')
        fichier.write(ET.tostring(root, encoding='utf-8', pretty_print=True).decode('utf-8'))

   # Ajout des instructions de traitement XML
  

    # Création de l'élément music

    
    # Enregistrement du fichier XML
    tree = ET.ElementTree(root)
    


    #with open("mei_vierge_test", 'wb', encoding=utfx) as file:
      #  file.write(root)

file_creator("Ceci est le premier test")
print("test réalisé")
#Les fonctions

def a_propos():
    msgtext = "GallicOvuM (https://github.com/daftcloud/GallicOvuM) a été développé par Aurélien Balland Chatignon, ingénieur d'étude CNRS - IReMus (UMR 8223) dans le cadre de l'ANR Collabscore (https://anr.fr/Projet-ANR-20-CE27-0014)." \
    "\n\nCette application utilise le wrapper Pygallica (https://github.com/ian-nai/PyGallica)." \
    "\n\nA.B.Chatignon, Mai 2023"
    window = tk.Tk()
    window.title("À propos")
    Message =  tk.Label(window, text=msgtext, justify="left", wraplength=1600)
    close_button = tk.Button(window, text="Fermer cette fenêtre", command=window.destroy)
    Message.pack()
    close_button.pack()
    
    
def ark_purification(ark):
    #Met en forme l'ark afin qu'il soit utilisable par document_api
    ark = ark.strip()
    if "#" in ark:
        ark = ark[:-1]
    ark = ark.replace(";","")
    while ark.count("/") != 1:
        if ark.find("item") !=-1:
            ark = ark[:ark.rfind("/")]
        if ark[-1] == "/":
            ark = ark[:-1]
        if ark.count("/") == 0:
            ark = "12148/"+ ark
        elif ark.count("/") > 1:
            if ark.find("ark:/") != -1:
                ark = ark[ark.find("ark:/")+4:]
            else:
                ark = ark[ark.find("/")+1:]    

    return ark

def all_kind_contributor():
    #Dans les metadonnées de gallica, l'étiquette attribué au nom de l'auteur du texte littéraire d'une oeuvre n'est pas toujours la même.
    #la fonction all_kind_contributor va puiser toutes les étiquettes de contributeurs d'un corpus d'ark en CSV pour en faire un état des lieux.
    #C'est grâce à cette fonction que nous avons établis la liste "lyrilist" qui est utilisé dans la fonction extract_data
    csv_file = askopenfilename()
    contributorslist = []
    i=0
    with open(csv_file, "r", encoding= "utf-8") as File:
        reader=csv.reader(File, delimiter=',')
        for row in reader:
            row = ark_purification(row.pop())
            res = Document.OAI(row)
            i += 1
            #on vérifie qu'il y a pas d'erreur 
            if "dc:contributor" in res["results"]["notice"]["record"]["metadata"]["oai_dc:dc"]:
                #on vérifie si c'est une liste
                if type(res["results"]["notice"]["record"]["metadata"]["oai_dc:dc"]["dc:contributor"]) == list:
                    #si on a une liste de contributeur, on doit d'abord les séparer et les étudier 1 par 1
                    for element in res["results"]["notice"]["record"]["metadata"]["oai_dc:dc"]["dc:contributor"]:
                        dot = element.rfind(".")
                        element = element[dot+1:]
                        if element not in contributorslist:
                            contributorslist.append(element)
                    #Si on a qu'un seul contributeur, on doit recuperer son type
                else :
                    element = res["results"]["notice"]["record"]["metadata"]["oai_dc:dc"]["dc:contributor"]
                    dot = element.rfind(".")
                    element = element[dot+1:]
                    if element not in contributorslist:
                        contributorslist.append(element)

    print("###### liste des éléments : #####")
    for element in contributorslist:   
        print(element)

def find_mei():
   global mei_file 
   mei_file.set(askopenfilename())

def arkyer(gmei_file, ark, Gprenom,Gnom,Eprenom,Enom):
    #arkyer prend l'ark et l'insère dans le fichier MEI.
    global mei_file
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(gmei_file, parser)

    meiHead_tag = tree.find(".//mei:meiHead", ns)

    pubStmt = tree.find(".//mei:pubStmt", ns)
    if pubStmt is None:
        pubStmt = ET.SubElement(meiHead_tag, "pubStmt")
    print(pubStmt)
    
    sourceDesc_tag = ET.Element("sourceDesc")
    pubStmt.addnext(sourceDesc_tag)
    source_tag = ET.SubElement(sourceDesc_tag, "source")
    source_tag.set("auth.uri", "https://gallica.bnf.fr/ark:/" + ark)
    bibl_tag = ET.SubElement(sourceDesc_tag, "bibl")
    source_tag.append(bibl_tag)

    tree.write(gmei_file, pretty_print=True, encoding=utfx)
    mei_file.set("Aucun fichier sélectionné")
    link_entry.delete(0, tk.END)
    extract_data(ark, gmei_file, Gprenom,Gnom,Eprenom,Enom)

def analyse(ark):
      #analyse permet de voir les meta-données d'un ark sans les inscrire dans un fichier.
      res= Document.OAI(ark)
      print("####################")
      for cle in res["results"]["notice"]["record"]["metadata"]["oai_dc:dc"]:
          print(cle, ":==)=======>", res["results"]["notice"]["record"]["metadata"]["oai_dc:dc"][cle])
          print("---------------------")

def find_tag(tree, name, ns):
    tag = tree.find(".//mei:"+name, ns)
    if tag is None:
        tag = ET.Element(name)

    return tag

def clean_tag(tree, tag):
    x_element = tree.find(tag)

    # Vérifier si la balise 'X' a été trouvée
    while x_element is not None:
        # Supprimer la balise 'X' si elle a été trouvée
        tree.remove(x_element)
        x_element = tree.find(tag)


def extract_data(ark, gmei_file, Gprenom,Gnom,Eprenom,Enom):
    #fonction principale de ce script. extract_data va puiser les metadonnées depuis gallica pour les inscrire dans le fichier MEI.

    print("le lien =", ark)
    res= Document.OAI(ark)
    result = res["results"]["notice"]["record"]["metadata"]["oai_dc:dc"]

    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(gmei_file, parser)

    #Supprimmer des balises potentiellement preexistante
    #clean_tag(tree, "lyricist")

    #trouver les differents éléments preexistants
    bibl_tag = tree.find(".//mei:bibl", ns)
    
    meiHead_tag = tree.find(".//mei:meiHead", ns)
    fileDesc_tag = tree.find(".//mei:fileDesc", ns)
    
    # --- Création/récupération des balises ---
    #altId
    altId_tag = ET.Element("altId")

    #fileDesc
    #F-Title
    FTtitleStmt_tag = find_tag(tree,"titleStmt", ns)
    FTtitle_tag = find_tag(tree,"title", ns)
    FTsubtitle_tag = ET.Element("title")
    FTsubtitle_tag.set("type", "subtitle" )
    FTsubtitle_tag.text=": an electronic transcription"
    FTtitle_tag.addnext(FTsubtitle_tag)
    FTcomposer_tag = ET.SubElement(FTtitleStmt_tag,"composer")
    FTrespStmt_tag= tree.find('.//mei:respStmt', ns)
    FTencoded_resp_tag = ET.SubElement(FTrespStmt_tag,"resp")
    FTencoded_resp_tag.text="Encoded by:"
    FTencoded_name_tag = ET.SubElement(FTrespStmt_tag,"name")
    FTencoded_name_tag.text = Enom+", "+Eprenom
    FTengraved_resp_tag = ET.SubElement(FTrespStmt_tag,"resp")
    FTengraved_resp_tag.text="Engraved by:"
    FTengraved_name_tag = ET.SubElement(FTrespStmt_tag,"name")
    FTengraved_name_tag.text = Gnom+", "+ Gprenom
    #F-Edition
    FEeditionStmt_tag = ET.SubElement(FTtitleStmt_tag,'editionStmt')
    FErespStmt_tag = ET.SubElement(FEeditionStmt_tag,'respStmt')
    FEpersName_tag=ET.SubElement(FErespStmt_tag, "persName")
    FEpersName_tag.set("role","Editor")
    FEedition_tag = ET.SubElement(FEeditionStmt_tag,'edition')
    FEdate_tag=ET.SubElement(FEedition_tag,"date")
    #F-Extent
    FXextent_tag=ET.SubElement(FTtitleStmt_tag,'extent')
    FXextent_tag.set("unit", "pages")

    #encodindDesc
    encodingDesc_tag = tree.find(".//mei:encodingDesc", ns)
    Eapplication_sibmei_tag = tree.find(".//mei:application[@xml:id='sibmei']", ns)
    #Si l'application pour créer le mei est bien sibmei, on ajoute un texte qui explique l'utilisation de sibmei
    if Eapplication_sibmei_tag is not None:
        Esibmei_p_tag = ET.SubElement(Eapplication_sibmei_tag, 'p')
        Esibmei_p_tag.text = "Export to the Music Encoding Initiative (MEI) Format"
    #On ajoute la mention de cette application
    app_info_tag = tree.find('.//mei:appInfo', ns)
    Ethis_app_tag = ET.SubElement(app_info_tag,'application')
    Ethis_app_tag.set("version","1.0")
    Ethis_app_name_tag = ET.SubElement(Ethis_app_tag, "name")
    Ethis_app_name_tag.text="GallicOvuM"
    Ethis_app_p_tag = ET.SubElement(Ethis_app_tag, "p")
    Ethis_app_p_tag.text = "Metadata creation by extracting from Gallica"
    Ephotoscore_tag = ET.SubElement(app_info_tag,'application')
    Ephotoscore_tag.set("version","2020.1.14 (9.0.2) - 14th January, 2020")
    Ephotoscore_name_tag = ET.SubElement(Ephotoscore_tag, "name")
    Ephotoscore_name_tag.text = "PhotoScore & NotateMe"
    Ephotoscore_p_tag = ET.SubElement(Ephotoscore_tag, "p")
    Ephotoscore_p_tag.text = "Engraving by Optical Music Recognition"
    EprojectDesc_tag=ET.SubElement(encodingDesc_tag,"projectDesc")
    EprojectDesc_tag.text="ANR CollabScore (https://anr.fr/Projet-ANR-20-CE27-0014) - IReMus UMR 8223  Aurélien Balland Chatignon, Thomas Bottini, Christophe Guillotel-Nothmann, Fabien Guilloux, Simon Raguet."

    #workList
    workList_tag = find_tag(tree,"workList", ns)
    work_tag = find_tag(tree,"work", ns)
    Wtitle_tag=ET.SubElement(work_tag,'title')
    Wcomposer_tag = ET.Element("composer")
    Wtitle_tag.addnext(Wcomposer_tag)
    Wcreation_tag = ET.Element("creation")
    Wcomposer_tag.addnext(Wcreation_tag)
    Wdate_tag = ET.SubElement(Wcreation_tag,"date")

    #manifestationList
    manifestationList_tag= ET.SubElement(meiHead_tag,'manifestationList')
    manifestation_tag =ET.SubElement(manifestationList_tag, 'manifestation')
    MphysDesc_tag = ET.SubElement(manifestation_tag,'physDesc')
    Mextent_tag= ET.SubElement(MphysDesc_tag, "extent")
    Mextent_tag.set("unit", "pages")
    MseriesStmt_tag=ET.SubElement(manifestation_tag,"seriesStmt")
    MseriesStmt_tag.set("type","Music Genre")
    MeditionStmt_tag=ET.Element("editionStmt")
    MseriesStmt_tag.addnext(MeditionStmt_tag)
    Mtitle_tag=ET.SubElement(MeditionStmt_tag,"title")
    Mcomposer_tag=ET.SubElement(MeditionStmt_tag, "composer")
    MitemList_tag=ET.Element("itemList")
    MeditionStmt_tag.addnext(MitemList_tag)
    Mitem_tag=ET.SubElement(MitemList_tag,"item")
    MphysLoc_tag=ET.SubElement(Mitem_tag, "physLoc")
    Mrepository_tag=ET.SubElement(MphysLoc_tag,"repository")
    MrelationList_tag=ET.Element('relationList')
    MphysLoc_tag.addnext(MrelationList_tag)
    Mrelation_tag=ET.SubElement(MrelationList_tag,"relation")
    Mrelation_tag.text="This MEI file "+os.path.splitext(os.path.basename(gmei_file))[0]+ " is an electronic transcription of this item"

    #revisionDesc
    revisionDesc_tag=ET.SubElement(meiHead_tag,"revisionDesc")
    change_tag=ET.SubElement(revisionDesc_tag,"change")
    change_tag.set("n",str(1))

    revisions_p_tag = ET.SubElement(change_tag, "p")
    revisions_p_tag.text="Creation of metadata by extraction from Gallica"

    revision_date_tag = ET.SubElement(change_tag, "date")
    revision_date_tag.set("isodate", str(datetime.datetime.now().strftime("%Y-%m-%d") ))
    revision_resp_tag = ET.SubElement(change_tag, "resp")
    revision_resp_tag.text = "GallicOvuM"
   

    # --- récupération des data ---

    #indexCollabscore
    altId_tag.text = os.path.splitext(os.path.basename(gmei_file))[0]

    #compositeur
    if "dc:creator" in result:
        composer = result["dc:creator"]
        if type(composer) is list:
            composer = composer[0]
            composer = composer[:composer.find("(")].strip()
        else:
            composer = composer[:composer.find("(")].strip()
        FTcomposer_tag.text = composer
        Wcomposer_tag.text = composer
        Mcomposer_tag.text=composer

    #date
    if "dc:date" in result:
        date = result["dc:date"].strip()
        FEdate_tag.text = date
        Wdate_tag.text = date

    if "dc:format" in result:
        #nombre de pages
        for element in result["dc:format"]:
            if "Nombre total" in element:
                nbr_page_index = result["dc:format"].index(element)
                nbr_page = result["dc:format"][nbr_page_index]
                nbr_page = nbr_page[nbr_page.find(":")+1:].strip()
                FXextent_tag.text = nbr_page
                Mextent_tag.text=nbr_page
        

    if "dc:type" in result:
        if result["dc:type"] == list:
            le_type = result["dc:type"][0]
            dot = le_type.find(":")
            le_type = le_type[dot:].strip()
        else:
            le_type = result["dc:type"]
            dot = le_type.find(":")
            le_type = le_type[dot+1:].strip()
            

        MseriesStmt_tag.text=le_type
        print("Letype =", le_type)

    if "dc:source" in result:
        source = result["dc:source"]
        bibl_tag.text= source
        Mrepository_tag.text = source.strip()

        #titre
    if "dc:description" in result:
        print("Titre uniforme")
        titre = result["dc:description"][0]
        if len(titre)< 2:
            titre = result["dc:description"]
        tu_start = titre.find("[")
        tu_end = titre.find("]")
        titre = titre[tu_start:tu_end+1].strip()
    else:
        titre = result["dc:title"]
    FTtitle_tag.text = titre
    Wtitle_tag.text=titre
    Mtitle_tag.text=titre

    print("titre=", titre)
        

        #l'éditeur
    if "dc:publisher" in result:
        editor = result["dc:publisher"].strip()
        FEedition_tag.text = editor
        FEpersName_tag.text = editor
        
    if "dc:contributor" in result:
        #lyrilist est une liste contenant toutes les occurrences differentes sous laquelle un auteur peut être appellé sur gallica
        lyrilist = ["Parolier","Auteur du texte", "Auteur ou responsable intellectuel", "Auteur adapté", "Librettiste"]
        
        dccontributor = result["dc:contributor"]
        #Si les contibuteurs sont contenu dans une liste
        if type(dccontributor) == list:
            for element in dccontributor:
                #les contributeurs
                dot = element.rfind(".")
                role = element[dot+1:].strip()
                if role in lyrilist:
                    FTlyricist_tag=ET.Element("lyricist")
                    Wlyricist_tag=ET.Element("lyricist")
                    Mlyricist_tag=ET.Element("lyricist")
                    lyricist = element[:dot]
                    lyricist = lyricist[:lyricist.find("(")].strip()
                    FTlyricist_tag.text = lyricist
                    Wlyricist_tag.text = lyricist
                    Mlyricist_tag.text = lyricist
                    FTcomposer_tag.addnext(FTlyricist_tag)
                    Wcomposer_tag.addnext(Wlyricist_tag)
                    Mcomposer_tag.addnext(Mlyricist_tag)
                    FTcontributeur_tag=ET.SubElement(FTrespStmt_tag,'persName')
                    FTcontributeur_tag.set("role", role)
                    FTcontributeur_tag.text=lyricist        
                else:
                    FTcontributeur_tag=ET.SubElement(FTrespStmt_tag,'persName')
                    FTcontributeur_tag.set('role', role )
                    contributeur_name = element[:dot]
                    parenthese = contributeur_name.find("(")
                    contributeur_name = contributeur_name[:parenthese].strip()
                    FTcontributeur_tag.text= contributeur_name
                    tree.write(gmei_file, pretty_print=True, encoding=utfx)
        else:
            #si les contributeur ne sont pas dans une liste (c'est à dire qu'il n'y en a qu'un.)
            dot = dccontributor.rfind(".")
            role = dccontributor[dot+1:].strip()
            if role in lyrilist:               
                FTlyricist_tag=ET.Element("lyricist")
                Wlyricist_tag=ET.Element("lyricist")
                Mlyricist_tag=ET.Element("lyricist")
                lyricist = dccontributor[:dot].strip()
                lyricist = lyricist[:lyricist.find("(")].strip()
                FTlyricist_tag.text = lyricist
                Wlyricist_tag.text = lyricist
                Mlyricist_tag.text = lyricist
                FTcomposer_tag.addnext(FTlyricist_tag)
                Wcomposer_tag.addnext(Wlyricist_tag)
                Mcomposer_tag.addnext(Mlyricist_tag)
                print("b : ", role," et " ,lyricist)
                FTcontributeur_tag=ET.SubElement(FTrespStmt_tag,'persName')
                FTcontributeur_tag.set("role", role.strip())
                FTcontributeur_tag.text=lyricist
                tree.write(gmei_file, pretty_print=True, encoding=utfx)
            else :
                FTcontributeur_tag=ET.SubElement(FTrespStmt_tag,'persName')
                FTcontributeur_tag.set('role',role )
                FTcontributeur_tag.text= dccontributor[:dot]


            print("element", element)
            

    #Mise en place des balises
    #altId
    meiHead_tag.insert(meiHead_tag.index(fileDesc_tag), altId_tag)



    tree.write(gmei_file, pretty_print=True, encoding=utfx)
    #with open(gmei_file, "w", encoding="utf-8") as f:
        #f.write(ET.tostring(tree, encoding="unicode", pretty_print=True))
    
#Début de l'application
# I. Récupération du fichier MEI & du lien Ark avec une fenêtre
#Préparation de la fenêtre


root = tk.Tk()
root.title("GallicOvuM")
root.geometry("610x235")
root.resizable(False, False)
Prenom = "Aurélien"
Nom = "Balland Chatignon"

#Création des Widgets
frame_Graveur = tk.Frame(root, borderwidth=2, relief="ridge")
Graveur_Label = tk.Label(frame_Graveur, text="Graveur :")
Graveur_prenom = tk.Entry(frame_Graveur, bg="blue")
Graveur_prenom.insert(0,Prenom)
Graveur_nom = tk.Entry(frame_Graveur, bg="blue")
Graveur_nom.insert(0,Nom)

frame_encodeur = tk.Frame(root, borderwidth=2, relief="ridge")
Encodeur_Label = tk.Label(frame_encodeur, text="Encodeur :")
Encodeur_prenom = tk.Entry(frame_encodeur, bg="blue")
Encodeur_prenom.insert(0,Prenom)
Encodeur_nom = tk.Entry(frame_encodeur, bg="blue")
Encodeur_nom.insert(0,Nom)

mei_file = tk.StringVar(root)
mei_file.set("Aucun fichier sélectionné")

mei_button = tk.Button(root, text="Choisir le fichier MEI", command=find_mei)
mei_label= tk.Label(root, textvariable = mei_file, background="GREY")

analyse_button = tk.Button(root, text="Analyser", command= lambda: analyse(ark_purification(link_entry.get())))
ark_button = tk.Button(root, text="analyser plusieurs ark", command=all_kind_contributor)
a_propos_button = tk.Button(root, text="À propos", command = a_propos)
action_button = tk.Button(root, text="Lancer le programme", command=lambda: arkyer(mei_file.get(), ark_purification(link_entry.get()),Graveur_prenom.get(),Graveur_nom.get(),Encodeur_prenom.get(),Encodeur_nom.get()))

link_label = tk.Label(root, text="Lien Ark :")
link_entry = tk.Entry(root, bg="blue")
link_entry.config(width="31")

# Widget pour le Graveur
Graveur_Label.grid(row=2, column=0, padx=5, pady=5, sticky="n")
Graveur_prenom.grid(row=3, column=0, padx=5, pady=5, sticky="sw")
Graveur_nom.grid(row=4, column=0, padx=5, pady=5, sticky="sw")

# Widget pour l'Encodeur
Encodeur_Label.grid(row=2, column=1, padx=5, pady=5, sticky="n")
Encodeur_prenom.grid(row=3, column=1, padx=5, pady=5, )
Encodeur_nom.grid(row=4, column=1, padx=5, pady=5, )

# Autres widgets
a_propos_button.grid(row=5, column=2, sticky="w")
mei_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
mei_button.grid(row=1, column=0, padx=5, pady=5, sticky="we")
link_label.grid(row=0, column=0, padx=5, pady=5, sticky="we")
link_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
analyse_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")
#ark_button.grid(row=2, column=0, padx=5, pady=5, sticky="e")
action_button.grid(row=5, column=0, padx=5, pady=5, sticky="w")
frame_encodeur.grid(row=2, column=1, padx=5, pady=5, sticky="w")
frame_Graveur.grid(row=2, column=0, padx=5, pady=5, sticky="w")


root.mainloop()


