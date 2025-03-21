## Bio-Toolbox2025

# Authors
**Emiel Bosma**   
**Ruben van Dam**  
**Michelle Hazeveld**  
**Keren Saint Fleur**

# Version 
*0,1*

# Date
*03/03/2025*

## Description
# What can you do with the website and the tool?
  The web application combines KEGG Pull and KEGG Mapper into a single centralized environment, making the analysis and visualization of biological data more efficient and user-friendly. KEGG Pull enables the extraction of relevant data, such as gene sequences, pathways, and orthologs, from the KEGG database. KEGG Mapper helps visualize this data and allows experimental data to be linked to known biological processes.  
  The web application is designed for a broad audience within the life sciences, including researchers in bioinformatics and systems biology, molecular biologists, geneticists, students, and educators. With this tool, users can easily retrieve specific genetic and metabolic data, analyze and visualize pathways and biological processes.
  By integrating KEGG tools into an accessible online environment, it becomes easier for both researchers and students to use large molecular datasets and gain a better understanding of biological systems.
    
   KEGG is a database used to understand high-level (cell-level or higher) functions and the practical use of biological systems, such as the cell, organism, and ecosystem—based on molecular-level information (GenomeNet, n.d.). This information is primarily obtained from large-scale molecular datasets derived from genome sequencing and other high-throughput (partially automated, efficient) experimental technologies. The website, along with the KEGG pull and KEGG mapper tools, provides options for analyzing and visualizing biological data at different levels.
      
   The website is suitable for various groups within the life sciences. Some of these groups include:
        
   * Researchers in bioinformatics and systems biology.
   * Molecular biologists and geneticists.
   * Students and educators in the life sciences.
   * Bioinformaticians.
   # What questions can be answered using the website and tool?
   Which genes are involved in specific biological pathways and processes?
   How are certain metabolic pathways organized, and which enzymes play a role in them?
   What are the orthologous genes of different species for a given function?
   How can experimental data (e.g., gene expression) be integrated with known biological pathways?
   What molecular mechanisms underlie certain diseases?
   Which biochemical reactions are related to specific chemical compounds or enzymes?

# Installation guide

To use Kegg Pull you need to at least have Python 3.10 or above. 
To prevent to install this package on your companies or personal server, it is strongly advised to install this package in a virtual environment (.venv). 
To install this package, you need to provide the following command line in your python-IDE-terminal (for example in PyCharm or VSC): 
    
**Linux or Mac OS X**:pip install kegg-pull 
    
**Windows**: pip install kegg-pull 
    
There are different errors that may occur. Underneath are a few noted issues, if your problem is not amongst these, please contact one of the authors.  
    
Colons will – on some systems (mainly Windows) – be changed to underscores. This applies to KEGG entry ID’s. 
    
If py is not installed on Windows, the installation command is the same as Linux and Mac OS X. 
    
If the ‘kegg_pull’ console script is not found on Windows, the CLI can be used via pip install keg_pull’ or ‘path\to\console\script\kegg_pull.exe’. 
Alternatively, the directory where the console script is located can be added to the Path environment variable. 
Look at the following example of where the console script may be installed: c:\users\<username>\appdata\local\programs\python\python310\Scripts\ 


# Commandline example
Usage:  
* kegg_pull -h | --help           Show this help message.  
* kegg_pull -v | --version        Displays the package version.
* kegg_pull --full-help           Show the help message of all sub commands.
* kegg_pull pull ...              Pull, separate, and store an arbitrary number of KEGG entries to the local file system.
* kegg_pull entry-ids ...         Obtain a list of KEGG entry IDs.
* kegg_pull map ...               Obtain a mapping of entry IDs (KEGG or outside databases) to the IDs of related entries.
* kegg_pull pathway-organizer ... Creates a flattened version of a pathways Brite hierarchy.
* kegg_pull rest ...              Executes one of the KEGG REST API operations.

# Support
github namen
emielbosma
Keren8772
michellehazeveld
RCvanDam
# References
BioMed Central Ltd (z.d.).  KEGG_pull. Geraadpleegd op 22 en 23 februari 2025, van https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-023-05208-0 

GenomeNet (z.d.). KEGG: Kyoto Encyclopedia of Genes and Genomes. Geraadpleegd op 21 februari 2025, van https://www.genome.jp/kegg/ 

GenomeNet (z.d.). KEGG Mapper. Geraadpleegd op 21 en 24 februari 2025, van https://www.genome.jp/kegg/mapper/  

Leren. (z.d.). Leren > Cursus > Management > Projectmanagement > Projectplan. Geraadpleegd op 24 februari 2025, van https://www.leren.nl/cursus/management/projectmanagement/projectplan.html  

De online omgeving van eJournal (2025) Geraadpleegd op 24 februari 2025  

Zhang, C., Chen, Z., Zhang, M., & Jia, S. (2023, 1 februari). KEGG_Extractor: An Effective Extraction Tool for KEGG Orthologs. Geraadpleegd op 21 februari 2025, van https://pmc.ncbi.nlm.nih.gov/articles/PMC9956942/  


