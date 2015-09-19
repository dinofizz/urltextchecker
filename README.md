# urltextchecker
Python script which searches the HTML for a given URL for specific text. Sends email if the text is/is not found (configurable).

##Requirements
See the requirement.txt for the required packages (available from pip)

##Usage examples

I want to know when the Realforce 87U Tenkeyless 55g (Black) is back in stock. To check this I run the script with the 'inverse' switch so that I am emailed when the text "NO STOCK" is no longer found on the page. This script is run as a cron job.

```python urltextchecker.py -u "http://www.elitekeyboards.com/products.php?sub=topre_keyboards,rftenkeyless&pid=rf_se18t0" -t "NO STOCK" -e "user@example.com" -s "Realforce 87U 55g is IN STOCK!"```
