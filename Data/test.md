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


Emprise bâti et non-bâti :
https://opendata.paris.fr/explore/dataset/emprise-batie-et-non-batie/map/?location=17,48.86254,2.40412&basemap=jawg.streets
Espaces non-batis : 
https://opendata.paris.fr/pages/catalogue/?disjunctive.theme&disjunctive.publisher&sort=modified&refine.theme=Urbanisme%20et%20Logements
Volumes_bati : https://opendata.paris.fr/explore/dataset/volumesbatisparis/map/?location=17,48.84008,2.39706&basemap=jawg.streets
Hauteur maximale constructible : https://opendata.paris.fr/explore/dataset/plub_hauteur/map/?basemap=jawg.dark&location=13,48.85257,2.33288
Données environnementales (présences d’arbres, d’espaces verts)
https://opendata.paris.fr/explore/dataset/ilots-de-fraicheur-espaces-verts-frais/map/?disjunctive.arrondissement&disjunctive.ouvert_24h&disjunctive.horaires_periode&disjunctive.statut_ouverture&disjunctive.canicule_ouverture&disjunctive.ouverture_estivale_nocturne&disjunctive.type&basemap=jawg.dark&location=12,48.85903,2.34748
https://opendata.paris.fr/explore/dataset/arbres-plantes-hors-peuplement-forestier/map/?location=16,48.83322,2.34862&basemap=jawg.streets
https://opendata.paris.fr/explore/dataset/espaces_verts/map/?disjunctive.type_ev&disjunctive.categorie&disjunctive.adresse_codepostal&disjunctive.presence_cloture&basemap=jawg.dark&location=11,48.83239,2.34692
https://opendata.paris.fr/explore/dataset/les-arbres/information/?disjunctive.espece&disjunctive.typeemplacement&disjunctive.arrondissement&disjunctive.genre&disjunctive.libellefrancais&disjunctive.varieteoucultivar&disjunctive.stadedeveloppement&disjunctive.remarquable
https://opendata.paris.fr/explore/dataset/plub_arbralign/map/?basemap=jawg.dark&location=15,48.85879,2.33145

Colonnes à verre : https://opendata.paris.fr/explore/dataset/dechets-menagers-points-dapport-volontaire-colonnes-a-verre/information/
Secteurs de déficit d’arbres : https://opendata.paris.fr/explore/dataset/plub_srv_daev/map/?basemap=jawg.dark&location=12,48.86167,2.33815
Marchés découverts
https://opendata.paris.fr/explore/dataset/marches-decouverts/information/?disjunctive.produit&disjunctive.ardt&disjunctive.jours_tenue&disjunctive.gestionnaire
Voirie et transport
Stationnement :
https://opendata.paris.fr/explore/dataset/stationnement-sur-voie-publique-stationnement-interdit/map/?disjunctive.regpar&disjunctive.regpri&disjunctive.arrond&disjunctive.signhor&disjunctive.signvert&disjunctive.confsign&disjunctive.parite&disjunctive.zoneres&disjunctive.tar&basemap=jawg.dark&location=16,48.86776,2.40268
https://opendata.paris.fr/explore/dataset/stationnement-sur-voie-publique-emprises/map/?disjunctive.regpri&disjunctive.regpar&disjunctive.typsta&disjunctive.arrond&disjunctive.locsta&disjunctive.zoneres&disjunctive.parite&disjunctive.signhor&disjunctive.signvert&disjunctive.confsign&disjunctive.typemob&basemap=jawg.dark&location=16,48.85864,2.38511
https://opendata.paris.fr/explore/dataset/stationnement-en-ouvrage/map/?disjunctive.hauteur_max&disjunctive.gratuit&disjunctive.type_usagers&disjunctive.insee&disjunctive.tarif_pmr&disjunctive.type_ouvrage&disjunctive.info&disjunctive.id_entrees&disjunctive.arrdt&disjunctive.deleg&disjunctive.horaire_na&disjunctive.asc_surf&disjunctive.parc_amod&disjunctive.parc_relai&disjunctive.tarif_pr&disjunctive.tarif_res&disjunctive.zones_res&disjunctive.tf_pr_moto&basemap=jawg.dark&location=12,48.85489,2.39227

Des promesses de limitations … : https://opendata.paris.fr/explore/dataset/plub_limstat/map/?basemap=jawg.dark&location=12,48.86072,2.33596

