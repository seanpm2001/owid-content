# %% [markdown]
# # Source-switching Inequality Data Explorer
# This code creates the tsv file for the main inequality explorer in the inequality topic page, available [here](https://owid.cloud/admin/explorers/preview/inequality)

import textwrap
from pathlib import Path

import numpy as np

# %%
import pandas as pd

PARENT_DIR = Path(__file__).parent.parent.parent.parent.absolute()
outfile = PARENT_DIR / "explorers" / "inequality.explorer.tsv"

# %% [markdown]
# ## Google sheets auxiliar data
# These spreadsheets provide with different details depending on each type of welfare measure or tables considered.

# %%
# MULTI-SOURCE
# Read Google sheets
sheet_id = "1wcFsNZCEn_6SJ05BFkXKLUyvCrnigfR8eeemGKgAYsI"

# All the tables sheet (this contains PIP, WID and LIS dataset information)
sheet_name = "all_the_tables"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
all_the_tables = pd.read_csv(url, keep_default_na=False)

# NOTE: We decided to drop LIS from the main inequality explorer

# WORLD INEQUALITY DATABASE
# Read Google sheets
sheet_id = "18T5IGnpyJwb8KL9USYvME6IaLEcYIo26ioHCpkDnwRQ"

# Welfare type sheet
sheet_name = "welfare"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
wid_welfare = pd.read_csv(url, keep_default_na=False)

# Tables sheet
sheet_name = "tables"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
wid_tables = pd.read_csv(url, keep_default_na=False)

# WORLD BANK POVERTY AND INEQUALITY PLATFORM
# Read Google sheets
sheet_id = "17KJ9YcvfdmO_7-Sv2Ij0vmzAQI6rXSIqHfJtgFHN-a8"

# Relative poverty sheet
sheet_name = "povlines_rel"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
pip_povlines_rel = pd.read_csv(url)

# Survey type sheet
sheet_name = "table"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
pip_tables = pd.read_csv(url)

# %% [markdown]
# ## Header
# General settings of the explorer are defined here, like the title, subtitle, default country selection, publishing status and others.

# %%
# The header is defined as a dictionary first and then it is converted into a index-oriented dataframe
header_dict = {
    "explorerTitle": "Economic Inequality Data Explorer",
    "selection": [
        "Chile",
        "Brazil",
        "South Africa",
        "United States",
        "France",
        "China",
    ],
    "explorerSubtitle": "",
    "isPublished": "true",
    "googleSheet": "",
    "wpBlockId": "57760",
    "entityType": "country or region",
    "pickerColumnSlugs": "gini decile10_share palma_ratio headcount_ratio_50_median p0p100_gini_pretax p90p100_share_pretax palma_ratio_pretax",
}

# Index-oriented dataframe
df_header = pd.DataFrame.from_dict(header_dict, orient="index", columns=None)
# Assigns a cell for each entity separated by comma (like in `selection`)
df_header = df_header[0].apply(pd.Series)

# %% [markdown]
# ## Tables
# Variables are grouped by type of welfare to iterate by different survey types at the same time. The output is the list of all the variables being used in the explorer, with metadata.
# ### Tables for variables not showing breaks between surveys
# These variables consider a continous series, without breaks due to changes in surveys' methodology

# %%

###########################################################################################
# WORLD BANK POVERTY AND INEQUALITY PLATFORM
###########################################################################################
sourceName = "World Bank Poverty and Inequality Platform (2022)"
dataPublishedBy = "World Bank. (2022). Poverty and Inequality Platform (version 20220909_2017_01_02_PROD) [Data set]. World Bank Group. https://pip.worldbank.org/. Accessed  2022-10-03."
sourceLink = "https://pip.worldbank.org/"
tolerance = 5
colorScaleEqualSizeBins = "true"
new_line = "<br><br>"

additional_description = new_line.join(
    [
        "Depending on the country and year, the data relates to income measured after taxes and benefits, or consumption, per capita. 'Per capita' means that the incomes of each household are attributed equally to each member of the household (including children).",
        "Non-market sources of income, including food grown by subsistence farmers for their own consumption, are taken into account.",
    ]
)

notes_title = "NOTES ON HOW WE PROCESSED THIS INDICATOR"

processing_description = new_line.join(
    [
        "For a small number of country-year observations, the World Bank PIP data contains two estimates: one based on income data and one based on consumption data. In these cases we keep only the consumption estimate in order to obtain a single series for each country.",
        "You can find the data with all available income and consumption data points, including these overlapping estimates, in our <a href='https://github.com/owid/poverty-data#a-global-dataset-of-poverty-and-inequality-measures-prepared-by-our-world-in-data-from-the-world-banks-poverty-and-inequality-platform-pip-database'>complete dataset</a> of the World Bank PIP data.",
    ]
)
ppp_description = "The data is measured in international-$ at 2017 prices – this adjusts for inflation and for differences in the cost of living between countries."

# Table generation
df_tables_pip = pd.DataFrame()
j = 0

