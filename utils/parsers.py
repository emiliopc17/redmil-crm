import fitz  # pymupdf
import pandas as pd
import re

def clean_price(price_str):
    """Cleans price string to float."""
    if not price_str:
        return 0.0
    # Remove currency symbols and commas
    clean = re.sub(r'[^\d.]', '', str(price_str).replace(',', ''))
    try:
        return float(clean)
    except ValueError:
        return 0.0

def parse_pdf_inventory(file_stream):
    """
    Parses an inventory PDF using robust word-stream analysis.
    
    Strategy:
    1. Extract all words with coordinates.
    2. Group words into lines based on Y-coordinate alignment.
    3. For each line, identify:
       - First token = Code.
       - First 'numeric-looking' token after the code and some text = Price.
       - Everything in between = Description.
    4. Handles extra columns after Price by ignoring them.
    5. Filters headers and garbage lines.
    """
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    products = []
    
    for page in doc:
        # get_text("words") returns: (x0, y0, x1, y1, "word", block_no, line_no, word_no)
        words = page.get_text("words")
        if not words:
            continue
            
        # Group words by Line (using y0, with a small tolerance)
        rows = []
        current_row = []
        last_y = -999
        
        # Sort by vertical position (y0), then horizontal (x0)
        # However, words are usually returned in reading order. 
        # Standard sort just in case:
        words.sort(key=lambda w: (w[1], w[0]))
        
        for w in words:
            y = w[1]
            if abs(y - last_y) > 5: # New line threshold (5 pixels)
                if current_row:
                    rows.append(current_row)
                current_row = []
                last_y = y
            current_row.append(w)
        if current_row:
            rows.append(current_row)
            
        # Process items
        for row in rows:
            # row is a list of word tuples.
            # We filter out empty or very short lines
            if len(row) < 3:
                continue
                
            # Extract text tokens strings from valid words
            tokens = [w[4] for w in row]
            
            # --- HEURISTIC 1: Header Detection ---
            # If the line contains "CODIGO" and "DESCRIPCION", it's a header.
            line_str = " ".join(tokens).upper()
            if "CODIGO" in line_str or "DESCRIPCION" in line_str or "PRECIO" in line_str or "PAGE" in line_str:
                continue
                
            # --- HEURISTIC 2: Structure Detection ---
            # Pattern: Code [Desc...] Price [Others...]
            
            # Code is the first token.
            code = tokens[0]
            
            # Price is a number. We look for the *first* number that appears after index 1.
            # Why first? Because user said "Code, Desc, Price" are the first 3 columns.
            # If there are other price columns later, we want the first one (USD).
            
            price_index = -1
            price_str = ""
            
            # Start strict search from index 1.
            # We want to avoid capturing model numbers (e.g. "15", "S24") as prices.
            # INVENTORY PRICE ASSUMPTION: Prices usually have decimals (e.g. 10.00, 1,234.50).
            # Model numbers are usually integers.
            
            for i in range(1, len(tokens)):
                t = tokens[i]
                t_clean = t.replace('$', '').replace(',', '')
                
                # Regex: Must start with digits, have a dot, and end with digits.
                # Or just be a float larger than 0 if it has a dot.
                # Not perfect (some prices might be integer "100"), but safer for "iPhone 15".
                # If User's PDF has "100" without decimals, this might skip it.
                # Compromise: Look for dot OR ensure it is at the end of the line (if length match).
                # But we have extra columns. 
                # Let's enforce the Decimal rule. It's the most robust way to distinguish "15" from "15.00".
                
                if re.match(r'^\d+\.\d+$', t_clean):
                    # It has a dot and numbers. High probability of being a price.
                    price_index = i
                    price_str = t
                    break
            
            # Fallback: If no decimal found, but we scanned everything, maybe the price IS an integer?
            # But we can't distinguish "Samsung S23" (23 is model) from "Price 23".
            # We'll skip this row or assume strict formatting is required.
            # BETTER FALLBACK: If we didn't find a decimal-price, try to look for the LAST numeric token 
            # *before* any obvious non-numeric "Extra Info" begins? Hard to say.
            # Let's stick to decimal requirement for now as it solves the "Truncated Description" complaint.
            
            if price_index != -1 and price_index > 1: # Need at least one word for Desc
                # Found Code, found Price.
                # Description is everything in between.
                
                desc_tokens = tokens[1:price_index]
                description = " ".join(desc_tokens)
                
                # Validation
                if len(description) < 2: 
                    continue # Too short
                    
                price_val = clean_price(price_str)
                
                products.append({
                    "product_code": code,
                    "description": description,
                    "cost_usd": price_val,
                    "category": "General",
                    "brand": "Unknown"
                })
            
            # Fallback: Maybe the price is at the very end (ignoring extra columns logic failure)
            # If we didn't find a price in the middle, check the last token? 
            # Risk: Last token might be Lempiras or something else.
            # Stick to "First numeric after text" logic for now as it matches "Code Desc Price [Other]"
                
    return products

def parse_excel_inventory(file_stream):
    """
    Parses an Excel file with robust column matching.
    """
    try:
        df = pd.read_excel(file_stream)
        
        # 1. Normalize strict column map
        # We'll normalize the dataframe columns to: lower, stripped, no-accents
        
        def normalize_str(s):
            import unicodedata
            if not isinstance(s, str): return str(s)
            s = s.lower().strip()
            # Remove accents
            s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
            return s
            
        # Create a mapping from formatted col -> original col
        df_cols_map = {normalize_str(col): col for col in df.columns}
        
        # Targets we need: 'product_code', 'description', 'cost_usd', 'brand'
        # Candidates for each
        candidates = {
            'product_code': ['codigo', 'code', 'sku', 'id', 'item'],
            'description': ['descripcion', 'description', 'nombre', 'producto', 'desc'],
            'cost_usd': ['precio', 'price', 'costo', 'cost', 'valor', 'usd'],
            'brand': ['marca', 'brand', 'fabricante']
        }
        
        final_rename_map = {}
        
        for target, synonyms in candidates.items():
            for syn in synonyms:
                if syn in df_cols_map:
                    # Found a match! Map original col -> target
                    original_col = df_cols_map[syn]
                    final_rename_map[original_col] = target
                    break
        
        # Apply rename
        if not final_rename_map:
            print("No matching columns found after normalization.")
            return []
            
        df = df.rename(columns=final_rename_map)
        
        # Check required
        required_cols = ['product_code', 'description', 'cost_usd']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            print(f"Missing required columns: {missing}. Found: {df.columns.tolist()}")
            return []
            
        # Optional: Clean data
        df['cost_usd'] = df['cost_usd'].apply(clean_price)
        df['product_code'] = df['product_code'].astype(str).str.strip()
        df['description'] = df['description'].astype(str).str.strip()
        
        # Handle Brand if missing
        if 'brand' not in df.columns:
            df['brand'] = 'Unknown'
        else:
            df['brand'] = df['brand'].fillna('Unknown').astype(str).str.strip()
            
        return df.to_dict('records')
    except Exception as e:
        print(f"Error parsing Excel: {e}")
        return []
