#!/bin/bash
# run_404grab.sh
# This script will run the 404grab.py script, which will generate an excel spreadsheet of 404 links.
# It will then email the current report, and delete ones in the directory that are older than 15 days.

# Load Bash Profile
. ~/.bash_profile

# Get the present working directory.
WORK_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
CURRENT_DATE=$(date +"%Y.%m.%d")

# Run the python script and generate the report
echo "Generating Report..."
python3.4 "$WORK_DIRECTORY"404grab.py
if [ $? -eq 0 ]
then
    echo "Report generated."
else
    echo "ERROR: Running script failed! Make sure python is installed/python script intact." >&2
    exit 1
fi

# Email Report
echo "Emailing report..."
mutt -s "404 Report for $CURRENT_DATE" -a "${WORK_DIRECTORY}reports/urls_spreadsheet.${CURRENT_DATE}.xls" -- EMAILADDRESS@MAIL.COM < /dev/null
mutt -s "404 Report for $CURRENT_DATE" -a "${WORK_DIRECTORY}reports/urls_spreadsheet.${CURRENT_DATE}.xls" -- EMAILADDRESS@MAIL.COM < /dev/null
mutt -s "404 Report for $CURRENT_DATE" -a "${WORK_DIRECTORY}reports/urls_spreadsheet.${CURRENT_DATE}.xls" -- EMAILADDRESS@MAIL.COM < /dev/null
if [ $? -eq 0 ]
then
    echo "Report emailed."
else
    echo "ERROR: email failed! Is mutt installed? Did the report generate properly?." >&2
    exit 2
fi


# Deletes all files in the reports directory that are older than 15 days.
echo "Clearing out old reports..."
find "$WORK_DIRECTORY"reports/ -type f -mtime +15 -exec rm -f {} \;
if [ $? -eq 0 ]
then
    echo "Done."
else
    echo "ERROR: Delete failed. Check reports directory." >&2
    exit 3
fi