for survey in range(len(pip_tables)):
    # Define country as entityName
    df_tables_pip.loc[j, "name"] = "Country"
    df_tables_pip.loc[j, "slug"] = "country"
    df_tables_pip.loc[j, "type"] = "EntityName"
    df_tables_pip.loc[j, "tableSlug"] = pip_tables["table_name"][survey]
    j += 1

    # Define year as Year
    df_tables_pip.loc[j, "name"] = "Year"
    df_tables_pip.loc[j, "slug"] = "year"
    df_tables_pip.loc[j, "type"] = "Year"
    df_tables_pip.loc[j, "tableSlug"] = pip_tables["table_name"][survey]
    j += 1

    # Gini coefficient
    df_tables_pip.loc[j, "name"] = f"Gini coefficient (World Bank PIP)"
    df_tables_pip.loc[j, "slug"] = f"gini"
    df_tables_pip.loc[j, "description"] = new_line.join(
        [
            "The Gini coefficient measures inequality on a scale from 0 to 1. Higher values indicate higher inequality.",
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables_pip.loc[j, "unit"] = np.nan
    df_tables_pip.loc[j, "shortUnit"] = np.nan
    df_tables_pip.loc[j, "type"] = "Numeric"
    df_tables_pip.loc[
        j, "colorScaleNumericBins"
    ] = "0.25;0.3;0.35;0.4;0.45;0.5;0.55;0.6"
    df_tables_pip.loc[j, "colorScaleNumericMinValue"] = 1
    df_tables_pip.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables_pip.loc[j, "colorScaleScheme"] = "Oranges"
    df_tables_pip.loc[j, "tableSlug"] = pip_tables["table_name"][survey]
    j += 1

    # Share of the top 10%
    df_tables_pip.loc[
        j, "name"
    ] = f"{pip_tables.text[survey].capitalize()} share of the richest 10% (World Bank PIP)"
    df_tables_pip.loc[j, "slug"] = f"decile10_share"
    df_tables_pip.loc[j, "description"] = new_line.join(
        [
            f"The share of after tax income or consumption received by the richest 10% of the population.",
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables_pip.loc[j, "unit"] = "%"
    df_tables_pip.loc[j, "shortUnit"] = "%"
    df_tables_pip.loc[j, "type"] = "Numeric"
    df_tables_pip.loc[j, "colorScaleNumericBins"] = "20;25;30;35;40;45;50"
    df_tables_pip.loc[j, "colorScaleNumericMinValue"] = 100
    df_tables_pip.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables_pip.loc[j, "colorScaleScheme"] = "OrRd"
    df_tables_pip.loc[j, "tableSlug"] = pip_tables["table_name"][survey]
    j += 1

    # Share of the bottom 50%
    df_tables_pip.loc[
        j, "name"
    ] = f"{pip_tables.text[survey].capitalize()} share of the poorest 50% (World Bank PIP)"
    df_tables_pip.loc[j, "slug"] = f"bottom50_share"
    df_tables_pip.loc[j, "description"] = new_line.join(
        [
            f"The share of after tax income or consumption received by the poorest 50% of the population.",
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables_pip.loc[j, "unit"] = "%"
    df_tables_pip.loc[j, "shortUnit"] = "%"
    df_tables_pip.loc[j, "type"] = "Numeric"
    df_tables_pip.loc[j, "colorScaleNumericBins"] = "15;20;25;30;35"
    df_tables_pip.loc[j, "colorScaleNumericMinValue"] = 100
    df_tables_pip.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables_pip.loc[j, "colorScaleScheme"] = "Blues"
    df_tables_pip.loc[j, "tableSlug"] = pip_tables["table_name"][survey]
    j += 1

    # Palma ratio
    df_tables_pip.loc[j, "name"] = f"Palma ratio (World Bank PIP)"
    df_tables_pip.loc[j, "slug"] = f"palma_ratio"
    df_tables_pip.loc[j, "description"] = new_line.join(
        [
            f"The Palma ratio is a measure of inequality that divides the share received by the richest 10% by the share of the poorest 40%. Higher values indicate higher inequality.",
            additional_description,
            notes_title,
            processing_description,
        ]
    )
    df_tables_pip.loc[j, "unit"] = np.nan
    df_tables_pip.loc[j, "shortUnit"] = np.nan
    df_tables_pip.loc[j, "type"] = "Numeric"
    df_tables_pip.loc[j, "colorScaleNumericBins"] = "0.5;1;1.5;2;2.5;3;3.5;4;4.5;5;5.5"
    df_tables_pip.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables_pip.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrBr"
    df_tables_pip.loc[j, "tableSlug"] = pip_tables["table_name"][survey]
    j += 1

    # Headcount ratio (rel)
    df_tables_pip.loc[j, "name"] = f"Share in relative poverty (World Bank PIP)"
    df_tables_pip.loc[j, "slug"] = f"headcount_ratio_50_median"
    df_tables_pip.loc[j, "description"] = new_line.join(
        [
            f"The share of population with after tax income or consumption below 50% of the median. Relative poverty reflects the extent of inequality within the bottom of the distribution.",
            additional_description,
            notes_title,
            "Measures of relative poverty are not directly available in the World Bank PIP data. To calculate this metric we take the median income or consumption for the country and year, calculate a relative poverty line – in this case 50% of the median – and then run a specific query on the PIP API to return the share of population below that line.",
            processing_description,
        ]
    )
    df_tables_pip.loc[j, "unit"] = "%"
    df_tables_pip.loc[j, "shortUnit"] = "%"
    df_tables_pip.loc[j, "type"] = "Numeric"
    df_tables_pip.loc[j, "colorScaleNumericBins"] = "3;6;9;12;15;18;21;24;27"
    df_tables_pip.loc[j, "colorScaleNumericMinValue"] = 0
    df_tables_pip.loc[j, "colorScaleEqualSizeBins"] = "true"
    df_tables_pip.loc[j, "colorScaleScheme"] = "YlOrBr"
    df_tables_pip.loc[j, "tableSlug"] = pip_tables["table_name"][survey]
    j += 1

df_tables_pip["sourceName"] = sourceName
df_tables_pip["dataPublishedBy"] = dataPublishedBy
df_tables_pip["sourceLink"] = sourceLink
df_tables_pip["tolerance"] = tolerance

###########################################################################################
# WORLD INEQUALITY DATABASE (WID)
###########################################################################################

# Table generation

sourceName = "World Inequality Database (WID.world) (2023)"
dataPublishedBy = "World Inequality Database (WID), https://wid.world"
sourceLink = "https://wid.world"
tolerance = 5
new_line = "<br><br>"

additional_description = new_line.join(
    [
        "The data is estimated from a combination of household surveys, tax records and national accounts data. This combination can provide a more accurate picture of the incomes of the richest, which tend to be captured poorly in household survey data alone.",
        "These underlying data sources are not always available. For some countries, observations are extrapolated from data relating to other years, or are sometimes modeled based on data observed in other countries.",
    ]
)
ppp_description = "The data is measured in international-$ at 2022 prices – this adjusts for inflation and for differences in the cost of living between countries."

df_tables_wid = pd.DataFrame()
j = 0

for tab in range(len(wid_tables)):
    # Define country as entityName
    df_tables_wid.loc[j, "name"] = "Country"
    df_tables_wid.loc[j, "slug"] = "country"
    df_tables_wid.loc[j, "type"] = "EntityName"
    j += 1

    # Define year as Year
    df_tables_wid.loc[j, "name"] = "Year"
    df_tables_wid.loc[j, "slug"] = "year"
    df_tables_wid.loc[j, "type"] = "Year"
    j += 1

    for wel in range(len(wid_welfare)):
        # Gini coefficient
        df_tables_wid.loc[
            j, "name"
        ] = f"Gini coefficient {wid_welfare['title'][wel]} (World Inequality Database)"
        df_tables_wid.loc[j, "slug"] = f"p0p100_gini_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[j, "description"] = new_line.join(
            [
                f"The Gini coefficient measures inequality on a scale from 0 to 1. Higher values indicate higher inequality.",
                wid_welfare["description"][wel],
                additional_description,
            ]
        )
        df_tables_wid.loc[j, "unit"] = np.nan
        df_tables_wid.loc[j, "shortUnit"] = np.nan
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_gini"][wel]
        df_tables_wid.loc[j, "colorScaleNumericMinValue"] = 1
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "Oranges"
        j += 1

        # Share of the top 10%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 10% {wid_welfare['title'][wel]} (World Inequality Database)"
        df_tables_wid.loc[j, "slug"] = f"p90p100_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[j, "description"] = new_line.join(
            [
                f"The share of {wid_welfare['welfare_type'][wel]} received by the richest 10% of the population.",
                wid_welfare["description"][wel],
                additional_description,
            ]
        )
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_top10"][wel]
        df_tables_wid.loc[j, "colorScaleNumericMinValue"] = 100
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "OrRd"
        j += 1

        # Share of the top 1%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 1% {wid_welfare['title'][wel]} (World Inequality Database)"
        df_tables_wid.loc[j, "slug"] = f"p99p100_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[j, "description"] = new_line.join(
            [
                f"The share of {wid_welfare['welfare_type'][wel]} received by the richest 1% of the population.",
                wid_welfare["description"][wel],
                additional_description,
            ]
        )
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_top1"][wel]
        df_tables_wid.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "OrRd"
        j += 1

        # Share of the top 0.1%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 0.1% {wid_welfare['title'][wel]} (World Inequality Database)"
        df_tables_wid.loc[j, "slug"] = f"p99_9p100_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[j, "description"] = new_line.join(
            [
                f"The share of {wid_welfare['welfare_type'][wel]} received by the richest 0.1% of the population.",
                wid_welfare["description"][wel],
                additional_description,
            ]
        )
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_top01"][wel]
        df_tables_wid.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "OrRd"
        j += 1

        # Share of the bottom 50%
        df_tables_wid.loc[
            j, "name"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the poorest 50% {wid_welfare['title'][wel]} (World Inequality Database)"
        df_tables_wid.loc[j, "slug"] = f"p0p50_share_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[j, "description"] = new_line.join(
            [
                f"The share of {wid_welfare['welfare_type'][wel]} received by the poorest 50% of the population.",
                wid_welfare["description"][wel],
                additional_description,
            ]
        )
        df_tables_wid.loc[j, "unit"] = "%"
        df_tables_wid.loc[j, "shortUnit"] = "%"
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare["scale_bottom50"][
            wel
        ]
        df_tables_wid.loc[j, "colorScaleNumericMinValue"] = 100
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "Blues"
        j += 1

        # Palma ratio
        df_tables_wid.loc[
            j, "name"
        ] = f"Palma ratio {wid_welfare['title'][wel]} (World Inequality Database)"
        df_tables_wid.loc[j, "slug"] = f"palma_ratio_{wid_welfare['slug'][wel]}"
        df_tables_wid.loc[j, "description"] = new_line.join(
            [
                f"The Palma ratio is a measure of inequality that divides the share received by the richest 10% by the share of the poorest 40%. Higher values indicate higher inequality.",
                wid_welfare["description"][wel],
                additional_description,
            ]
        )
        df_tables_wid.loc[j, "unit"] = np.nan
        df_tables_wid.loc[j, "shortUnit"] = np.nan
        df_tables_wid.loc[j, "type"] = "Numeric"
        df_tables_wid.loc[j, "colorScaleNumericBins"] = wid_welfare[
            "scale_palma_ratio"
        ][wel]
        df_tables_wid.loc[j, "colorScaleNumericMinValue"] = 0
        df_tables_wid.loc[j, "colorScaleEqualSizeBins"] = "true"
        df_tables_wid.loc[j, "colorScaleScheme"] = "YlOrBr"
        j += 1

    df_tables_wid["tableSlug"] = wid_tables["name"][tab]

df_tables_wid["sourceName"] = sourceName
df_tables_wid["dataPublishedBy"] = dataPublishedBy
df_tables_wid["sourceLink"] = sourceLink
df_tables_wid["tolerance"] = tolerance

# Keep only pretax national values for WID:
df_tables_wid = df_tables_wid[
    ~(df_tables_wid["slug"].str.contains("posttax_nat"))
].reset_index(drop=True)

# Concatenate all the tables into one
df_tables = pd.concat([df_tables_pip, df_tables_wid], ignore_index=True)
# Make tolerance integer (to not break the parameter in the platform)
df_tables["tolerance"] = df_tables["tolerance"].astype("Int64")

# %% [markdown]
# ### Grapher views
# Similar to the tables, this creates the grapher views by grouping by types of variables and then running by welfare type.

# %%
# Grapher table generation

###########################################################################################
# WORLD INEQUALITY DATABASE (WID)
###########################################################################################

# Grapher table generation

yAxisMin = 0
mapTargetTime = 2019

df_graphers_wid = pd.DataFrame()

j = 0

for tab in range(len(wid_tables)):
    for wel in range(len(wid_welfare)):
        # Gini coefficient
        df_graphers_wid.loc[j, "title"] = f"Gini coefficient"
        df_graphers_wid.loc[j, "ySlugs"] = f"p0p100_gini_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[
            j, "Data Radio"
        ] = f"{wid_welfare['radio_option'][wel]} ({wid_tables['source_name'][tab]})"
        df_graphers_wid.loc[j, "Indicator Dropdown"] = "Gini coefficient"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"The Gini coefficient measures inequality on a scale from 0 to 1. Higher values indicate higher inequality. {wid_welfare['subtitle_ineq'][wel]}"
        df_graphers_wid.loc[j, "note"] = wid_welfare["note"][wel]
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # Share of the top 10%
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 10%"
        df_graphers_wid.loc[j, "ySlugs"] = f"p90p100_share_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[
            j, "Data Radio"
        ] = f"{wid_welfare['radio_option'][wel]} ({wid_tables['source_name'][tab]})"
        df_graphers_wid.loc[j, "Indicator Dropdown"] = "Share of the richest 10%"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"The share of income received by the richest 10% of the population. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = wid_welfare["note"][wel]
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # Share of the top 1%
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 1%"
        df_graphers_wid.loc[j, "ySlugs"] = f"p99p100_share_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[
            j, "Data Radio"
        ] = f"{wid_welfare['radio_option'][wel]} ({wid_tables['source_name'][tab]})"
        df_graphers_wid.loc[j, "Indicator Dropdown"] = "Share of the richest 1%"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"The share of income received by the richest 1% of the population. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = wid_welfare["note"][wel]
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # Share of the top 0.1%
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the richest 0.1%"
        df_graphers_wid.loc[j, "ySlugs"] = f"p99_9p100_share_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[
            j, "Data Radio"
        ] = f"{wid_welfare['radio_option'][wel]} ({wid_tables['source_name'][tab]})"
        df_graphers_wid.loc[j, "Indicator Dropdown"] = "Share of the richest 0.1%"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"The share of income received by the richest 0.1% of the population. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = wid_welfare["note"][wel]
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # Share of the bottom 50%
        df_graphers_wid.loc[
            j, "title"
        ] = f"{wid_welfare['welfare_type'][wel].capitalize()} share of the poorest 50%"
        df_graphers_wid.loc[j, "ySlugs"] = f"p0p50_share_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[
            j, "Data Radio"
        ] = f"{wid_welfare['radio_option'][wel]} ({wid_tables['source_name'][tab]})"
        df_graphers_wid.loc[j, "Indicator Dropdown"] = "Share of the poorest 50%"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"The share of income received by the poorest 50% of the population. {wid_welfare['subtitle'][wel]}"
        df_graphers_wid.loc[j, "note"] = wid_welfare["note"][wel]
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

        # # P90/P10
        # df_graphers_wid.loc[
        #     j, "title"
        # ] = f"P90/P10 ratio"
        # df_graphers_wid.loc[j, "ySlugs"] = f"p90_p10_ratio_{wid_welfare['slug'][wel]}"
        # df_graphers_wid.loc[
        #     j, "Data Radio"
        # ] = f"{wid_welfare['radio_option'][wel]} ({wid_tables['source_name'][tab]})"
        # df_graphers_wid.loc[j, "Indicator Dropdown"] = "P90/P10"
        # df_graphers_wid.loc[
        #     j, "subtitle"
        # ] = f"P90 and P10 are the levels of {wid_welfare['welfare_type'][wel]} below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. {wid_welfare['subtitle'][wel]}"
        # df_graphers_wid.loc[j, "note"] = f"wid_welfare['note'][wel]"
        # df_graphers_wid.loc[j, "type"] = np.nan
        # df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        # df_graphers_wid.loc[j, "hasMapTab"] = "true"
        # df_graphers_wid.loc[j, "tab"] = "map"
        # j += 1

        # # P90/P50
        # df_graphers_wid.loc[
        #     j, "title"
        # ] = f"P90/P50 ratio"
        # df_graphers_wid.loc[j, "ySlugs"] = f"p90_p50_ratio_{wid_welfare['slug'][wel]}"
        # df_graphers_wid.loc[
        #     j, "Data Radio"
        # ] = f"{wid_welfare['radio_option'][wel]} ({wid_tables['source_name'][tab]})"
        # df_graphers_wid.loc[j, "Indicator Dropdown"] = "P90/P50"
        # df_graphers_wid.loc[
        #     j, "subtitle"
        # ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median {wid_welfare['welfare_type'][wel]}. {wid_welfare['subtitle'][wel]}"
        # df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        # df_graphers_wid.loc[j, "type"] = np.nan
        # df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        # df_graphers_wid.loc[j, "hasMapTab"] = "true"
        # df_graphers_wid.loc[j, "tab"] = "map"
        # j += 1

        # # P50/P10
        # df_graphers_wid.loc[
        #     j, "title"
        # ] = f"P50/P10 ratio"
        # df_graphers_wid.loc[j, "ySlugs"] = f"p50_p10_ratio_{wid_welfare['slug'][wel]}"
        # df_graphers_wid.loc[
        #     j, "Data Radio"
        # ] = f"{wid_welfare['radio_option'][wel]} ({wid_tables['source_name'][tab]})"
        # df_graphers_wid.loc[j, "Indicator Dropdown"] = "P50/P10"
        # df_graphers_wid.loc[
        #     j, "subtitle"
        # ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median {wid_welfare['welfare_type'][wel]} is two times higher than that of someone just falling in the poorest tenth of the population. {wid_welfare['subtitle'][wel]}"
        # df_graphers_wid.loc[j, "note"] = f"{wid_welfare['note'][wel]}"
        # df_graphers_wid.loc[j, "type"] = np.nan
        # df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        # df_graphers_wid.loc[j, "hasMapTab"] = "true"
        # df_graphers_wid.loc[j, "tab"] = "map"
        # j += 1

        # # Palma ratio
        df_graphers_wid.loc[j, "title"] = f"Palma ratio"
        df_graphers_wid.loc[j, "ySlugs"] = f"palma_ratio_{wid_welfare['slug'][wel]}"
        df_graphers_wid.loc[
            j, "Data Radio"
        ] = f"{wid_welfare['radio_option'][wel]} ({wid_tables['source_name'][tab]})"
        df_graphers_wid.loc[j, "Indicator Dropdown"] = "Palma ratio"
        df_graphers_wid.loc[
            j, "subtitle"
        ] = f"The Palma ratio is a measure of inequality that divides the share received by the richest 10% by the share of the poorest 40%. Higher values indicate higher inequality. {wid_welfare['subtitle_ineq'][wel]}"
        df_graphers_wid.loc[j, "note"] = wid_welfare["note"][wel]
        df_graphers_wid.loc[j, "type"] = np.nan
        df_graphers_wid.loc[j, "selectedFacetStrategy"] = np.nan
        df_graphers_wid.loc[j, "hasMapTab"] = "true"
        df_graphers_wid.loc[j, "tab"] = "map"
        j += 1

    df_graphers_wid["tableSlug"] = wid_tables["name"][tab]

