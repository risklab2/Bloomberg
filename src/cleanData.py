from collections import defaultdict
import re
import os
import pandas as pd
from tqdm import tqdm


def getInfo(df):
  # Get the index and column names
  index = df.index  # Shows the index labels and dtype
  columns = df.columns  # Shows column names

  print("1st Print")
  print("Index details:", index)
  print("Column names:", columns)


  print("\n\n2st Print")
  # =COUNTA(UNIQUE(B5:B310))
  # =COUNTA(C6:EL6)
  numRows, numColumns = df.shape
  print("Number of rows:", numRows)
  print("Number of columns:", numColumns)

  print("\n\n3rd Print")
  print("Column data types:")
  print(df.dtypes)
  print("Index name(s):", df.index.names)




def cleanExcel(fileName):
    df = pd.read_excel(fileName, header=None)
    
    # Saving the Stock Name
    Stock_Name = df.iloc[0, 0]  
    Stock_Name = Stock_Name.replace(" ", "_")

    #-------------------------
    # Step 1 Extract everything from row 6 onward RAW
    df_from_row_6 = df.iloc[5:].copy()  # Rows start from 0, so row 6 is index 5

    # General Clean up of the Excel
    df_from_row_6.iloc[0, 1] = "Parameter"

    df_from_row_6.columns = df_from_row_6.iloc[0]
    df_from_row_6 = df_from_row_6.reset_index(drop=True)
    df_from_row_6 = df_from_row_6.drop(0).reset_index(drop=True)

    # Saving the initial Names of the Variables
    parameterToName = defaultdict(list)
    parameterToName['_'].append('Total Assets')

    for i in df_from_row_6.index:
        parameterToName[df_from_row_6.iloc[i, 1]].append(df_from_row_6.iloc[i, 0])

    df_from_row_6 = df_from_row_6.drop('Total Assets', axis=1)
    # Dropping NaN Parameters because they should not have any data
    df_from_row_6 = df_from_row_6.dropna(subset=['Parameter'])
    df_from_row_6 = df_from_row_6.drop_duplicates(subset=['Parameter'])


    #-------------------------
    # Step 2 Transposing the Dataframe
    transposed_df = df_from_row_6.set_index("Parameter").T.copy()
    # Cleaning up the Date column and the Index
    transposed_df['Date']=transposed_df.index.astype(str)
    transposed_df = transposed_df.reset_index(drop=True)

    # Reordering the dataframe
    cols = ["Date"] + [col for col in transposed_df.columns if col != "Date"]
    transposed_df = transposed_df[cols]

    return transposed_df


def cleanExcelSegments(fileName):
    df = pd.read_excel(fileName, header=None)
    
    # Saving the Stock Name
    #Stock_Name = df.iloc[0, 0]  
    #Stock_Name = Stock_Name.replace(" ", "_")

    #-------------------------
    # Step 1 Extract everything from row 6 onward RAW
    df_from_row_6 = df.iloc[4:].copy()  # Rows start from 0, so row 6 is index 5

    # General Clean up of the Excel
    df_from_row_6.iloc[0, 0] = "Parameter"
    for col in df_from_row_6.columns:
        if pd.isna(df_from_row_6.iloc[0][col]):
            df_from_row_6 = df_from_row_6.drop(columns=[col])
    df_from_row_6.columns = df_from_row_6.iloc[0, :]

    df_from_row_6 = df_from_row_6.reset_index(drop=True)
    df_from_row_6 = df_from_row_6.drop(0).reset_index(drop=True)

    # Saving the initial Names of the Variables
    parameterToName = defaultdict(list)
    parameterToName['_'].append('Revenue')

    for i in df_from_row_6.index:
        parameterToName[df_from_row_6.iloc[i, 1]].append(df_from_row_6.iloc[i, 0])

    #df_from_row_6 = df_from_row_6.drop('Parameter', axis=1)

    # Dropping NaN Parameters because they should not have any data
    df_from_row_6 = df_from_row_6.dropna(subset=['Parameter'])
    
    # print("RIGHT BEFORE DROPPING DUPLICATES")
    # print(df_from_row_6['Parameter'].dtype)
    # print(df_from_row_6['Parameter'])
    #print(df_from_row_6)
    #temp = df_from_row_6.drop_duplicates(subset=['Parameter'])
    # print("RIGHT AFTER DROPPING DUPLICATES")
    # print(df_from_row_6['Parameter'].dtype)
    # print(df_from_row_6['Parameter'])
    # print(df_from_row_6)


    #-------------------------
    # Step 2 Transposing the Dataframe
    transposed_df = df_from_row_6.set_index("Parameter").T.copy()
    # Cleaning up the Date column and the Index
    transposed_df['Date']=transposed_df.index.astype(str)
    transposed_df = transposed_df.reset_index(drop=True)

    # Reordering the dataframe
    #transposed_df.insert(0, 'Date', transposed_df.pop('Date'))
    #cols = ["Date"] + [col.replace(' ', '_') for col in transposed_df.columns if col != "Date"]
    cols = ["Date"] + [col for col in transposed_df.columns if col != "Date"]

    #transposed_df = pd.concat([transposed_df[['Date']], transposed_df.drop(columns=['Date'])], axis=1)
    #print(transposed_df.columns)
    #final_df = transposed_df.set_index("Date").reset_index()
    
    #-----------------------------------------------
    #-----------------------------------------------
    #-----------------------------------------------
    # I think the issue was a formatting issue (all might be good)
    #-----------------------------------------------
    #-----------------------------------------------
    #-----------------------------------------------

    return transposed_df[cols]

