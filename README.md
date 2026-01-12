# project-1
Project of Team 1
 
Contexte :
Les données GPS (Global Positioning System) collectées sur des stations fixes permettent de suivre les déplacements
de la croûte terrestre avec une grande précision. Ces informations sont particulièrement utiles pour étudier les
mouvements tectoniques, les déformations de terrain et les effets des séismes sur la surface de la Terre. Elles peuvent
également être croisées avec des catalogues de tremblements de terre afin de mieux comprendre les interactions entre
les mouvements lents de la lithosphère et les événements sismiques brusques.


But / Problématique
L’objectif de cette analyse est de traiter les données GPS afin d’extraire des informations temporelles sur les
déplacements d’une station donnée. Plus précisément, il s’agit de :
• Pour chaque point de donnée GPS, représenter la latitude en fonction du temps
• Pour chaque point de donnée GPS, représenter la longitude en fonction du temps
• Pour chaque point de donnée GPS, représenter l’altitude en fonction du temps
• Représenter les trajectoires GPS sur une carte en fonction du temps
• Construire un modèle 3D (avec une exagération verticale) pour visualiser les déplacements dans l’espace en
fonction du temps
• Ecrire un script pour télécharger toute la donnée automatiquement
Ces analyses permettront de visualiser les tendances de déplacement et d’évaluer l’impact potentiel d’événements
sismiques sur ces mouvements.

	
	Sous-groupe A :
		- Zélie Daniau-Cabanillas (@ZelieDC)
		- Lina Ben Aissa (@lina-ben-aissa)
		- Arnaud Gascou (@agascou)

 			OBJECTIF : Créer un interface graphique où l'utilisateur peut communiquer et obtenir les informations qu'il souhaite : 
				   L'interface possède une barre de recherche dans laquelle l'utilisateur entre le nom de la station GPS. 
				   Une fois, le nom rentré, l'interface renvoie les graphiques (altitude en fonction du temps, latitude en fonction du temps et longitude en fonction du temps), le modèle 2D et le modèle 3D de ce point.
				   L'interface fait donc le lien entre tous les travaux des autres groupes. Il prend la donnée de l'utilisateur et va chercher ses informations dans les différents fichiers adéquats réalisés par les sous-groupes.

	Sous-groupe B :
		- Léonie Dagonneau (@leonie19)
		- Peio Comet Ducasse (@PeioCD)
		- Mélissa Devun (@Melissa22031)

			OBJECTIF : Créer les modèles 2D et 3D.
				   Leurs données d'entrées (latitude, longitude et altitude) sont récupérés par le sous-groupe C et leur sont transmis par l'interface. De ce fait, les données sont déjà extraites, chiffrées.
				   Le modèle 2D représente la longitude et la latitude en fonction du temps. Avec le temps, il y a donc la notion de vitesse : la longueur de la flèche, du vecteur, qui représente le point est proportionnel à la vitesse.
				   Le modèle 3D représente la longitude, la latitude et l'altitude en fonction du temps.
				   L'interface récupère ces données.


	Sous-groupe C :
		- Raphael Chapuis (@2Raph)
		- Manon Chopin (@Manon625)

			OJECTIF : Récupérer les données de la station GPS via le site de la NASA. Ces valeurs sont enregistrées dans un document notepad à cause de la sécurité du site de la NASA, et sont stockées dans une variable.
				  Tracer 3 graphiques à l'aide de ses données :
						- latitude en fonction du temps
						- longitude en fonction du temps
						- altitude en fonction du temps
				  L'interface récupère ces données.