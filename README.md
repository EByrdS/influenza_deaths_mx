# A Python project to create an accurate estimation of deaths by Influenza in Mexico in 2009.
In 2009, **366** deaths were registered with a cause related to **Influenza virus**, but this work shows that a more realistic number is ***at least double*: 732**.

### Official numbers:
![Raw deaths of 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/2009_official_numbers.jpg?raw=true)

### The estimation of this project:
![Our estimate of deaths for 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/2009_our_estimate.jpg?raw=true)

## Introduction
In this repository, I present a method to estimate how many deaths of influenza were recorded as *atypical pneumonia*.
The motivation is to create a clear method on how to do the same with regards to the COVID-19 pandemic
of 2020.

> This is the code of my final project in the course *Machine Learning*, from the *MSc in Computer Science* program, in *Tecnologico de Monterrey*, Mexico. I would like to thank CONACYT for their support.

## Source of the problem
Many people are dying from the disease of COVID-19, produced by the infection of the virus SARS-CoV-2,
but it is a known fact that many people who died **infected** by the **SARS-CoV-2** are not being
taken into account on the public reports of the disease.

This mismatch might be because of lack of tests or their economic costs, but we will not dive into that.

Because *some* cause of infection (or death) has to be recorded for each case, the most convenient
way of recording them is *atypical pneumonia*, which is the same as saying *lung inflammation of
unknown cause*.

## Why focus on *deaths*?
A death is a tragic event, and it is an important event for health, statistics and legal reasons.
Each event creates a unique record and is thoroughly recorded, along with its reasons.

## INEGI (*The National Institute of Statiscics and Geography*, Mexico)
Each time a person dies, a death certificate is generated with many copies. One of those copies is 
used to feed the yearly database of deaths. These databases are published yearly and can be 
accessed by anyone (*thanks for the public access to information!*).

The oldest deaths database available is from 1990. Their columns include manny useful information
like the date of birth, the district of living, the district of death, if the person was
using the social security plan, sex, level of studies, cause of death and many more.

The most important attributr is the cause of death, which is recorded using a 
standardized method to identify human health problems, created by the World Health Organization.

## The International Classification of Diseases (ICD)
The World Health Organization created the ICD. This document have had revisions over time,
we are currently using the *10th* edition (ICD-10), which was first used in 1994 and will
be replaced in 1-Jan-2022 when the oficial *11th* version comes into effect. This means that
all records between 1994 and 2021 will have the same standard.

The codes start with a letter and then three numbers, for example:
* **B23.0:** Acute HIV infection syndrome.

Diseases that are similar have a similar code. The diseases are divided into
different levels of similarity. From general to speficic, these divisions are
the *Chapter*, *Group*, *Disease* and *Specification*. The deaths databases contain one
column for the Chapter (`'capitulo'`), one for the Group (`grupo`) and one for the
Specification (`causa_def`), the Disease can be obtained just by trimming the last
digit of the Specification, which was done in this project.

For the project, I used only the following codes from Chapter X of ICD-10:
* **Chapter X:** Diseases of the respiratory system (*J00-J99*)
  1. ... (I discarded *J00* through *J08*)
  2. **J09**: Influenza due to identified zoonotic or pandemic influenza virus
  3. **J10**: Influenza due to identified seasonal influenza virus
  4. **J11**: Influenza, virus not identified
  5. **J12**: Viral pneumonia, not elsewhere classified
  6. **J13**: Pneumonia due to Streptococcus pneumoniae
  7. **J14**: Pneumonia due to Haemophilus influenzae
  8. **J15**: Bacterial pneumonia, not elsewhere classified
  9. **J16**: Pneumonia due to other infectious organisms, not elsewhere classified
  10. *J17*: Pneumonia in diseases classified elsewhere. (not valid as a death cause)
  11. **J18**: Pneumonia, organism unspecified
  12. ... (*J19* trough *J99* were not used)

It is logical to think that COVID-19 will get a code of its own, just as influenza did in 2009.
This code will very likely belong in this group. Some of the codes presented have a **specific**
organism, while others clearly specify an **unspecified** organism. I grouped them in two groups:

|Specified pneumonia | Unspecified pneumonia|
|--------|--------|
| J09, J10, J11, J13, J14 | J12, J15, J16, J18 |

The idea is that the number of deaths recorded with codes for *Unspecified pneumonia* will be
predictable through the years, and any changes should be reflected **also** in the deaths
by *Specified pneumonia*.

From all the selected rows and columns, the deaths by *J18* (Pneumonia, organism unspecified)
account for 94% of the rows, and *J09* for 1.5%, approximately.

## Data Cleaning
All record with empty values in the selected columns were dropped. 
The files that do this process are inside **/data**, namely *data_to_hdf.py* and *transform_hdf_cols.py*.
From all the available columns I selected only the following:

|Name | Meaning|
|----|----|
|`ent_resid`|State of living|
|`causa_def`|Cause of death (*Specification with 4 characters*)|
|`sexo`|Sex|
|`dia_ocurr`|Day of death|
|`mes_ocurr`|Month of death|
|`anio_ocur`|Year of death|
|`edad_agru`|Age group|

### Age Groups
We selected only deaths between 5 and 99 years old inclusive. Individuals younger than 5 years old
and older than 99 represent a different case study.
From the original age groups, there was a different group each 5 years of age. I found these
groups too small, so I created groups of age with steps of 10 years:

|`new_age_group`|Age at death|
|-----|-----|
|0|5-9|
|1|10-19|
|2|20-29|
|3|30-39|
|...|...|
|9|90-99|

### Handling of time
I added a column `day_of_year_index` representing the day of the year as incremental number from 1 to 366
to plot the data. And another column `day_global_index` to represent the number of days passed since
31-Dec-2004, so that 1-Jan-2005 is day 1, and used this new column to graph years in sequence.

### Codes ICD-10
I created a new column `death_cie10` using the first three digits of the column `causa_def`. (CIE stands
for ICD in spanish).

### Sex
I dropped the rows with unspecified sex, code 99. They were too few to produce significant results
in a large scale. The remaining codes are:

|Code | Meaning|
|-----|-----|
|1|Men|
|2|Women|

## The number of deaths cycle with the seasons
The first thing to do was to visualize how the accumulated deaths for each of the days looked
throughout the years:

![Visualization of deaths from 2005 to 2008](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/1_2005_2018_visualized.jpg?raw=true)
> Blue: codes on unspecified pneumonia. Orange: Influenza and other specified pneumonia codes.

As you can see, the number of deaths increase with winter and decrease in summer.
You can also see that the general trend of deaths increase with time, this is probably due to
the increase of population.

The first spike of the orange line occurrs somewhere in March 2009. The first case of 
**AH1N1** in Mexico was registered in 17-March-2009, so it checks out. The orange line before that
day shows only deaths by other organisms.

The year 2009 has an unexpected fluctuation in the unspecified deaths, this fluctiation
starts almost at the same time that the first case of Influenza, and settles down when the
spikes of Influenza dissipate.

![Closeup of the unspecified and Influenza deaths from 2005 to 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/2_2005_2009_visualized.jpg?raw=true)

I use the behavior of the years 2005, 2006, 2007 and 2008 to predict the behavior of the blue
line in 2009. And use this prediction to accurately know how many deaths of unspecified pneumonia
are unexpected.

## Adjusting for the population growth
We cannot train a model on the years 2005-2008 as they are, because the model would
predit a small number of deaths, I first needed to compensate for the population growth.

I selected a 28-day period of the year with low variance of the number of deaths,
which was somewhere between late June and late August, and used
that timelapse as a reference point of the entire year. The average number of deaths of those
28 days was plotted alongside the years, and I created an exponential regression for those points,
to be able to predict how that point would look like in 2009.

![Population growth](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/3_population_growth.png?raw=true)

> Red: Real average of deaths for the selected 28 days. Green: Exponential fit of the red line.

Using the exponential fit, I now predict how this selected average would look line between lateJult and
late August of 2009. Now I only need to multiply the previous years, each by a different number,
so that all averages are equal to the one expected in 2009. This is similar as saying: 
*If the total population of the previous years was similar as the population in 2009,
how would their number of deaths look like?*.

