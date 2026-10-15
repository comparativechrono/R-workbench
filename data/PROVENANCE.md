# The data of the R workbench

The files in this folder are copied into each user's `~/data` folder on their first visit (the user can change or
delete their copies; the originals here stay as they are).

| File | What it is | Source and licence |
|---|---|---|
| `penguins.csv` | 344 penguins of three species from three islands of the Palmer Archipelago, Antarctica: species, island, bill length and depth (mm), flipper length (mm), body mass (g), sex, year (2007–2009). Missing values are `NA`. | R's `datasets::penguins` (R 4.5 and later), written with `write.csv(penguins, row.names = FALSE)` in R 4.6.0 and saved without quotes. The data come from the palmerpenguins package (Horst, Hill & Gorman 2020) and were collected by Dr Kristen Gorman and the Palmer Station Long Term Ecological Research program: Gorman KB, Williams TD, Fraser WR (2014) *PLoS ONE* 9(3): e90081, doi:10.1371/journal.pone.0090081. Licence: CC0 1.0 (public domain). |
| `penguins.xlsx` | The same data as an Excel workbook: a sheet `penguins` (missing values are empty cells) and a sheet `about` that describes the columns. | Made from `penguins.csv` with Python's openpyxl. Licence: CC0 1.0. |
