# Code

-   calculate betweenness centrality
-   calculate the time to spread/diffusion (is this feasible for all nodes?)
-   visualize the graph in a nice way.
-   calculate clustering coefficient and graph diameter

# Report

-   complete background
-   Thorough introduction of your problem
-   Review of the relevant prior work
-   Description of the data collection/processing
-   Description of any initial findings or summary statistics from your dataset
-   Description of any mathematical background necessary for your problem
-   Formal description of any important algorithms used
-   Description of general difficulties with your problem which bear elaboration

# TODO now

## Hannes

-   hur många rör sig mellan flygplatserna. Plotta detta.
-   Hur många rör sig mellan flygplatserna baserat på degree, plotta degree mot antalet personer
-   Hur kan man skriva sambandet mellan smittad massa på olika flygplatser och hur de smittar varandra.

## Juius

-   Intern modell för hur smitta beter sig inom noderna.

-   Steg
    -   smitta externt
    -   smitta internt
    -   man blir frisk

Simuleringssteg

-   Jämför eigenvector centrality och betweenness centrality. Vilken typ av smittokurva skapar de olika metoder.
-   Vi börjar alltid med en infekterad nod och simulerar 100 steg i simuleringen. Vi plottar antalet infekterade noder mot tidssteg för detta som en point plot (ej kurva för det blir svårt att se).
-   Vi startar med 20 slumpmässiga noder ur grafen som den noden som ska vara infekterad från början. Dessa väljs ur ett spektrum från grafen som baserat på degree.
