from typing import Any, Dict, List, Optional
from pandas import DataFrame
from ipywidgets import Checkbox, VBox, Button, Layout, AppLayout, HTML, GridspecLayout
from bqplot import LinearScale, Lines, Axis, Figure, ColorScale, Bars, OrdinalScale
from Setup_des_graphs_v1 import plot_multi # Ne plot pas vraiment un graphe, renvoie juste les données nécessaires pour le graphe multi-disciplinaire.
from src.core.crud_aspects import get_aspects, get_aspect_id
from src.core.process_engine import ProcessEngine




def generate_prospective_scenario_figure(
        process_data: Dict[str, Any],
        figure_title: str,
        color_palette: Optional[List[str]] = None
    ) -> Figure:
    """
    Initialise un graphique des "émissions annuelles" avec les valeurs par défaut.

    Arguments :
    - `process_data (dict [str, Any])` : Les données récolté à partir d'AéroMaps, permettant de tracer les différentes courbes du graphe.
    - `figure_title (str)` : Le titre du graphique généré.
    - `color_palette (List[str], optional)` : La palette de couleurs à utiliser dans le graphique (doit posséder exactement 7 couleurs).

    Returns :
    - `Figure` : Le graphique généré, à partir des données de `process_data`.
    """
    # Récupération des données de référence :
    DF_vector_outputs: DataFrame  = process_data["vector_outputs"]
    DF_climate_outputs: DataFrame = process_data["climate_outputs"]
    years: List[int]              = process_data["years"]["full_years"]        # Liste d'entiers allant de 2000 à 2050.
    historic_years: List[int]     = process_data["years"]["historic_years"]    # Liste d'entiers allant de 2000 à 2019.
    prospective_years: List[int]  = process_data["years"]["prospective_years"] # Liste d'entiers allant de 2019 à 2050.

    # Paramétrage de la palette de couleurs :
    default_palette = ["#000000", "#1f77b4", "#ff7f0e", "#2ca02c", "#8c564b", "#9467bd", "#d62728"]
    palette = color_palette if color_palette and len(color_palette) == len(default_palette) else default_palette
    color_scale = ColorScale(colors = palette)

    # Paramétrage des axes :
    x_scale = LinearScale()
    y_scale = LinearScale()
    x_axis = Axis(
        scale = x_scale,
        num_ticks = 6,
        label = "Années",
        label_offset = "40px"
    )
    y_axis = Axis(
        scale = y_scale,
        orientation = "vertical",
        label = "Emissions de CO2, en Mt",
        label_offset = "40px"
    )

    # Tracé des émissions historiques (ligne noire allant de 2000 à 2019) :
    historic_line = Lines(
        x = historic_years,
        y = DF_climate_outputs.loc[historic_years, "co2_emissions"],
        color = [0],
        scales = {"x": x_scale, "y": y_scale, "color": color_scale}
    )

    # Tracé des émissions prospectives (lignes allant de 2019 à 2050 : noir = "Business as usual", rouge = "Emissions restantes après application des aspects") :
    prospective_y_lines = [
        DF_climate_outputs.loc[prospective_years, "co2_emissions"] - DF_vector_outputs.loc[prospective_years, "carbon_offset"],
        DF_vector_outputs.loc[prospective_years, "co2_emissions_2019technology_baseline3"]
    ]
    prospective_lines = Lines(
        x = prospective_years,
        y = prospective_y_lines,
        color = [6, 0],
        scales = {"x": x_scale, "y": y_scale, "color": color_scale},
        labels = [
            "Emissions restantes",
            "Historique (2000-2019) / Business as usual (2019-2050)"
        ],
        display_legend = True
    )

    # Tracé des zones associées à chaque aspect permettant de réduire les émissions :
    aspects_y_areas = [
        DF_vector_outputs.loc[years, "co2_emissions_2019technology_baseline3"],
        DF_vector_outputs.loc[years, "co2_emissions_2019technology"],
        DF_vector_outputs.loc[years, "co2_emissions_including_aircraft_efficiency"],
        DF_vector_outputs.loc[years, "co2_emissions_including_load_factor"],
        DF_vector_outputs.loc[years, "co2_emissions_including_energy"],
    ]
    aspects_colors_indices = [1, 2, 3, 4, 5]
    aspects_areas = Lines(
        x = years,
        y = aspects_y_areas,
        color = aspects_colors_indices,
        stroke_width = 0,
        fill = "between",
        fill_colors = [palette[i] for i in aspects_colors_indices],
        fill_opacities = [0.3] * len(aspects_y_areas),
        labels = [
            "Changement de la demande",
            "Efficacité technologique",
            "Opérations en vol",
            "Energies alternatives",
            "Compensation carbone"
        ],
        display_legend = True,
        scales={"x": x_scale, "y": y_scale, "color": color_scale},
    )

    # Création de la figure avec tous les tracés (lignes et aires) et les axes :
    figure = Figure(
        marks = [historic_line, prospective_lines, aspects_areas],
        axes = [x_axis, y_axis],
        title = figure_title,
        animation_duration = 1000,
        legend_location = "top-left",
        legend_style = {"stroke-width": 0}
    )
    return figure