Vélib https://opendata.paris.fr/explore/dataset/velib-emplacement-des-stations/information/
Taxi :https://opendata.paris.fr/explore/dataset/bornes-dappel-taxi/information/
(tenter d’avoir accès aux arrêts de bus ???) :https://opendata.paris.fr/explore/dataset/plan-de-voirie-mobiliers-urbains-abris-voyageurs-points-darrets-bus/information/?disjunctive.lib_level&disjunctive.num_pave&location=18,48.85808,2.40129&basemap=jawg.streets
https://opendata.paris.fr/explore/dataset/plan-de-voirie-paves-mosaiques-du-plan-de-voirie-de-paris/information/?disjunctive.numero_pave
https://opendata.paris.fr/explore/dataset/plan-de-voirie-mobiliers-urbains-kiosques-toilettes-publiques-panneaux-publicita/information/?disjunctive.lib_level&disjunctive.num_pave
Linéaire de  voie : https://opendata.paris.fr/explore/dataset/voie/map/?location=17,48.85704,2.37839&basemap=jawg.streets
Tronçons de voie : https://opendata.paris.fr/explore/dataset/troncon_voie/information/
Très importants : donne la surface des chaussées : https://opendata.paris.fr/explore/dataset/plan-de-voirie-chaussees/map/?disjunctive.num_pave&basemap=jawg.dark&location=17,48.86156,2.40738
Voies privées fermées : https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-privees-fermees/map/?disjunctive.num_pave&location=16,48.84747,2.40013&basemap=jawg.streets
Voies en escalier : https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-en-escalier/map/?disjunctive.num_pave&location=18,48.8602,2.40385&basemap=jawg.streets
Liaisons piétonnières et al.(à traiter/filtrer) : https://opendata.paris.fr/explore/dataset/plub_lpcppc/map/?basemap=jawg.dark&location=16,48.85975,2.37202
Aire mixte véhicule piéton : https://opendata.paris.fr/explore/dataset/plan-de-voirie-aires-mixtes-vehicules-et-pietons/information/?disjunctive.num_pave
Aire piétonne :https://opendata.paris.fr/explore/dataset/aires-pietonnes/map/?basemap=jawg.dark&location=15,48.85922,2.40317
Zone de rencontre https://opendata.paris.fr/explore/dataset/zones-de-rencontre/information/?disjunctive.first_arrdt
Aménagements cyclables : https://opendata.paris.fr/explore/dataset/amenagements-cyclables/map/?disjunctive.arrondissement&disjunctive.position_amenagement&disjunctive.vitesse_maximale_autorisee&disjunctive.source&disjunctive.amenagement&location=12,48.85898,2.34772&basemap=jawg.streets
Voies et aménagemtns piétonniers (espace public hors espaces vert et service public) (données pas totalement complètes encore sniff) https://opendata.paris.fr/explore/dataset/plub_voie/map/?basemap=jawg.dark&location=16,48.85772,2.36687
Permet d’obtenir la surface totale d’espace public :https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-ilots-prives/map/?disjunctive.num_pave&basemap=jawg.dark&location=18,48.85918,2.4091
Espaces verts (autres données) : https://opendata.paris.fr/explore/dataset/plan-de-voirie-emprises-espaces-verts/map/?disjunctive.num_pave&location=15,48.85905,2.40146&basemap=jawg.streets
https://opendata.paris.fr/explore/dataset/plan-de-voirie-voies-privees-fermees/map/?disjunctive.num_pave&location=16,48.85502,2.40283&basemap=jawg.streets
Qualité douteuse, mais sait-on jamais :https://opendata.paris.fr/explore/dataset/plan-de-voirie-pistes-cyclables-et-couloirs-de-bus/information/?disjunctive.lib_classe&disjunctive.num_pave
Accès métro et parking : https://opendata.paris.fr/explore/dataset/plan-de-voirie-acces-pietons-metro-et-parkings/map/?disjunctive.lib_level&disjunctive.num_pave&location=18,48.85875,2.34827&basemap=jawg.streets

SECTEURS
https://opendata.paris.fr/explore/dataset/etablissements-scolaires-ecoles-elementaires/information/?disjunctive.arr_libelle&disjunctive.annee_scol&disjunctive.id_projet&disjunctive.arr_insee&disjunctive.type_etabl
https://opendata.paris.fr/explore/dataset/quartier_paris/information/?disjunctive.c_ar
https://opendata.paris.fr/explore/dataset/arrondissements/information/?disjunctive.l_ar&disjunctive.c_arinsee&disjunctive.c_ar
https://opendata.paris.fr/explore/dataset/secteurs-des-bureaux-de-vote-2025/map/?location=12,48.85889,2.35638&basemap=jawg.streets
PROPRETE
Dans ma rue : https://opendata.paris.fr/explore/dataset/dans-ma-rue/map/?disjunctive.conseilquartier&disjunctive.intervenant&disjunctive.type&disjunctive.soustype&disjunctive.arrondissement&disjunctive.prefixe&disjunctive.code_postal&basemap=jawg.dark&location=12,48.85899,2.34742
Fontaines : https://opendata.paris.fr/explore/dataset/fontaines-a-boire/information/?disjunctive.type_objet&disjunctive.modele&disjunctive.commune&disjunctive.dispo
Chiottes : https://opendata.paris.fr/explore/dataset/sanisettesparis/map/?disjunctive.type&disjunctive.arrondissement&disjunctive.horaire&disjunctive.acces_pmr&disjunctive.relais_bebe&disjunctive.statut&basemap=jawg.dark&location=12,48.86007,2.34785
