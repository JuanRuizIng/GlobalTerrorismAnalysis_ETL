# Global Terrorism Analysis - ETL Project 💣

**Realized by:**

- *[Martín García](https://github.com/mitgar14)*
- *[David Melo](https://github.com/Davidmelo9133)*
- *[Juan Andrés Ruiz](https://github.com/JuanRuizIng/)*

## Overview ✨

In this case we decided to use a dataset that includes information on terrorist attacks worldwide from 1970 to 2017. **[The dataset used](https://www.kaggle.com/datasets/START-UMD/gtd)** has 181.691 rows and 135 columns: we subjected it to loading, cleaning and transformation processes to find interesting insights about the different terrorist attacks recorded there.

***The tools used are:***

* Python 3.10 ➜ [Download site](https://www.python.org/downloads/)
* Jupyter Notebook ➜ [VS Code tool for using notebooks](https://youtu.be/ZYat1is07VI?si=BMHUgk7XrJQksTkt)
* PostgreSQL ➜ [Download site](https://www.postgresql.org/download/)
* Power BI (Desktop version) ➜ [Download site](https://www.microsoft.com/es-es/power-platform/products/power-bi/desktop)

The dependencies needed for Python are:

* Apache Airflow
* Dotenv
* Pandas
* Matplotlib
* Seaborn
* SQLAlchemy

These dependencies are included in the *requirements.txt* file of the Python project. The step-by-step installation will be described later.

## Dataset Information <img src="https://github.com/user-attachments/assets/5fa5298c-e359-4ef1-976d-b6132e8bda9a" alt="Dataset" width="30px"/>

> [!NOTE]
> This information is based on [the following file](https://www.start.umd.edu/gtd/downloads/Codebook.pdf).

After a rigorous cleaning and transformation process, our dataset has the following columns arranged for the analysis and visualization of your data:

* **eventid**: ID of the event in the GTD. It's a 12-digit number indicating the date of the incident (first 8 digits) and a sequential case number (last 4 digits).
* **iyear**: Year of the incident.
* **imonth**: Month of the incident.
* **iday**: Day of the incident.
* **extended**: Indicates if the duration of an incident extended more than 24 hours. Values: `1` for "Yes", `0` for "No".
* **country_txt**: Name of the country where the incident occurred.
* **country**: Country code where the incident occurred.
* **region_txt**: Name of the region where the incident occurred.
* **region**: Region code where the incident occurred.
* **city**: City where the incident occurred.
* **latitude**: Geographic latitude of the incident.
* **longitude**: Geographic longitude of the incident.
* **vicinity**: Indicates if the incident occurred in the vicinity of a city or locality. Values: `1` for "Yes, nearby", `0` for "No, at the exact location", `9` for "Unknown".
* **crit1, crit2, crit3**: Criteria for inclusion in the database, evaluating if the incident meets certain terrorism standards. Values: `1` for "Yes", `0` for "No".
* **doubtterr**: Indicates if there are doubts about whether the incident is an act of terrorism. Values: `1` for "Yes", `0` for "No (Essentially, there is no doubt that it is a terrorist act)".
* **multiple**: Indicates if the incident is part of multiple related incidents. Values: `1` for "Yes", `0` for "No".
* **success**: Indicates if the terrorist attack was successful. Values: `1` for "Yes", `0` for "No".
* **suicide**: Indicates if the attack was a suicide attack. Values: `1` for "Yes", `0` for "No".
* **attacktype1_txt**: Textual description of the type of attack.
* **attacktype1**: Code of the type of attack.
* **targtype1_txt**: Textual description of the type of target.
* **targtype1**: Code of the type of target.
* **natlty1_txt**: Textual description of the nationality of the target.
* **natlty1**: Code of the nationality of the target.
* **gname**: Name of the group that carried out the attack.
* **guncertain1**: Indicates if the perpetrator group is suspected or unconfirmed. Values: `1` for "Yes", `0` for "No".
* **individual**: Indicates if the perpetrators were individuals not affiliated with a group. Values: `1` for "Yes", `0` for "No".
* **nperpcap**: Number of captured perpetrators.
* **claimed**: Indicates if someone claimed responsibility for the attack. Values: `1` for "Yes", `0` for "No".
* **weaptype1_txt**: Textual description of the type of weapon.
* **weaptype1**: Code of the type of weapon.
* **nkill**: Number of people killed.
* **property**: Indicates if there was property damage. Values: `1` for "Yes", `0` for "No", `9` for "Unknown".
* **ishostkid**: Indicates if there was a hostage kidnapping. Values: `1` for "Yes", `0` for "No", `9` for "Unknown".
* **INT_ANY**: Indicates international participation. Values: `1` for "Yes", `0` for "No", `9` for "Unknown".

## API Information <img src="https://cdn-icons-png.flaticon.com/512/10169/10169724.png" alt="API" width="30px"/>

Insertar información sobre la API.

## Data flow

![Data flow](https://github.com/user-attachments/assets/44665b88-3789-4821-94cc-70fe05df9658)

## Run the project <img src="https://github.com/user-attachments/assets/99bffef1-2692-4cb8-ba13-d6c8c987c6dd" alt="Running code" width="30px"/>

### Clone the repository

> [!IMPORTANT]
> Although in this case the example is done with Ubuntu using WSL, this process can be done for any operating system (OS).

Execute the following command to clone the repository:

```bash
  git clone https://github.com/JuanRuizIng/GlobalTerrorismAnalysis_ETL.git
```

### Download the dataset

Given the large size of the file to be analyzed, we recommend downloading the dataset on your own at [this link](https://www.kaggle.com/datasets/START-UMD/gtd). Once downloaded, create a folder called data in the cloned repository: inside it save the CSV file.

#### Demonstration of the process

![CSV file](https://github.com/user-attachments/assets/f6da9726-8423-46c9-a146-cd2a1db33dc9)

### Enviromental variables

> From now on, the steps will be done in VS Code.

To establish the connection to the database, we use a module called *connection.py*. In this Python script we call a file where our environment variables are stored, this is how we will create this file:

1. We create a directory named ***env*** inside our cloned repository.

2. There we create a file called ***.env***.

3. In that file we declare 6 enviromental variables. Remember that the variables in this case go without double quotes, i.e. the string notation (`"`):
   ```python
    PG_HOST = # host address, e.g. localhost or 127.0.0.1
    PG_PORT = # PostgreSQL port, e.g. 5432

    PG_USER = # your PostgreSQL user
    PG_PASSWORD = # your user password
    
    PG_DATABASE = # your database name, e.g. postgres
   ```

#### Demonstration of the process

![ENV file](https://github.com/user-attachments/assets/ed5d86b4-aab7-4085-adb2-ff790ad2b35b)

### Virtual environment

Como se crea

#### Demonstration of the process

demostración

### Install the dependencies

pip install -r requirements.txt

#### Demonstration of the process

demostración

### Deploy the database in the cloud

link del notebook

### Run the notebooks

We execute the 3 notebooks following the next order. You can run these by just pressing the "Execute All" button:

   1. *001_rawDataLoad.ipynb*
   2. *002_GlobalTerrorismEDA.ipynb*
   3. *003_cleanDataLoad.ipynb*
   4. NOTEBOOK-API

![image](https://github.com/user-attachments/assets/ed210736-f1ce-4ef3-a5b5-d8777202e132)

Remember to choose **the right Python kernel** at the time of running the notebook.

imagen kernel

### Airflow environment

variables de entorno, airflow standalone, configurar airflow.cfg

## Thank you! 💕🐍

Thanks for visiting our project. Any suggestion or contribution is always welcome, 👄.
