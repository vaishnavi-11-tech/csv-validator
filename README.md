++**CSV-Validator**++

**Purpose**:- Before Mass change action on the customers, this will validate the csv file if the data is formatted with specific rules.

**Install**:- We have to install Python Latest Version, Pytest for these. And need to use the modules or libraries whatever is needed like below:-

**argparse** :- to parse the arguments direcly in the command line with the required fieldnames.

**csv**:- to convert the csv file into dictionary in the form of fieldnames as keys and each data rows as one dictionary.

**Sys**:- to give the input in the command line instead of in the code and it will help to exit the program at any time.

**pathlib** :-  To retrive the files/folders in the local, we will use path module.

**One Usage Line:**- The csv file will be validated by checking if there is any missing column names or any null values or missing data. If the wrong column names exist, It will validate and return the output with the data.

**There are three exit codes**. If the required column is missing, then it will exit with the code 2. 

If there is an blank column or any rows are duplicated, then it will exit with the code 1.

If there are no errors in the csv files it will exit with the code 0 which is successfully validated without errors or bugs.

Input Format:- We have to give the below input format while executing in the command line.

`python validator.py sample.csv --required id,name,email`

**Below are the example output**

row 3: blank column name

row 4: blank column email

row 5: duplicate of row 2

If a csv file is clean and no issues, then it will exits with 0 and there will be no output.

