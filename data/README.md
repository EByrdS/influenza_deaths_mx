# data
There are two files provided inside the directory **/deaths_hdf**:
. `deaths_05_18_clean_checkpoint_1.h5`
. `deaths_05_18_new_cols_checkpoint_1.h5`

The numbers `05_18` stand for the years they encompass, from 2005 to 2018. They both end 
with `checkpoint_1`, this is only helpful to differentiate between versions of the same file,
which will be usefull your you if you want to download the databases from source.

The file `clean` is the first one produced, it contains only the columns and
only rows of interest. Some trivial errors in the databases are
solved at this point: all data is stored in its correct `datatype`, 
there are no empty values and all death dates are valid.
In here, the column `death_cie10` was added to be able to filter only the codes of interest.

The file `new_cols` is the one used in the final analysis. 
It is a digested version of the file `clean`, with three more colunmns:
`new_age_group`, `day_of_year_index` and `day_global_index`.

If you want, you can create these two files from scratch. First make sure that you have
downloaded the source databases from INEGI. To do that, go under the directory
**Mortalidad-INEGI** and execute the file `download_data.py`.

Now, because the oldest databases are stored in **.dbf** format, you will need
to install `simpledbf`:

```bash
$ pip install simpledbf
```

When you have the raw databases and `simpledbf`, execute first the file `data_to_hdf.py`. It will generate the
`deaths_05_18_clean_checkpoint_1.h5`. And you should see in your console the following output:

```bash
{
  '2005': {'original': 495240, 'final': 10271}, 
  '2006': {'original': 494471, 'final': 10737}, 
  '2007': {'original': 514420, 'final': 10676}, 
  '2008': {'original': 539530, 'final': 11454}, 
  '2009': {'original': 564673, 'final': 15096}, 
  '2010': {'original': 592018, 'final': 13605}, 
  '2011': {'original': 590693, 'final': 12955}, 
  '2012': {'original': 602354, 'final': 13794}, 
  '2013': {'original': 623599, 'final': 15541}, 
  '2014': {'original': 633641, 'final': 18638}, 
  '2015': {'original': 655688, 'final': 17146}, 
  '2016': {'original': 685766, 'final': 19828}, 
  '2017': {'original': 703047, 'final': 20200}, 
  '2018': {'original': 722611, 'final': 26677}
}

Original rows: 8417751
Selected rows: 216618
```

Each year shows the number of rows (individual deaths) originally available, and the 
number of the records we stored from it in the final file.
This output is a validation method to ensure that the databases you are downloading are
the same as the ones I downloaded. The initial databases contain almost 8.5 millions rows
(deaths), and we only used 216k of them.

After you have this first *.hdf5* file, execute the file `transform_hdf_cols`.
It will digest the previous database and create the `deaths_05_18_new_cols_checkpoint_1.h5`
file, adding the three rows that we need to plot and group the data successfully.
When running this script, you should see the following output:

```bash
Original shape: (216618, 8)
Final shape: (216408, 11)
```

Use this output as a validation method, your final database should have exactly the same
shape. You can see a small decrease in the number of rows, this is because I dropped all
deaths that ocurred in 2004.

You only need the last file to run the analysis. If you want to optimize memory,
you can delete the `deaths_05_18_clean_checkpoint_1.h5` database.

> Note: By the time I created this repository (June-2020), the links to download the databases from INEGI
have no *captcha* and can be downloaded using a script. If this changes, you will have to
download them manually before you can execute the files that digest them.