def update_all_figures(
    _btn: Button,
    processes: List[ProcessEngine],
    widget_lists: List[List[Checkbox]],
    figures: List[Figure]
) -> None:
    for idx, engine in enumerate(processes):
        # Lire l’état des widgets AU CLIC
        aspect_ids = [
            get_aspect_id(cb.description)
            for cb in widget_lists[idx]
            if getattr(cb, "value", False)
        ]
        # Recompute
        new_data = engine.compute(aspect_ids)
        # Nouveau jeu de marks
        new_fig = generate_prospective_scenario_figure(new_data, figures[idx].title)
        # MAJ atomique de la Figure
        with figures[idx].hold_sync():
            figures[idx].marks = new_fig.marks



"""
Etape de refactorisation du code :
    - Mettre à jour le Trello avec les tâches suivantes (et celles déjà faîtes !).
    - Ce qu'il reste à faire (dans ce fichier) :
        - Finir de factoriser `run_graph_v3()`.
        - Mettre sous forme de classe les graphiques `fig_n` et `bar_n` pour chaque groupe.
        - Faire fonctionner de nouveau le bouton "Calculer" pour mettre à jour les graphiques.
        - Retravailler l'interface (positionnement des widgets, des graphiques, etc...).
        - Ajouter des commentaires et de la documentation.
    - Ce qu'il reste à faire (en dehors de ce fichier) :
        - Refactoriser tout le code nouvellement factorisé (créer un agencement BEAUCOUP plus optimal, quitte à coder de nouveau certaines parties), en :
            - Créant, rennomant et supprimant les fichiers actuels.
            - Créant des dossiers.
            - Renommer les CLASSES, FONCTIONS et VARIABLES.
            - Ecrivant des commentaires plus précis.
            - Ext...
        - Supprimer le fichier `temp.ipynb` lorsqu'on aura fini la refactorisation du code.
        - Ajouter Docker.
        - Tester un déploiment du code sur `onready.com` pour vérifier que tout fonctionne correctement (si non, pleurer).
Fin de l'étape de refactorisation du code.
"""