# Keep only pretax national values for WID:
df_graphers_wid = df_graphers_wid[
    df_graphers_wid["ySlugs"].str.contains("pretax")
].reset_index(drop=True)

# %% [markdown]
# Add yAxisMin and mapTargetTime
df_graphers_wid["yAxisMin"] = yAxisMin
df_graphers_wid["mapTargetTime"] = mapTargetTime

###########################################################################################
# WORLD BANK POVERTY AND INEQUALITY PLATFORM
###########################################################################################
yAxisMin = 0
mapTargetTime = 2019

df_graphers_pip = pd.DataFrame()

j = 0

for survey in range(len(pip_tables)):
    # Gini coefficient
    df_graphers_pip.loc[j, "title"] = f"Gini coefficient"
    df_graphers_pip.loc[j, "ySlugs"] = f"gini"
    df_graphers_pip.loc[
        j, "Data Radio"
    ] = f"{pip_tables['dropdown_option'][survey]} ({pip_tables['source_name'][tab]})"
    df_graphers_pip.loc[j, "Indicator Dropdown"] = "Gini coefficient"
    df_graphers_pip.loc[j, "tableSlug"] = f"{pip_tables.table_name[survey]}"
    df_graphers_pip.loc[
        j, "subtitle"
    ] = f"The Gini coefficient measures inequality on a scale from 0 to 1. Higher values indicate higher inequality. Depending on the country and year, the data relates to income measured after taxes and benefits, or consumption, per capita."
    df_graphers_pip.loc[j, "note"] = ""
    df_graphers_pip.loc[j, "type"] = np.nan
    df_graphers_pip.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers_pip.loc[j, "hasMapTab"] = "true"
    df_graphers_pip.loc[j, "tab"] = "map"
    j += 1

    # Share of the top 10%
    df_graphers_pip.loc[
        j, "title"
    ] = f"{pip_tables.text[survey].capitalize()} share of the richest 10%"
    df_graphers_pip.loc[j, "ySlugs"] = f"decile10_share"
    df_graphers_pip.loc[
        j, "Data Radio"
    ] = f"{pip_tables['dropdown_option'][survey]} ({pip_tables['source_name'][tab]})"
    df_graphers_pip.loc[j, "Indicator Dropdown"] = "Share of the richest 10%"
    df_graphers_pip.loc[j, "tableSlug"] = f"{pip_tables.table_name[survey]}"
    df_graphers_pip.loc[
        j, "subtitle"
    ] = f"The share of after tax income or consumption received by the richest 10% of the population."
    df_graphers_pip.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to income measured after taxes and benefits, or consumption, per capita."
    df_graphers_pip.loc[j, "type"] = np.nan
    df_graphers_pip.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers_pip.loc[j, "hasMapTab"] = "true"
    df_graphers_pip.loc[j, "tab"] = "map"
    j += 1

    # Share of the bottom 50%
    df_graphers_pip.loc[
        j, "title"
    ] = f"{pip_tables.text[survey].capitalize()} share of the poorest 50%"
    df_graphers_pip.loc[j, "ySlugs"] = f"bottom50_share"
    df_graphers_pip.loc[
        j, "Data Radio"
    ] = f"{pip_tables['dropdown_option'][survey]} ({pip_tables['source_name'][tab]})"
    df_graphers_pip.loc[j, "Indicator Dropdown"] = "Share of the poorest 50%"
    df_graphers_pip.loc[j, "tableSlug"] = f"{pip_tables.table_name[survey]}"
    df_graphers_pip.loc[
        j, "subtitle"
    ] = f"The share of after tax income or consumption received by the poorest 50% of the population."
    df_graphers_pip.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to income measured after taxes and benefits, or consumption, per capita."
    df_graphers_pip.loc[j, "type"] = np.nan
    df_graphers_pip.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers_pip.loc[j, "hasMapTab"] = "true"
    df_graphers_pip.loc[j, "tab"] = "map"
    j += 1

    # # P90/P10
    # df_graphers_pip.loc[j, "title"] = f"P90/P10 ratio"
    # df_graphers_pip.loc[j, "ySlugs"] = f"p90_p10_ratio"
    # df_graphers_pip.loc[
    #     j, "Data Radio"
    # ] = f"{pip_tables['dropdown_option'][survey]} ({pip_tables['source_name'][tab]})"
    # df_graphers_pip.loc[j, "Indicator Dropdown"] = "P90/P10"
    # df_graphers_pip.loc[j, "tableSlug"] = f"{pip_tables.table_name[survey]}"
    # df_graphers_pip.loc[
    #     j, "subtitle"
    # ] = f"P90 and P10 are the levels of {pip_tables.text[survey]} below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population."
    # df_graphers_pip.loc[
    #     j, "note"
    # ] = f"Depending on the country and year, the data relates to disposable {pip_tables.text[survey]} per capita."
    # df_graphers_pip.loc[j, "type"] = np.nan
    # df_graphers_pip.loc[j, "selectedFacetStrategy"] = np.nan
    # df_graphers_pip.loc[j, "hasMapTab"] = "true"
    # df_graphers_pip.loc[j, "tab"] = "map"
    # j += 1

    # # P90/P50
    # df_graphers_pip.loc[j, "title"] = f"P90/P50 ratio"
    # df_graphers_pip.loc[j, "ySlugs"] = f"p90_p50_ratio"
    # df_graphers_pip.loc[
    #     j, "Data Radio"
    # ] = f"{pip_tables['dropdown_option'][survey]} ({pip_tables['source_name'][tab]})"
    # df_graphers_pip.loc[j, "Indicator Dropdown"] = "P90/P50"
    # df_graphers_pip.loc[j, "tableSlug"] = f"{pip_tables.table_name[survey]}"
    # df_graphers_pip.loc[
    #     j, "subtitle"
    # ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median {pip_tables.text[survey]}."
    # df_graphers_pip.loc[
    #     j, "note"
    # ] = f"Depending on the country and year, the data relates to disposable {pip_tables.text[survey]} per capita."
    # df_graphers_pip.loc[j, "type"] = np.nan
    # df_graphers_pip.loc[j, "selectedFacetStrategy"] = np.nan
    # df_graphers_pip.loc[j, "hasMapTab"] = "true"
    # df_graphers_pip.loc[j, "tab"] = "map"
    # j += 1

    # # P50/P10
    # df_graphers_pip.loc[j, "title"] = f"P50/P10 ratio"
    # df_graphers_pip.loc[j, "ySlugs"] = f"p50_p10_ratio"
    # df_graphers_pip.loc[
    #     j, "Data Radio"
    # ] = f"{pip_tables['dropdown_option'][survey]} ({pip_tables['source_name'][tab]})"
    # df_graphers_pip.loc[j, "Indicator Dropdown"] = "P50/P10"
    # df_graphers_pip.loc[j, "tableSlug"] = f"{pip_tables.table_name[survey]}"
    # df_graphers_pip.loc[
    #     j, "subtitle"
    # ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median {pip_tables.text[survey]} is two times higher than that of someone just falling in the poorest tenth of the population."
    # df_graphers_pip.loc[
    #     j, "note"
    # ] = f"Depending on the country and year, the data relates to disposable {pip_tables.text[survey]} per capita."
    # df_graphers_pip.loc[j, "type"] = np.nan
    # df_graphers_pip.loc[j, "selectedFacetStrategy"] = np.nan
    # df_graphers_pip.loc[j, "hasMapTab"] = "true"
    # df_graphers_pip.loc[j, "tab"] = "map"
    # j += 1

    # Palma ratio
    df_graphers_pip.loc[j, "title"] = f"Palma ratio"
    df_graphers_pip.loc[j, "ySlugs"] = f"palma_ratio"
    df_graphers_pip.loc[
        j, "Data Radio"
    ] = f"{pip_tables['dropdown_option'][survey]} ({pip_tables['source_name'][tab]})"
    df_graphers_pip.loc[j, "Indicator Dropdown"] = "Palma ratio"
    df_graphers_pip.loc[j, "tableSlug"] = f"{pip_tables.table_name[survey]}"
    df_graphers_pip.loc[
        j, "subtitle"
    ] = f"The Palma ratio is a measure of inequality that divides the share received by the richest 10% by the share of the poorest 40%. Higher values indicate higher inequality. Depending on the country and year, the data relates to income measured after taxes and benefits, or consumption, per capita."
    df_graphers_pip.loc[j, "note"] = ""
    df_graphers_pip.loc[j, "type"] = np.nan
    df_graphers_pip.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers_pip.loc[j, "hasMapTab"] = "true"
    df_graphers_pip.loc[j, "tab"] = "map"
    j += 1

    # Headcount ratio (rel)
    df_graphers_pip.loc[j, "title"] = "Share of people in relative poverty"
    df_graphers_pip.loc[j, "ySlugs"] = f"headcount_ratio_50_median"
    df_graphers_pip.loc[
        j, "Data Radio"
    ] = f"{pip_tables['dropdown_option'][survey]} ({pip_tables['source_name'][tab]})"
    df_graphers_pip.loc[j, "Indicator Dropdown"] = f"Share in relative poverty"
    df_graphers_pip.loc[j, "tableSlug"] = f"{pip_tables.table_name[survey]}"
    df_graphers_pip.loc[
        j, "subtitle"
    ] = f"The share of population with after tax income or consumption below 50% of the median. Relative poverty reflects the extent of inequality within the bottom of the distribution."
    df_graphers_pip.loc[
        j, "note"
    ] = f"Depending on the country and year, the data relates to income measured after taxes and benefits, or consumption, per capita."
    df_graphers_pip.loc[j, "type"] = np.nan
    df_graphers_pip.loc[j, "selectedFacetStrategy"] = np.nan
    df_graphers_pip.loc[j, "hasMapTab"] = "true"
    df_graphers_pip.loc[j, "tab"] = "map"
    j += 1

