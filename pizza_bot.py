"""Pizza-Bot : le programme complet.

Rassemble les fonctions des quatre parties et affiche, en une seule exécution,
les quatre résultats de la note à la direction.

Règles du projet : Python de base, aucun import.
Chaque fonction ne dépend que de ce qu'on lui passe : aucune ne lit une variable
laissée par un bloc précédent. C'est ce qui permet de les réunir ici sans rien casser.

Lancement : python3 pizza_bot.py
"""

# =====================================================================
# Les données
# =====================================================================

EMPLACEMENTS = ["Campus", "Gare"]

GAINS_EMPLACEMENT = {
    ("Campus", "Campus"): (4, 4),
    ("Campus", "Gare"): (9, 7),
    ("Gare", "Campus"): (6, 8),
    ("Gare", "Gare"): (3, 3),
}

GAMMES = ["Discount", "Premium"]

GAINS_GAMME = {
    "Discount": {"Discount": 2, "Premium": 8},
    "Premium": {"Discount": 10, "Premium": 3},
}

CROYANCE = {"Discount": 0.3, "Premium": 0.7}

TEMPERATURES = [3, 5, 6, 8, 10, 11, 13, 15, 17, 18, 20, 22, 24, 26, 28, 31]
VENTES = [132, 126, 110, 113, 112, 109, 96, 92, 92, 82, 82, 69, 73, 61, 63, 61]
SEUIL_RENTABILITE = 50

HISTORIQUE_CALIBRATION = [
    102.5, 102.1, 96.9, 101.0, 98.9, 97.5, 100.3, 101.3, 104.1, 99.5,
    102.4, 93.2, 99.3, 99.9, 98.8, 101.9, 99.5, 101.9, 102.0, 98.0,
    99.6, 99.8, 99.6, 98.3, 98.4, 100.9, 98.2, 98.9, 101.6, 101.4,
    100.0, 97.6, 96.0, 100.2, 99.9, 101.9, 101.8, 99.1, 99.6, 100.0,
    100.2, 100.9, 102.7, 100.9, 100.6, 99.5, 98.5, 98.6, 98.7, 100.1,
]

FLUX_TEMPS_REEL = [
    100.4, 99.1, 101.7, 98.6, 100.9, 106.8, 99.8, 100.3, 97.9, 101.2,
    92.4, 100.6, 99.4, 102.3, 100.1, 98.8, 103.2, 104.1, 104.9, 105.6,
    106.3,
]

PERSISTANCE = 3
PIZZAS_PAR_JOUR = 400


# =====================================================================
# Partie 1 : le duel d'emplacements
# =====================================================================

def meilleure_reponse_pizzabot(gains, choix_mamma, emplacements):
    """L'emplacement qui rapporte le plus à Pizza-Bot quand Mamma-Auto joue choix_mamma."""
    meilleur = emplacements[0]
    for choix in emplacements:
        if gains[(choix, choix_mamma)][0] > gains[(meilleur, choix_mamma)][0]:
            meilleur = choix
    return meilleur


def meilleure_reponse_mamma(gains, choix_pizzabot, emplacements):
    """L'emplacement qui rapporte le plus à Mamma-Auto quand Pizza-Bot joue choix_pizzabot."""
    meilleur = emplacements[0]
    for choix in emplacements:
        if gains[(choix_pizzabot, choix)][1] > gains[(choix_pizzabot, meilleur)][1]:
            meilleur = choix
    return meilleur


def est_equilibre_nash(gains, choix_pizzabot, choix_mamma, emplacements):
    """True si aucun joueur ne gagne strictement plus en changeant seul de stratégie."""
    gain_pizzabot = gains[(choix_pizzabot, choix_mamma)][0]
    gain_mamma = gains[(choix_pizzabot, choix_mamma)][1]

    for autre in emplacements:
        if gains[(autre, choix_mamma)][0] > gain_pizzabot:
            return False
    for autre in emplacements:
        if gains[(choix_pizzabot, autre)][1] > gain_mamma:
            return False
    return True


def trouver_equilibres_nash(gains, emplacements):
    """La liste de toutes les cases qui sont des équilibres de Nash."""
    equilibres = []
    for choix_pizzabot in emplacements:
        for choix_mamma in emplacements:
            if est_equilibre_nash(gains, choix_pizzabot, choix_mamma, emplacements):
                equilibres.append((choix_pizzabot, choix_mamma))
    return equilibres


# =====================================================================
# Partie 2 : ordre de jeu et choix de gamme
# =====================================================================

