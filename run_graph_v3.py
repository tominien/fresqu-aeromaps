from ipywidgets import Checkbox, VBox, Button, Layout, AppLayout, HTML, GridspecLayout
from bqplot import LinearScale, Lines, Axis, Figure, ColorScale, Bars, OrdinalScale
from Setup_des_graphs_v1 import plot_multi
from Setup_des_process import compute_process




def run_graph_v3():
    """
    Section qui créé les graphiques d'émissions annuelles avec les valeurs par défaut, pour qu'ensuite une fonction viens les modifier.
    """

    #initialisation des listes qui serviront pour les widgets (qui sont en fait les boutons à cocher), 
    #et de la liste qui sert d'abscisse dans le graph
    Liste_des_widgets1 = []
    Liste_des_widgets2 = []
    Liste_des_widgets3 = []
    x_ans = [2000, 2010, 2020, 2030, 2040, 2050]

    #initialisation des process avec les hypothèses du scénario de référence pour pouvoir tracer les graphiques.
    #d'où la nécessité d'initaliser les listes de widgets ci-dessus
    process_ref_data = compute_process()
    process1_data = compute_process(Liste_des_widgets1)
    process2_data = compute_process(Liste_des_widgets2)
    process3_data = compute_process(Liste_des_widgets3)

    #import des valeurs pour les différents axes du graphique
    years = process_ref_data["years"]["full_years"]
    historic_years = process_ref_data["years"]["historic_years"]
    prospective_years = process_ref_data["years"]["prospective_years"]

    #paramétrage des axes.
    sc_x = LinearScale()
    sc_y = LinearScale()
    sc_col = ColorScale(colors = ["Black", "Blue", "Yellow", "Orange", "Green", "Magenta", "Red"])
    ax_x = Axis(scale = sc_x, num_ticks = len(x_ans), tick_value = x_ans, label = "Années")
    ax_y = Axis(scale = sc_y, orientation = "vertical", label = "Emissions de CO2, en Mt")

    ##création du graphique des émissions annuelles

    #paramétrage du tracé : attribution des couleurs, des légendes, des différentes lignes
    df_ref = process_ref_data["vector_outputs"]
    df_ref_climate = process_ref_data["climate_outputs"]
    line_ref = Lines(
        x = years,
        y = [
            df_ref.loc[years,"co2_emissions_2019technology_baseline3"],
            df_ref["co2_emissions_2019technology"],
            df_ref["co2_emissions_including_aircraft_efficiency"],
            df_ref["co2_emissions_including_load_factor"],
            df_ref["co2_emissions_including_energy"],
            df_ref_climate.loc[years, "co2_emissions"] - df_ref.loc[years, "carbon_offset"]
        ],
        color = [1, 2, 3, 4, 5, 6],
        stroke_width = 0,
        fill = 'between',
        fill_colors = ["Blue", "Yellow", "Orange", "Green", "Magenta"],
        fill_opacities = [0.3, 0.3, 0.3, 0.3, 0.3],
        labels = [
            "Changement de la demande", "Efficacité technologique", "Opérations en vol", "Energies alternatives", "Compensation carbone", "Emission restantes"
        ],
        display_legend = True,
        scales = {"x" : sc_x, "y" : sc_y, "color" : sc_col}
    )

    #tracé des émissions historiques, car les lignes précédentes n'étaient que pou rla prospective
    line_ref_h = Lines(
        x = historic_years,
        y = df_ref_climate.loc[historic_years, "co2_emissions"],
        color = [0],
        scales = {"x" : sc_x, "y" : sc_y, "color" : sc_col}
    )

    #tracé de la ligne des émissions avec un scénario "business as usual" pour faire ressortir les émissions évitées
    line_ref_p = Lines(
        x = prospective_years,
        y = [
            df_ref_climate.loc[prospective_years, "co2_emissions"] - df_ref.loc[prospective_years, "carbon_offset"],
            df_ref.loc[prospective_years,"co2_emissions_2019technology_baseline3"]
        ],
        color = [6, 0],
        scales={"x" : sc_x, "y" : sc_y, "color" : sc_col}
    )

    #assemblages de tous les tracés précédents sur une même figure interactive
    fig_ref = Figure(
        marks = [line_ref, line_ref_h, line_ref_p],
        axes = [ax_x, ax_y],
        title = "Scénario de référence", 
        animation_duration = 1000,
        legend_location = "top-left",
        legend_style = {'stroke-width': 0}
    )

    #reproduction de la création du tracé pour le premier groupe
    df1 = process1_data["vector_outputs"]
    df1_climate = process1_data["climate_outputs"]
    line1 = Lines(
        x = years,
        y = [
            df1.loc[years,"co2_emissions_2019technology_baseline3"],
            df1["co2_emissions_2019technology"],
            df1["co2_emissions_including_aircraft_efficiency"],
            df1["co2_emissions_including_load_factor"],
            df1["co2_emissions_including_energy"],
            df1_climate.loc[years, "co2_emissions"] - df1.loc[years, "carbon_offset"]
        ],
        color = [1, 2, 3, 4, 5, 6],
        stroke_width = 0,
        fill = 'between',
        fill_colors = ["Blue", "Yellow", "Orange", "Green", "Magenta"],
        fill_opacities = [0.3, 0.3, 0.3, 0.3, 0.3],
        labels = [
            "Changement de la demande", "Efficacité technologique", "Opérations en vol", "Energies alternatives", "Compensation carbone", "Emission restantes"
        ],
        display_legend = True,
        scales={"x" : sc_x, "y" : sc_y, "color" : sc_col}
    )

    line1_h = Lines(
        x = historic_years,
        y = df1_climate.loc[historic_years, "co2_emissions"],
        color = [0],
        scales = {"x" : sc_x, "y" : sc_y, "color" : sc_col}
    )

    line1_p = Lines(
        x = prospective_years,
        y = [
            df1_climate.loc[prospective_years, "co2_emissions"] - df1.loc[prospective_years, "carbon_offset"],
            df1.loc[prospective_years,"co2_emissions_2019technology_baseline3"]
        ],
        color = [6, 0],
        scales = {"x" : sc_x, "y" : sc_y, "color" : sc_col}
    )

    fig1 = Figure(
        marks = [line1, line1_h, line1_p],
        axes = [ax_x, ax_y],
        title = "Scénario du groupe 1",
        animation_duration = 1000,
        legend_location = "top-left",
        legend_style = {'stroke-width': 0}
    )

    #reproduction de la création du tracé pour le deuxième groupe
    df2 = process2_data["vector_outputs"]
    df2_climate = process2_data["climate_outputs"]
    line2 = Lines(x=years, 
                y=[df2.loc[years,"co2_emissions_2019technology_baseline3"],
                    df2["co2_emissions_2019technology"],
                    df2["co2_emissions_including_aircraft_efficiency"],
                    df2["co2_emissions_including_load_factor"],
                    df2["co2_emissions_including_energy"],
                    df2_climate.loc[years, "co2_emissions"] - df2.loc[years, "carbon_offset"]],
                color=[1,2,3,4,5,6],
                stroke_width=0,
                fill='between',
                fill_colors=["Blue","Yellow","Orange","Green","Magenta"],
                fill_opacities=[0.3]*5,
                labels=["Changement de la demande","Efficacité technologique","Opérations en vol",
                        "Energies alternatives","Compensation carbone","Emission restantes"],
                display_legend=True,
                scales={"x": sc_x, "y": sc_y, "color" : sc_col},
    )

    line2_h = Lines(x=historic_years, 
                y=df2_climate.loc[historic_years, "co2_emissions"],
                color=[0], 
                scales={"x": sc_x, "y": sc_y, "color" : sc_col}
    )

    line2_p = Lines(x=prospective_years, 
                y=[df2_climate.loc[prospective_years, "co2_emissions"] - df2.loc[prospective_years, "carbon_offset"],
                    df2.loc[prospective_years,"co2_emissions_2019technology_baseline3"]],
                color=[6,0], 
                scales={"x": sc_x, "y": sc_y, "color" : sc_col},
    )
    fig2=Figure(marks=[line2,line2_h,line2_p], 
                axes=[ax_x, ax_y],
                title="Scénario du groupe 2", 
                animation_duration = 1000,
                legend_location="top-left",
                legend_style = {'stroke-width': 0})

    #reproduction de la création du tracé pour le troisième groupe
    df3 = process3_data["vector_outputs"]
    df3_climate = process3_data["climate_outputs"]
    line3 = Lines(x=years, 
                y=[df3.loc[years,"co2_emissions_2019technology_baseline3"],
                    df3["co2_emissions_2019technology"],
                    df3["co2_emissions_including_aircraft_efficiency"],
                    df3["co2_emissions_including_load_factor"],
                    df3["co2_emissions_including_energy"],
                    df3_climate.loc[years, "co2_emissions"] - df3.loc[years, "carbon_offset"]],
                color=[1,2,3,4,5,6],
                stroke_width=0,
                fill='between',
                fill_colors=["Blue","Yellow","Orange","Green","Magenta"],
                fill_opacities=[0.3]*5,
                labels=["Changement de la demande","Efficacité technologique","Opérations en vol",
                        "Energies alternatives","Compensation carbone","Emission restantes"],
                display_legend=True,
                scales={"x": sc_x, "y": sc_y, "color" : sc_col},
    )

    line3_h = Lines(x=historic_years, 
                y=df3_climate.loc[historic_years, "co2_emissions"],
                color=[0], 
                scales={"x": sc_x, "y": sc_y, "color" : sc_col}
    )

    line3_p = Lines(x=prospective_years, 
                y=[df3_climate.loc[prospective_years, "co2_emissions"] - df3.loc[prospective_years, "carbon_offset"],
                    df3.loc[prospective_years,"co2_emissions_2019technology_baseline3"]],
                color=[6,0], 
                scales={"x": sc_x, "y": sc_y, "color" : sc_col},
    )

    fig3=Figure(marks=[line3,line3_h,line3_p], 
                axes=[ax_x, ax_y],
                title= "Scénario du groupe 3",
                animation_duration = 1000,legend_location="top-left",legend_style = {'stroke-width': 0})

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
    Liste_des_cartes=['Allouer un budget carbone','Réglementation et mesures économiques','Sobriété',
                    'Compensation des émissions','Nouveaux vecteurs énergétiques','Report modal',
                    'Efficacité des opérations','Technologie']

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
        process1_data=compute_process(Liste_des_widgets1)
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
            process2_data=compute_process(Liste_des_widgets2)
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
            process3_data=compute_process(Liste_des_widgets3)
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
    Update_btn.on_click(on_btn_click)

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
    grid[slice(0, 2), 0] = app_layout_ref
    grid[slice(0, 2), 1] = app_layout1
    grid[slice(2, 4), 0] = app_layout2
    grid[slice(2, 4), 1] = app_layout3
    grid[4, slice(None)] = centre
    grid[slice(5, 7), 0] = bar_ref
    grid[slice(5, 7), 1] = bar1
    grid[slice(7, 9), 0] = bar2
    grid[slice(7, 9), 1] = bar3

    return grid