# Add yAxisMin and mapTargetTime
df_graphers_pip["yAxisMin"] = yAxisMin
df_graphers_pip["mapTargetTime"] = mapTargetTime

# We are removing LIS from this main explorer
# ###########################################################################################
# # LUXEMBOURG INCOME STUDY (LIS)
# ###########################################################################################

# yAxisMin = 0
# mapTargetTime = 2019

# df_graphers_lis = pd.DataFrame()

# j = 0

# for tab in range(len(lis_tables)):
#     for wel in range(len(lis_welfare)):
#         for eq in range(len(lis_equivalence_scales)):
#             # Gini coefficient
#             df_graphers_lis.loc[
#                 j, "title"
#             ] = f"Gini coefficient"
#             df_graphers_lis.loc[
#                 j, "ySlugs"
#             ] = f"gini_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
#             df_graphers_lis.loc[
#                 j, "Data Radio"
#             ] = f"{lis_tables['source_name'][tab]} - {lis_welfare['welfare_type'][wel].capitalize()} {lis_welfare['title'][wel]}"
#             df_graphers_lis.loc[j, "Indicator Dropdown"] = "Gini coefficient"
#             df_graphers_lis.loc[
#                 j, "equivalized"
#             ] = f"{lis_equivalence_scales['text'][eq]}"
#             df_graphers_lis.loc[
#                 j, "subtitle"
#             ] = f"The Gini coefficient measures inequality on a scale between 0 and 1, where higher values indicate greater inequality. {lis_welfare['subtitle'][wel]}"
#             df_graphers_lis.loc[j, "note"] = f"{lis_equivalence_scales['note'][eq]}"
#             df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
#             df_graphers_lis.loc[j, "hasMapTab"] = "true"
#             df_graphers_lis.loc[j, "tab"] = "map"
#             j += 1