def induction_a_rebours(gains, emplacements):
    """Mamma-Auto joue en premier. Renvoie (choix_mamma, choix_pizzabot, gains_de_la_case)."""
    choix_retenu = None
    reponse_retenue = None
    case_retenue = None

    for choix_mamma in emplacements:
        reponse = meilleure_reponse_pizzabot(gains, choix_mamma, emplacements)
        case = gains[(reponse, choix_mamma)]
        if case_retenue is None or case[1] > case_retenue[1]:
            choix_retenu = choix_mamma
            reponse_retenue = reponse
            case_retenue = case

    return (choix_retenu, reponse_retenue, case_retenue)


def esperance_gain(gains, croyance, gamme):
    """Espérance de gain de Pizza-Bot s'il choisit `gamme`, selon sa croyance."""
    total = 0
    for type_mamma in croyance:
        total = total + croyance[type_mamma] * gains[gamme][type_mamma]
    return total


def meilleure_gamme(gains, croyance, gammes):
    """Le couple (gamme, espérance) de la gamme d'espérance maximale."""
    gamme_retenue = None
    esperance_retenue = None
    for gamme in gammes:
        esperance = esperance_gain(gains, croyance, gamme)
        if esperance_retenue is None or esperance > esperance_retenue:
            gamme_retenue = gamme
            esperance_retenue = esperance
    return (gamme_retenue, esperance_retenue)


def croyance_de_bascule(gains, nb_pas=1000):
    """La première valeur de c = P(Premium) où Discount rapporte au moins autant que Premium."""
    for i in range(nb_pas + 1):
        c = i / nb_pas
        croyance = {"Premium": c, "Discount": 1 - c}
        if esperance_gain(gains, croyance, "Discount") >= esperance_gain(gains, croyance, "Premium"):
            return c
    return None


def valeur_information_parfaite(gains, croyance, gammes):
    """Le prix maximal d'une étude qui donnerait le type de Mamma-Auto avant le choix."""
    esperance_avec_info = 0
    for type_mamma in croyance:
        meilleur_gain = None
        for gamme in gammes:
            gain = gains[gamme][type_mamma]
            if meilleur_gain is None or gain > meilleur_gain:
                meilleur_gain = gain
        esperance_avec_info = esperance_avec_info + croyance[type_mamma] * meilleur_gain
    return esperance_avec_info - meilleure_gamme(gains, croyance, gammes)[1]


# =====================================================================
# Partie 3 : prévoir les ventes
# =====================================================================

def moyenne(valeurs):
    return sum(valeurs) / len(valeurs)


def variance(valeurs):
    """V(X), en divisant par N : on décrit la série observée."""
    m = moyenne(valeurs)
    total = 0
    for v in valeurs:
        total = total + (v - m) ** 2
    return total / len(valeurs)


def covariance(x, y):
    """cov(X, Y), en divisant par N."""
    if len(x) != len(y):
        raise ValueError("x et y n'ont pas la même longueur")
    mx = moyenne(x)
    my = moyenne(y)
    total = 0
    for xi, yi in zip(x, y):
        total = total + (xi - mx) * (yi - my)
    return total / len(x)


def coefficient_correlation(x, y):
    """r, sans unité, compris entre -1 et 1."""
    return covariance(x, y) / ((variance(x) ** 0.5) * (variance(y) ** 0.5))


def droite_moindres_carres(x, y):
    """Le couple (a, b) de la droite y = ax + b."""
    a = covariance(x, y) / variance(x)
    b = moyenne(y) - a * moyenne(x)
    return (a, b)


def predire(a, b, x):
    return a * x + b


def dans_la_plage(x, observees):
    """True si x est dans la plage des valeurs observées, bornes comprises."""
    return min(observees) <= x <= max(observees)


def temperature_seuil(a, b, seuil):
    """La température à laquelle la droite vaut `seuil`."""
    return (seuil - b) / a


# =====================================================================
# Partie 4 : superviser la buse
# =====================================================================

def ecart_type_estime(valeurs):
    """Écart-type estimé à partir d'un échantillon : division par N - 1."""
    m = moyenne(valeurs)
    total = 0
    for v in valeurs:
        total = total + (v - m) ** 2
    return (total / (len(valeurs) - 1)) ** 0.5


def z_score(valeur, mu, sigma):
    return (valeur - mu) / sigma


def est_anomalie(valeur, mu, sigma, k=2):
    """True si la valeur sort de [mu - k*sigma ; mu + k*sigma]."""
    return abs(z_score(valeur, mu, sigma)) > k


