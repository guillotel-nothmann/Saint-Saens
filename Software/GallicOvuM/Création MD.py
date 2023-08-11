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

altlist = [("	C000_1	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541695073	"),
("	C002	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169461j	"),
("	C004	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169489m	"),
("	C005	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169478t	"),
("	C006	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620473	"),
("	C007	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169443m	"),
("	C008	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694493	"),
("	C009	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162026x	"),
("	C010	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k386168k	"),
("	C012	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169491p	"),
("	C013	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161981x	"),
("	C014_0	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169498k	"),
("	C019	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169493h	"),
("	C021	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169445f	"),
("	C023	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170187m/f10.item	"),
("	C024	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162046p	"),
("	C025	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620384	"),
("	C026_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162060z	"),
("	C026_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620599	"),
("	C026_2	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162058w	"),
("	C027_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11619860	"),
("	C027_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161985k	"),
("	C029_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162003x	"),
("	C029_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162002h	"),
("	C030	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308997h/f17.item	"),
("	C031	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k393936p	"),
("	C032	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308997h/f71.item	"),
("	C034	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308997h/f21.item	"),
("	C035	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k3939359	"),
("	C036	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k3821202	"),
("	C037	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170187m/f14.item	"),
("	C038	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k3821194	"),
("	C039	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308997h/f26.item	"),
("	C040	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170187m/f20.item	"),
("	C041	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k393934x	"),
("	C042	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k382118r	"),
("	C043	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170187m/f26.item	"),
("	C044	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308997h/f31.item	"),
("	C045	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162061c	"),
("	C046	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k382117c	"),
("	C047	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308997h/f38.item	"),
("	C048	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k870961j	"),
("	C049	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170187m/f36.item	"),
("	C050	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308997h/f53.item	"),
("	C051	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308997h/f59.item	"),
("	C052	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308997h/f66.item	"),
("	C054	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162069p	"),
("	C055	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620688	"),
("	C056_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162067v	"),
("	C056_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162066f	"),
("	C058	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620651	"),
("	C062	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620562	"),
("	C064	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1182767t/f5.item	"),
("	C066	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162032n"),
("	C067	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620369	"),
("	C069	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620228	"),
("	C071	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k3842923	"),
("	C072	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162020f	"),
("	C074	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k321521z	"),
("	C076_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162035w	"),
("	C078_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620510	"),
("	C078_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170192x	"),
("	C079	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162049x	"),
("	C080	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162028r	"),
("	C082	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162014q	"),
("	C084	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162005r	"),
("	C087	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162053t	"),
("	C088	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k321523q	"),
("	C090	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162017z	"),
("	C091	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162016j	"),
("	C092	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11827709	"),
("	C093	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161999m	"),
("	C094_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11619986	"),
("	C098	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161978f	"),
("	C099	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11619756	"),
("	C100	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k8733549	"),
("	C101	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162030t	"),
("	C102	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k8709605	"),
("	C103_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620154	"),
("	C104	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620139	"),
("	C105	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620102	"),
("	C107	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k3855675	"),
("	C109	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k3211482	"),
("	C110_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k383689c	"),
("	C111_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161992q	"),
("	C113	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161990w	"),
("	C114	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11619897	"),
("	C119	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k385494r	"),
("	C121	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161983r	"),
("	C122	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161980h	"),
("	C123	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162037q	"),
("	C124	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161974s	"),
("	C125	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161973c	"),
("	C126	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161971j	"),
("	C129	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161969g	"),
("	C130	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11619682	"),
("	C131	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161965t	"),
("	C132	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k3861731	"),
("	C133	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161964d	"),
("	C135	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541695251	"),
("	C136	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162009d	"),
("	C137	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162048h	"),
("	C141_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162023p	"),
("	C142_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11620636	"),
("	C143_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162052d	"),
("	C144	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161987d	"),
("	C145_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161979v	"),
("	C146	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162025h	"),
("	C160	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166873k	"),
("	C163	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161967n	"),
("	C171	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694604	"),
("	C173	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161994j	"),
("	C174	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11619667	"),
("	C201	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166869p	"),
("	C202	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694886	"),
("	C203_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281531f	"),
("	C203_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166880q	"),
("	C203_2	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170231k	"),
("	C208	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166878n	"),
("	C209	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163845b	"),
("	C210	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11702305	"),
("	C213	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668599	"),
("	C300	",	"	https://gallica.bnf.fr/ark:/12148/btv1b52502461g	"),
("	C303	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11592787	"),
("	C304	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163820h/f60.item	"),
("	C305	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281525q	"),
("	C306	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166891h	"),
("	C307	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541695006	"),
("	C307	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281536h	"),
("	C309	",	"	https://gallica.bnf.fr/ark:/12148/btv1b52000847s	"),
("	C313	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169452k	"),
("	C314	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169466m	"),
("	C319	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162012w	"),
("	C404	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281532v	"),
("	C405	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694441	"),
("	C407	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169446v	"),
("	C408	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169459g	"),
("	C409	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169484j	"),
("	C410	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281538b	"),
("	C411	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668814/f38.item	"),
("	C412	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163820h/f80.item	"),
("	C413	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163820h	"),
("	C414	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668814/f18.item	"),
("	C415	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163820h/f110.item	"),
("	C422	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169441s	"),
("	C423	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169469v	"),
("	C424	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11913734	"),
("	C425	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694478	"),
("	C426	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1191375z	"),
("	C427	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694671	"),
("	C428	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694990	"),
("	C430	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169468f	"),
("	C432	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169454d	"),
("	C437	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11702001	"),
("	C438	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170201f	"),
("	C439	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668740	"),
("	C440	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170208b	"),
("	C441	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11748915	"),
("	C446	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1162011g	"),
("	C449	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11748737	"),
("	C450	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k321149f	"),
("	C452_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174892k	"),
("	C453_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174897n	"),
("	C454	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11748789	"),
("	C455	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166887m	"),
("	C456_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174905r	"),
("	C457	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k12815338	"),
("	C458	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k12815264	"),
("	C459	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281539r	"),
("	C460	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169509x	"),
("	C462	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169486c	"),
("	C464	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163819v/f38.item	"),
("	C469	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163819v/f26.item	"),
("	C471	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668814/f55.item	"),
("	R025	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11638408	"),
("	R028	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169448p	"),
("	R031	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11638490	"),
("	R032	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694923	"),
("	R033	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694515	"),
("	R034	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169463c	"),
("	R035	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163846r	"),
("	R036	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169462z	"),
("	R040	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694975	"),
("	R041	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1509514x	"),
("	R042	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169494x	"),
("	R043	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169520z	"),
("	R044	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169464s	"),
("	R045	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694530	"),
("	R046	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11748967	"),
("	R047	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174902h	"),
("	R048	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174881s	"),
("	R049	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11702216	"),
("	R051	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541695199	"),
("	R054	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166853t	"),
("	R055	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169487s	"),
("	R056	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k15095887	"),
("	R057	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668547	"),
("	R058	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694567	"),
("	R059	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169521c	"),
("	R061	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169512d	"),
("	R063	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174903x	"),
("	R064	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308948w	"),
("	R065	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170180q	"),
("	R066	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694797	"),
("	R067	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166848h	"),
("	R068_0	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169529p	"),
("	R069	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166850k	"),
("	R070	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174899g	"),
("	R071	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668510	"),
("	R077	",	"	https://gallica.bnf.fr/ark:/12148/btv1b52502461g/f17.item	"),
("	R078	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163844x	"),
("	R080	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11702231	"),
("	R083_h	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694834	"),
("	R083_O	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169482q	"),
("	R087_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170243s	"),
("	R087_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k925647k	"),
("	R094	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170185s	"),
("	R095	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11702127	"),
("	R096	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281534p	"),
("	R097	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170220s	"),
("	R102	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11669179	"),
("	R107	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169470h	"),
("	R109	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694656	"),
("	R110_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163834j	"),
("	R110_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11638319	"),
("	R110_2	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k15095924	"),
("	R110_3	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1509593j	"),
("	R110_4	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1182775c	"),
("	R110_5	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11638334	"),
("	R112_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1182780p	"),
("	R113	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169522s	"),
("	R114	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166899t	"),
("	R115	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169515n	"),
("	R117	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169510k	"),
("	R118	",	"	https://gallica.bnf.fr/ark:/12148/btv1b52000918c	"),
("	R120	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169524m	"),
("	R121	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11748930	"),
("	R122	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k8590281	"),
("	R123	",	"	https://gallica.bnf.fr/ark:/12148/btv1b525013878	"),
("	R124	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174877w	"),
("	R125	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k3142767	"),
("	R126	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668562	"),
("	R127	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169496r	"),
("	R128	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169495b	"),
("	R129	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170175d	"),
("	R130	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1159281q	"),
("	R132_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166885s	"),
("	R132_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11669038	"),
("	R133	",	"	https://gallica.bnf.fr/ark:/12148/btv1b100737172	"),
("	R135	",	"	https://gallica.bnf.fr/ark:/12148/btv1b520009117	"),
("	R136	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668903	"),
("	R137	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169508h	"),
("	R138	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169506p	"),
("	R139	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694760	"),
("	R140	",	"	https://gallica.bnf.fr/ark:/12148/btv1b525019327	"),
("	R141	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10073716m	"),
("	R143	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10318595d	"),
("	R144	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1509586d	"),
("	R145	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169518w	"),
("	R146	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169477d	"),
("	R147	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169457n	"),
("	R148	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170213n	"),
("	R149_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k321991m	"),
("	R149_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k858037q	"),
("	R150	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166849x	"),
("	R151	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k3168156	"),
("	R152	",	"	https://gallica.bnf.fr/ark:/12148/btv1b10308947f	"),
("	R161	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1167162p	"),
("	R162	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k858036b	"),
("	R164	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166915g	"),
("	R165	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170233d	"),
("	R168	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169527v	"),
("	R169	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11669142	"),
("	R170	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166913n	"),
("	R171_0	",	"	https://gallica.bnf.fr/ark:/12148/btv1b52502625c	"),
("	R171_1	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541695236	"),
("	R171_2	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170239w	"),
("	R171_3	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170198d	"),
("	R171_4	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11702038	"),
("	R172_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166910d	"),
("	R172_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668970	"),
("	R173_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163828t	"),
("	R173_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1163827d	"),
("	R174_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170240j	"),
("	R174_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k12815353	"),
("	R174_2	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170241z	"),
("	R175_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166916w	"),
("	R175_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11638386	"),
("	R176	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1159285c	"),
("	R178_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1182773j	"),
("	R178_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170227p	"),
("	R178_2	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11702372/	"),
("	R180_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k858041s	"),
("	R181	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k858035z	"),
("	R183	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1161958p	"),
("	R184	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166861c	"),
("	R185_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11669053	"),
("	R185_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11638475	"),
("	R186	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174879q	"),
("	R188	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11827724	"),
("	R190	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166906h	"),
("	R191	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11702268	"),
("	R192	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k3208945	"),
("	R193	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166909r/	"),
("	R196_0	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541695162	"),
("	R197	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166908b	"),
("	R198	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166907x	"),
("	R199_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k15095835	"),
("	R199_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1509589n	"),
("	R200_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k8580336	"),
("	R200_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11701792	"),
("	R201_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11701777	"),
("	R202_1	",	"	https://gallica.bnf.fr/ark:/12148/btv1b72006362	"),
("	R203_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k858040d/	"),
("	R203_1	",	"	https://gallica.bnf.fr/ark:/12148/btv1b525014023/	"),
("	R204_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174904b	"),
("	R204_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174894d	"),
("	R204_2	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11748893	"),
("	R205	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1170234t	"),
("	R206_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1166862s	"),
("	R207_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k8580425	"),
("	R208	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k8580383	"),
("	R209_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k858039g	"),
("	R210_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1158794r	"),
("	R210_1	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169480w	"),
("	R212_0	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169559t	"),
("	R212_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k15095850	"),
("	R216	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281529c	"),
("	R225_0	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668421	"),
("	R225_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668421/f7.item	"),
("	R244	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281528z	"),
("	R253	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1174900p	"),
("	R263	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281537x	"),
("	R264	",	"	https://gallica.bnf.fr/ark:/12148/bd6t541694426	"),
("	R268	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k12815301	"),
("	R278	",	"	https://gallica.bnf.fr/ark:/12148/bd6t54169450r	"),
("	R298	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1509504j	"),
("	R317	",	"	https://gallica.bnf.fr/ark:/12148/btv1b525032021	"),
("	R320	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k11668651	"),
("	R328_1	",	"	https://gallica.bnf.fr/ark:/12148/bpt6k1281527j	")]

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
    Ephotoscore_tag = ET.SubElement(app_info_tag,'application')
    xmlId(Ephotoscore_tag)
    Ephotoscore_tag.set("version","2020.1.14 (9.0.2) - 14th January, 2020")
    Ephotoscore_name_tag = ET.SubElement(Ephotoscore_tag, "name")
    xmlId(Ephotoscore_name_tag)
    Ephotoscore_name_tag.text = "PhotoScore & NotateMe"
    Ephotoscore_p_tag = ET.SubElement(Ephotoscore_tag, "p")
    xmlId(Ephotoscore_p_tag)
    Ephotoscore_p_tag.text = "Engraving by Optical Music Recognition"
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


