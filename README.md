# Pizza-Bot

Mini-projet de sciences appliquées : quatre questions posées par la direction d'une entreprise
de distributeurs automatiques de pizzas, traitées de bout en bout, du brouillon au programme,
puis du programme à la note écrite.

Théorie des jeux, jeux séquentiels, statistiques descriptives et détection d'anomalies, en
Python sans aucune bibliothèque.

## Les quatre questions

| Question | Méthode | Réponse |
|---|---|---|
| Où installer le distributeur ? | Matrice des gains, équilibres de Nash, induction à rebours | La Gare, 6 k€/mois |
| Quelle gamme proposer ? | Espérance, croyance sur les types, croyance de bascule | Discount, 6,2 k€/mois |
| Combien de pizzas prévoir ? | Corrélation, droite des moindres carrés | ventes = −2,63 × température + 134,30 |
| Comment détecter un déréglage ? | Loi normale, z-score, persistance | Seuil à 2σ et 3 anomalies consécutives |

La note à la direction donne, pour chacune, la recommandation, le chiffre qui la fonde et la
limite de ce chiffre.

## Contraintes de code

Le sujet impose deux règles, respectées partout :

- **Python de base uniquement** : listes, dictionnaires, tuples, boucles, conditions, fonctions.
  Fonctions natives autorisées : `sum`, `len`, `min`, `max`, `abs`, `round`, `zip`, `enumerate`.
- **Aucun import** : ni `math`, ni `statistics`, ni `numpy`. La racine carrée s'écrit `x ** 0.5`.

Seules les cellules de tracé des notebooks utilisent `matplotlib`, uniquement pour visualiser.
Elles sont signalées en commentaire et ne font aucun calcul. Le fichier `pizza_bot.py`, lui,
n'importe rien du tout.

## Structure du dépôt

```
pizza-bot/
├── pizza_bot.py                        Programme complet : les 4 réponses en une exécution
├── notebooks/
│   ├── partie1_duel_emplacements.ipynb     Équilibres de Nash, stratégies mixtes
│   ├── partie2_ordre_et_gamme.ipynb        Induction à rebours, espérance, bascule
│   ├── partie3_prevoir_les_ventes.ipynb    Covariance, corrélation, moindres carrés
│   ├── partie4_supervision_buse.ipynb      Écart-type estimé, z-score, persistance
│   └── pour_aller_plus_loin.ipynb          Trois emplacements, persistance, seuil glissant
├── brouillons/                         Le travail à la main, avec les photos
│   ├── Partie1_brouillon.docx
│   ├── Partie2_brouillon.docx
│   ├── Partie3_brouillon.docx
│   └── Partie4_brouillon.docx
├── interpretations/                    Les questions écrites et les QCM
│   ├── Partie1_interpretations.docx
│   ├── Partie2_interpretations.docx
│   ├── Partie3_interpretations.docx
│   ├── Partie4_interpretations.docx
│   ├── Partie1_bonus.docx                  Stratégies mixtes
│   ├── Partie2_bonus.docx                  Valeur de l'information parfaite
│   └── Partie4_bonus.docx                  Effet de masquage
└── rapport/
    └── Rapport_direction.docx          La note d'une page
```

Chaque partie est livrée en quatre pièces : le brouillon fait à la main, le notebook exécuté,
les interprétations rédigées et, quand il existe, le bonus. La partie 3 n'a pas de bonus.

## Lancer le projet

Python 3 suffit, sans installation. Pour les notebooks, il faut Jupyter et matplotlib.

```bash
git clone https://github.com/VOTRE-COMPTE/pizza-bot.git
cd pizza-bot

python3 pizza_bot.py                 # les quatre réponses en une exécution
jupyter notebook notebooks/          # les notebooks, partie par partie
```

Les `assert` du sujet sont conservés dans chaque notebook : si aucun ne proteste et que le
message de validation s'affiche, les fonctions sont justes.

## Résultats obtenus

**Partie 1.** Deux équilibres de Nash : (Campus ; Gare) avec les gains (9 ; 7) et
(Gare ; Campus) avec (6 ; 8). Aucune stratégie dominante : c'est un jeu d'anti-coordination.
Équilibre en stratégies mixtes : q = 5/8 pour Pizza-Bot, p = 3/4 pour Mamma-Auto.

**Partie 2.** Mamma-Auto s'installant en premier choisit le Campus, Pizza-Bot répond la Gare.
Gamme Discount, avec 6,20 k€/mois contre 5,10 pour Premium. Croyance de bascule c* = 8/13,
soit environ 0,615, pour une croyance estimée à 0,70 : la décision n'est pas robuste. Valeur de
l'information parfaite : 2,40 k€/mois.

**Partie 3.** r = −0,977 et r² = 0,954. Chaque degré supplémentaire fait perdre 2,6 pizzas par
jour. Le seuil de rentabilité de 50 pizzas est atteint vers 32,1 °C, hors de la plage observée
de 3 à 31 °C : c'est une extrapolation, donc une valeur qu'on ne peut pas affirmer.

**Partie 4.** mu = 99,89 g et sigma = 1,901 g, soit un intervalle de tolérance [96,09 ; 103,69].
Trois pesées de calibration sur cinquante en sortent, ce qui est attendu à 2σ. Sur le flux de
production : 5 alertes et arrêt de la machine à la pesée 19, après trois anomalies consécutives.
Ce réglage produit environ 18 fausses alertes par jour pour 400 pizzas servies.

**Pour aller plus loin.** Les fonctions de la partie 1 acceptent un troisième emplacement sans
modification. La persistance de 3 est le meilleur compromis : à 1 la machine s'arrête sur un pic
isolé, à 5 la dérive passe inaperçue. Enfin, sur une dérive lente, une référence glissante ne
déclenche aucune alerte, là où la référence fixe en déclenche 126 : le seuil a suivi la dérive
et l'a acceptée comme le nouveau normal.

## La méthode suivie

1. Poser le modèle au brouillon : les joueurs et leurs gains, l'arbre, le nuage, la loi.
2. Programmer le geste du brouillon, et lui seul.
3. Tester sur un cas qui se calcule de tête avant de lancer les vraies données.
4. Confronter le programme au brouillon et aux contrôles que la théorie fournit gratuitement :
   le point moyen, le signe commun de a et r, la croyance de bascule.
5. Traduire chaque nombre en une phrase, et l'accompagner de sa limite.

## Auteur

Habiba Daïrou
