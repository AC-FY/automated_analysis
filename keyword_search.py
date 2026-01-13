import pandas as pd

# search configuration #
SEARCH_NAMES = [
    '[]',
    '[]',
    '[]'
]
OUTPUT_FILE = '[].csv'
CASE_SENSITIVE = True
PARTIAL_MATCH = True

CSV_FILE_1 = 'tweet_threats.csv'
SEARCH_COLUMN_1 = 'NameLast'
CSV_FILE_2 = 'tta_data.csv'
SEARCH_COLUMN_2 = 'text'

# search function #
def search_csv(file_path, column_name, search_terms, case_sensitive=False, partial_match=False):
    try:
        df = pd.read_csv(file_path)
        
        if column_name not in df.columns:
            print(f"Error: Column '{column_name}' not found in {file_path}")
            print(f"Available columns: {list(df.columns)}")
            return pd.DataFrame()
        
        if not case_sensitive:
            search_terms = [term.lower() for term in search_terms]
            search_column = df[column_name].astype(str).str.lower()
        else:
            search_column = df[column_name].astype(str)
        
        if partial_match:
            mask = search_column.apply(
                lambda x: any(term in x for term in search_terms)
            )
        else:
            mask = search_column.isin(search_terms)
        
        matches = df[mask].copy()
        matches['source_file'] = file_path
        matches['matched_column'] = column_name
        
        return matches
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return pd.DataFrame()

def main():
    print("="*60)
    print("CSV Search Tool")
    print("="*60)
    print(f"\nSearching for {len(SEARCH_NAMES)} names...")
    print(f"Names: {', '.join(SEARCH_NAMES[:3])}{'...' if len(SEARCH_NAMES) > 3 else ''}")
    print()
    
    print(f"Searching in {CSV_FILE_1} (column: {SEARCH_COLUMN_1})...")
    results_1 = search_csv(
        CSV_FILE_1,
        SEARCH_COLUMN_1,
        SEARCH_NAMES,
        CASE_SENSITIVE,
        PARTIAL_MATCH
    )
    print(f"  Found {len(results_1)} matches")
    
    print(f"\nSearching in {CSV_FILE_2} (column: {SEARCH_COLUMN_2})...")
    results_2 = search_csv(
        CSV_FILE_2,
        SEARCH_COLUMN_2,
        SEARCH_NAMES,
        CASE_SENSITIVE,
        PARTIAL_MATCH
    )
    print(f"  Found {len(results_2)} matches")
    
    if not results_1.empty or not results_2.empty:
        all_results = pd.concat([results_1, results_2], ignore_index=True)
        all_results.to_csv(OUTPUT_FILE, index=False)        
        print(f"\n{'='*60}")
        print(f"Total matches found: {len(all_results)}")
        print(f"Results saved to: {OUTPUT_FILE}")
        print(f"{'='*60}")
        print("\nBreakdown by source:")
        print(all_results['source_file'].value_counts())        
        print("\nFirst 5 results:")
        print(all_results.head())
        
    else:
        print("\nNo matches found in either file.")
    
    print("\n✓ Search complete!")

if __name__ == "__main__":
    main()
