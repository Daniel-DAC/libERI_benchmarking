import os
import re
import csv
from datetime import datetime  # Used for timestamping the output CSV file

# -----------------------
# Regex patterns to extract specific data from GAMESS log files
# -----------------------

# Final RHF energy and number of SCF iterations
energy_pattern = re.compile(r"FINAL RHF ENERGY IS\s+([-.\d]+).*?(\d+)\s+ITERATIONS")

# Timings for specific stages of the calculation
fock_pattern = re.compile(r"Fock build time\s+([.\d]+)")
diag_pattern = re.compile(r"Diagonalization\s+([.\d]+)")
total_iter_pattern = re.compile(r"Total iter time\s+([.\d]+)")

# Number of Cartesian Gaussian basis functions
basis_func_pattern = re.compile(r"NUMBER OF CARTESIAN GAUSSIAN BASIS FUNCTIONS\s*=\s*(\d+)")

# -----------------------
# Function to extract data from a single GAMESS log file
# -----------------------
def extract_data_from_log(log_path):
    """Extracts relevant performance and output data from a GAMESS .log file."""
    with open(log_path, "r", errors="ignore") as f:
        content = f.read()

    # Attempt to match each pattern
    energy_match = energy_pattern.search(content)
    fock_match = fock_pattern.search(content)
    diag_match = diag_pattern.search(content)
    total_iter_match = total_iter_pattern.search(content)
    basis_func_match = basis_func_pattern.search(content)

    # Extract energy and SCF iteration count
    if energy_match:
        energy = float(energy_match.group(1))
        iterations = int(energy_match.group(2))
    else:
        energy = iterations = None

    # Extract timings
    fock_time = float(fock_match.group(1)) if fock_match else None
    diag_time = float(diag_match.group(1)) if diag_match else None
    total_iter_time = float(total_iter_match.group(1)) if total_iter_match else None

    # Extract number of basis functions
    basis_functions = int(basis_func_match.group(1)) if basis_func_match else None

    return energy, iterations, fock_time, diag_time, total_iter_time, basis_functions

# -----------------------
# Function to scan subdirectories and extract data from all GAMESS log files
# -----------------------
def scan_and_extract(base_dir="."):
    """Scans subdirectories for GAMESS log files and extracts data."""
    data = []
    current_dir = os.path.basename(os.path.abspath(base_dir))

    # Loop through subdirectories (each represents a calculation set)
    for subdir in sorted(os.listdir(base_dir)):
        subdir_path = os.path.join(base_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue

        # Loop through files in each subdirectory
        for filename in os.listdir(subdir_path):
            if filename.endswith(".log"):
                log_path = os.path.join(subdir_path, filename)
                input_name = filename.replace(".log", ".inp")

                # Extract data from log file
                energy, iterations, fock, diag, total, basis = extract_data_from_log(log_path)

                # Append to data list in desired column order
                data.append({
                    "Directory": subdir,
                    "Input": input_name,
                    "Basis functions": basis,
                    "Energy": energy,
                    "Iterations": iterations,
                    "Fock build time": fock,
                    "Diagonalization": diag,
                    "Total iter time": total
                })

    return data, current_dir

# -----------------------
# Function to write extracted data into a timestamped, sorted CSV file
# -----------------------
def write_csv(data, dir_name):
    """Writes extracted GAMESS data into a CSV file, sorted by basis functions."""
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Perlmutter_benchmarks_{dir_name}_{timestamp}.csv"

    # Define column order (matching dictionary keys)
    headers = [
        "Directory",
        "Input",
        "Basis functions",  # Appears as the third column
        "Energy",
        "Iterations",
        "Fock build time",
        "Diagonalization",
        "Total iter time"
    ]

    # Sort data by number of basis functions (None values sorted last)
    data = sorted(data, key=lambda x: (x["Basis functions"] is None, x["Basis functions"]))

    # Write CSV file
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        # Write metadata and headers
        writer.writerow([f"GAMESS summary for directory: {dir_name}"])
        writer.writerow([])  # Blank line for spacing
        writer.writerow(headers)

        # Write each row of sorted data
        for row in data:
            writer.writerow([row[h] for h in headers])

    print(f"✅ Data extracted and sorted for {len(data)} GAMESS log files.")
    print(f"📄 Output written to {filename}")

# -----------------------
# Main execution entry point
# -----------------------
if __name__ == "__main__":
    data, dir_name = scan_and_extract()
    write_csv(data, dir_name)