def run_graph_v3():
    """
    Section qui créé les graphiques d'émissions annuelles avec les valeurs par défaut, pour qu'ensuite une fonction viens les modifier.
    """

    #initialisation des listes qui serviront pour les widgets (qui sont en fait les boutons à cocher), 
    #et de la liste qui sert d'abscisse dans le graph
    Liste_des_widgets1 = []
    Liste_des_widgets2 = []
    Liste_des_widgets3 = []

    #initialisation des process avec les hypothèses du scénario de référence pour pouvoir tracer les graphiques.
    #d'où la nécessité d'initaliser les listes de widgets ci-dessus
    process_ref = ProcessEngine()
    process1 = ProcessEngine()
    process2 = ProcessEngine()
    process3 = ProcessEngine()
    process_ref_data = process_ref.compute()
    process1_data = process1.compute([get_aspect_id(aspect) for aspect in Liste_des_widgets1 if aspect in get_aspects()])
    process2_data = process2.compute([get_aspect_id(aspect) for aspect in Liste_des_widgets2 if aspect in get_aspects()])
    process3_data = process3.compute([get_aspect_id(aspect) for aspect in Liste_des_widgets3 if aspect in get_aspects()])

    #...
    fig_ref = generate_prospective_scenario_figure(process_ref_data, "Scénario de référence")
    fig1 = generate_prospective_scenario_figure(process1_data, "Scénario du groupe 1")
    fig2 = generate_prospective_scenario_figure(process2_data, "Scénario du groupe 2")
    fig3 = generate_prospective_scenario_figure(process3_data, "Scénario du groupe 3")

    """
    Création du graphique multi-disciplinaire
    """

    #paramétrage des axes
    x_ord = OrdinalScale()
    y_sc = LinearScale()
    categories = ["ERF (CO₂ et non-CO₂)","Emissions de CO₂","Biomasse","Electricité"]
    ax_x = Axis(scale=x_ord, tick_style={'font-weight': 'bold'})
    ax_y = Axis(scale=y_sc, tick_format="0.2f", orientation="vertical",label="Part du budget mondial (en %)")

    #création du graphique de référence
    [consumptions_ref,budgets_ref]=plot_multi(process_ref_data)

    #tracé des barres
    cons_ref = Bars(x=categories, 
                y=consumptions_ref, 
                scales={"x": x_ord, "y": y_sc},
                colors=["Orange"]*4,
            )

    #mise en forme du graphique
    bar_ref=Figure(marks=[cons_ref], 
                axes=[ax_x, ax_y], 
                padding_x=0.025, padding_y=0.025, 
                title="Scénario de référence",
                animation_duration = 1000,)

    #création du graphique du premier groupe
    [consumptions1,budgets1]=plot_multi(process1_data)
    cons1 = Bars(x=categories, 
                y=consumptions1, 
                scales={"x": x_ord, "y": y_sc},
                colors=["Orange"]*4,
            )

    bar1=Figure(marks=[cons1], 
                axes=[ax_x, ax_y], 
                padding_x=0.025, padding_y=0.025, 
                title="Scénario du groupe 1",
                animation_duration = 1000,)

    #création du graphique du deuxième groupe
    [consumptions2,budgets2]=plot_multi(process2_data)
    cons2 = Bars(x=categories, 
                y=consumptions2, 
                scales={"x": x_ord, "y": y_sc},
                colors=["Orange"]*4,
            )
    bar2=Figure(marks=[cons2], 
                axes=[ax_x, ax_y], 
                padding_x=0.025, padding_y=0.025, 
                title="Scénario du groupe 2",
                animation_duration = 1000,)

    #création du graphique du troisième groupe
    [consumptions3,budgets3]=plot_multi(process3_data)
    cons3 = Bars(x=categories, 
                y=consumptions3, 
                scales={"x": x_ord, "y": y_sc},
                colors=["Orange"]*4,
            )
    bar3=Figure(marks=[cons3], 
                axes=[ax_x, ax_y], 
                padding_x=0.025, padding_y=0.025, 
                title="Scénario du groupe 3",
                animation_duration = 1000,)

    """
    Création des cases à cocher grâce à la librairie widgets
    """

    #Liste des cartes sélectionnables pour pouvoir nommer les cases à cocher
    Liste_des_cartes = get_aspects()

    #création des 8 widgets par groupe en utilisant une boucle et la liste des cartes
    for carte in Liste_des_cartes :
        Liste_des_widgets1.append(Checkbox(
            value=False,
            description=carte,
            indent=False,
        ))
        Liste_des_widgets2.append(Checkbox(
            value=False,
            description=carte,
            indent=False,
        ))
        Liste_des_widgets3.append(Checkbox(
            value=False,
            description=carte,
            indent=False,
        ))
        
    #mise en forme de chaque liste de widgets pour les agencer verticalement
    Choix_cartes1 = VBox(Liste_des_widgets1)
    Choix_cartes2 = VBox(Liste_des_widgets2) 
    Choix_cartes3 = VBox(Liste_des_widgets3) 

    #création des cases à cocher pour le choix du nombre de groupes
    mode_2_groupes = Checkbox(
        value=False,
        description='mode 2 groupes',
        indent=False
    )
    mode_3_groupes = Checkbox(
        value=False,
        description='mode 3 groupes',
        indent=False
    )
    #agencement des choix groupes en bar verticale
    Choix_groupes = VBox([mode_2_groupes,mode_3_groupes])

    #création du bouton update 
    Update_btn=Button(description="Calculer", button_style="success",layout=Layout(width='300px', height='50px'))

    """
    Création de la fonction "de mise à jour", qui s'active lorsqu'on utilise le bouton update
    """

    def on_btn_click(btn):

        #on utilise la fonction compute pour calculer les datas de sortie avec les paramètres changs par la liste de widgets
        process1_data = process1.compute([get_aspect_id(aspect) for aspect in Liste_des_widgets1 if aspect in get_aspects()])
        #on associe ensuite ces datas en plusieurs catégories pour pouvoir traiter chaque type de données correctement
        df1 = process1_data["vector_outputs"]
        df1_climate = process1_data["climate_outputs"]
        float_outputs1 = process1_data["float_outputs"]
        
        #la fonction hold_sync() permet de s'assurer que le graph reste affiché et sera animé lors du changement de courbe
        with line1.hold_sync():
            #on retrace chaque courbe
            line1.y =[df1.loc[years, "co2_emissions_2019technology_baseline3"],
                    df1["co2_emissions_2019technology"],
                    df1["co2_emissions_including_aircraft_efficiency"],
                    df1["co2_emissions_including_load_factor"],
                    df1["co2_emissions_including_energy"],
                    df1_climate.loc[years, "co2_emissions"] - df1.loc[years, "carbon_offset"]]
        #on continue à retracer les courbes
        with line1_p.hold_sync():
            line1_p.y =[df1_climate.loc[prospective_years, "co2_emissions"] - df1.loc[prospective_years, "carbon_offset"],
                        df1.loc[prospective_years,"co2_emissions_2019technology_baseline3"]],
            
        #on retrace ici les barres du graph multidisciplinaire
        with cons1.hold_sync():
            cons1.y = [
                max(float(df1_climate.loc[2050, "cumulative_total_equivalent_emissions"]) / float_outputs1["equivalent_gross_carbon_budget_2050"] * 100, 0),
                float(df1.loc[2050, "cumulative_co2_emissions"]) / float_outputs1["gross_carbon_budget_2050"] * 100,
                float_outputs1["biomass_consumption_end_year"] / float_outputs1["available_biomass_total"] * 100,
                float_outputs1["electricity_consumption_end_year"] / float_outputs1["aviation_available_electricity"]
            ]
        
        #on procède de même avec le graph du groupe 2 si la case a été cochée
        if mode_2_groupes.value or mode_3_groupes.value :        
            process2_data = process2.compute([get_aspect_id(aspect) for aspect in Liste_des_widgets2 if aspect in get_aspects()])
            df2 = process2_data["vector_outputs"]
            df2_climate = process2_data["climate_outputs"]
            float_outputs2 = process2_data["float_outputs"]

            with line2.hold_sync():
                line2.y =[df2.loc[years, "co2_emissions_2019technology_baseline3"],
                        df2["co2_emissions_2019technology"],
                        df2["co2_emissions_including_aircraft_efficiency"],
                        df2["co2_emissions_including_load_factor"],
                        df2["co2_emissions_including_energy"],
                        df2_climate.loc[years, "co2_emissions"] - df2.loc[years, "carbon_offset"]]
            with line2_p.hold_sync():
                line2_p.y =[df2_climate.loc[prospective_years, "co2_emissions"] - df2.loc[prospective_years, "carbon_offset"],
                            df2.loc[prospective_years,"co2_emissions_2019technology_baseline3"]],
            with cons2.hold_sync():
                cons2.y = [
                    max(float(df2_climate.loc[2050, "cumulative_total_equivalent_emissions"]) / float_outputs2["equivalent_gross_carbon_budget_2050"] * 100, 0),
                    float(df2.loc[2050, "cumulative_co2_emissions"]) / float_outputs2["gross_carbon_budget_2050"] * 100,
                    float_outputs2["biomass_consumption_end_year"] / float_outputs2["available_biomass_total"] * 100,
                    float_outputs2["electricity_consumption_end_year"] / float_outputs2["aviation_available_electricity"]
                ]
                
        #on procède de même avec le graph du groupe 3 si la case a été cochée
        if mode_3_groupes.value :
            process3_data = process3.compute([get_aspect_id(aspect) for aspect in Liste_des_widgets3 if aspect in get_aspects()])
            df3 = process3_data["vector_outputs"]
            df3_climate = process3_data["climate_outputs"]
            float_outputs3 = process3_data["float_outputs"]

            with line3.hold_sync():
                line3.y =[df3.loc[years, "co2_emissions_2019technology_baseline3"],
                        df3["co2_emissions_2019technology"],
                        df3["co2_emissions_including_aircraft_efficiency"],
                        df3["co2_emissions_including_load_factor"],
                        df3["co2_emissions_including_energy"],
                        df3_climate.loc[years, "co2_emissions"] - df3.loc[years, "carbon_offset"]]
            with line3_p.hold_sync():
                line3_p.y =[df3_climate.loc[prospective_years, "co2_emissions"] - df3.loc[prospective_years, "carbon_offset"],
                            df3.loc[prospective_years,"co2_emissions_2019technology_baseline3"]],  

            with cons3.hold_sync():
                cons3.y = [
                    max(float(df1_climate.loc[2050, "cumulative_total_equivalent_emissions"]) / float_outputs3["equivalent_gross_carbon_budget_2050"] * 100, 0),
                    float(df3.loc[2050, "cumulative_co2_emissions"]) / float_outputs3["gross_carbon_budget_2050"] * 100,
                    float_outputs3["biomass_consumption_end_year"] / float_outputs3["available_biomass_total"] * 100,
                    float_outputs3["electricity_consumption_end_year"] / float_outputs3["aviation_available_electricity"]
                ]

    #association de la fonction que l'on vient de définir au bouton update
    Update_btn.on_click(
        lambda btn: update_all_figures(
            btn,
            [process1, process2, process3],
            [Liste_des_widgets1, Liste_des_widgets2, Liste_des_widgets3],
            [fig1, fig2, fig3]
        )
    )

    """
    Mise en forme des graphiques avec leurs cases à cocher à côté
    """

    app_layout_ref= AppLayout(
    header=None,
    left_sidebar=Choix_groupes,
    center=fig_ref,
    right_sidebar=None,
    footer=None,
    align_items="center",
    width='100%'
    )
    app_layout1= AppLayout(
    header=None,
    left_sidebar=Choix_cartes1,
    center=fig1,
    right_sidebar=None,
    footer=None,
    align_items="center",
    width='100%'
    )

    app_layout2= AppLayout(
    header=None,
    left_sidebar=Choix_cartes2,
    center=fig2,
    right_sidebar=None,
    footer=None,
    align_items="center",
    width='100%'
    )
    app_layout3= AppLayout(
    header=None,
    left_sidebar=Choix_cartes3,
    center=fig3,
    right_sidebar=None,
    footer=None,
    align_items="center",
    width='100%'
    )

    #création d'un widget pour le titre du graph multi-disciplinaire
    titre= HTML(
        value="<FONT size='5'><u><b>Ci-dessous : Pourcentages du budget des ressources mondiales utilisés par l'aviation (budgets estimés sur la période 2019-2050)</b></u></FONT>",
        layout=Layout(margin="40px 0px 20px 0px")
    )
    #agencement de ce qui sera l'entre-deux graph avec le bouton update et le titre
    centre = VBox([Update_btn, titre])

    """
    Agencement des différents graphs, titres, boutons en grille 
    """

    grid = GridspecLayout(9, 2, grid_gap="5px")
    grid[0, slice(0, 2)] = app_layout_ref
    grid[1, slice(0, 2)] = app_layout1
    grid[2, slice(0, 2)] = app_layout2
    grid[3, slice(0, 2)] = app_layout3
    grid[4, slice(None)] = centre
    grid[slice(5, 7), 0] = bar_ref
    grid[slice(5, 7), 1] = bar1
    grid[slice(7, 9), 0] = bar2
    grid[slice(7, 9), 1] = bar3

    return grid
