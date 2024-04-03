# Automated cross-check documentation

## Document purpose

The aim of this document is to describe how the Python script developed to automate cross-checking between the S-101 FC and DCEG works, and to give advice to developers who may wish to adapt it for other S-100 products.

The Python scripts will be maintained by DQWG.

## Fonctionnement du script

The tool consists of 3 python scripts:

-   *read_files_S101.py:* parses and reads information contained in the S-101 FC and DCEG

-   *compare_files_S101.py:* compares information extracted from S-101 FC and DCEG

-   *cross_check_S101.py:* executes the functions defined in the 2 previous scripts

*N.B.: Knowledge of the Python programming language is strongly recommended for those wishing to adapt the script to compare other DCEG/FC of S-100 products.*

### read_files_S101.py

The following functions are defined in the file *read_files_S101.py*:

#### read_FC_S101

Function to extract the elements of interest in S-101 FC.

**Input:** S-101 FC in .xml format

**Output:** Dictionary containing the S-101 FC elements to be compared (Simple Attributes, Complex Attributes, Roles, Feature Associations, Information Types, Feature Types)

**How it works:** The function first parses the input .xml file (here S-101 FC), then isolates and stores in a dictionary the elements to be compared with the S-101 DCEG.

For information about parsing and extracting XML data in Python, see <https://docs.python.org/3/library/xml.etree.elementtree.html>

#### read_DCEG_S101

Function to extract the elements of interest in S-101 DCEG.

**Input:** S-101 DCEG in .docx format

**Output:** Dictionary containing the elements of the DCEG S-101, organized according to the title levels of the Word document.

**How it works:** The function parses the input .docx file (here S-101 DCEG), then stores its titles and paragraphs in a dictionary, referencing them by title and paragraph number.

For information about parsing Word document in Python, see <https://dadoverflow.com/2022/01/30/parsing-word-documents-with-python/>

### compare_files_S101.py

The following functions are defined in the file *compare_files_S101.py*:

#### compare_FC_DCEG_S101_SimpleAttributes

Function to check omission and consistency of Simple Attributes between FC and DCEG

**Input:**

-   S-101 FC dictionary

-   S-101 DCEG dictionary

**Output:**

Lists of omissions and inconsistencies identified between S-101 FC and DCEG for Simple Attributes on the following points:

-   Definition

-   Alias

-   Type

In the case of an enumeration attribute, for each enumerated value:

-   Label

-   Definition

-   Code

**How it works:**

The function retrieves the information contained in the DCEG dictionary for the chapters corresponding to the Simple Attibutes (27, 28 and 30). It then isolates the DCEG paragraphs corresponding to the information to be compared (definition, alias, etc.) and compares the string with that of the FC.

*N.B.: Some typology differences between DCEG and FC for special characters are accepted and implemented in the function.*

#### compare_FC_DCEG_S101_ComplexAttributes

Function to check omission and consistency of Complex Attributes between FC and DCEG

**Input:**

-   S-101 FC dictionary

-   S-101 DCEG dictionary

**Output:**

Lists of omissions and inconsistencies identified between S-101 FC and DCEG for Complex Attributes on the following points:

-   Title

-   Definition

-   Alias

-   Sub attributes

**How it works:**

Same operating principle as for compare_FC_DCEG_S101_SimpleAttributes, here for chapter 29.

#### compare_FC_DCEG_S101_Roles

Function to check omission and consistency of Roles between FC and DCEG

**Input:**

-   S-101 FC dictionary

-   S-101 DCEG dictionary

**Output:**

Lists of omissions and inconsistencies identified between S-101 FC and DCEG for Roles on the following points:

-   Title

-   Definition

**How it works:**

Same operating principle as for compare_FC_DCEG_S101_SimpleAttributes, here for chapter 26.

*compare_FC_DCEG_S101_FeatureAssociations*

Function to check omission and consistency of Feature Associations between FC and DCEG

**Input:**

-   S-101 FC dictionary

-   S-101 DCEG dictionary

**Output:**

Lists of omissions and inconsistencies identified between S-101 FC and DCEG for Feature Associations on the following points:

-   Title

-   Definition

-   Roles

**How it works:**

Same operating principle as for compare_FC_DCEG_S101_SimpleAttributes, here for chapter 25.

#### compare_FC_DCEG_S101_InformationTypes

Function to check omission and consistency of Information Types between FC and DCEG

**Input:**

-   S-101 FC dictionary

-   S-101 DCEG dictionary

**Output:**

Lists of omissions and inconsistencies identified between S-101 FC and DCEG for Information Types on the following points:

-   Title

-   Definition

-   Attributes

-   Multiplicity

**How it works:**

Same operating principle as for compare_FC_DCEG_S101_SimpleAttributes, here for chapter 24.

#### compare_FC_DCEG_S101_FeatureTypes

Function to check omission and consistency of Feature Types between FC and DCEG

**Input:**

-   S-101 FC dictionary

-   S-101 DCEG dictionary

**Output:**

Lists of omissions and inconsistencies identified between S-101 FC and DCEG for Feature Types on the following points:

-   Title

-   Definition

-   Alias

-   Attributes

-   Multiplicity

-   Permitted Values

**How it works:**

Same operating principle as for compare_FC_DCEG_S101_SimpleAttributes, here for chapter 3 to 23.

### cross_check_S101.py

Les fonctions définies dans read_files_S101.py et compare_files_S101.py sont exécutées via ce script qui permet de tout centraliser.

*N.B.: A human analysis of the elements reported by the script is still systematically necessary to identify precisely where the inconsistency lies, and whether it is indeed worth reporting.*