def cleanFileName(fileName):
  # File Name Clean Up and Adding _V2
  filePath = fileName.replace("Raw_data", "Working_Data")
  fileNameWithoutExt = os.path.splitext(filePath)[0]
  newFileName = fileNameWithoutExt + "_V2.csv"
  return newFileName






base_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory is src/
root_dir = os.path.dirname(base_dir)

raw_data_folder = os.path.join(root_dir, 'Raw_data')  # Path to Raw_data folder
working_data_folder = os.path.join(root_dir, 'Working_Data')

keywords = {
    "segments": r"Segments",
    "quarter": r"Quarter|Quarterly",
    "yearly": r"Annual|Yearly|Annually"
}

# Lists to hold file paths for each category
segments_files = []
quarter_files = []
yearly_files = []

# === Group 1: File Selection Based on Keywords ===
# Traverse through subfolders and files in the data folder
for root, dirs, files in os.walk(raw_data_folder):
    for file in files:
        # Check for "Segments" keyword in file name
        if re.search(keywords["segments"], file, re.IGNORECASE):
            segments_files.append(os.path.join(root, file))
        # Check for "Quarter", "Quarterly" keywords in file name
        elif re.search(keywords["quarter"], file, re.IGNORECASE):
            quarter_files.append(os.path.join(root, file))
        # Check for "Annual", "Yearly", "Annually" keywords in file name
        elif re.search(keywords["yearly"], file, re.IGNORECASE):
            yearly_files.append(os.path.join(root, file))

        else:
            print(f"No matching keyword found in file: {file}")
#i = 0
for segment, quarter, yearly in tqdm(zip(segments_files, quarter_files, yearly_files), desc="Cleaning Files", total=len(quarter_files)):
    # Complete Segment later
    # print("quarter len: ", len(quarter_files))
    # print("zip len: ", len(list(zip(segments_files, quarter_files, yearly_files))))
    # print("yearly len: ", len(yearly_files))
    
    
    
    #-----------------------------------------------
    #-----------------------------------------------
    #-----------------------------------------------
    # I think the issue was a formatting issue (all might be good)
    #-----------------------------------------------
    #-----------------------------------------------
    #-----------------------------------------------
    
    
    
    #i += 1
    #if (i != 24 and i != 18): continue
    
    quarterDF = cleanExcel(quarter)
    yearlyDF = cleanExcel(yearly)
    #print(segment)
    segmentDF = cleanExcelSegments(segment)
    
    #print(cleanFileName(quarter))
    #print(cleanFileName(yearly))
    #print(cleanFileName(segment))
    #print(segmentDF)
    
    #print(i) # 23, 17, 
    #if i == 10: break
    
    #print(quarterDF)
    #print(yearlyDF)
    quarterDF.to_csv(cleanFileName(quarter), index=False)
    yearlyDF.to_csv(cleanFileName(yearly), index=False)
    segmentDF.to_csv(cleanFileName(segment), index=False)