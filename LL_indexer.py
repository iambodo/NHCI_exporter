# this file cleans the data import by removing identifiers to trace back the record.
import pandas as pd

 # custom functions
def clean_column_names(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
         .str.replace('gen - ', '')
        .str.replace(' ', '_')
        .str.replace(r'[^\w\s]', '', regex=True)
    )
    return df

def calculate_years_between(start_date, end_date):
    if pd.isnull(start_date) or pd.isnull(end_date):
        return 0
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    return (end_date - start_date) / pd.Timedelta(days=365.25)


# Read the CSV file
df = pd.read_csv('input_file.csv')

#print("Columns in input file")
#print(df.columns)

df = clean_column_names(df)

# Create a new unique index ID based on the values of the merged column
df['reg_ID'] = df['program_instance'].astype('category').cat.codes

# Calculate age from DOB
df['age_enrolled_by_dob'] = df.apply(lambda row: calculate_years_between(row['date_of_birth'], row['registration_date']), axis=1)

# Delete the TEI ID, Enrollment Id, Event ID, and DOB

df.drop(columns=['tracked_entity_instance', 'program_instance','event','date_of_birth'], axis=1, inplace=True)

#  add a one if contains a supporter . repeat for phone number

df['has_supporter'] = df['supporters_name'].notna().astype(int)
df.drop(columns='supporters_name', inplace=True)


df['has_phone'] = df['patient_phone_number'].notna().astype(int)
df.drop(columns='patient_phone_number', inplace=True)


# Save the modified DataFrame to a new CSV file
df.to_csv('output_file.csv', index=False)


print("New CSV file saved successfully!")

print("Columns in cleaned file")
print(df.columns.tolist())
 
