import re

def clean_data(entries_list):
    """
    Performs data cleaning on the list of scraped admission entries.
    - Removes "Other Misc Details" key (as it was removed from collection).
    - Ensures "Comments" is a string (N/A if no actual comments).
    """
    # print(f"Cleaning {len(entries_list)} entries...") # Optional progress message
    cleaned_entries = []
    for entry in entries_list:
        # "Other Misc Details" is no longer added, so no need to pop if get_empty_admission_entry is source
        # However, if it somehow slipped in, this would remove it:
        entry.pop("Other Misc Details", None) 
        
        # Ensure Comments field is a string, not a list (should be handled by parsing now)
        if "Comments" in entry and isinstance(entry["Comments"], list):
            entry["Comments"] = "; ".join(entry["Comments"]) if entry["Comments"] else "N/A"
            
        # Example: Further cleaning for Decision Date String if it contains extraneous info
        if entry.get("Decision Date String") and entry["Decision Date String"] != "N/A":
            # Simple example: if it contains time or other text, try to isolate date part
            # This is just a placeholder, actual date cleaning can be complex
            pass 

        cleaned_entries.append(entry)
    return cleaned_entries