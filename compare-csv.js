#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Function to parse CSV content into array of arrays
function parseCSV(content) {
    const lines = content.split('\n').filter(line => line.trim() !== '');
    return lines.map(line => {
        // Simple CSV parsing - handles basic cases
        const result = [];
        let current = '';
        let inQuotes = false;
        
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                result.push(current.trim());
                current = '';
            } else {
                current += char;
            }
        }
        
        result.push(current.trim());
        return result;
    });
}

// Function to compare two CSV arrays
function compareCSV(csv1, csv2, file1Name, file2Name) {
    const differences = [];
    const maxRows = Math.max(csv1.length, csv2.length);
    
    console.log(`\n=== CSV Comparison Results ===`);
    console.log(`File 1: ${file1Name} (${csv1.length} rows)`);
    console.log(`File 2: ${file2Name} (${csv2.length} rows)`);
    console.log(`================================\n`);
    
    // Check for row count differences
    if (csv1.length !== csv2.length) {
        differences.push({
            type: 'row_count',
            message: `Row count differs: ${file1Name} has ${csv1.length} rows, ${file2Name} has ${csv2.length} rows`
        });
        console.log(`⚠️  Row count difference: ${file1Name} has ${csv1.length} rows, ${file2Name} has ${csv2.length} rows\n`);
    }
    
    // Compare each row
    for (let rowIndex = 0; rowIndex < maxRows; rowIndex++) {
        const row1 = csv1[rowIndex] || [];
        const row2 = csv2[rowIndex] || [];
        const maxCols = Math.max(row1.length, row2.length);
        
        // Check if row exists in both files
        if (!csv1[rowIndex]) {
            differences.push({
                type: 'missing_row',
                row: rowIndex + 1,
                message: `Row ${rowIndex + 1} exists only in ${file2Name}`,
                data: row2
            });
            console.log(`➕ Row ${rowIndex + 1} exists only in ${file2Name}:`);
            console.log(`   ${row2.join(' | ')}\n`);
            continue;
        }
        
        if (!csv2[rowIndex]) {
            differences.push({
                type: 'missing_row',
                row: rowIndex + 1,
                message: `Row ${rowIndex + 1} exists only in ${file1Name}`,
                data: row1
            });
            console.log(`➖ Row ${rowIndex + 1} exists only in ${file1Name}:`);
            console.log(`   ${row1.join(' | ')}\n`);
            continue;
        }
        
        // Check column count for this row
        if (row1.length !== row2.length) {
            differences.push({
                type: 'column_count',
                row: rowIndex + 1,
                message: `Row ${rowIndex + 1} has different column counts: ${row1.length} vs ${row2.length}`
            });
        }
        
        // Compare each cell in the row
        let rowHasDifferences = false;
        const cellDifferences = [];
        
        for (let colIndex = 0; colIndex < maxCols; colIndex++) {
            const cell1 = row1[colIndex] || '';
            const cell2 = row2[colIndex] || '';
            
            if (cell1 !== cell2) {
                rowHasDifferences = true;
                cellDifferences.push({
                    column: colIndex + 1,
                    value1: cell1,
                    value2: cell2
                });
                
                differences.push({
                    type: 'cell_difference',
                    row: rowIndex + 1,
                    column: colIndex + 1,
                    value1: cell1,
                    value2: cell2,
                    message: `Cell (${rowIndex + 1}, ${colIndex + 1}): "${cell1}" vs "${cell2}"`
                });
            }
        }
        
        // Display row differences
        if (rowHasDifferences) {
            console.log(`🔄 Row ${rowIndex + 1} differences:`);
            cellDifferences.forEach(diff => {
                console.log(`   Column ${diff.column}: "${diff.value1}" → "${diff.value2}"`);
            });
            console.log();
        }
    }
    
    return differences;
}

// Function to generate summary report
function generateSummary(differences) {
    console.log(`\n=== Summary ===`);
    
    if (differences.length === 0) {
        console.log(`✅ Files are identical!`);
        return;
    }
    
    const stats = {
        row_count: 0,
        missing_row: 0,
        column_count: 0,
        cell_difference: 0
    };
    
    differences.forEach(diff => {
        stats[diff.type]++;
    });
    
    console.log(`Total differences found: ${differences.length}`);
    if (stats.row_count > 0) console.log(`- Row count differences: ${stats.row_count}`);
    if (stats.missing_row > 0) console.log(`- Missing rows: ${stats.missing_row}`);
    if (stats.column_count > 0) console.log(`- Column count differences: ${stats.column_count}`);
    if (stats.cell_difference > 0) console.log(`- Cell value differences: ${stats.cell_difference}`);
}

// Function to save differences to JSON file
function saveDifferencesToFile(differences, outputFile) {
    const report = {
        timestamp: new Date().toISOString(),
        totalDifferences: differences.length,
        differences: differences
    };
    
    fs.writeFileSync(outputFile, JSON.stringify(report, null, 2));
    console.log(`\n📄 Detailed report saved to: ${outputFile}`);
}

// Main function
function main() {
    const args = process.argv.slice(2);
    
    if (args.length < 2) {
        console.log('Usage: node compare-csv.js <file1.csv> <file2.csv> [output.json]');
        console.log('');
        console.log('Examples:');
        console.log('  node compare-csv.js data1.csv data2.csv');
        console.log('  node compare-csv.js data1.csv data2.csv differences.json');
        process.exit(1);
    }
    
    const file1Path = args[0];
    const file2Path = args[1];
    const outputFile = args[2] || null;
    
    // Check if files exist
    if (!fs.existsSync(file1Path)) {
        console.error(`❌ Error: File "${file1Path}" not found`);
        process.exit(1);
    }
    
    if (!fs.existsSync(file2Path)) {
        console.error(`❌ Error: File "${file2Path}" not found`);
        process.exit(1);
    }
    
    try {
        // Read and parse CSV files
        console.log('📖 Reading CSV files...');
        const content1 = fs.readFileSync(file1Path, 'utf-8');
        const content2 = fs.readFileSync(file2Path, 'utf-8');
        
        const csv1 = parseCSV(content1);
        const csv2 = parseCSV(content2);
        
        // Compare the CSV files
        console.log('🔍 Comparing files...');
        const differences = compareCSV(csv1, csv2, path.basename(file1Path), path.basename(file2Path));
        
        // Generate summary
        generateSummary(differences);
        
        // Save to file if requested
        if (outputFile) {
            saveDifferencesToFile(differences, outputFile);
        }
        
        // Exit with appropriate code
        process.exit(differences.length > 0 ? 1 : 0);
        
    } catch (error) {
        console.error(`❌ Error: ${error.message}`);
        process.exit(1);
    }
}

// Run the script
if (require.main === module) {
    main();
}

module.exports = { parseCSV, compareCSV };