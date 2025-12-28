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


[Données du bâti, utile pour obtenir une expression de la densité du bâti]
[Emprise bâti et non-bâti :](https://opendata.paris.fr/explore/dataset/emprise-batie-et-non-batie/map/?location=17,48.86254,2.40412&basemap=jawg.streets)

[Espaces non-bâtis](https://opendata.paris.fr/pages/catalogue/?disjunctive.theme&disjunctive.publisher&sort=modified&refine.theme=Urbanisme%20et%20Logements)

[Volumes-bâtis :](https://opendata.paris.fr/explore/dataset/volumesbatisparis/map/?location=17,48.84008,2.39706&basemap=jawg.streets)

[Hauteur maximale constructible :](https://opendata.paris.fr/explore/dataset/plub_hauteur/map/?basemap=jawg.dark&location=13,48.85257,2.33288)

Données environnementales (présences d’arbres, d’espaces verts)

à l'air meilleur que espace vert, car plus précis (ex, ne prend pas les rues) [Ilots de fraîcheur - Espaces verts "frais"](https://opendata.paris.fr/explore/dataset/ilots-de-fraicheur-espaces-verts-frais/map/?disjunctive.arrondissement&disjunctive.ouvert_24h&disjunctive.horaires_periode&disjunctive.statut_ouverture&disjunctive.canicule_ouverture&disjunctive.ouverture_estivale_nocturne&disjunctive.type&basemap=jawg.dark&location=12,48.85903,2.34748)

[Les arbres d'alignement (plantés hors peuplement forestier)](https://opendata.paris.fr/explore/dataset/arbres-plantes-hors-peuplement-forestier/map/?location=16,48.83322,2.34862&basemap=jawg.streets)

[Espaces verts et assimilés](https://opendata.paris.fr/explore/dataset/espaces_verts/map/?disjunctive.type_ev&disjunctive.categorie&disjunctive.adresse_codepostal&disjunctive.presence_cloture&basemap=jawg.dark&location=11,48.83239,2.34692)

plus simple à utiliser, on a juste à compter le nb d'arbre --> [Arbres](https://opendata.paris.fr/explore/dataset/les-arbres/information/?disjunctive.espece&disjunctive.typeemplacement&disjunctive.arrondissement&disjunctive.genre&disjunctive.libellefrancais&disjunctive.varieteoucultivar&disjunctive.stadedeveloppement&disjunctive.remarquable)

[PLU bioclimatique - Alignements d'arbres et compositions arborées protégées](https://opendata.paris.fr/explore/dataset/plub_arbralign/map/?basemap=jawg.dark&location=15,48.85879,2.33145)

Colonnes à verre : [point de collecte des verres](https://opendata.paris.fr/explore/dataset/dechets-menagers-points-dapport-volontaire-colonnes-a-verre/information/)

Secteurs de déficit d’arbres : [déficit d'arbres et d'espaces végétalisés](https://opendata.paris.fr/explore/dataset/plub_srv_daev/map/?basemap=jawg.dark&location=12,48.86167,2.33815)

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

[Stationnement sur voie publique - emprises](https://opendata.paris.fr/explore/dataset/stationnement-sur-voie-publique-emprises/map/?disjunctive.regpri&disjunctive.regpar&disjunctive.typsta&disjunctive.arrond&disjunctive.locsta&disjunctive.zoneres&disjunctive.parite&disjunctive.signhor&disjunctive.signvert&disjunctive.confsign&disjunctive.typemob&basemap=jawg.dark&location=16,48.85864,2.38511)

[Stationnement en ouvrage](https://opendata.paris.fr/explore/dataset/stationnement-en-ouvrage/map/?disjunctive.hauteur_max&disjunctive.gratuit&disjunctive.type_usagers&disjunctive.insee&disjunctive.tarif_pmr&disjunctive.type_ouvrage&disjunctive.info&disjunctive.id_entrees&disjunctive.arrdt&disjunctive.deleg&disjunctive.horaire_na&disjunctive.asc_surf&disjunctive.parc_amod&disjunctive.parc_relai&disjunctive.tarif_pr&disjunctive.tarif_res&disjunctive.zones_res&disjunctive.tf_pr_moto&basemap=jawg.dark&location=12,48.85489,2.39227)

Des promesses de limitations … : [PLU bioclimatique - Limitations des parcs de stationnement](https://opendata.paris.fr/explore/dataset/plub_limstat/map/?basemap=jawg.dark&location=12,48.86072,2.33596)

[Vélib](https://opendata.paris.fr/explore/dataset/velib-emplacement-des-stations/information/)

[Taxi](https://opendata.paris.fr/explore/dataset/bornes-dappel-taxi/information/)
(tenter d’avoir accès aux arrêts de bus ???) 

[arrêt de bus](https://opendata.paris.fr/explore/dataset/plan-de-voirie-mobiliers-urbains-abris-voyageurs-points-darrets-bus/information/?disjunctive.lib_level&disjunctive.num_pave&location=18,48.85808,2.40129&basemap=jawg.streets)

[Plan de voirie - Pavés mosaïques du Plan de voirie de Paris](https://opendata.paris.fr/explore/dataset/plan-de-voirie-paves-mosaiques-du-plan-de-voirie-de-paris/information/?disjunctive.numero_pave)

[toilettes publiques](https://opendata.paris.fr/explore/dataset/plan-de-voirie-mobiliers-urbains-kiosques-toilettes-publiques-panneaux-publicita/information/?disjunctive.lib_level&disjunctive.num_pave)

[Linéaire de  voie](https://opendata.paris.fr/explore/dataset/voie/map/?location=17,48.85704,2.37839&basemap=jawg.streets)

[Tronçons de voie](https://opendata.paris.fr/explore/dataset/troncon_voie/information/)

Très importants : [donne la surface des chaussées](https://opendata.paris.fr/explore/dataset/plan-de-voirie-chaussees/map/?disjunctive.num_pave&basemap=jawg.dark&location=17,48.86156,2.40738)

[Voies privées fermées](https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-privees-fermees/map/?disjunctive.num_pave&location=16,48.84747,2.40013&basemap=jawg.streets)

[Voies en escalier](https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-en-escalier/map/?disjunctive.num_pave&location=18,48.8602,2.40385&basemap=jawg.streets)

[Liaisons piétonnières et al.](https://opendata.paris.fr/explore/dataset/plub_lpcppc/map/?basemap=jawg.dark&location=16,48.85975,2.37202)(à traiter/filtrer) : 

[Aire mixte véhicule piéton](https://opendata.paris.fr/explore/dataset/plan-de-voirie-aires-mixtes-vehicules-et-pietons/information/?disjunctive.num_pave)

[Aire piétonne](https://opendata.paris.fr/explore/dataset/aires-pietonnes/map/?basemap=jawg.dark&location=15,48.85922,2.40317)

[Zone de rencontre](https://opendata.paris.fr/explore/dataset/zones-de-rencontre/information/?disjunctive.first_arrdt)

[Aménagements cyclables](https://opendata.paris.fr/explore/dataset/amenagements-cyclables/map/?disjunctive.arrondissement&disjunctive.position_amenagement&disjunctive.vitesse_maximale_autorisee&disjunctive.source&disjunctive.amenagement&location=12,48.85898,2.34772&basemap=jawg.streets)

Voies et aménagemtns piétonniers (espace public hors espaces vert et service public) (données pas totalement complètes encore sniff) https://opendata.paris.fr/explore/dataset/plub_voie/map/?basemap=jawg.dark&location=16,48.85772,2.36687
Permet d’obtenir la surface totale d’espace public :https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-ilots-prives/map/?disjunctive.num_pave&basemap=jawg.dark&location=18,48.85918,2.4091
[Espaces verts (autres données)](https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-espaces-verts/map/?disjunctive.num_pave&location=15,48.85905,2.40146&basemap=jawg.streets)
[voies privées](https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-privees-fermees/map/?disjunctive.num_pave&location=16,48.85502,2.40283&basemap=jawg.streets)
Qualité douteuse, mais sait-on jamais :
[pistes cyclabes et couloires de bus](https://opendata.paris.fr/explore/dataset/plan-de-voirie-pistes-cyclables-et-couloirs-de-bus/information/?disjunctive.lib_classe&disjunctive.num_pave)
[Accès métro et parking](https://opendata.paris.fr/explore/dataset/plan-de-voirie-acces-pietons-metro-et-parkings/map/?disjunctive.lib_level&disjunctive.num_pave&location=18,48.85875,2.34827&basemap=jawg.streets)

SECTEURS
[école élémentaire](https://opendata.paris.fr/explore/dataset/etablissements-scolaires-ecoles-elementaires/information/?disjunctive.arr_libelle&disjunctive.annee_scol&disjunctive.id_projet&disjunctive.arr_insee&disjunctive.type_etabl)
[Quartiers administratifs](https://opendata.paris.fr/explore/dataset/quartier_paris/information/?disjunctive.c_ar)
[Arrondissements](https://opendata.paris.fr/explore/dataset/arrondissements/information/?disjunctive.l_ar&disjunctive.c_arinsee&disjunctive.c_ar)
[Secteurs des bure"<éaux de vote 2025](https://opendata.paris.fr/explore/dataset/secteurs-des-bureaux-de-vote-2025/map/?location=12,48.85889,2.35638&basemap=jawg.streets)
PROPRETE
--> indice de propreté [Dans ma rue- Anomalies signalées](https://opendata.paris.fr/explore/dataset/dans-ma-rue/map/?disjunctive.conseilquartier&disjunctive.intervenant&disjunctive.type&disjunctive.soustype&disjunctive.arrondissement&disjunctive.prefixe&disjunctive.code_postal&basemap=jawg.dark&location=12,48.85899,2.34742)


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
SECTEUR ADMIN
Quartiers arrdt bureau de votes (on peut regrouper par)




Densité du bâti : âge des batiments
Carte explicite de l’age
Carte explicite de la densité

Le but est d'avoir une ville efficace pour les habitants (bien être, accès aux transports, espace vert, ...) tout en minimisant les coûts d'entretient de chaussées.
Pour voir l'efficacité de la voirie dans Paris on peut étudier la relation entre la voirie et le bâti croisée avec : 

- [ ] le niveau de vie (INSEE)

- [ ] les transports publiques [RATP]()

- [ ] Les secteurs étudié sont-ils salles déchets ([Dans ma rue- Anomalies signalées](https://opendata.paris.fr/explore/dataset/dans-ma-rue/map/?disjunctive.conseilquartier&disjunctive.intervenant&disjunctive.type&disjunctive.soustype&disjunctive.arrondissement&disjunctive.prefixe&disjunctive.code_postal&basemap=jawg.dark&location=12,48.85899,2.34742))

- [ ] bien être des habitant quantifié avec les espaces verts ou les arbres --> ([Arbres](https://opendata.paris.fr/explore/dataset/les-arbres/information/?disjunctive.espece&disjunctive.typeemplacement&disjunctive.arrondissement&disjunctive.genre&disjunctive.libellefrancais&disjunctive.varieteoucultivar&disjunctive.stadedeveloppement&disjunctive.remarquable) et [espaces verts](https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-espaces-verts/map/?disjunctive.num_pave&location=15,48.85905,2.40146&basemap=jawg.streets))

- [ ] le stationnement se trouve souvent sur les voies donc on peut étudier le cas avec la voirie moins les places de parking publiques ([Stationnement sur voie publique - emprises](https://opendata.paris.fr/explore/dataset/stationnement-sur-voie-publique-emprises/map/?disjunctive.regpri&disjunctive.regpar&disjunctive.typsta&disjunctive.arrond&disjunctive.locsta&disjunctive.zoneres&disjunctive.parite&disjunctive.signhor&disjunctive.signvert&disjunctive.confsign&disjunctive.typemob&basemap=jawg.dark&location=16,48.85864,2.38511))

- [ ] enlever les espaces verts pour étudier par arrondissement ()
