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

listepourplustard = [("https://gallica.bnf.fr/ark:/12148/bpt6k11827724","R178_0"),("","C441")]

altlist = [("R039_0",	"https://gallica.bnf.fr/ark:/12148/bpt6k1509584k/f72.item"),]

i = 0



def xmlId(x):
    global i 
    i += 1
    x.set('{http://www.w3.org/XML/1998/namespace}id','g-'+str(i))
    print(i)

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

while len(altlist) > 0:
    pop = altlist.pop()
    ark = pop[1]
    ark = ark_purification(ark)
    print("Ark = ", ark)
    name = pop[0]
    name = name.strip()
    if len(name)==4:
        name= name+"_0"
    print("name =", name)

    mei = ET.Element('mei', ns)
    mei.set('xmlns', 'http://www.music-encoding.org/ns/mei')
    xmlId(mei)
    #mei.set('{http://www.w3.org/XML/1998/namespace}id', 'g-1')
    mei.set('meiversion', '4.0.1')

        # Création de l'élément <meiHead>
    meiHead_tag = ET.SubElement(mei, 'meiHead')
    xmlId(meiHead_tag)
        # Création de l'élément <music>
    music = ET.SubElement(mei, 'music')
    xmlId(music)
        # Création de l'objet ElementTree
    tree = ET.ElementTree(mei)

    global mei_file
    #parser = ET.XMLParser(remove_blank_text=True)
    #tree = ET.parse("Users/iremus/GitHub/Saint-Saens/Software/GallicOvuM/x.mei", parser)

    pubStmt = ET.SubElement(meiHead_tag, "pubStmt")
    xmlId(pubStmt)    
    sourceDesc_tag = ET.Element("sourceDesc")
    xmlId(sourceDesc_tag)
    pubStmt.addnext(sourceDesc_tag)
    source_tag = ET.SubElement(sourceDesc_tag, "source")
    xmlId(source_tag)
    source_tag.set("auth.uri", "https://gallica.bnf.fr/ark:/" + ark)
    bibl_tag = ET.SubElement(sourceDesc_tag, "bibl")
    xmlId(bibl_tag)
    source_tag.append(bibl_tag)

    #fonction principale de ce script. extract_data va puiser les metadonnées depuis gallica pour les inscrire dans le fichier MEI.

    print("le lien =", ark)
    res= Document.OAI(ark)
    result = res["results"]["notice"]["record"]["metadata"]["oai_dc:dc"]

    fileDesc_tag = ET.SubElement(meiHead_tag, "fileDesc")
    xmlId(fileDesc_tag)
        # --- Création/récupération des balises ---
        #altId
    altId_tag = ET.Element("altId")
    xmlId(altId_tag)

        #fileDesc
        #F-Title
    FTtitleStmt_tag = ET.Element("titleStmt")
    xmlId(FTtitleStmt_tag)
    FTtitle_tag = ET.SubElement(FTtitleStmt_tag, "title")
    xmlId(FTtitle_tag)
    FTsubtitle_tag = ET.Element("title")
    xmlId(FTsubtitle_tag)
    FTsubtitle_tag.set("type", "subtitle" )
    FTsubtitle_tag.text=": an electronic transcription"
    FTtitle_tag.addnext(FTsubtitle_tag)
    FTcomposer_tag = ET.SubElement(FTtitleStmt_tag,"composer")
    xmlId(FTcomposer_tag)
    FTrespStmt_tag= ET.SubElement(meiHead_tag, 'respStmt')
    xmlId(FTrespStmt_tag)
    FTencoded_resp_tag = ET.SubElement(FTrespStmt_tag,"resp")
    xmlId(FTencoded_resp_tag)
    FTencoded_resp_tag.text="Encoded by:"
    FTencoded_name_tag = ET.SubElement(FTrespStmt_tag,"name")
    xmlId(FTencoded_name_tag)
    FTencoded_name_tag.text = "Balland Chatignon"+", "+"Aurélien"
        #F-Edition
    FEeditionStmt_tag = ET.SubElement(FTtitleStmt_tag,'editionStmt')
    xmlId(FEeditionStmt_tag)
    FErespStmt_tag = ET.SubElement(FEeditionStmt_tag,'respStmt')
    xmlId(FErespStmt_tag)
    FEpersName_tag=ET.SubElement(FErespStmt_tag, "persName")
    xmlId(FEpersName_tag)
    FEpersName_tag.set("role","Editor")
    FEedition_tag = ET.SubElement(FEeditionStmt_tag,'edition')
    xmlId(FEedition_tag)
    FEdate_tag=ET.SubElement(FEedition_tag,"date")
    xmlId(FEdate_tag)

        #F-Extent
    FXextent_tag=ET.SubElement(FTtitleStmt_tag,'extent')
    xmlId(FXextent_tag)
    FXextent_tag.set("unit", "pages")

        #encodindDesc
    encodingDesc_tag = ET.SubElement(meiHead_tag, "encodingDesc")
    xmlId(encodingDesc_tag)

        #On ajoute la mention de cette application
    app_info_tag = ET.SubElement(meiHead_tag, 'appInfo')
    xmlId(app_info_tag)
    Ethis_app_tag = ET.SubElement(app_info_tag,'application')
    xmlId(Ethis_app_tag)
    Ethis_app_tag.set("version","1.0")
    Ethis_app_name_tag = ET.SubElement(Ethis_app_tag, "name")
    xmlId(Ethis_app_name_tag)
    Ethis_app_date_tag = ET.SubElement(Ethis_app_name_tag, "date")
    xmlId(Ethis_app_date_tag)
    Ethis_app_date_tag .set("isodate", datetime.datetime.now().strftime("%Y-%m-%d") )
    Ethis_app_name_tag.text="GallicOvuM"
    Ethis_app_p_tag = ET.SubElement(Ethis_app_tag, "p")
    xmlId(Ethis_app_p_tag)
    Ethis_app_p_tag.text = "Metadata creation by extracting from Gallica"
    EprojectDesc_tag=ET.SubElement(encodingDesc_tag,"projectDesc")
    xmlId(EprojectDesc_tag)
    EprojectDesc_tag.text="ANR CollabScore (https://anr.fr/Projet-ANR-20-CE27-0014) - IReMus UMR 8223  Aurélien Balland Chatignon, Thomas Bottini, Christophe Guillotel-Nothmann, Fabien Guilloux, Simon Raguet."

        #workList
    workList_tag = ET.SubElement(meiHead_tag,"workList")
    xmlId(workList_tag)
    work_tag = ET.SubElement(workList_tag,"work")
    xmlId(work_tag)
    Wtitle_tag=ET.SubElement(work_tag,'title')
    xmlId(Wtitle_tag)
    Wcomposer_tag = ET.Element("composer")
    xmlId(Wcomposer_tag)
    Wtitle_tag.addnext(Wcomposer_tag)
    Wcreation_tag = ET.Element("creation")
    xmlId(Wcreation_tag)
    Wcomposer_tag.addnext(Wcreation_tag)
    Wdate_tag = ET.SubElement(Wcreation_tag,"date")
    xmlId(Wdate_tag)

        #manifestationList
    manifestationList_tag= ET.SubElement(meiHead_tag,'manifestationList')
    xmlId(manifestationList_tag)
    manifestation_tag =ET.SubElement(manifestationList_tag, 'manifestation')
    xmlId(manifestation_tag)
    MphysDesc_tag = ET.SubElement(manifestation_tag,'physDesc')
    xmlId(MphysDesc_tag)
    Mextent_tag= ET.SubElement(MphysDesc_tag, "extent")
    xmlId(Mextent_tag)
    Mextent_tag.set("unit", "pages")
    MseriesStmt_tag=ET.SubElement(manifestation_tag,"seriesStmt")
    xmlId(MseriesStmt_tag)
    MseriesStmt_tag.set("type","Music Genre")
    MeditionStmt_tag=ET.Element("editionStmt")
    xmlId(MeditionStmt_tag)
    MseriesStmt_tag.addnext(MeditionStmt_tag)
    Mtitle_tag=ET.SubElement(MeditionStmt_tag,"title")
    xmlId(Mtitle_tag)
    Mcomposer_tag=ET.SubElement(MeditionStmt_tag, "composer")
    xmlId(Mcomposer_tag)
    MitemList_tag=ET.Element("itemList")
    xmlId(MitemList_tag)
    MeditionStmt_tag.addnext(MitemList_tag)
    Mitem_tag=ET.SubElement(MitemList_tag,"item")
    xmlId(Mitem_tag)
    MphysLoc_tag=ET.SubElement(Mitem_tag, "physLoc")
    xmlId(MphysLoc_tag)
    Mrepository_tag=ET.SubElement(MphysLoc_tag,"repository")
    xmlId(Mrepository_tag)
    MrelationList_tag=ET.Element('relationList')
    xmlId(MrelationList_tag)
    MphysLoc_tag.addnext(MrelationList_tag)
    Mrelation_tag=ET.SubElement(MrelationList_tag,"relation")
    xmlId(Mrelation_tag)
    Mrelation_tag.text="This MEI file "+os.path.splitext(os.path.basename(name))[0]+ " is an electronic transcription of this item"

        #revisionDesc
    revisionDesc_tag=ET.SubElement(meiHead_tag,"revisionDesc")
    xmlId(revisionDesc_tag)
    change_tag=ET.SubElement(revisionDesc_tag,"change")
    xmlId(change_tag)
    change_tag.set("n",str(1))
    revisions_p_tag = ET.SubElement(change_tag, "p")
    xmlId(revisions_p_tag)
    revisions_p_tag.text="Creation of metadata by extraction from Gallica"

    revision_date_tag = ET.SubElement(change_tag, "date")
    xmlId(revision_date_tag)
    revision_date_tag.set("isodate", datetime.datetime.now().strftime("%Y-%m-%d") )
    revision_resp_tag = ET.SubElement(change_tag, "resp")
    xmlId(revision_resp_tag)
    revision_resp_tag.text = "GallicOvuM"
    

        # --- récupération des data ---

        #indexCollabscore
    altId_tag.text = os.path.splitext(os.path.basename(name))[0]

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
        if len(titre)< 2 :
            titre = result["dc:title"]
    else:
        titre = result["dc:title"]
    FTtitle_tag.text = titre
    Wtitle_tag.text=titre
    Mtitle_tag.text=titre

    print("titre=", titre)
            

            #l'éditeur
    if "dc:publisher" in result:
        if type(result["dc:publisher"]) == str :
            editor = result["dc:publisher"].strip()
            FEedition_tag.text = editor
            FEpersName_tag.text = editor
        else:
            while len(result["dc:publisher"]) > 0:
                publi = result["dc:publisher"].pop()
                editor = publi.strip()
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
                    tree.write(name+".mei", pretty_print=True, encoding="utf-16")
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
                tree.write(name+".mei", pretty_print=True, encoding="utf-16")
            else :
                FTcontributeur_tag=ET.SubElement(FTrespStmt_tag,'persName')
                FTcontributeur_tag.set('role',role )
                FTcontributeur_tag.text= dccontributor[:dot]


            print("element", element)
                

        #Mise en place des balises
        #altId
    meiHead_tag.insert(meiHead_tag.index(fileDesc_tag), altId_tag)



    tree.write(name+".mei", pretty_print=True, encoding="utf-16")
    i=0


