# CSV File Comparison Tool

A JavaScript script to compare two CSV files (such as Excel files saved in CSV format) and identify differences between them.

## Features

- **Row-by-row comparison**: Compares each row between two CSV files
- **Cell-level differences**: Identifies specific cells that differ
- **Missing row detection**: Finds rows that exist in one file but not the other
- **Column count validation**: Detects rows with different numbers of columns
- **Detailed output**: Shows exactly what changed and where
- **JSON export**: Optionally save detailed differences to a JSON file
- **Summary statistics**: Provides a summary of all differences found

## Usage

### Basic Usage
```bash
node compare-csv.js file1.csv file2.csv
```

### Save Differences to JSON
```bash
node compare-csv.js file1.csv file2.csv differences.json
```

### Make it Executable (Optional)
```bash
chmod +x compare-csv.js
./compare-csv.js file1.csv file2.csv
```

## Output Types

The script identifies and reports several types of differences:

1. **Row Count Differences**: When files have different numbers of rows
2. **Missing Rows**: Rows that exist in one file but not the other
3. **Column Count Differences**: Rows with different numbers of columns
4. **Cell Value Differences**: Individual cells with different values

## Example Output

```
=== CSV Comparison Results ===
File 1: sample1.csv (5 rows)
File 2: sample2.csv (6 rows)
================================

⚠️  Row count difference: sample1.csv has 5 rows, sample2.csv has 6 rows

🔄 Row 2 differences:
   Column 2: "30" → "31"
   Column 4: "50000" → "52000"

🔄 Row 4 differences:
   Column 3: "Chicago" → "Miami"

➕ Row 6 exists only in sample2.csv:
   Mike Wilson | 40 | Seattle | 60000

=== Summary ===
Total differences found: 5
- Row count differences: 1
- Missing rows: 1
- Cell value differences: 3
```

## JSON Output Format

When saving to JSON, the output includes:

```json
{
  "timestamp": "2025-07-30T13:32:31.209Z",
  "totalDifferences": 5,
  "differences": [
    {
      "type": "cell_difference",
      "row": 2,
      "column": 2,
      "value1": "30",
      "value2": "31",
      "message": "Cell (2, 2): \"30\" vs \"31\""
    }
  ]
}
```

## CSV Format Support

The script handles:
- Comma-separated values
- Quoted fields (basic support)
- Empty cells
- Different row lengths
- Files with different numbers of rows

## Requirements

- Node.js (any recent version)
- No external dependencies - uses only built-in Node.js modules

## Exit Codes

- `0`: Files are identical
- `1`: Differences found or error occurred

## Use Cases

Perfect for:
- Comparing Excel files exported to CSV format
- Data validation and quality assurance
- Tracking changes between file versions
- Automated testing of data transformations
- Auditing data migrations

## Limitations

- Basic CSV parsing (may not handle all edge cases of complex CSV files)
- Loads entire files into memory (not suitable for extremely large files)
- Case-sensitive comparisons
- No fuzzy matching or similarity detection
