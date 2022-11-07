DOI: [Exploitation of Deaths Registry in Mexico to Estimate the Total Deaths by Influenza Virus: A Preparation to Estimate the Advancement of COVID-19](https://link.springer.com/chapter/10.1007/978-3-030-60884-2_35)

# A Python project to create an accurate estimation of deaths by Influenza in Mexico in 2009.

In 2009, **366** deaths were registered with a cause related to **Influenza virus**, but this work shows that a more realistic number is **_at least double_: 732**.

### Official numbers:

![Raw deaths of 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/2009_official_numbers.jpg?raw=true)

### The estimation of this project:

![Our estimate of deaths for 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/2009_our_estimate.jpg?raw=true)

## Introduction

This repository presents a simple method to estimate how many deaths of influenza were recorded as _atypical pneumonia_.
The motivation is to create a clear method on how to do the same for the COVID-19 pandemic
of 2020.

> This code was created as a final project of the _Machine Learning_ course, from the _MSc in Computer Science_ program, in _Tecnologico de Monterrey_, Mexico. We thank CONACYT for their support.

## Source of the problem

Many people are dying from the disease of COVID-19, produced by the infection of the virus SARS-CoV-2,
but it is suspected that many people who died **infected** by the **SARS-CoV-2** are not being
registered on the public reports of that disease.

Although such mismatch may be caused by different variables, it is out of the scope of this work.

Because _some_ cause of infection (or death) has to be recorded for each case, the most direct
way of recording them is _atypical pneumonia_, which is the same as saying _lung inflammation of
unknown cause_.

## Why focus on _deaths_?

A death is a tragic event, and it is an important event for health, statistics and legal reasons.
Each event creates a unique record and is thoroughly recorded, along with its reasons.

## INEGI (_The National Institute of Statiscics and Geography_, Mexico)

Each time a person dies, a death certificate is generated with many copies. One of those copies is
used to feed the yearly database of deaths. These databases are published yearly and can be
accessed by anyone.

The oldest deaths database available is from 1990. Their columns include useful information
like the date of birth, the district of living, the district of death, if the person was
using the social security plan, sex, level of studies, cause of death and many more.

The most important attribute for this work is the cause of death, which is recorded using a
standardized method to identify human health problems, [created by the World Health Organization](https://icd.who.int/browse10/2016/en).

## The International Classification of Diseases (ICD)

The World Health Organization created the ICD. This document have had revisions over time,
and this work uses the _10th_ edition (ICD-10), which was first used in 1994 and will
be replaced in 1-Jan-2022 when the oficial _11th_ version comes into effect. This means that
all records between 1994 and 2021 will have the same standard.

The codes start with a letter and then three numbers, for example:

- **B23.0:** Acute HIV infection syndrome.

Diseases that are similar have a similar code. The diseases are divided into
different levels of similarity. From general to speficic, these divisions are
the _Chapter_, _Group_, _Disease_ and _Specification_. The deaths databases contain one
column for the Chapter (`'capitulo'`), one for the Group (`grupo`) and one for the
Specification (`causa_def`), the Disease can be obtained just by trimming the last
digit of the Specification, as it was done in this project.

This work used only the following codes from Chapter X of ICD-10:

- **Chapter X:** Diseases of the respiratory system (_J00-J99_)
  1. ... (_J00_ through _J08_ were discarded)
  2. **J09**: Influenza due to identified zoonotic or pandemic influenza virus
  3. **J10**: Influenza due to identified seasonal influenza virus
  4. **J11**: Influenza, virus not identified
  5. **J12**: Viral pneumonia, not elsewhere classified
  6. **J13**: Pneumonia due to Streptococcus pneumoniae
  7. **J14**: Pneumonia due to Haemophilus influenzae
  8. **J15**: Bacterial pneumonia, not elsewhere classified
  9. **J16**: Pneumonia due to other infectious organisms, not elsewhere classified
  10. _J17_: Pneumonia in diseases classified elsewhere. (not valid as a death cause)
  11. **J18**: Pneumonia, organism unspecified
  12. ... (_J19_ trough _J99_ were not used)

It is logical to think that COVID-19 will get a code of its own, just as influenza did in 2009.
If that code is created, it will very likely belong in this same group.
Some of the codes presented have a **specific**
organism, while others clearly specify an **unspecified** organism.
So, this work grouped them in two different classifications:

| Specified pneumonia     | Unspecified pneumonia |
| ----------------------- | --------------------- |
| J09, J10, J11, J13, J14 | J12, J15, J16, J18    |

The idea is that the number of deaths recorded with codes for _Unspecified pneumonia_ will be
predictable through the years, and any changes should be reflected **also** in the deaths
by _Specified pneumonia_.

From all the selected rows and columns, the deaths by _J18_ (Pneumonia, organism unspecified)
account for 94% of the rows, and _J09_ for approximately 1.5%.

## Data Cleaning

Those records with empty values in these selected columns were dropped.
The files that do this process are inside **/data**, namely _data_to_hdf.py_ and _transform_hdf_cols.py_.
From all the available columns, only the following were selected as relevant for this work:

| Name        | Meaning                                            |
| ----------- | -------------------------------------------------- |
| `ent_resid` | State of living                                    |
| `causa_def` | Cause of death (_Specification with 4 characters_) |
| `sexo`      | Sex                                                |
| `dia_ocurr` | Day of death                                       |
| `mes_ocurr` | Month of death                                     |
| `anio_ocur` | Year of death                                      |
| `edad_agru` | Age group                                          |

### Age Groups

Only deaths between 5 and 99 years old inclusive were selected. Individuals younger than 5 years old
and older than 99 represent a different case study.
Groups of age with steps of 10 years were created:

| `new_age_group` | Age at death |
| --------------- | ------------ |
| 0               | 5-9          |
| 1               | 10-19        |
| 2               | 20-29        |
| 3               | 30-39        |
| ...             | ...          |
| 9               | 90-99        |

### Handling of time

A new column `day_of_year_index` was added, representing the day of the year as incremental number from 1 to 366
to plot the data. And another column `day_global_index` to represent the number of days passed since
31-Dec-2004, so that 1-Jan-2005 is day 1, and used this new column to graph years in sequence.

### Codes ICD-10

A new column `death_cie10` was created, using the first three digits of the column `causa_def`. (CIE stands
for ICD in spanish).

### Sex

Available values were `1` _Men_, `2` _Women_ and `99` _Unspecified_.
The rows with unspecified sex (code _99_) were dropped,
as they were too few to produce significant results in a large scale.
The remaining codes are:

| Code | Meaning |
| ---- | ------- |
| 1    | Men     |
| 2    | Women   |

## The number of deaths cycle with the seasons

The first thing to do was to visualize how the accumulated deaths for each of the days looked
throughout the years:

![Visualization of deaths from 2005 to 2008](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/1_2005_2018_visualized.jpg?raw=true)

> Blue: codes on unspecified pneumonia. Orange: Influenza and other specified pneumonia codes.

As it can be appreciated, the number of deaths increase with winter and decrease in summer months.
The general trend of deaths increase with time, very likely being attributable to
the increase of population.

The first case of **AH1N1** in Mexico was registered in 17-March-2009,
corresponding to first spike of the orange line in March 2009. The orange line before that
day shows only deaths by other organisms.

The year 2009 has an unexpected fluctuation in the unspecified deaths, this fluctiation
starts almost at the same time as the first case of Influenza, and settles down when the
spikes of Influenza dissipate.

![Closeup of the unspecified and Influenza deaths from 2005 to 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/2_2005_2009_visualized.jpg?raw=true)

The behavior of the years 2005, 2006, 2007 and 2008 was used to predict the behavior of the blue
line in 2009. This prediction was used to estimate know how many deaths of unspecified pneumonia
were unexpected.

## Adjusting for the population growth

The strategy of this work starts by compensating for the population growth.

A 28-day period with low variance of the number of deaths,
which was somewhere between late June and late August, was used
as a reference point of the entire year. The average number of deaths of those
28 days was plotted alongside the years, and an exponential regression for those points
was used to predict how that reference point would look like in 2009.

![Population growth](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/3_population_growth.png?raw=true)

> Red: Real average of deaths for the selected 28 days. Green: Exponential fit of the red line.

The reference point of previous years were lifted to the predicted point of 2009, so that all years are comparable.
This is similar as saying:
_If the total population of the previous years was similar as the population in 2009,
how would their number of deaths look like?_.

After all years have the same scale, the average of deaths across the same day on each year was computed,
using the `day_of_year_index`.

## Dividing the total population in groups

This simple method that predicts the behaviour of unspecified deaths for 2009 can
be replicated on different subgroups of the total population.

The motivation for obtainind the prediction for subgroups is that those predictions
should be more precise, and adding them up should produce a more specific number of
deviations for the global behavior.

This concept is illustrated by separating the population into men and women.

![Average of deaths between 2005-2008 adjusted to 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/4_average_deaths_men.jpg?raw=true)

> Blue: Average of deaths between 2005-2008 adjusted to the expected growth of 2009.
> Green: Polynomial fit curve of 12th degree for the blue line.

The green line is the prediction for 2009. The next graph shows the actual number of deaths in 2009:

![Real number of deaths in 2009 for men](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/unspecified_deaths_men_2009.jpg?raw=true)

A polynomial fit of a larger degree was used to better represent smaller fluctuations.
Then, the difference between the expected and the observed behavior is obtained:

![Comparison between expected and actual deaths for men in 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/comparison_predicted_actual_unspecified_men_2009.png?raw=true)

> Unspecified deaths of men in 2009. Blue: predicted behavior. Orange: actual behavior.

The positive difference between the orange and the blue lines accounts for how many deaths for the group `men`
were above the expected. The same process is done for the group `women`, and both differences are added.

The resulting deviation from the expectation was obtained from two different groups of the population.

![Unspecified deaths reconstruction](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/unspecified_deaths_reconstruction.jpg?raw=true)

> Unspecified deaths of 2009. Freen: Actual daily deaths.
> Blue: prediction for the entire population.
> Orange: Addition of the total prediction and the surplus obtained from women and men.

The orange line matches the green one as expected. Recall that this line was obtained
by adding two different surpluses, one from men and one from women. With this graph we can conclude
that all those deaths above the blue line are deviating from the expected behavior.

Now, the surplus (orange) of deaths by **Influenza** is contrasted with the actual behavior.

![Comparison between deviations and findings in 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/comparison_findings_deviations_men_women_2009.jpg?raw=true)

> 2009. Blue: Daily deaths of **Influenza**. Orange: number of unspecified deaths that
>       surpassed our prediction for each sex.

This graph is the most important of this work. The blue line accounts for the registered
Influenza deaths across 2009, it looks at first glance as if the orange line was the
polynomial fit of the blue, but it is not.
The orange line is the number of unspecified deaths that surpassed our prediction,
obtained from two different groups of the population.
Their great similarity shows their deep correlation.

**What does this mean?** It means that approximately for every death registered as **Influenza**,
there is one death registered as **Unspecified pneumonia** that is above the expectations.
In other words: The registered deaths of **Influenza** account for approximately only 50%
of the total deaths **for the same infection**.

There is an almost 1:1 ratio between registered deaths and (_possibly_) miss-classified deaths of the same virus.

## Correcting the number of deaths by Influenza

Knowing that the missclassification ratio is almost 1:1, we can see how the year 2009 would
look like if the number of deaths by Influenza was doubled (so that is shows the 100%),
and their number were compensated in the deaths by unspecified pneumonia.

![Respiratory deaths adjusted from 2005 to 2010](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/respiratory_deaths_adjusted_2005_2010.jpg?raw=true)

> 2005-2010: Blue: Adjusted daily deaths of unspecified pneumonia. Orange: adjusted daily deaths of
> Influenza.

Note that the unexpected behavior of the blue line in 2009 (the 5th cycle) has almost disappeared.

The next graph shows the same data, but without the correction. The official numbers:

![Raw deaths from 2005 to 2010](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/raw_deaths_2005_2010.jpg?raw=true)

# Running the code on your own.

The same procedure of dividing the population in groups, getting their prediction, and adding them up
can be replicated for the dimensions of state of living and age groups (`ent_resid` and `new_age_group`).

To do that, run the file `deaths_separation.py` with a change in the function call at the end:

```python
get_difference(deaths,
               'sexo', # <-- ('ent_resid', 'sexo', 'new_age_group')
               [2005, 2006, 2007, 2008], 2009,
               ['J09', 'J10', 'J11', 'J13', 'J14'],
               ['J12', 'J15', 'J16', 'J18'],
               12, 80)
```

You will see all the generated graphs for each subgroup, with the titles correctly displayed
so that you can understand what is being graphed.

The process will print accuracy measures for each of the regression lines.

# Discussion

After the adjustment, we can still see that there is a small deviation of
deaths by unspecified pneumonia in early 2009. This is probably because people
started dying of that disease some weeks before the first official case,
which makes sense if the event was unexpected at that time. The reader should be able
to deduce how to substract these deaths and locate them in the deaths by Influenza.

# What about COVID-19?

The deaths databases for the years 2019 and 2020 [have not yet been published](https://www.inegi.org.mx/programas/mortalidad/default.html#Datos_abiertos).

However, this method provides enough information and knownledge to do exactly the same
when they are published:

1. Year by year, adjust the number of deaths by Influenza, adjusting for the
   population growth.
2. When the year 2019 is correctly adjusted, we should use knowlegde on the ratio between
   specified and unspecified Influenza to substract the deaths by **Influenza** from 2020 first.
   (Because Influenza is still here).
3. Perform the presented procedure and see if the remaining deviation is a shadow of the
   deaths by COVID.
4. Get the ratio of the previous point and adjust for the number of deaths by COVID.
5. At the end we should have one oscilating blue line, one line for Influenza and a
   large line for COVID. The large line of COVID will be an accurate estimation of deaths for that
   virus.

## An alternative to waiting before the new databases are published.

We know that the deaths registered with a specified microorganism are a statistical representation of the deviation
from the norm of deaths by unspecified pneumonia, even if dividing the population into subgroups.

One of the divisions performed was by states of the nation (which you can do on your own
with the provided code). But the databases contain information of each **district**.
Performing the same procedure on Mexico City, dividing by districts, should show
the same correlation.

If the correlation between Influenza and unexpected deaths in Mexicy City is still 1:1,
then we could conclude that the ratio of representation between Mexico City and the entire nation
is the same. And we would only need the death registry of Mexico City in 2020.

Some approaches to gather that information [have been published](https://datos.nexos.com.mx/?p=1435),
but they do not cover the entire year 2020, nor 2019. They only cover some months.
However, in this work the reader should also see that the relation of 1:1 is almost consistent across
the year. So, if we find the correct ratio of deaths for COVID-19 in some period,
we should be able to **stumbly** generalize to the deaths of the entire country,
because [we can use the registered number of deaths by COVID-19 in Mexico](https://www.gob.mx/salud/documentos/datos-abiertos-152127)
and "cast a shadow" into the country. The first problem is to find how big that shadow should be.

## This is an open problem, and contributions are welcome.

You can fork this project and create a Pull Request from your branch, which would be subject
to review and happily merged. Some interesting data sources and other information are available in the following links:

- [INEGI: Open database of deaths by COVID in Mexico](https://www.gob.mx/salud/documentos/datos-abiertos-152127)
- [INEGI: Deaths databases in .dbf format](https://www.inegi.org.mx/programas/mortalidad/default.html#Microdatos)
- [INEGI: Deaths databases in .csv format](https://www.inegi.org.mx/programas/mortalidad/default.html#Datos_abiertos)
- [WHO: International Classification of Diseases 10th (ICD-10)](https://icd.who.int/browse10/2016/en)
- [nexos: What the death certificats tell us in Mexico City? (spanish)](https://datos.nexos.com.mx/?p=1388)
- [nexos: The death causes during the pandemic (covid\*) in Mexicy City (spanish)](https://datos.nexos.com.mx/?p=1435) (Here you can find a method to create the deaths database of Mexico City of 2020).
