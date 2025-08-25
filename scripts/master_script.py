# master_script.py

import check_gamess_runs
import extract_gamess_data

def main():
    print("🔍 Checking GAMESS run logs...\n")
    failed, skipped = check_gamess_runs.check_gamess_logs()

    # Write the report file
    check_gamess_runs.write_report(failed, skipped, check_gamess_runs.REPORT_FILENAME)

    if failed:
        print("❌ Some GAMESS runs failed. Skipping data extraction.\n")
        print(f"📄 See report: {check_gamess_runs.REPORT_FILENAME}")
    else:
        print("✅ All GAMESS runs completed successfully.")
        print("📊 Extracting data from log files...\n")

        # Run data extraction
        results, dir_name = extract_gamess_data.scan_and_extract()
        extract_gamess_data.write_csv(results, dir_name)

if __name__ == "__main__":
    main()

