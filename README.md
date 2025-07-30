# CSV File Comparison Tool

A Python script to compare two CSV files (Excel files exported as CSV) and identify differences between them.

## Features

- **Structural Comparison**: Detects differences in columns and row counts
- **Data Comparison**: Identifies modified, added, or removed rows
- **Cell-level Changes**: Shows exactly which cells have changed and their old/new values
- **Row Position Analysis**: Finds rows that may have moved positions
- **Clear Output**: Provides formatted, readable difference reports
- **Export Results**: Option to save comparison results to a file

## Requirements

Install the required dependencies:

```bash
pip install pandas numpy
```

Or on Ubuntu/Debian systems:

```bash
sudo apt install python3-pandas python3-numpy
```

## Usage

### Basic Usage

```bash
python3 csv_compare.py file1.csv file2.csv
```

### Save Results to File

```bash
python3 csv_compare.py file1.csv file2.csv --output comparison_report.txt
```

### Specify File Encoding

```bash
python3 csv_compare.py file1.csv file2.csv --encoding utf-8
```

## Example Output

```
============================================================
CSV COMPARISON SUMMARY
============================================================
File 1: sample1.csv (4 rows, 4 columns)
File 2: sample2.csv (4 rows, 5 columns)

STRUCTURAL DIFFERENCES:
------------------------------
• Added columns in file2: Department

DATA DIFFERENCES:
------------------------------
• Row 1: Modified - Salary: '50000' -> '52000', Age: '25' -> '26'
• Row 3: Modified - Salary: '60000' -> '65000', City: 'Chicago' -> 'Los Angeles'
• Row 4: Modified - Name: 'Carol' -> 'David', Salary: '55000' -> '70000', City: 'Boston' -> 'Seattle', Age: '28' -> '32'

📊 TOTAL DIFFERENCES FOUND: 4
```

## What the Script Detects

1. **Column Differences**: Added or removed columns
2. **Row Count Changes**: Different number of rows between files
3. **Cell Modifications**: Changed values in existing cells
4. **Added Rows**: Rows present only in the second file
5. **Removed Rows**: Rows present only in the first file
6. **Position Changes**: Rows that moved to different positions

## Files Included

- `csv_compare.py` - Main comparison script
- `requirements.txt` - Python dependencies
- `sample1.csv` - Sample CSV file for testing
- `sample2.csv` - Sample CSV file with differences for testing
- `README.md` - This documentation

## Command Line Options

- `file1` - Path to the first CSV file (required)
- `file2` - Path to the second CSV file (required)
- `-o, --output` - Output file path (optional)
- `--encoding` - File encoding (default: utf-8)

## Error Handling

The script handles common issues:
- Missing files
- Empty CSV files
- Encoding problems
- Large files (limits output to prevent overwhelming results)

## Notes

- The script compares files row by row based on position
- For large files, only the first 50 differences are shown
- Row position analysis is limited to the first 20 matches
- Files are assumed to have headers in the first row
