from typing import Any, Dict, List, Optional
from ipywidgets import Checkbox, VBox, Button, Layout, AppLayout, HTML, GridspecLayout
from bqplot import LinearScale, Axis, Figure, Bars, OrdinalScale
from Setup_des_graphs_v1 import plot_multi # Ne plot pas vraiment un graphe, renvoie juste les données nécessaires pour le graphe multi-disciplinaire.
from crud.crud_cards import get_cards, get_card_id
from src.core.process_engine import ProcessEngine
from src.bqplot_graphs.prospective_scenario_graph import ProspectiveScenarioGraph




def update_ps_figures(
    _btn: Button,
    engines: List[ProcessEngine],
    widget_lists: List[List[Checkbox]],
    ps_graphs: List[ProspectiveScenarioGraph]
) -> None:
    for index in range(len(widget_lists)):
        # 1) Récupère les IDs cochés :
        selected_ids = [
            get_card_id(cb.description)
            for cb in widget_lists[index]
            if cb.value and cb.description in get_cards()
        ]
        # 2) Re-calcul :
        new_data = engines[index].compute(selected_ids)
        # 3) Mise à jour du graphe :
        ps_graphs[index].update(new_data)


def run_graph_v3():
    # ...
    Liste_des_widgets1 = []
    Liste_des_widgets2 = []
    Liste_des_widgets3 = []

    # ...
    process_reference = ProcessEngine()
    process_1 = ProcessEngine()
    process_2 = ProcessEngine()
    process_3 = ProcessEngine()
    process_reference_data = process_reference.compute()
    process_1_data = process_1.compute([get_card_id(card) for card in Liste_des_widgets1 if card in get_cards()])
    process_2_data = process_2.compute([get_card_id(card) for card in Liste_des_widgets2 if card in get_cards()])
    process_3_data = process_3.compute([get_card_id(card) for card in Liste_des_widgets3 if card in get_cards()])

    """
    Graphiques "Prospective Scenario" :
    """
    ps_reference = ProspectiveScenarioGraph("Scénario de référence")
    ps_1 = ProspectiveScenarioGraph("Scénario du groupe 1")
    ps_2 = ProspectiveScenarioGraph("Scénario du groupe 2")
    ps_3 = ProspectiveScenarioGraph("Scénario du groupe 3")
    ps_figure_reference = ps_reference.draw(process_reference_data)
    ps_figure_1 = ps_1.draw(process_1_data)
    ps_figure_2 = ps_2.draw(process_2_data)
    ps_figure_3 = ps_3.draw(process_3_data)

    """
    Graphiques "Multidisciplinary" :
    """
    x_ord = OrdinalScale()
    y_sc = LinearScale()
    categories = [
        "ERF (CO₂ et non-CO₂)",
        "Emissions de CO₂",
        "Biomasse",
        "Electricité"
    ]
    ax_x = Axis(
        scale = x_ord,
        tick_style = {'font-weight': 'bold'}
    )
    ax_y = Axis(
        scale = y_sc,
        tick_format = "0.2f",
        orientation = "vertical",
        label = "Part du budget mondial (en %)"
    )

    # Reference graph :
    consumptions_ref = plot_multi(process_reference_data)[0]
    cons_ref = Bars(
        x = categories,
        y = consumptions_ref,
        scales = {"x": x_ord, "y": y_sc},
        colors = ["Orange"] * 4,
    )
    bar_ref = Figure(
        marks = [cons_ref],
        axes = [ax_x, ax_y],
        padding_x = 0.025,
        padding_y = 0.025,
        title = "Scénario de référence",
        animation_duration = 1000
    )

    # First group graph :
    consumptions1 = plot_multi(process_1_data)[0]
    cons1 = Bars(
        x = categories,
        y = consumptions1,
        scales = {"x": x_ord, "y": y_sc},
        colors = ["Orange"] * 4,
    )
    bar1 = Figure(
        marks = [cons1],
        axes = [ax_x, ax_y],
        padding_x = 0.025,
        padding_y = 0.025,
        title = "Scénario du groupe 1",
        animation_duration = 1000
    )

    # Second group graph :
    consumptions2 = plot_multi(process_2_data)[0]
    cons2 = Bars(
        x = categories,
        y = consumptions2,
        scales = {"x": x_ord, "y": y_sc},
        colors = ["Orange"] * 4,
    )
    bar2 = Figure(
        marks = [cons2],
        axes = [ax_x, ax_y],
        padding_x = 0.025,
        padding_y = 0.025,
        title = "Scénario du groupe 2",
        animation_duration = 1000
    )

    # Third group graph :
    consumptions3 = plot_multi(process_3_data)[0]
    cons3 = Bars(
        x = categories,
        y = consumptions3,
        scales = {"x": x_ord, "y": y_sc},
        colors = ["Orange"] * 4,
    )
    bar3 = Figure(
        marks = [cons3],
        axes = [ax_x, ax_y],
        padding_x = 0.025,
        padding_y = 0.025,
        title = "Scénario du groupe 3",
        animation_duration = 1000
    )


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


    """
    Création des cases à cocher grâce à la librairie widgets
    """

    #Liste des cartes sélectionnables pour pouvoir nommer les cases à cocher
    Liste_des_cartes = get_cards()

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
        process_1_data = process_1.compute([get_card_id(card) for card in Liste_des_widgets1 if card in get_cards()])
        #on associe ensuite ces datas en plusieurs catégories pour pouvoir traiter chaque type de données correctement
        df1 = process_1_data["vector_outputs"]
        df1_climate = process_1_data["climate_outputs"]
        float_outputs1 = process_1_data["float_outputs"]
        
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
            process_2_data = process_2.compute([get_card_id(card) for card in Liste_des_widgets2 if card in get_cards()])
            df2 = process_2_data["vector_outputs"]
            df2_climate = process_2_data["climate_outputs"]
            float_outputs2 = process_2_data["float_outputs"]

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
            process_3_data = process_3.compute([get_card_id(card) for card in Liste_des_widgets3 if card in get_cards()])
            df3 = process_3_data["vector_outputs"]
            df3_climate = process_3_data["climate_outputs"]
            float_outputs3 = process_3_data["float_outputs"]

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
        lambda btn: update_ps_figures(
            btn,
            [process_1, process_2, process_3],
            [Liste_des_widgets1, Liste_des_widgets2, Liste_des_widgets3],
            [ps_1, ps_2, ps_3]
        )
    )

    """
    Mise en forme des graphiques avec leurs cases à cocher à côté
    """

    app_layout_ref= AppLayout(
    header=None,
    left_sidebar=Choix_groupes,
    center=ps_figure_reference,
    right_sidebar=None,
    footer=None,
    align_items="center",
    width='100%'
    )
    app_layout1= AppLayout(
    header=None,
    left_sidebar=Choix_cartes1,
    center=ps_figure_1,
    right_sidebar=None,
    footer=None,
    align_items="center",
    width='100%'
    )

    app_layout2= AppLayout(
    header=None,
    left_sidebar=Choix_cartes2,
    center=ps_figure_2,
    right_sidebar=None,
    footer=None,
    align_items="center",
    width='100%'
    )
    app_layout3= AppLayout(
    header=None,
    left_sidebar=Choix_cartes3,
    center=ps_figure_3,
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

    grid = GridspecLayout(9, 2, grid_gap = "5px")
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