Now that all previous years have the same scale, I selected the average of deaths across each year,
for each day of the year using the `day_of_year_index`.

## Divigind the total population in groups
Now that I have a method to predict the behavior of unspecified deaths for 2009,
I applied this method for different subgroups of the total population of rows.

The idea is that if I obtain the exact number of how much deaths differ from their
prediction, and add them up, I should obtain a much more specific number of
deviations for the global behavior.

I chose to illustratte this concept by separating the population into two groups: men and women.

![Average of deaths between 2005-2008 adjusted to 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/4_average_deaths_men.jpg?raw=true)

> Blue: Average of deaths between 2005-2008 adjusted to the expected growth of 2009.
Green: Polynomial fit curve of 12th degree for the blue line.

The green line is the prediction for 2009. The next graph shows the actual number of deaths in 2009:

![Real number of deaths in 2009 for men](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/unspecified_deaths_men_2009.jpg?raw=true)

I added a polynomial fit of a larger degree to grasp better the smaller fluctuations.
Now I can substract the difference between the expected and the observed behavior:

![Comparison between expected and actual deaths for men in 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/comparison_predicted_actual_unspecified_men_2009.png?raw=true)

> Unspecified deaths of men in 2009. Blue: predicted behavior. Orange: actual behavior.

The positive difference between the orange and the blue lines accounts for how many deaths for men
were above the expected. We can do the same process for the group of women, and add both differences.

We know have the deviation from the expectetion obtained from two different groups of the population.
If we predict the behavior of the entire population and add these differences, we should get
a very close approximation of the actual behavior.

![Unspecified deaths reconstruction](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/unspecified_deaths_reconstruction.jpg?raw=true)

> Unspecified deaths of 2009. Freen: Actual daily deaths. 
Blue: prediction for the entire population. 
Orange: Addition of the total prediction and the surplus obtained from women and men.

The orange line matches the green one as expected. But recall that this line was obtained
by adding two different surpluses, one from men and one from women. With this graph we can conclude
that all those deaths above the blue line are deviating from the expected behavior. Good so far.

We now contrast the surplus (orange) with the actual behavior of deaths by **Influenza**.
Rumble of drums...

![Comparison between deviations and findings in 2009](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/comparison_findings_deviations_men_women_2009.jpg?raw=true)

> 2009. Blue: Daily deaths of **Influenza**. Orange: number of unspecified deaths that
surpassed our prediction for each sex.

This graph is the most important of this work. The blue line accounts for the registered
Influenza deaths across 2009, it looks at first glance as if the orange line was the
polynomial fit of the blue, but it is not. 
The orange line is the number of unspecified deaths that surpassed our prediction
(obtained from two different groups of the population!).
They match almost perfectly.

**What does this mean?** It means that approximately for every death registered as **Influenza**,
there is one death registered as **Unspecified pneumonia** that should not be there.
Said in other words: The registered deaths of **Influenza** account for approximately only 50%
of the total deaths **for the same infection**.

There is an almost 1:1 ratio between registered deaths and miss-classified deaths of the same virus.

## Correcting the number of deaths by Influenza
Now that we know that the ratio is almost 1:1, I will show how the year 2009 would
look like if the number of deaths by Influenza was doubled (so that is shows the 100%).
and their number are compensated in the deaths by unspecified pneumonia.

![Respiratory deaths adjusted from 2005 to 2010](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/respiratory_deaths_adjusted_2005_2010.jpg?raw=true)

> 2005-2010: Blue: Adjusted daily deaths of unspecified pneumonia. Orange: adjusted daily deaths of
Influenza.

Note that the unexpected behavior of the blue line in 2009 (the 5th cycle) has almost disappeared.

The next graph shows the same data, but without the correction. The official numbers:

![Raw deaths from 2005 to 2010](https://github.com/EByrdS/influenza_deaths_mx/blob/master/images/raw_deaths_2005_2010.jpg?raw=true)

# Running the code on your own.
Remember the columns `ent_resid` and `new_age_group` (State of living and age in groups of 10)?
You can use those columns to do the same procedure, but instead of dividing by sex as in this
example, you can divide by any of those other two dimension.

To do that, run the file `deaths_separation.py` with a change in the function call at the end:
```python
get_difference(deaths,
               'sexo', # ('ent_resid', 'sexo', 'new_age_group')
               [2005, 2006, 2007, 2008], 2009,
               ['J09', 'J10', 'J11', 'J13', 'J14'],
               ['J12', 'J15', 'J16', 'J18'],
               12, 80)
```

You will see all the generated graphs for each subgroup, with the titles correctly displayed
so that you can understand what is being graphed.

The process will print accuracy measures for each of the regression lines,
which you might find useful.

# Discussion
After the adjustment, we can still see that there is a small deviation of
deaths by unspecified pneumonia in earl 2009. This is probably because people
started dying of that disease some weeks before the first official case,
which makes sense if the event was unexpected at that time. The reader should be able
to deduce how to substract these deaths and locate them in the deaths by Influenza.

However, doing that is not necesarrily important, since 2009 was more than 10 years ago.
What is important is that **the number of deaths can be adjusted if we know the relation
between specified and unspecified deaths for the same organism**, which in this case was 1:1.

# What about COVID-19?
The deaths databases for the years 2019 and 2020 [have not yet been published](https://www.inegi.org.mx/programas/mortalidad/default.html#Datos_abiertos).

However, this method provides enough information and knownledge to do exactly the same
when they are published. The methodology should be as follows:

1. Year by year, adjust the number of deaths by Influenza, so that we can better predict the 
population growth.
2. When the year 2019 is correctly adjusted, we should use knowlegde on the ratio between
specified and unspecified Influenza to substract the deaths by **Influenza** from 2020 first.
(Because Influenza is still here).
3. Perform the presented procedure and see if the remaining deviation is a shadow of the
deaths by COVID.
4. Get the ratio of the previous point and adjust for the number of deaths by COVID.
5. At the end we should have one nice oscilating blue line, one line for Influenza and a
large line for COVID. The large line of COVID will be an accurate estimation of deaths for that 
virus.

## I can not wait until the databases are published.
We know that the registered deaths are a statistical representation of the deviation
from the norm of deaths by unspecified pneumonia, even if we divide the population into subgroups.

One of the divisions performed was by states of the nation (which you can do on your own
with the provided code). But the databases contain information of each **district**.
If we perform the same procedure on the City of Mexico, dividing by districts, we should expect
the same correlation.

If the correlation between Influenza and unexpected deaths in Mexicy City is still 1:1,
then we could conclude that the ratio of representation between Mexico City and the entire nation
is the same. And we would only need the death registry of Mexico City in 2020.

Some approaches to gather this information [have been published](https://datos.nexos.com.mx/?p=1435),
but they do not cover the entire year 2020, nor 2019. They only cover some months.
However, in this work the reader should also see that the relation of 1:1 is almost consistent across
the year. So, if we find the correct ratio of deaths for COVID-19 in some period,
we should be able to **stumbly** generalize to the deaths of the entire country,
because [we can use the registered number of deaths by COVID-19 in Mexico](https://www.gob.mx/salud/documentos/datos-abiertos-152127)
and "cast a shadow" into the country. The first problem is to find how big that shadow should be.

## This is an open problem, and contributions are welcome.
You can fork this project and create a Pull Request from your branch, which would be subject
to review and happily merged. Some interesting data sources and other information are available in the following links:

* [INEGI: Open database of deaths by COVID in Mexico](https://www.gob.mx/salud/documentos/datos-abiertos-152127)
* [INEGI: Deaths databases in .dbf format](https://www.inegi.org.mx/programas/mortalidad/default.html#Microdatos)
* [INEGI: Deaths databases in .csv format](https://www.inegi.org.mx/programas/mortalidad/default.html#Datos_abiertos)
* [WHO: International Classification of Diseases 10th (ICD-10)](https://icd.who.int/browse10/2016/en)
* [nexos: What the death certificats tell us in Mexico City? (spanish)](https://datos.nexos.com.mx/?p=1388)
* [nexos: The death causes during the pandemic (covid*) in Mexicy City (spanish)](https://datos.nexos.com.mx/?p=1435) (Here you can find a method to create the deaths database of Mexico City of 2020).

Thak you for reading this project, have fun and be safe!
