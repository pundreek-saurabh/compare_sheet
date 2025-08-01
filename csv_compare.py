#!/usr/bin/env python3
"""
CSV File Comparison Tool

This script compares two CSV files and outputs the differences between them.
It can detect:
- Added rows
- Removed rows
- Modified cells
- Column differences

Usage:
    python csv_compare.py file1.csv file2.csv [--output output.txt]
"""

import pandas as pd
import argparse
import sys
from pathlib import Path
from typing import Tuple, List, Dict, Any
import numpy as np

class CSVComparator:
    def __init__(self, file1_path: str, file2_path: str):
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.df1 = None
        self.df2 = None
        self.differences = []
        
    def load_files(self) -> bool:
        """Load both CSV files into pandas DataFrames"""
        try:
            print(f"Loading {self.file1_path}...")
            self.df1 = pd.read_csv(self.file1_path)
            print(f"Loading {self.file2_path}...")
            self.df2 = pd.read_csv(self.file2_path)
            return True
        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            return False
        except pd.errors.EmptyDataError as e:
            print(f"Error: Empty CSV file - {e}")
            return False
        except Exception as e:
            print(f"Error loading files: {e}")
            return False
    
    def compare_structure(self) -> List[str]:
        """Compare the structure (columns) of both DataFrames"""
        structure_diffs = []
        
        # Compare columns
        cols1 = set(self.df1.columns)
        cols2 = set(self.df2.columns)
        
        if cols1 != cols2:
            added_cols = cols2 - cols1
            removed_cols = cols1 - cols2
            
            if added_cols:
                structure_diffs.append(f"Added columns in file2: {', '.join(added_cols)}")
            if removed_cols:
                structure_diffs.append(f"Removed columns in file2: {', '.join(removed_cols)}")
        
        # Compare number of rows
        rows1, rows2 = len(self.df1), len(self.df2)
        if rows1 != rows2:
            structure_diffs.append(f"Row count difference: file1 has {rows1} rows, file2 has {rows2} rows")
        
        return structure_diffs
    
    def compare_data(self) -> List[str]:
        """Compare the actual data between DataFrames"""
        data_diffs = []
        
        # Get common columns for comparison
        common_cols = list(set(self.df1.columns) & set(self.df2.columns))
        
        if not common_cols:
            return ["No common columns found for data comparison"]
        
        # Align DataFrames to same columns for comparison
        df1_common = self.df1[common_cols].copy()
        df2_common = self.df2[common_cols].copy()
        
        # Reset index to ensure proper comparison
        df1_common = df1_common.reset_index(drop=True)
        df2_common = df2_common.reset_index(drop=True)
        
        # Find row-level differences
        max_rows = max(len(df1_common), len(df2_common))
        
        for i in range(max_rows):
            if i >= len(df1_common):
                # Row exists only in df2
                row_data = df2_common.iloc[i].to_dict()
                data_diffs.append(f"Row {i+1}: Added in file2 - {row_data}")
            elif i >= len(df2_common):
                # Row exists only in df1
                row_data = df1_common.iloc[i].to_dict()
                data_diffs.append(f"Row {i+1}: Removed in file2 - {row_data}")
            else:
                # Compare cells in the row
                row1 = df1_common.iloc[i]
                row2 = df2_common.iloc[i]
                
                cell_diffs = []
                for col in common_cols:
                    val1 = row1[col]
                    val2 = row2[col]
                    
                    # Handle NaN values
                    if pd.isna(val1) and pd.isna(val2):
                        continue
                    elif pd.isna(val1) or pd.isna(val2) or val1 != val2:
                        cell_diffs.append(f"{col}: '{val1}' -> '{val2}'")
                
                if cell_diffs:
                    data_diffs.append(f"Row {i+1}: Modified - {', '.join(cell_diffs)}")
        
        return data_diffs
    
    def find_similar_rows(self) -> List[str]:
        """Find rows that might be similar but in different positions"""
        similarity_info = []
        
        # This is a basic implementation - could be enhanced with fuzzy matching
        common_cols = list(set(self.df1.columns) & set(self.df2.columns))
        if not common_cols:
            return similarity_info
        
        # Convert to string representation for easier comparison
        df1_strings = self.df1[common_cols].astype(str).apply(lambda x: '|'.join(x), axis=1)
        df2_strings = self.df2[common_cols].astype(str).apply(lambda x: '|'.join(x), axis=1)
        
        # Find rows in df1 that don't exist in df2 at the same position but exist elsewhere
        for i, row_str in enumerate(df1_strings):
            if i < len(df2_strings) and row_str != df2_strings.iloc[i]:
                # Check if this row exists elsewhere in df2
                matches = df2_strings[df2_strings == row_str]
                if not matches.empty:
                    match_indices = matches.index.tolist()
                    similarity_info.append(
                        f"Row {i+1} from file1 found at position(s) {[idx+1 for idx in match_indices]} in file2"
                    )
        
        return similarity_info
    
    def generate_summary(self) -> str:
        """Generate a summary of the comparison"""
        summary = []
        summary.append("=" * 60)
        summary.append("CSV COMPARISON SUMMARY")
        summary.append("=" * 60)
        summary.append(f"File 1: {self.file1_path} ({len(self.df1)} rows, {len(self.df1.columns)} columns)")
        summary.append(f"File 2: {self.file2_path} ({len(self.df2)} rows, {len(self.df2.columns)} columns)")
        summary.append("")
        
        return "\n".join(summary)
    
    def compare(self) -> str:
        """Main comparison method that returns formatted differences"""
        if not self.load_files():
            return "Failed to load files for comparison"
        
        result = []
        result.append(self.generate_summary())
        
        # Structure comparison
        structure_diffs = self.compare_structure()
        if structure_diffs:
            result.append("STRUCTURAL DIFFERENCES:")
            result.append("-" * 30)
            for diff in structure_diffs:
                result.append(f"• {diff}")
            result.append("")
        else:
            result.append("✓ No structural differences found")
            result.append("")
        
        # Data comparison
        data_diffs = self.compare_data()
        if data_diffs:
            result.append("DATA DIFFERENCES:")
            result.append("-" * 30)
            for diff in data_diffs[:50]:  # Limit to first 50 differences
                result.append(f"• {diff}")
            
            if len(data_diffs) > 50:
                result.append(f"... and {len(data_diffs) - 50} more differences")
            result.append("")
        else:
            result.append("✓ No data differences found")
            result.append("")
        
        # Similarity analysis
        similarity_info = self.find_similar_rows()
        if similarity_info:
            result.append("ROW POSITION ANALYSIS:")
            result.append("-" * 30)
            for info in similarity_info[:20]:  # Limit to first 20
                result.append(f"• {info}")
            result.append("")
        
        # Final summary
        total_diffs = len(structure_diffs) + len(data_diffs)
        if total_diffs == 0:
            result.append("🎉 FILES ARE IDENTICAL!")
        else:
            result.append(f"📊 TOTAL DIFFERENCES FOUND: {total_diffs}")
        
        return "\n".join(result)

def main():
    parser = argparse.ArgumentParser(description="Compare two CSV files and show differences")
    parser.add_argument("file1", help="Path to the first CSV file")
    parser.add_argument("file2", help="Path to the second CSV file")
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    parser.add_argument("--encoding", default="utf-8", help="File encoding (default: utf-8)")
    
    args = parser.parse_args()
    
    # Validate input files
    if not Path(args.file1).exists():
        print(f"Error: File '{args.file1}' does not exist")
        sys.exit(1)
    
    if not Path(args.file2).exists():
        print(f"Error: File '{args.file2}' does not exist")
        sys.exit(1)
    
    # Perform comparison
    comparator = CSVComparator(args.file1, args.file2)
    result = comparator.compare()
    
    # Output results
    if args.output:
        try:
            with open(args.output, 'w', encoding=args.encoding) as f:
                f.write(result)
            print(f"Comparison results saved to: {args.output}")
        except Exception as e:
            print(f"Error writing to output file: {e}")
            print("\nResults:")
            print(result)
    else:
        print(result)

if __name__ == "__main__":
    main()