#             # Share of the top 10%
#             df_graphers_lis.loc[
#                 j, "title"
#             ] = f"{lis_welfare['welfare_type'][wel].capitalize()} share of the richest 10%"
#             df_graphers_lis.loc[
#                 j, "ySlugs"
#             ] = f"share_p100_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
#             df_graphers_lis.loc[
#                 j, "Data Radio"
#             ] = f"{lis_tables['source_name'][tab]} - {lis_welfare['welfare_type'][wel].capitalize()} {lis_welfare['title'][wel]}"
#             df_graphers_lis.loc[j, "Indicator Dropdown"] = "Share of the richest 10%"
#             df_graphers_lis.loc[
#                 j, "equivalized"
#             ] = f"{lis_equivalence_scales['text'][eq]}"
#             df_graphers_lis.loc[
#                 j, "subtitle"
#             ] = f"This is the {lis_welfare['welfare_type'][wel]} of the richest 10% as a share of total {lis_welfare['welfare_type'][wel]}. {lis_welfare['subtitle'][wel]}"
#             df_graphers_lis.loc[j, "note"] = f"{lis_equivalence_scales['note'][eq]}"
#             df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
#             df_graphers_lis.loc[j, "hasMapTab"] = "true"
#             df_graphers_lis.loc[j, "tab"] = "map"
#             j += 1

