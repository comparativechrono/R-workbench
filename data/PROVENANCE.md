# The data used in the R workbench

The files in this folder are copied into each user's `~/data` folder on their first visit. Users can change or delete their own copies, but the originals here are not affected.

| File | What it contains | Source and licence |
|---|---|---|
| `penguins.csv` | Measurements of 344 penguins of three species from three islands in the Palmer Archipelago, Antarctica. The columns are species, island, bill length and depth (mm), flipper length (mm), body mass (g), sex and year (2007–2009). Missing values are written as `NA`. | This is R's `datasets::penguins` (available from R 4.5 onwards), written out with `write.csv(penguins, row.names = FALSE)` in R 4.6.0 and saved without quotes. The data come from the palmerpenguins package (Horst, Hill & Gorman 2020) and were collected by Dr Kristen Gorman and the Palmer Station Long Term Ecological Research program: Gorman KB, Williams TD, Fraser WR (2014) *PLoS ONE* 9(3): e90081, doi:10.1371/journal.pone.0090081. Licence: CC0 1.0 (public domain). |
| `penguins.xlsx` | The same data as an Excel workbook. It has a sheet called `penguins` (in which missing values are empty cells) and a sheet called `about` that describes the columns. | Made from `penguins.csv` with Python's openpyxl. Licence: CC0 1.0. |
