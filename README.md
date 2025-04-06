## Bio-Toolbox2025

# Authors  
**Emiel Bosma**  
**Ruben van Dam**  
**Michelle Hazeveld**  
**Keren Saint Fleur**  

# Version  
*0.2*  

# Date  
*March 29, 2025*  

## Description  
### What can you do with the website and the tool?  
The web application combines KEGG Pull and KEGG Mapper into a single centralized environment, making the analysis and visualization of biological data more efficient and user-friendly. KEGG Pull enables the extraction of relevant data, such as gene sequences, pathways, and orthologs, from the KEGG database. KEGG Mapper helps visualize this data and allows experimental data to be linked to known biological processes.  

The web application is designed for a broad audience within the life sciences, including researchers in bioinformatics and systems biology, molecular biologists, geneticists, students, and educators. With this tool, users can easily retrieve specific genetic and metabolic data, analyze and visualize pathways and biological processes.  

By integrating KEGG tools into an accessible online environment, it becomes easier for both researchers and students to use large molecular datasets and gain a better understanding of biological systems.  

KEGG is a database used to understand high-level (cell-level or higher) functions and the practical use of biological systems, such as the cell, organism, and ecosystem—based on molecular-level information (GenomeNet, n.d.). This information is primarily obtained from large-scale molecular datasets derived from genome sequencing and other high-throughput (partially automated, efficient) experimental technologies. The website, along with the KEGG Pull and KEGG Mapper tools, provides options for analyzing and visualizing biological data at different levels.  

The website is suitable for various groups within the life sciences, including:  
- Researchers in bioinformatics and systems biology.  
- Molecular biologists and geneticists.  
- Students and educators in the life sciences.  
- Bioinformaticians.  

### What questions can be answered using the website and tool?  
- Which genes are involved in specific biological pathways and processes?  
- How are certain metabolic pathways organized, and which enzymes play a role in them?  
- What are the orthologous genes of different species for a given function?  
- How can experimental data (e.g., gene expression) be integrated with known biological pathways?  
- What molecular mechanisms underlie certain diseases?  
- Which biochemical reactions are related to specific chemical compounds or enzymes?  

# Installation Guide  
To use KEGG Pull, you need at least Python 3.10 or later.  
To avoid installing this package directly on your company's or personal server, it is strongly advised to install it in a virtual environment (.venv).
To use this (.venv)-enviroment you need to need access to for example PyCharm. By creating a new file (f.e. while cloning this repository)
you need to check the (.venv)-box and the Flask one to run our project properly.
To install the required python packages, use the following command in your Python IDE terminal (such as PyCharm or VS Code)
this command applies to Linux, Mac OS X and Windows:  
  
**Windows, Linux and MacOS**:  
```bash
pip install -r requirements.txt
```
  
**Outside Python-IDE Windows**:  
```bash
python -m pip install -r requirements.txt
```

**Outside Python-IDE Linux or MacOS**:  
```bash
python3 -m pip install -r requirements.txt
```
#### Please check if the .venv is enabled

### Known Issues and Troubleshooting  
If you encounter any issues, please check the following common problems. If your issue is not listed, contact one of the authors.  

- **Colons (:) may be replaced with underscores (_) on some systems (mainly Windows).** This applies to KEGG entry IDs.  
- **If Python is not installed on Windows**, use the same installation command as for Linux and Mac OS X.  
- **If the 'kegg_pull' console script is not found on Windows**, you can use the CLI via:  
  ```bash
  pip install kegg_pull
  ```  
  Or use the direct path:  
  ```bash
  path\to\console\script\kegg_pull.exe
  ```  
  Alternatively, add the directory containing the console script to your system's Path environment variable. An example location of the script could be:  
  ```bash
  C:\Users\<username>\AppData\Local\Programs\Python\Python310\Scripts\
  ```  

# Command Line Usage  
Usage:  
```bash
kegg_pull -h | --help           # Show this help message.  
kegg_pull -v | --version        # Display the package version.  
kegg_pull --full-help           # Show the help message for all subcommands.  
kegg_pull pull ...              # Pull, separate, and store an arbitrary number of KEGG entries to the local file system.  
kegg_pull entry-ids ...         # Obtain a list of KEGG entry IDs.  
kegg_pull map ...               # Obtain a mapping of entry IDs (KEGG or external databases) to the IDs of related entries.  
kegg_pull pathway-organizer ... # Create a flattened version of a pathway's Brite hierarchy.  
kegg_pull rest ...              # Execute one of the KEGG REST API operations.  
```
  
# Support  
GitHub usernames of the authors:  
- **Emiel Bosma**: emielbosma  
- **Keren Saint Fleur**: Keren8772  
- **Michelle Hazeveld**: michellehazeveld  
- **Ruben van Dam**: RCvanDam  

# References  
- BioMed Central Ltd. (n.d.). *KEGG Pull*. Retrieved on February 22-23, 2025, from [BioMed Central](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-023-05208-0)  
- GenomeNet (n.d.). *KEGG: Kyoto Encyclopedia of Genes and Genomes*. Retrieved on February 21, 2025, from [GenomeNet](https://www.genome.jp/kegg/)  
- GenomeNet (n.d.). *KEGG Mapper*. Retrieved on February 21-24, 2025, from [GenomeNet](https://www.genome.jp/kegg/mapper/)  
- Learning. (n.d.). *Project Management - Project Plan*. Retrieved on February 24, 2025, from [Leren](https://www.leren.nl/cursus/management/projectmanagement/projectplan.html)  
- eJournal Online Environment (2025). Retrieved on February 24, 2025.  
- Zhang, C., Chen, Z., Zhang, M., & Jia, S. (2023, February 1). *KEGG Extractor: An Effective Extraction Tool for KEGG Orthologs*. Retrieved on February 21, 2025, from [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9956942/)  
