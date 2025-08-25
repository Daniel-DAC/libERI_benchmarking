# Anything and everything you need to benchmark libERI

How to run these benchmarks:

1. Make the main scripts executable

1.1 Do $chmod +x copy_scripts_in_dirs.sh
1.2 Do $chmod +x submit_jobs.sh
1.3 Do $chmod +x check_and_extract_logs.sh


2. Modify scripts to run properly

2.1 MODIFY scripts/bash_script_multiple
    Load whichever modules are required
    Set the appropriate number of threads 
    In line 39, set the path to your rungms-dev script

2.2 In your rungms-dev, hardcode the $GMSPATH instead of having it be `pwd`

2.3 MODIFY scripts/extract_gamess_data.py
    In line 60, change the file name to show the system where you are benchmarking


3. Execute the main scripts

3.1 Copy the scripts in "scripts/" to all subdirectories:
  $./copy_scripts_in_dirs

3.2 Submit the execution of all the benchmarks:
  $./submit_jobs.sh

3.3 Wait until they all finish or have run out of time

3.4 Run the checks and data extraction with:
  $./check_and_extract_logs.sh

  The check and extraction will generate .csv files in each subdirectory

3.5 Collect the .csv files:
  $./gather_csv_results.sh

