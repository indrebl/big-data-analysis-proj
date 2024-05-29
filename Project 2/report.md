# Big data assignment 2
# Indrė Blagnytė
## Purpose of python program
This program (big_data_2assign.py) was created to enable more informative conversion from genbank to fasta formats. In genetics DNA code is primarily stored in two formats: genbank or fasta. Genbank is a very informative format that contains a lot of information about the sequence and how and when it was acquired. Fasta is a very simple format that only includes a sequence name and the genetic sequence itself. Most analysis and comparison programs only accept fasta files, however when a simple conversion is used, all the information needed to understand the results is lost. To avoid the need for crossreferencing separate information files, I wrote this python program that extracts the neccesarry information from the genbank file and converts it to fasta while encoding the information in the sequence name in the format: **strain|country|collection_date|segment**. Because the sequences are uploaded by the scientists that sequenced them, the formats in which the information was written were also not always consistent and had to be standardized. For example some scientists used the term isolate instead of strain, and collection dates were written in different formats and with variable accuracy. This program is primarily meant for working with virus genomes and has the variable `segment` that can be set to `True` or `False` depending on whether the type of viruses analyzed are segmented or not. To show how this code works I used an input file gene_seq.gb - a genbank file that includes 1294 individual sequences from various strains and segments of segmented viruses. The output is a fasta file with the same as input file name but an .fasta extension.

## Creating Docker image
I created a directory where I put my python program big_data_2assign.py and the input file gene_seq.gb. In that same directory I created requirements.txt file containing:
```
bio==1.7.0
biopython==1.83
biothings-client==0.3.1
certifi==2024.2.2
charset-normalizer==3.3.2
colorama==0.4.6
gprofiler-official==1.0.0
idna==3.7
mygene==3.2.2
numpy==1.26.4
packaging==24.0
pandas==2.2.2
platformdirs==4.2.2
pooch==1.8.1
python-dateutil==2.9.0.post0
pytz==2024.1
requests==2.32.2
six==1.16.0
tqdm==4.66.4
tzdata==2024.1
urllib3==2.2.1
```
and also a Dockerfile containing:
```
# Parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy current directory contents into the container
COPY . .

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "./big_data_2assign.py"]
```

In command line after navigating to the directory with the Dockerfile the image was created with the command:

```
docker build -t genbank-to-fasta .
```
## Running the Docker container
First I ran the container normally, using the command in command-line:
```
docker run genbank-to-fasta
```

The process ran successfully with no errors. While the fasta file was created I couldn't check the contents, so I ran the container in detached mode and copied the output file to my computer with the commands:

```
docker run -d genbank-to-fasta
docker cp container_name:/usr/src/app/gene_seq.fasta C:\Users\Indre\Downloads/gene_seq.fasta
docker stop container_name
```

After checking the copied over output file, the conversion was successful.

Pushed to a public dockerhub repository **indrebl/big_data2**, used tag **latest**:

```
docker login
docker tag genbank-to-fasta indrebl/big_data2:latest
docker push indrebl/big_data2:latest
```
command for pulling **latest**
```
docker pull indrebl/big_data2:latest
```