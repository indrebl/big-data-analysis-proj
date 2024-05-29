from Bio import SeqIO
from dateutil import parser
import pandas as pd
import os

def autoRecognizeDate(date_str):
    """
    Attempt to recognize and format a date string to a Year-month-day format with variable precision.

    Args:
    date_str (str): The date string to be parsed and formatted.

    Returns:
    str or None: The formatted date string if recognized, otherwise None.
    """
    try:
        parsed_date = parser.parse(date_str)
        # Check if the day is explicitly stated or not present
        if date_str.count("-") == 1:
            return parsed_date.strftime('%Y-%m')
        else:
            return parsed_date.strftime('%Y-%m-%d')
    except ValueError:
        return None  # Unable to recognize the date format

def get_info(gb_file, segment):
    """
    Extract and compile gene information from a GenBank file.

    Args:
    gb_file (str): Path to the GenBank file.
    segment (bool): Whether to include the segment information (for segmented genomes).

    Returns:
    pd.DataFrame: DataFrame containing the extracted gene information.
    """
    # List to store gene data
    gene_data = []

    # Parse the GenBank file and extract relevant information
    for gb_record in SeqIO.parse(open(gb_file, "r"), "genbank"):
        gb_feature = gb_record.features[0]
        gb_qual = gb_feature.qualifiers

        if "strain" not in gb_qual and "isolate" in gb_qual:
            gb_qual["strain"] = gb_qual.pop("isolate")

        # Keys to be extracted from the qualifiers
        selected_keys = ["strain", "collection_date", "country"]

        # Optionally add "segment" to the keys if required
        if segment:
            selected_keys.append("segment")

        # Extract the required information, defaulting to "Unknown" if a key is missing
        gene_info = {key: gb_qual.get(key, ["Unknown"])[0] for key in selected_keys}
        gene_data.append(gene_info)

    # Convert the list to a DataFrame
    df = pd.DataFrame(gene_data, columns=selected_keys)

    # Process all collection_date values in the DataFrame
    df['collection_date'] = df['collection_date'].apply(autoRecognizeDate)

    return df


def rename_n_convert(gb_file, segment):
    """
    Rename sequences based on extracted information and convert GenBank file to FASTA format.

    Args:
    gb_file (str): Path to the GenBank file.
    segment (bool): Whether to include the segment information in the renaming (for segmented genomes).
    """
    df = get_info(gb_file, segment)
    # Get the base filename without the extension
    base_filename = os.path.splitext(gb_file)[0]

    fasta_file = f"{base_filename}.fasta"
    records = []
    count = 0

    # Parse the GenBank file and rename each record
    for record in SeqIO.parse(gb_file, "genbank"):
        record.description = ""  # Clear the description
        record.name = ""  # Clear the name
        record.id = ""  # Clear the ID

        # Construct the new name for the record
        if segment:
            new_name = f"{df['strain'][count]}|{df['country'][count]}|{df['collection_date'][count]}|segment {df['segment'][count]}"
        else:
            new_name = f"{df['strain'][count]}|{df['country'][count]}|{df['collection_date'][count]}"

        record.id = new_name
        records.append(record)
        count += 1  # Increment count to move to the next record

    # Write the renamed records to a FASTA file
    with open(fasta_file, 'w') as output_file:
        SeqIO.write(records, output_file, 'fasta')
        print(f"file {fasta_file} created successfully")


# Call the function to process the GenBank file and convert to FASTA
gb_file = "gene_seq.gb"
segment = True
rename_n_convert(gb_file, segment)