def surveiller(flux, mu, sigma, k=2, persistance=3):
    """Renvoie (alertes, indice_arret) ; indice_arret vaut None sans arrêt."""
    alertes = []
    consecutives = 0
    for indice, valeur in enumerate(flux):
        if est_anomalie(valeur, mu, sigma, k):
            alertes.append((indice, valeur))
            consecutives = consecutives + 1
            if consecutives == persistance:
                return (alertes, indice)
        else:
            consecutives = 0
    return (alertes, None)


# =====================================================================
# Les quatre réponses de la note à la direction
# =====================================================================

def question_1_emplacement():
    print("1. OU INSTALLER LE DISTRIBUTEUR ?")
    for case in trouver_equilibres_nash(GAINS_EMPLACEMENT, EMPLACEMENTS):
        gains = GAINS_EMPLACEMENT[case]
        print(f"   equilibre de Nash : Pizza-Bot {case[0]:6} / Mamma-Auto {case[1]:6} -> {gains}")
    choix_mamma, reponse, case = induction_a_rebours(GAINS_EMPLACEMENT, EMPLACEMENTS)
    print(f"   Mamma-Auto s'installe en premier a {choix_mamma}, Pizza-Bot repond {reponse}")
    print(f"   Recommandation : {reponse}, pour {case[0]} k€/mois")
    print()


def question_2_gamme():
    print("2. QUELLE GAMME PROPOSER ?")
    for gamme in GAMMES:
        print(f"   E[gain | {gamme:8}] = {esperance_gain(GAINS_GAMME, CROYANCE, gamme):.2f} k€/mois")
    gamme, esperance = meilleure_gamme(GAINS_GAMME, CROYANCE, GAMMES)
    bascule = croyance_de_bascule(GAINS_GAMME)
    valeur = valeur_information_parfaite(GAINS_GAMME, CROYANCE, GAMMES)
    print(f"   bascule vers Discount des P(Premium) = {bascule}")
    print(f"   valeur d'une etude de marche : {valeur:.2f} k€/mois au maximum")
    print(f"   Recommandation : {gamme}, pour {esperance:.2f} k€/mois")
    print()


def question_3_ventes():
    print("3. COMBIEN DE PIZZAS PREVOIR ?")
    r = coefficient_correlation(TEMPERATURES, VENTES)
    a, b = droite_moindres_carres(TEMPERATURES, VENTES)
    print(f"   r = {r:.3f}   r2 = {r * r:.3f}")
    print(f"   ventes = {a:.3f} x temperature + {b:.2f}")
    for t in (10, 20, 30):
        print(f"   a {t:2} °C : {predire(a, b, t):5.1f} pizzas")
    t_seuil = temperature_seuil(a, b, SEUIL_RENTABILITE)
    nature = "interpolation" if dans_la_plage(t_seuil, TEMPERATURES) else "EXTRAPOLATION"
    print(f"   seuil de {SEUIL_RENTABILITE} pizzas atteint vers {t_seuil:.1f} °C ({nature})")
    print(f"   Recommandation : indexer l'approvisionnement sur la temperature annoncee")
    print()


def question_4_supervision():
    print("4. COMMENT SAVOIR QUE LA MACHINE SE DEREGLE ?")
    mu = moyenne(HISTORIQUE_CALIBRATION)
    sigma = ecart_type_estime(HISTORIQUE_CALIBRATION)
    alertes, arret = surveiller(FLUX_TEMPS_REEL, mu, sigma, 2, PERSISTANCE)
    print(f"   mu = {mu:.2f} g   sigma = {sigma:.3f} g")
    print(f"   intervalle de tolerance : [{mu - 2 * sigma:.2f} ; {mu + 2 * sigma:.2f}]")
    print(f"   {len(alertes)} alertes sur le flux, arret a la pesee {arret}")
    print(f"   fausses alertes attendues : environ {0.0455 * PIZZAS_PAR_JOUR:.0f} par jour a 2 sigma")
    print(f"   Recommandation : seuil a 2 sigma et persistance de {PERSISTANCE} pesees")
    print()


def main():
    print("=" * 68)
    print("PIZZA-BOT : LES QUATRE REPONSES A LA DIRECTION")
    print("=" * 68)
    print()
    question_1_emplacement()
    question_2_gamme()
    question_3_ventes()
    question_4_supervision()
    print("=" * 68)
    print("Chaque chiffre a sa limite : voir la note a la direction.")
    print("=" * 68)


if __name__ == "__main__":
    main()