#             # Share of the bottom 50%
#             df_graphers_lis.loc[
#                 j, "title"
#             ] = f"{lis_welfare['welfare_type'][wel].capitalize()} share of the poorest 50%"
#             df_graphers_lis.loc[
#                 j, "ySlugs"
#             ] = f"share_bottom50_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
#             df_graphers_lis.loc[
#                 j, "Data Radio"
#             ] = f"{lis_tables['source_name'][tab]} - {lis_welfare['welfare_type'][wel].capitalize()} {lis_welfare['title'][wel]}"
#             df_graphers_lis.loc[j, "Indicator Dropdown"] = "Share of the poorest 50%"
#             df_graphers_lis.loc[
#                 j, "equivalized"
#             ] = f"{lis_equivalence_scales['text'][eq]}"
#             df_graphers_lis.loc[
#                 j, "subtitle"
#             ] = f"This is the {lis_welfare['welfare_type'][wel]} of the poorest 50% as a share of total {lis_welfare['welfare_type'][wel]}. {lis_welfare['subtitle'][wel]}"
#             df_graphers_lis.loc[j, "note"] = f"{lis_equivalence_scales['note'][eq]}"
#             df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
#             df_graphers_lis.loc[j, "hasMapTab"] = "true"
#             df_graphers_lis.loc[j, "tab"] = "map"
#             j += 1

