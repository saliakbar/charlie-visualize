# Note
This is a reproduction project as part of the MSR course 2021/22 at UniKo, CS department, SoftLang Team.

## Names of team/students

**Team Name:** Charlie  
**Members:** 
- Syed Ali Akbar (220202744 - aliakbar@uni-koblenz.de)
- Dafina Uka (220202435 - dafinauka@uni-koblenz.de)
- Syed Ahmer Mashhadi (220201221 - mashhadi@uni-koblenz.de)

## Baseline study
### Aspect of the reproduction project
- We as team Charlie, chose to reproduce the visualization aspeect of the thesis, with which we aim to create a class map visualization of any given Java projeect, and these mappings will be seen in form of HTML and pdf files. The visualization aspect of the thesis is also related to the Assignment 0 that we had taken previously, and this made us go with this implementation as well. 
### Input data
- The input were written through the datasets structured as per the Novetta/CLAVIN repository. These files are in CSV standard, after going through different earlier phases. These CSV files are the direct input to this visualization aspect.
### Output data
- The output is in the form of HTML and pdf files that shows the visualization of the input Java project.

## Findings of replication

### Process delta
The project is a replication of the visualization and therefore does not contain any major changes, although if valid input files provided, the project will work flawlessly for that case.
### Output delta
The output files will be generated in the ".data/visualization" folder, apart from that, there is no further changes in this replication.

## Implementation of replication
### Hardware requirements
#### Windows: 
- Processor: Intel i5-6600k (4 core 3.5 GHz) or AMD Ryzen 5 2400 G (4 core 3.6 GHz)
- Memory:	4.00 GB
- System type:	64-bit operating system, x64-based processor
- OS:	Windows 10, 11
#### MAC OS
- Processor: 2.2 GHz 6-Core Intel Core i7
- Memory: 16 GB 2400 MHz DDR4
- OS: MAC OS Monterey v12.1
### Software requirements
* Java
	* Java 1.8
* python
	* pandas
	* plotly
	* pyspark
	
### Validation
To verify the output, it is best to open the generated files and go through the results in "data/visualization" folder. 

### Data
We have used the Novetta_CLAVIN dataset as the initial implementation and for additional work, we collected datasets from Team X-ray, and implemented our approach to generate visualization files as well. All the results can be found within `./data/visualization` folder. 
Following files are being used as the datasets: 

Folder type  	| 	Folder Name
----------------|--------------
Dataset (Group X-Ray) 	| `./data/data_DependencyTrack_dependency-track.csv`
Dataset (Original)	| `./data/data_Novetta_CLAVIN.csv`
Dataset (Group X-Ray)	| `./data/data_Stratio_cassandra-lucene-index.csv`
Dataset (Group X-Ray) 	| `./data/data_dice-group_AGDISTIS.csv`
Dataset (Group X-Ray) 	| `./data/data_dice-group_Palmetto.csv `
Dataset (Group X-Ray) 	| `./data/data_intuit_fuzzy-matcher.csv`
Dataset (Group X-Ray) 	| `./data/data_javasoze_clue.csv`
Dataset (Group X-Ray) 	| `./data/data_senseidb_zoie.csv `
Dataset (Group X-Ray) 	| `./data/data_weiboad_fiery.csv `
Dataset (Group X-Ray) 	| `./data/data_ysc_word.csv `
