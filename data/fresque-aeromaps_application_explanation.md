<h1 align="center">
Fresqu'AéroMAPS - Outil de simulation des choix de solution
</h1>

<h4 align="center">
Ce logiciel a pour but de simuler les choix des différents groupes de l'atelier lors de la partie finale de l'atelier Fresqu'Aéro.
</h4>

**<u>Cet outil repose sur l'outil AéroMAPS ([Site Web](https://aeromaps.isae-supaero.fr/)) :</u>**

Planès, T., Delbecq, S., Salgas, A. (2023). AeroMAPS : a framework for performing multidisciplinary assessment of prospective scenarios for air transport. Submitted to Journal of Open Aviation Science.

<h2 align="center">
Quelques chiffres importants pour comprendre le scénario de référence
</h2>

<u>Les résultats des groupes seront ensuite comparés avec un scénario de référence, qui correspond à la tendance actuelle de l'industrie. Quantitativement, les chiffres viennent notamment du scénario Airbus (2024) :</u>

- La croissance du trafic est de 3% par an, constante et conforme aux prévisions de l'OACI.
- Le renouvellement de la flotte a une période de 20 ans.
- Il n'y a pas de technologie disruptive avant 2050 (électrique ou hydrogène).
- Les opérations au sol et en vol font gagner environ 5% d'efficacité en 2050.
- L'amélioration incrémentale technologique est de 0,5% par an, la tendance depuis une vingtaine d'années, et conforme aux prévisions Global Market Forecast 2024 Airbus.
- L'allocation des ressources pour l'aérien est conservée par rapport à l'actuelle répartition. On pourrait discuter cette répartition.

<h2 align="center">
Quantification des cartes solutions de la Fresqu'Aéro
</h2>

<u>Une quantification de chaque solution a été choisie comme suit :</u>

- **Sobriété** : la croissance de la demande est revue à 1,5% par an pour toutes les distances (choix arbitraire, pour comparaison, le GMF2019 prévoyait 4,3% de croissance, revue à 3,3% dans le GMF2024).
- **Compensation des émissions** : 10% des émissions résiduelles par rapport à la neutralité sont compensées (Waypoint 2050, moyenne des scénarios, ATAG).
- **Nouveaux vecteurs énergétiques** : la planification de ReFuelEU est respectée et étendue au monde entier. Elle différencie bioSAF et eSAF, et porte leur part à 37.5% chacun en 2050, avec des points de passage intermédiaires et progressifs.
- **Report modal** : 2% de croissance en moins sur le court-courrier, peut se cumuler avec la sobriété.
- **Efficacité des opérations** : Les opérations au sol et en vol font gagner environ 10% d'efficacité en 2050, et le load factor atteint 90% sur la période (Waypoint 2050, scénario 1, ATAG).
- **Technologie** : L'amélioration incrémentale technologique est de 1% par an.
- **`[NI]` Allouer un budget carbone** : ...
- **`[NI]` Réglementation et mesures économiques** : ...
- **`[NI]` Sensibiliser & Éduquer** : ...

Ces choix reflètent des tendances possibles mais sont largement discutables. Par exemple, le choix de la technologie pourrait être dissocié entre technologie disruptive et amélioration incrémentale, la sobriété n'influe peut-être pas de la même manière sur toutes les distances, etc.

**Il faut donc garder en tête que cette simulation n'est que partielle, et grossière. Elle donne une idée des chiffres envisageables associés aux cartes et de leur portée, mais reste loin d'inclure toutes les nuances existantes.**

**De plus, certains aspects ne sont pas traités : notamment les aspects sociaux, l'impact économique des mesures, les investissements et leur chronologie nécessaires à certaines solutions, ou encore les dynamiques et volontés différentes entre régions du monde.**

**<u>Note :</u>** Certaines cartes sont précédées d'un `[NI]`, cela signifie qu'elles n'ont pas encore été implémentées dans le logiciel (dans l'attente du développement d'un modèle coût-demande de l'outil AéroMAPS), elles n'impactent pas les simulations pour le moment.

<h2 align="center">
Mode d'emploi
</h2>

1. Choisir le nombre de groupes réalisant l'activité *(entre 1 et 10 groupes, 3 groupes par défaut)*.
2. Appuyer sur le bouton "Mettre à jour le nombre de groupes" pour appliquer le nombre de groupes choisis. *Cette opération prend 15 à 20 secondes par groupe ajouté.*
3. Pour chaque groupe, cocher les cartes sélectionnées dans le tableau de sélection des cartes.
4. Appuyer sur le bouton "Mettre à jour les graphiques" pour appliquer les choix de cartes de chaque groupe. *Cette opération prend 15 à 20 secondes par groupe.*

**<u>Note :</u>** Il est possible de zoomer / dézoomer la page avec la molette de votre souris afin de voir plus de graphiques à la fois.