#             # P90/P10
#             df_graphers_lis.loc[
#                 j, "title"
#             ] = f"P90/P10 ratio"
#             df_graphers_lis.loc[
#                 j, "ySlugs"
#             ] = f"p90_p10_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
#             df_graphers_lis.loc[
#                 j, "Data Radio"
#             ] = f"{lis_tables['source_name'][tab]} - {lis_welfare['welfare_type'][wel].capitalize()} {lis_welfare['title'][wel]}"
#             df_graphers_lis.loc[j, "Indicator Dropdown"] = "P90/P10"
#             df_graphers_lis.loc[
#                 j, "equivalized"
#             ] = f"{lis_equivalence_scales['text'][eq]}"
#             df_graphers_lis.loc[
#                 j, "subtitle"
#             ] = f"P90 and P10 are the levels of {lis_welfare['welfare_type'][wel]} below which 90% and 10% of the population live, respectively. This variable gives the ratio of the two. It is a measure of inequality that indicates the gap between the richest and poorest tenth of the population. {lis_welfare['subtitle'][wel]}"
#             df_graphers_lis.loc[j, "note"] = f"{lis_equivalence_scales['note'][eq]}"
#             df_graphers_lis.loc[j, "type"] = np.nan
#             df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
#             df_graphers_lis.loc[j, "hasMapTab"] = "true"
#             df_graphers_lis.loc[j, "tab"] = "map"
#             j += 1

#             # P90/P50
#             df_graphers_lis.loc[
#                 j, "title"
#             ] = f"P90/P50 ratio"
#             df_graphers_lis.loc[
#                 j, "ySlugs"
#             ] = f"p90_p50_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
#             df_graphers_lis.loc[
#                 j, "Data Radio"
#             ] = f"{lis_tables['source_name'][tab]} - {lis_welfare['welfare_type'][wel].capitalize()} {lis_welfare['title'][wel]}"
#             df_graphers_lis.loc[j, "Indicator Dropdown"] = "P90/P50"
#             df_graphers_lis.loc[
#                 j, "equivalized"
#             ] = f"{lis_equivalence_scales['text'][eq]}"
#             df_graphers_lis.loc[
#                 j, "subtitle"
#             ] = f"The P90/P50 ratio measures the degree of inequality within the richest half of the population. A ratio of 2 means that someone just falling in the richest tenth of the population has twice the median {lis_welfare['welfare_type'][wel]}. {lis_welfare['subtitle'][wel]}"
#             df_graphers_lis.loc[j, "note"] = f"{lis_equivalence_scales['note'][eq]}"
#             df_graphers_lis.loc[j, "type"] = np.nan
#             df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
#             df_graphers_lis.loc[j, "hasMapTab"] = "true"
#             df_graphers_lis.loc[j, "tab"] = "map"
#             j += 1

#             # P50/P10
#             df_graphers_lis.loc[
#                 j, "title"
#             ] = f"P50/P10 ratio"
#             df_graphers_lis.loc[
#                 j, "ySlugs"
#             ] = f"p50_p10_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
#             df_graphers_lis.loc[
#                 j, "Data Radio"
#             ] = f"{lis_tables['source_name'][tab]} - {lis_welfare['welfare_type'][wel].capitalize()} {lis_welfare['title'][wel]}"
#             df_graphers_lis.loc[j, "Indicator Dropdown"] = "P50/P10"
#             df_graphers_lis.loc[
#                 j, "equivalized"
#             ] = f"{lis_equivalence_scales['text'][eq]}"
#             df_graphers_lis.loc[
#                 j, "subtitle"
#             ] = f"The P50/P10 ratio measures the degree of inequality within the poorest half of the population. A ratio of 2 means that the median {lis_welfare['welfare_type'][wel]} is two times higher than that of someone just falling in the poorest tenth of the population. {lis_welfare['subtitle'][wel]}"
#             df_graphers_lis.loc[j, "note"] = f"{lis_equivalence_scales['note'][eq]}"
#             df_graphers_lis.loc[j, "type"] = np.nan
#             df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
#             df_graphers_lis.loc[j, "hasMapTab"] = "true"
#             df_graphers_lis.loc[j, "tab"] = "map"
#             j += 1

