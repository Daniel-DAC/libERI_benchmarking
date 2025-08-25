import os
import re
import csv
from datetime import datetime  # Added for timestamp

# Regex patterns
energy_pattern = re.compile(r"FINAL RHF ENERGY IS\s+([-.\d]+).*?(\d+)\s+ITERATIONS")
fock_pattern = re.compile(r"Fock build time\s+([.\d]+)")
diag_pattern = re.compile(r"Diagonalization\s+([.\d]+)")
total_iter_pattern = re.compile(r"Total iter time\s+([.\d]+)")

def extract_data_from_log(log_path):
    with open(log_path, "r", errors="ignore") as f:
        content = f.read()

    energy_match = energy_pattern.search(content)
    fock_match = fock_pattern.search(content)
    diag_match = diag_pattern.search(content)
    total_iter_match = total_iter_pattern.search(content)

    if energy_match:
        energy = float(energy_match.group(1))
        iterations = int(energy_match.group(2))
    else:
        energy = iterations = None

    fock_time = float(fock_match.group(1)) if fock_match else None
    diag_time = float(diag_match.group(1)) if diag_match else None
    total_iter_time = float(total_iter_match.group(1)) if total_iter_match else None

    return energy, iterations, fock_time, diag_time, total_iter_time

def scan_and_extract(base_dir="."):
    data = []
    current_dir = os.path.basename(os.path.abspath(base_dir))
    for subdir in sorted(os.listdir(base_dir)):
        subdir_path = os.path.join(base_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue

        for filename in os.listdir(subdir_path):
            if filename.endswith(".log"):
                log_path = os.path.join(subdir_path, filename)
                input_name = filename.replace(".log", ".inp")
                energy, iterations, fock, diag, total = extract_data_from_log(log_path)
                data.append({
                    "Directory": subdir,
                    "Input": input_name,
                    "Energy": energy,
                    "Iterations": iterations,
                    "Fock build time": fock,
                    "Diagonalization": diag,
                    "Total iter time": total
                })
    return data, current_dir

def write_csv(data, dir_name):
    # Add timestamp to filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"gamess_summary_{dir_name}_{timestamp}.csv"

    headers = ["Directory", "Input", "Energy", "Iterations", "Fock build time", "Diagonalization", "Total iter time"]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        # First line: directory label
        writer.writerow([f"GAMESS summary for directory: {dir_name}"])
        writer.writerow([])  # blank line

        # Headers + data
        writer.writerow(headers)
        for row in data:
            writer.writerow([row[h] for h in headers])

    print(f"✅ Data extracted for {len(data)} GAMESS log files.")
    print(f"📄 Output written to {filename}")

if __name__ == "__main__":
    data, dir_name = scan_and_extract()
    write_csv(data, dir_name)

