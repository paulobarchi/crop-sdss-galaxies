# Crop SDSS Galaxies (fits and images)

Script to crop SDSS galaxies by their Petrosian radius and produce fits
or png files.

If you try to run the script (`python crop-galaxies.py`) it will tell 
the necessary arguments.

The file `sample_example.csv` has a sample with an example for the 
input file (csv) in the accepted format.

## Input data

To get the input data as required, you need to:
* Upload a file with the aimed ObjIds (one per line) to CasJobs (https://skyserver.sdss.org/casjobs/) and obtain a table from it, let's call it "mydb.mytable".
* Then you can perform the query below at CasJobs (https://skyserver.sdss.org/casjobs/), with the context set to be "DR7/500" (can work on other contexts, although, this is used only for DR7).

```
SELECT
  m.ObjId,
  s.ra,s.dec,
  p.rowc_r,p.colc_r,p.b,p.l,p.petroRad_r,p.petroR50_r,
  p.deVAB_r,p.run,p.camcol,p.rerun, p.field, p.petroMag_r, w.seeing_r,
  p.rowc_r, p.colc_r,p.b,p.l,p.fieldID,
  s.z,
  ((3.14 * POWER(p.petroR50_r,2) ) / (3.14 * POWER(w.seeing_r/2, 2))) as areasRatio
    INTO mydb.my_table from mydb.my_table as m
    JOIN PhotoObj as p on m.ObjId = p.objid
    JOIN RunQA as w on p.fieldID = w.fieldID
    JOIN SpecObj as s on s.bestobjid = m.ObjId
``` 

## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```