#             # # Palma ratio
#             df_graphers_lis.loc[
#                 j, "title"
#             ] = f"Palma ratio"
#             df_graphers_lis.loc[
#                 j, "ySlugs"
#             ] = f"palma_ratio_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
#             df_graphers_lis.loc[
#                 j, "Data Radio"
#             ] = f"{lis_tables['source_name'][tab]} - {lis_welfare['welfare_type'][wel].capitalize()} {lis_welfare['title'][wel]}"
#             df_graphers_lis.loc[j, "Indicator Dropdown"] = "Palma ratio"
#             df_graphers_lis.loc[
#                 j, "equivalized"
#             ] = f"{lis_equivalence_scales['text'][eq]}"
#             df_graphers_lis.loc[
#                 j, "subtitle"
#             ] = f"The Palma ratio is the share of total {lis_welfare['welfare_type'][wel]} of the top 10% divided by the share of the bottom 40%. {lis_welfare['subtitle'][wel]}"
#             df_graphers_lis.loc[j, "note"] = f"{lis_equivalence_scales['note'][eq]}"
#             df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
#             df_graphers_lis.loc[j, "hasMapTab"] = "true"
#             df_graphers_lis.loc[j, "tab"] = "map"
#             j += 1

#             # Headcount ratio (rel)
#             df_graphers_lis.loc[
#                 j, "title"
#             ] = f"Relative poverty: Share of people below 50% of the median income"
#             df_graphers_lis.loc[
#                 j, "ySlugs"
#             ] = f"headcount_ratio_50_median_{lis_welfare['slug'][wel]}_{lis_equivalence_scales['slug'][eq]}"
#             df_graphers_lis.loc[
#                 j, "Data Radio"
#             ] = f"{lis_tables['source_name'][tab]} - {lis_welfare['welfare_type'][wel].capitalize()} {lis_welfare['title'][wel]}"
#             df_graphers_lis.loc[
#                 j, "Indicator Dropdown"
#             ] = f"Share in relative poverty (< 50% of the median)"
#             df_graphers_lis.loc[
#                 j, "equivalized"
#             ] = f"{lis_equivalence_scales['text'][eq]}"
#             df_graphers_lis.loc[
#                 j, "subtitle"
#             ] = f"Relative poverty is measured in terms of a poverty line that rises and falls over time with average incomes – in this case set at 50% of the median {lis_welfare['welfare_type'][wel]}. {lis_welfare['subtitle'][wel]}"
#             df_graphers_lis.loc[j, "note"] = f"{lis_equivalence_scales['note'][eq]}"
#             df_graphers_lis.loc[j, "type"] = np.nan
#             df_graphers_lis.loc[j, "selectedFacetStrategy"] = np.nan
#             df_graphers_lis.loc[j, "hasMapTab"] = "true"
#             df_graphers_lis.loc[j, "tab"] = "map"
#             j += 1

#     df_graphers_lis["tableSlug"] = lis_tables["name"][tab]

# # Keep only equivalized data
# df_graphers_lis = df_graphers_lis[
#     df_graphers_lis["equivalized"] == "equivalized"
# ].reset_index(drop=True)
# # Drop equivalized column
# df_graphers_lis = df_graphers_lis.drop(columns=["equivalized"])


# # Add yAxisMin and mapTargetTime
# df_graphers_lis["yAxisMin"] = yAxisMin
# df_graphers_lis["mapTargetTime"] = mapTargetTime

# Concatenate all the graphers dataframes
# df_graphers = pd.concat(
#     [df_graphers_pip, df_graphers_wid, df_graphers_lis], ignore_index=True
# )
df_graphers = pd.concat([df_graphers_wid, df_graphers_pip], ignore_index=True)

# %% [markdown]
# Final adjustments to the graphers table: add `relatedQuestion` link and `defaultView`:

# %%
# Add related question link
df_graphers["relatedQuestionText"] = np.nan
df_graphers["relatedQuestionUrl"] = np.nan

# Make mapTargetTime integer (to not break the parameter in the platform)
df_graphers["mapTargetTime"] = df_graphers["mapTargetTime"].astype("Int64")

# Select one default view
df_graphers.loc[
    (df_graphers["Data Radio"] == "World Inequality Database - Income before tax")
    & (df_graphers["Indicator Dropdown"] == "Gini coefficient"),
    ["defaultView"],
] = "true"


# %% [markdown]
# ## Explorer generation
# Here, the header, tables and graphers dataframes are combined to be shown in for format required for OWID data explorers.

# %%
# Define list of variables to iterate: table names (from table dataframe)
table_list = list(df_tables["tableSlug"].unique())

# Header is converted into a tab-separated text
header_tsv = df_header.to_csv(sep="\t", header=False)

# Graphers table is converted into a tab-separated text
graphers_tsv = df_graphers
graphers_tsv = graphers_tsv.to_csv(sep="\t", index=False)

# This table is indented, to follow explorers' format
graphers_tsv_indented = textwrap.indent(graphers_tsv, "\t")

# The dataframes are combined, including tables and links to the datasets
with open(outfile, "w", newline="\n", encoding="utf-8") as f:
    f.write(header_tsv)
    f.write("\ngraphers\n" + graphers_tsv_indented)

    for tab in table_list:
        table_tsv = (
            df_tables[df_tables["tableSlug"] == tab].copy().reset_index(drop=True)
        )
        table_tsv = table_tsv.drop(columns=["tableSlug"])
        table_tsv = table_tsv.to_csv(sep="\t", index=False)
        table_tsv_indented = textwrap.indent(table_tsv, "\t")
        f.write(
            "\ntable\t"
            + all_the_tables.loc[all_the_tables["name"] == tab, "link"].item()
            + "\t"
            + tab
        )
        f.write("\ncolumns\t" + tab + "\n" + table_tsv_indented)
