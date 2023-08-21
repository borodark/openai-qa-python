## zillow data scrape
Select all text on the prperty page of zillo, copy, paste to file z4 and run:

`grep -v -f exclude < z4 | awk 'NF' | tee z10.txt`

Add more to `exclude` file if necessary 
