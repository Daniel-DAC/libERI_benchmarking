import os
from datetime import datetime

SUCCESS_STRING = "EXECUTION OF GAMESS TERMINATED NORMALLY"
REPORT_FILENAME = "gamess_run_report.txt"

def check_gamess_logs(base_dir="."):
    failed_jobs = []
    skipped_dirs = []

    for subdir in sorted(os.listdir(base_dir)):
        subdir_path = os.path.join(base_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue

        log_files_found = False

        for filename in os.listdir(subdir_path):
            if filename.endswith(".inp"):
                base_name = filename[:-4]
                log_file_path = os.path.join(subdir_path, base_name + ".log")
                log_files_found = True

                if not os.path.isfile(log_file_path):
                    failed_jobs.append((subdir, filename, "Log file missing"))
                    continue

                with open(log_file_path, "r", errors="ignore") as f:
                    content = f.read()
                    if SUCCESS_STRING not in content:
                        failed_jobs.append((subdir, filename, "Run did not terminate normally"))

        if not log_files_found:
            skipped_dirs.append(subdir)

    return failed_jobs, skipped_dirs

def write_report(failed, skipped, report_file):
    with open(report_file, "w") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"GAMESS Run Check Report — {timestamp}\n")
        f.write("=" * 40 + "\n\n")

        if skipped:
            f.write(f"Skipped {len(skipped)} directories with no .inp files:\n")
            for d in skipped:
                f.write(f"  - {d}\n")
            f.write("\n")

        if failed:
            f.write(f"{len(failed)} failed or incomplete runs found:\n\n")
            for subdir, inp_file, reason in failed:
                f.write(f"[{subdir}] {inp_file} → {reason}\n")
        else:
            f.write("✅ All GAMESS runs terminated normally!\n")

        f.write("\n" + "=" * 40 + "\n")

if __name__ == "__main__":
    failed, skipped = check_gamess_logs()
    write_report(failed, skipped, REPORT_FILENAME)

    # Also print to terminal
    with open(REPORT_FILENAME, "r") as f:
        print(f.read())

