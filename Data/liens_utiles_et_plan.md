Quel lien entre la densité du bâti et transports/la densité du maillage à Paris ? https://github.com/Ramei6/p4ds
Données principalement issues du site opendata.paris.fr

[Projet de python pour la datascience : quel lien peut-on faire entre la densité du bâti et d'autres variables urbaines ?]

De nos jours, les sujets de l'urbanisme et de l'organisation l'espace public correspondent à un enjeu d'efficacité de l'usage des ressources et d'efficacité économique. Le but est d'avoir une ville efficace (bien-être, accès aux transports, espaces verts, ...) tout en minimisant les coûts. Dans ce cadre, la densité de l'activité est un facteur clef.

Pour étudier les fortes densités, nous allons nous appuyer sur différentes bases de données traitant de Paris intra-muros en raison d'une part de la grande quantité de données disponibles et d'autre part de la grande densité d'activité sur une surface importante qui caractérise cette ville. Cela nous permet a priori d'étudier la haute densité.

Lors de ce projet, nous allons notamment nous appuyer sur la [densité du bâti], définie comme la surface de bâtiments utilisable par unité de surface au sol, pour approcher l'activité humaine urbaine ou plutôt son potentiel. A priori, si l'on loge un habitant dans 30 mètres carré, au plus le nombre de mètres carré de bâtiment par kilomètre carré de surface au sol est important, au plus la densité de population maximale est importante. Nous avons choisi de nous appuyer sur cette variable pour mesurer l'activité humaine car la densité de population ne nous semblait pas satisfaisante. En effet, la répartition des bureaux, des habitants, des commerces touristiques (Appartement AirBNB, hôtels) n'est a priori pas uniforme. On pourra faire le lien avec nombreuses autres variables d'urbanisme.
On pourra également réaliser un état des lieux de la densité de bâti à Paris à différentes échelles.
[Volumes-bâtis :](https://opendata.paris.fr/explore/dataset/volumesbatisparis/map/?location=17,48.84008,2.39706&basemap=jawg.streets)
Cette base de données permet de géolocaliser chaque construction et d'en donner la surface bâtie totale M2_PL_TOT qui correspond au nombre de mètres carré utilisables par bâtiment. Pour un immeuble de 7 étages avec une surface au sol de 200 m2, cette variable vaut donc (7+1)*200 = 1600 m2. En sommant ces surfaces de bâtiments par zone géographique, on peut obtenir la densité de bâti de ces zones.

Un point important est le coût du transport. En ce qui concerne l'activité humaine urbaine, on veut vouloir garantir une même qualité de desserte pour un coût minimal. Dans ce cadre, la densité de l'activité est un facteur clé. Une haute densité réduit les surfaces à desservir et les distances.

Relativement aux transports en commun, si l'on souhaite par exemple disposer une station de transport en commun pour chaque carré de 500m par 500m, au plus l'activité est dense, c'est-à-dire se répartit sur une petite surface, au moins il faut bâtir et entretenir un nombre important de stations ainsi qu'un réseau routier ou ferroviaire important, au plus le coût de desserte de l'activité totale est réduit a priori. De plus, si l'on souhaite plutôt disposer une station de transport en commun pour chaque unité d'activité humaine, par exemple de 10 000 habitants, au plus cette activité est concentrée, dense, au plus cette activité est proche de la station de transport en commun, ce qui améliore la qualité de la desserte. Par ailleurs, a priori, au plus une activité importante se déroule à proximité d'une station de transport en commun, au plus elle va être utilisée, ce qui permet d'augmenter la fréquence de la desserte de la station et donc d'améliorer la qualité de la desserte.
Nous allons donc étudier le lien entre la [densité de la desserte en transports en commun] (stations de métropolitain par kilomètre carré, stations de bus par kilomètre carré) et la densité du bâti. Plus la première densité sera importante, plus l'on considère a priori la desserte comme bonne. Par ailleurs, plus la première est faible en comparaison à la seconde, plus a priori le coût de la desserte d'une unité d'activité humaine est faible, plus l'efficacité de la desserte est bonne.
[Gares et stations du réseau ferré d'Île-de-France (donnée généralisée) :](https://data.iledefrance-mobilites.fr/explore/dataset/emplacement-des-gares-idf-data-generalisee/table/)
Cette base de donnée permet de géolocaliser chaque gares et stations du réseau ferré, donc de géolocaliser l'ensemble des stations de métropolitain, de RER et de tramway présente à Paris et les affilier à des zones géographiques.
[Référentiel des arrêts : Arrêts :](https://data.iledefrance-mobilites.fr/explore/dataset/arrets/table/)
Cette base de données permet de géolocaliser chaque arrêt de bus, de métro, de tramway. On peut utiliser ArRName pour ne sélectionner qu’un arrêt par station et ArRGeopint pour les affilier à des zones géographiques.

A la frontière des transports en commun, on peut placer les réseaux de transports à usage individuel comme le taxi ou les stations de vélos en libre-service. On peut présumer qu'au plus la densité de bâti est importante, au plus ces solutions sont proposées. Mais qu'en est-il vraiment.
[Vélib](https://opendata.paris.fr/explore/dataset/velib-emplacement-des-stations/information/)
[Taxi](https://opendata.paris.fr/explore/dataset/bornes-dappel-taxi/information/)

Par ailleurs on peut se demander si les pouvoirs publics ont adapté ou non l'espace public à forte densité en donnant une plus grande part de la surface de stationnement aux moyens de transport individuels économes en place comme les motocyclettes et bicyclettes et en enfouissant davantage de parkings dédiés à l'automobile. On ne s’intéresse pas à la présence de zones piétonnes car le développement des super-blocks à Paris rend progressivement flou le caractère piétonnier ou non d’une rue, les rues à l’intérieur d’un [super-bloc] (https://www.youtube.com/watch?v=ZORzsubQA_M) étant de facto quasiment réservées aux piétons et aux vélos. 
[Stationnement sur voie publique - emprises](https://opendata.paris.fr/explore/dataset/stationnement-sur-voie-publique-emprises/map/?disjunctive.regpri&disjunctive.regpar&disjunctive.typsta&disjunctive.arrond&disjunctive.locsta&disjunctive.zoneres&disjunctive.parite&disjunctive.signhor&disjunctive.signvert&disjunctive.confsign&disjunctive.typemob&basemap=jawg.dark&location=16,48.85864,2.38511)
[Stationnement en ouvrage](https://opendata.paris.fr/explore/dataset/stationnement-en-ouvrage/map/?disjunctive.hauteur_max&disjunctive.gratuit&disjunctive.type_usagers&disjunctive.insee&disjunctive.tarif_pmr&disjunctive.type_ouvrage&disjunctive.info&disjunctive.id_entrees&disjunctive.arrdt&disjunctive.deleg&disjunctive.horaire_na&disjunctive.asc_surf&disjunctive.parc_amod&disjunctive.parc_relai&disjunctive.tarif_pr&disjunctive.tarif_res&disjunctive.zones_res&disjunctive.tf_pr_moto&basemap=jawg.dark&location=12,48.85489,2.39227)
La question vaut aussi pour la présence de piste cyclables.
[Linéaires d'aménagements cyclables :](https://opendata.paris.fr/explore/dataset/amenagements-cyclables/map/?disjunctive.arrondissement&disjunctive.position_amenagement&disjunctive.vitesse_maximale_autorisee&disjunctive.source&disjunctive.amenagement&location=16,48.85687,2.35247&basemap=jawg.streets)
A noter que dans cette base de données, une piste en double-sens est comptée deux fois. On peut calculer le ratio de distance totale de linéaires de pistes cyclables divisée par la distance totale de voies pour obtenir une approximation du développement des aménagements cyclables. 

Relativement à l'entretien des chaussées, a priori, au plus une activité est dense, au plus le nombre de mètres carré de chaussée nécessaire pour le desservir est faible, ce qui peut permettre d'en diminuer le coût d'entretien par unité d'activité humaine. 
Nous allons donc étudier le lien entre la [densité du bâti], surface de bâtiments utilisable par unité de surface au sol, et la [densité de chaussée], surface de chaussée par unité de surface au sol.
[Plan de Voirie – chaussée :](https://opendata.paris.fr/explore/dataset/plan-de-voirie-chaussees/map/?disjunctive.num_pave&basemap=jawg.dark&location=17,48.86156,2.40738)
Cette base de données contient la forme géométrique de toutes les chaussées. Cela permet pour chaque aire géographique de connaître la surface de chaussée utilisée pour la desserte. On utilise geo_shape qui donne la forme géométrique de chaque chaussée, ce qui nous permet d’allouer chaque partie d’une rue à tel ou tel quartier, arrondissement, telle ou telle zone géographique. On peut vouloir corriger cette donnée en y retranchant les surfaces de stationnement, lesquelles demandent un entretien a priori moindre. (On peut laisser le bitume de la zone de stationnement dans un état calamiteux sans perte d'utilité.)

Cependant, il nous semble important d'introduire une troisième notion de [densité de maillage routier], définie en nombre de kilomètres de voiries par kilomètre carré au sol. Cette variable donne une indication sur la structure de la desserte vicinale et le type d’urbanisme. En effet, on peut se demander si pour une même densité de bâti, il est préférable d'avoir une multitude de petites rues et de petits îlots urbains (=pâtés de maison), c'est-à-dire une grande densité de maillage routier, afin de minimiser la densité de chaussée, ou s'il est préférable d'avoir quelques larges rues et de grands îlots urbains. L'objectif est de trouver la structure de desserte et de bâti qui permet améliorer le ratio surface de chaussée/surface de bâti utilisable, pour chaque densité de bâti.
Croiser cette information avec les deux précédentes va peut-être permettre de trouver la structure de desserte et de bâti qui permet améliorer le ratio surface de chaussée/surface de bâti utilisable, pour chaque densité de bâti. Nous allons donc étudier le lien entre la [densité de maillage routier], la [densité du bâti] et la [densité de chaussée].
[Tronçons de voie](https://opendata.paris.fr/explore/dataset/troncon_voie/information/)
Cette base de données permet de connaître les longueurs de chaussée ainsi que leur géolocalisation, ce qui permet d'affilier les différentes longueurs de chaussées à des zones géographiques.




Cependant, il ne faut pas se borner à cette étude. En effet, l'accès à des espaces verts, de la verdure et la propreté sont des aspects importants de la qualité d'un lieu.

Ce faisant, nous allons étudier le lien entre la densité de bâti, la densité du maillage routier et le nombre de signalement d'anomalies dans les rues via l'application "Dans ma rue". Cela permet a priori d'obtenir un ordre d'idée de la perception de saleté des différents endroits.
[Dans ma rue- Anomalies signalées](https://opendata.paris.fr/explore/dataset/dans-ma-rue/map/?disjunctive.conseilquartier&disjunctive.intervenant&disjunctive.type&disjunctive.soustype&disjunctive.arrondissement&disjunctive.prefixe&disjunctive.code_postal&basemap=jawg.dark&location=12,48.85899,2.34742)
Chacun des signalements étant géolocalisé, on peut l'affilier à une zone géographique. Cependant, si l'arrondissement est directement disponible, il faut traduire l'adresse postale en coordonnées géographiques afin de positionner un signalement.

Egalement, nous allons étudier le lien entre la densité de bâti, du maillage routier et la présence d'arbres et d'espaces verts. Pour être plus précis, nous allons nous intéresser à la présence d'arbres dans les rues en fonction de la densité du maillage routier et donc au nombre d'arbres dans les rues au kilomètre carré.  Cette donnée permet de mesurer le degré d’artificialisation et donc mesurer une forme de qualité de vie. L’idée est de regarder alors le lien avec la densité du bâti et le type de maillage. (Est-ce que beaucoup de petites rues (probablement plus étroites) permettent de mettre plus ou moins d’arbre, et avec quel effet sur la densité du bâti ?)
Nous allons décompter les arbres présents en dehors des espaces verts afin de donner une approximation de la verdure perçue au quotidien, en dehors des grandes pauses. Nous allons également mesurer la part de la surface allouée aux espaces verts pour les différentes zones géographiques intra-muros.

[Arbres :](https://opendata.paris.fr/explore/dataset/les-arbres/information/?disjunctive.espece&disjunctive.typeemplacement&disjunctive.arrondissement&disjunctive.genre&disjunctive.libellefrancais&disjunctive.varieteoucultivar&disjunctive.stadedeveloppement&disjunctive.remarquable)
Cette base de données répertorie et géolocalise tous les arbres de Paris. Contrairement aux autres bases de données concernant les arbres de la ville de Paris, elle semble bien exhaustive. Notamment, c’est la seule à indiquer une quantité décente d’arbre sur les contre-allées du cour de Vincennes.
[PLU bioclimatique - Sous-secteur de déficit d'arbres et d'espaces végétalisés :](https://opendata.paris.fr/explore/dataset/plub_srv_daev/map/?basemap=jawg.dark&location=12,48.86167,2.33815)
Cette base répertorie les secteurs jugés en déficit d'arbres par le PLU bioclimatique.
[Ilots de fraîcheur - Espaces verts "frais" :](https://opendata.paris.fr/explore/dataset/ilots-de-fraicheur-espaces-verts-frais/map/?disjunctive.arrondissement&disjunctive.ouvert_24h&disjunctive.horaires_periode&disjunctive.statut_ouverture&disjunctive.canicule_ouverture&disjunctive.ouverture_estivale_nocturne&disjunctive.type&basemap=jawg.dark&location=12,48.83422,2.40086)
Cette base de données répertorie l'ensemble des espaces verts de Paris. Contrairement aux bases données de la ville de Paris prévue à cet effet, elle comptabilise bien le jardin du Luxembourg, le jardin des plantes.
[Espaces verts et assimilés :](https://opendata.paris.fr/explore/dataset/espaces_verts/map/?disjunctive.type_ev&disjunctive.categorie&disjunctive.adresse_codepostal&disjunctive.presence_cloture&refine.type_ev=Bois&basemap=jawg.dark&location=12,48.84484,2.38369)
Cette base de données ne répertorie pas le jardin des Tuileries, le jardin des plantes, le jardin du Luxembourg. Elle est donc inadaptée à l'études des espaces verts intra-muros. Par contre, elle a l'avantage de regrouper en quelques blocs les bois de Vincennes et de Boulogne, ce qui permet de corriger la surface des douzième et seizième arrondissements plus finement, car la base de données précédente n'inclut pas les bois l'importante voirie qui les compose.
A priori, on va utiliser ces deux bases de données pour essayer d'obtenir l'ensemble des surfaces qui sont incluses dans au moins une de ces deux bases de données pour obtenir l'ensemble exhaustifs des surfaces d'espaces verts.

Concernant notre méthodologie de mesure de la densité de bâti, si l'on souhaite faire le lien avec la densité du maillage routier, il faut calculer la densité de bâti en divisant par la surface non-allouée aux espaces verts, pour que par exemple le quartier du Père Lachaise ne voit pas sa densité de bâti artificiellement fortement diminuée par la présence du cimetière, ou pour que les douzième et seizième arrondissements ne voient par leur densité divisée par deux à cause des bois de Boulogne et de Vincennes. Pour l'étude de la densité, on souhaite comparer la typologie des zones construites.
Il faut aussi retrancher les voies d’eaux, comme la Seine.
[Plan de voirie - Voies d'eau :](https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-deau/map/?disjunctive.lib_level&disjunctive.lib_classe&disjunctive.num_pave&location=14,48.8768,2.36223&basemap=jawg.streets)
Il faut également retrancher les emprises ferroviaires.
[Plan-de-voirie : emprises ferroviaires :](https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-ferroviaires/map/?disjunctive.num_pave&location=12,48.83806,2.42832&basemap=jawg.streets)



#On peut également s'intéresser au lien entre le niveau de vie INSEE et densité même si ce n'est pas le cœur de notre étude.

#On peut aussi se demander si l'on peut relier la densité du bâti avec l'âge des bâtiments. Malheureusement, les données de la base de données de Paris semblent défectueuses. En effet, le Louvre y est daté de 2010, comme de nombreux bâtiments historiques, et des immeubles connus de certains membres du groupe sont également fortement rajeunis. Trouver des données de bonne qualité à ce sujet n'est pas chose aisée. Notre dernier espoir est la [BDNB de l'IGN :](https://bdnb.io/archives_data/bdnb_millesime_2025_07_a/)
Si cela fonctionne, on peut obtenir une carte explicite de l’âge des bâtiments dans le tout Paris, et croisée l'âge moyen des bâtiments d'une zone géographique avec sa densité de bâti ou de maillage routier.

Concernant les zones géographiques étudiées, on peut considérer :
[Arrondissements](https://opendata.paris.fr/explore/dataset/arrondissements/information/?disjunctive.l_ar&disjunctive.c_arinsee&disjunctive.c_ar)
/!\ Il faut autant que possible enlever les grands espaces verts ainsi que les surfaces de voies ferrées et fluviales qui faussent les calculs de densité du bâti.
[Quartiers administratifs](https://opendata.paris.fr/explore/dataset/quartier_paris/information/?disjunctive.c_ar)
[Les secteurs d'écoles élémentaires : ](https://opendata.paris.fr/explore/dataset/secteurs-scolaires-ecoles-elementaires/table/?disjunctive.annee_scol&disjunctive.id_projet&disjunctive.zone_commune)
[Stationnement sur voie publique – secteurs résidentiels :](https://opendata.paris.fr/explore/dataset/stationnement-sur-voie-publique-secteurs-residentiels/map/?basemap=jawg.dark&location=12,48.85889,2.34692)
[Plan de voirie - Pavés mosaïques du Plan de voirie de Paris :](https://opendata.paris.fr/explore/dataset/plan-de-voirie-paves-mosaiques-du-plan-de-voirie-de-paris/map/?disjunctive.numero_pave&refine.localisation=Paris&location=12,48.85889,2.34692&basemap=jawg.streets)
#En retranchant les espaces verts de grandes tailles, on obtient une bonne idée de la densité de bâti locale
[Iris]()
#Gabriel met la base de données que tu as utilisé s'il te plaît.
[Carroyage INSEE]()
#à ajouter
Ce maillage très fin permet de croiser les différentes données d’urbanisme avec les données socio-économiques.
[Ilots urbains](https://data.iledefrance.fr/explore/dataset/ilots-morphologiques-urbains-dile-de-france0/map/?location=16,48.87782,2.38472&basemap=jawg.sunny)
Utiliser ce maillage très fin permet de prendre en compte les surfaces de voies ferrées et d’espaces verts qui tendent à fausser les densités de bâtis sur les grandes zones géographiques.
[Plan de voire : emprises îlots privés :](https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-ilots-prives/map/?disjunctive.num_pave&basemap=jawg.dark&location=14,48.85094,2.37725)



Bases de données à fusionner pour les espaces verts
[plan de voirie espaces verts](https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-espaces-verts/map/?disjunctive.num_pave&location=13,48.85613,2.33717&basemap=jawg.streets)
[espaces verts](https://opendata.paris.fr/explore/dataset/espaces_verts/map/?disjunctive.type_ev&disjunctive.categorie&disjunctive.adresse_codepostal&disjunctive.presence_cloture&basemap=jawg.dark&location=12,48.83874,2.33356)
[ilots de fraicheur espaces verts](https://opendata.paris.fr/explore/dataset/ilots-de-fraicheur-espaces-verts-frais/export/?disjunctive.arrondissement&disjunctive.ouvert_24h&disjunctive.horaires_periode&disjunctive.statut_ouverture&disjunctive.canicule_ouverture&disjunctive.ouverture_estivale_nocturne&disjunctive.type&basemap=jawg.dark&location=13,48.82235,2.40532)


[Plan de voirie - Voies d'eau :](https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-deau/map/?disjunctive.lib_level&disjunctive.lib_classe&disjunctive.num_pave&location=14,48.8768,2.36223&basemap=jawg.streets)
Il faut également retrancher les emprises ferroviaires.
[Plan-de-voirie : emprises ferroviaires :](https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-ferroviaires/map/?disjunctive.num_pave&location=12,48.83806,2.42832&basemap=jawg.streets)





































POLLUTION : on le garde en stock, mais il faut le formaliser.

Le but est d'avoir une ville efficace pour les habitants (bien-être, accès aux transports, espace vert, ...) tout en minimisant les coûts d'entretien de chaussées.
Pour voir l'efficacité de la voirie dans Paris on peut étudier la relation entre la voirie et le bâti croisée avec : 

- [ ] le niveau de vie (INSEE)

- [ ] les transports publiques [RATP]()

- [ ] Les secteurs étudié sont-ils salles déchets ([Dans ma rue- Anomalies signalées](https://opendata.paris.fr/explore/dataset/dans-ma-rue/map/?disjunctive.conseilquartier&disjunctive.intervenant&disjunctive.type&disjunctive.soustype&disjunctive.arrondissement&disjunctive.prefixe&disjunctive.code_postal&basemap=jawg.dark&location=12,48.85899,2.34742))

- [ ] bien être des habitant quantifié avec les espaces verts ou les arbres --> ([Arbres](https://opendata.paris.fr/explore/dataset/les-arbres/information/?disjunctive.espece&disjunctive.typeemplacement&disjunctive.arrondissement&disjunctive.genre&disjunctive.libellefrancais&disjunctive.varieteoucultivar&disjunctive.stadedeveloppement&disjunctive.remarquable) et [espaces verts](https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-espaces-verts/map/?disjunctive.num_pave&location=15,48.85905,2.40146&basemap=jawg.streets))

- [ ] le stationnement se trouve souvent sur les voies donc on peut étudier le cas avec la voirie moins les places de parking publiques ([Stationnement sur voie publique - emprises](https://opendata.paris.fr/explore/dataset/stationnement-sur-voie-publique-emprises/map/?disjunctive.regpri&disjunctive.regpar&disjunctive.typsta&disjunctive.arrond&disjunctive.locsta&disjunctive.zoneres&disjunctive.parite&disjunctive.signhor&disjunctive.signvert&disjunctive.confsign&disjunctive.typemob&basemap=jawg.dark&location=16,48.85864,2.38511))

- [ ] enlever les espaces verts pour étudier par arrondissement ()

[Données du bâti, utile pour obtenir une expression de la densité du bâti]
[Emprise bâti et non-bâti :](https://opendata.paris.fr/explore/dataset/emprise-batie-et-non-batie/map/?location=17,48.86254,2.40412&basemap=jawg.streets)

[Espaces non-bâtis](https://opendata.paris.fr/pages/catalogue/?disjunctive.theme&disjunctive.publisher&sort=modified&refine.theme=Urbanisme%20et%20Logements)

[Volumes-bâtis :](https://opendata.paris.fr/explore/dataset/volumesbatisparis/map/?location=17,48.84008,2.39706&basemap=jawg.streets)

Colonnes à verre : [point de collecte des verres](https://opendata.paris.fr/explore/dataset/dechets-menagers-points-dapport-volontaire-colonnes-a-verre/information/)

[Marchés découverts](https://opendata.paris.fr/explore/dataset/marches-decouverts/information/?disjunctive.produit&disjunctive.ardt&disjunctive.jours_tenue&disjunctive.gestionnaire)

Voirie et transport
Stationnement :
Stationnement sur voie publique - emprises 
Cette base données décrit l’ensemble des places de stationnement et leur emprise. Chaque stationnement est décrit par :
Son régime prioritaire (Quel type de véhicule est stationné, avec quel mode de paiement):
Nom : regpri
Type : texte
Ex : Payant mixte/2 roues/livraison/payant rotatif/(GIG/GIC)/location/gratuit/électrique/autocar
Son régime particulier (similaire mais plus détaillé) :
Nom : regpar
Type : texte
Ex : vélos/motos payant rotatif
Arrondissement :
Nom : arrond
Type : int
Nombre places calculées (nombre de places calculées sur la zone considérée.) :
Nom : placal
Type : int
Nombre places réelles (nombre de places réelles sur la zone considérée:
Nom : plarel
Type : int
Zones résidentielles (à Paris, une zone résidentielle correspond à l’avantage suivant : dans le cas où une personne habite dans cette zone, cette personne peut stationner sa voiture  :
Nom : zoneres
Type : texte
Exemple : 13P

Des promesses de limitations … : [PLU bioclimatique - Limitations des parcs de stationnement](https://opendata.paris.fr/explore/dataset/plub_limstat/map/?basemap=jawg.dark&location=12,48.86072,2.33596)

[arrêt de bus](https://opendata.paris.fr/explore/dataset/plan-de-voirie-mobiliers-urbains-abris-voyageurs-points-darrets-bus/information/?disjunctive.lib_level&disjunctive.num_pave&location=18,48.85808,2.40129&basemap=jawg.streets)

[toilettes publiques](https://opendata.paris.fr/explore/dataset/plan-de-voirie-mobiliers-urbains-kiosques-toilettes-publiques-panneaux-publicita/information/?disjunctive.lib_level&disjunctive.num_pave)

[Voies privées fermées](https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-privees-fermees/map/?disjunctive.num_pave&location=16,48.84747,2.40013&basemap=jawg.streets)

[Voies en escalier](https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-en-escalier/map/?disjunctive.num_pave&location=18,48.8602,2.40385&basemap=jawg.streets)

[Liaisons piétonnières et al.](https://opendata.paris.fr/explore/dataset/plub_lpcppc/map/?basemap=jawg.dark&location=16,48.85975,2.37202)(à traiter/filtrer) : 

[Aire mixte véhicule piéton](https://opendata.paris.fr/explore/dataset/plan-de-voirie-aires-mixtes-vehicules-et-pietons/information/?disjunctive.num_pave)

[Aire piétonne](https://opendata.paris.fr/explore/dataset/aires-pietonnes/map/?basemap=jawg.dark&location=15,48.85922,2.40317)

[Zone de rencontre](https://opendata.paris.fr/explore/dataset/zones-de-rencontre/information/?disjunctive.first_arrdt)

Voies et aménagements piétonniers (espace public hors espaces vert et service public) (données pas totalement complètes encore sniff) https://opendata.paris.fr/explore/dataset/plub_voie/map/?basemap=jawg.dark&location=16,48.85772,2.36687
Permet d’obtenir la surface totale d’espace public :https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-ilots-prives/map/?disjunctive.num_pave&basemap=jawg.dark&location=18,48.85918,2.4091
[Espaces verts (autres données)](https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-espaces-verts/map/?disjunctive.num_pave&location=15,48.85905,2.40146&basemap=jawg.streets)
[voies privées](https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-privees-fermees/map/?disjunctive.num_pave&location=16,48.85502,2.40283&basemap=jawg.streets)
Qualité douteuse, mais sait-on jamais :
[pistes cyclabes et couloires de bus](https://opendata.paris.fr/explore/dataset/plan-de-voirie-pistes-cyclables-et-couloirs-de-bus/information/?disjunctive.lib_classe&disjunctive.num_pave)
[Accès métro et parking](https://opendata.paris.fr/explore/dataset/plan-de-voirie-acces-pietons-metro-et-parkings/map/?disjunctive.lib_level&disjunctive.num_pave&location=18,48.85875,2.34827&basemap=jawg.streets)

[Fontaines](https://opendata.paris.fr/explore/dataset/fontaines-a-boire/information/?disjunctive.type_objet&disjunctive.modele&disjunctive.commune&disjunctive.dispo)
[Chiottes](https://opendata.paris.fr/explore/dataset/sanisettesparis/map/?disjunctive.type&disjunctive.arrondissement&disjunctive.horaire&disjunctive.acces_pmr&disjunctive.relais_bebe&disjunctive.statut&basemap=jawg.dark&location=12,48.86007,2.34785)







https://github.com/AXLMRIN/presentations-ensae-tds/tree/main
Fiabel donnée
Github python
Supra communal 200 x 200
Densité du bati, de la voirie (surface, densité du maillage), des pistes cyclables, station de taxi, toilettes publique…, des stationnements/zone piétonne de rencontre, du maillage en transport en commun (par hab, par revenus, par…), arrdt, dans ma rue, cours oasis (comparer écart à la moyenne de l’arrdt), point d’apports volontaires de déchets=, vote (par bureau de vote : faire la moyenne) 
BBD DE LA VILLE DE PARIS A CROISER

URBANISME ET LOGEMENT/ 
https://opendata.paris.fr/pages/catalogue/?sort=modified&refine.theme=Urbanisme%20et%20Logements&disjunctive.theme&disjunctive.publisher







TRAITES :
DENSITE DU BATiS (stat intéressante)
Linéaire des voies => calcul de densité du maillage ?
Ce qui est :
Volumes batis
Espaces non-batis
Ce qui pourrait être : 
Emprises constructible maximale
Plafonds des hauteurs
Hauteurs maximal constructible
Volumétrie maximale

stationnment, stationnement en ouvrage
Piste cyclable

Station de taxi
VOIRIES
Aire pietonne
Zone de rencontre
Aire mixte véhicule pidéton
Plan de voiries point de nivellement
Emprise ilot privé (complément de voirie)
Plan de voirie chaussée (densité de chaussé par unité de surface, on peut la calculer)
Limitations des parcs de stationnments
Liaisons piétonnières
Voies et aménagements piétonniers
Secteur de déficit d’arbres

EXCLU
Technbiquememnt das admin publique y al a dette ms bon
TRUCS INUTILES MAIS MARRANT dans la rubrique environement
https://opendata.paris.fr/explore/dataset/dechets-menagers-points-dapport-volontaire-stations-trilib/table/
Respirons mieux dans le 20ème : bcp de données, qu’en faire ?
Points d’apport volontaires de déchets (dépend trop de la politique ?)

CITOYENNETE / CULTURE COMMERCES / EUQIPEMENT SERVICE SOCIAL / ENVIRONNEMENT / URBANISME LOGEMENT
CITOYENNETE
https://opendata.paris.fr/pages/catalogue/?disjunctive.theme&disjunctive.publisher&sort=modified&refine.theme=Citoyennet%C3%A9
Croisement des votes aux votations
Trotinettes en libre service
Stationnement suv
Végétalisation rue piétonnes)
Résultats aux municipales : (bureaux de vote par bureau de vote) : comment créer des arrondissements homogènes politiquement (sur les sujets locaux) en regroupant les bureaux de votes ? : Spectral clustering 
CULTURE :
Plaques commémoratives
Position des bibliothèques (distance à la bibliothèque la plus proche) (c’est la pénurie dans l’ouest)
https://opendata.paris.fr/pages/catalogue/?sort=modified&refine.theme=Culture&disjunctive.theme&disjunctive.publisher
EQUIPEMENT SERVICE ? SOCIAL :
https://opendata.paris.fr/pages/catalogue/?sort=modified&refine.theme=Equipements,%20Services,%20Social&disjunctive.theme&disjunctive.publisher
(pénurie ds l’ouest)
Réseau parisien d’inclusion numérique (bcp de donnéees)
Seniors à paris (activités seniors)
Toilettes publiques + fontaines à boire
Dans ma rue (saleté ) (à croiser avec la densité de population/la pauvreté/la densité du bati/des rues)

Secteurs scolaires
Cours oasis
Travaux engagés sur les équipements publics

Centres d’hébergements
Centre d’action sociale
Nbre de bénéficiares de l’actions sociale
Sans abrisme : place d’hébergement

En cas de demande de réutilisation
GAUTIER
Glenn
glenn.gautier@ensae.fr
Etude du lien entre la densité du bâti et d’autres paramètres
Madame, monsieur,
Etudiants à l’ENSAE (Ecole Nationale de Statistique et d’Administration Economique, école du groupement de l’Institut Polytechnique de Paris), dans le cadre d’un projet de groupe de la matière Python DS (= science des données = datascience), nous aimerions pouvoir étudier le lien entre la densité du bâti (volume de bâtiment par unité de surface, part de la surface occupée par le bâti) et d’autres données d’urbanisme, notamment la densité du maillage routier (nombre de kilomètres de rue par kilomètre carré, surface des chaussées par kilomètre carré, part du kilométrage de rue dotée d’une piste cyclable, présence de zone piétonne, de zone 30), mais aussi l’accès aux espaces verts, la présence d’arbres dans les rues, la propreté des rues ou du moins son sentiment (données de dans ma rue), la densité de population (si possible). Nous ne sommes pas sûr d’utiliser toutes les données que nous demandons (il faut réussir à les exploiter), mais nous vous transmettrons les résultats de notre travail.
Ce qui motive notre étude est la constatation suivante. La faible densité du bâti en zone pavillonnaire est associée à un kilométrage de voirie par unité de volume bâti très important (ce qui est coûteux en ressources), une distance aux services plus importantes, et une prépondérance plus forte de la voiture. De là, dans un premier temps, plus la densité du bâti augmente, plus le kilométrage de voirie par unité de volume bâti diminue, plus le vélo se développe, etc, etc. Maintenant, Paris est un cas d’extrême densité du bâti et d’extrême densité de population en France. On peut se demander si dans le cas d’une forte densité, la règle précédente s’applique, mais aussi quelle est la densité du maillage routier optimale pour maximiser le volume bâti par kilomètre carré, mais aussi quel effet cela peut avoir sur la présence de piste cyclable ou de zone piétonne ou d’espace vert ? (En français : faut-il faire beaucoup de petites rues, ou bien de grandes parcelles et des rues très larges ?) Le but de l’étude est de savoir ce qu’il en est.
En vous remerciant d’avance de nous donner accès aux données de la ville de Paris dans l’objectif de mener notre étude.
    Glenn GAUTIER


