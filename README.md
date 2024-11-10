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
* Docker ➜ [Download site for Docker Desktop](https://www.docker.com/products/docker-desktop/)
* PostgreSQL ➜ [Download site](https://www.postgresql.org/download/)
* Power BI (Desktop version) ➜ [Download site](https://www.microsoft.com/es-es/power-platform/products/power-bi/desktop)

> [!WARNING]
> Apache Airflow only runs correctly in Linux environments. If you have Windows, we recommend using a virtual machine or WSL.

The dependencies needed for Python are:

* apache-airflow
* python-dotenv
* kafka-python
* pandas
* matplotlib
* seaborn
* sqlalchemy
* psycopg2-binary
* scikit-learn
* xgboost

These libraries are included in the Poetry project config file ([`pyproject.toml`](https://github.com/JuanRuizIng/GlobalTerrorismAnalysis_ETL/blob/main/pyproject.toml)). The step-by-step installation will be described later.

---


## Dataset Information <img src="https://github.com/user-attachments/assets/5fa5298c-e359-4ef1-976d-b6132e8bda9a" alt="Dataset" width="30px"/>

> [!NOTE]
> This information is based on [the following file](https://www.start.umd.edu/gtd/downloads/Codebook.pdf).

After a rigorous cleaning and transformation process, our dataset has the following columns arranged for the analysis and visualization of your data:

| Column Name           | Type             | Description                                                                                                                                                                 |
|-----------------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **eventid**           | int64            | ID of the event in the GTD. It's a 12-digit number indicating the date of the incident (first 8 digits) and a sequential case number (last 4 digits).                       |
| **iyear**             | int64            | Year of the incident.                                                                                                                                                       |
| **imonth**            | int64            | Month of the incident.                                                                                                                                                      |
| **iday**              | int64            | Day of the incident.                                                                                                                                                        |
| **extended**          | int64            | Indicates if the duration of an incident extended more than 24 hours. Values: 1 for "Yes", 0 for "No".                                                                      |
| **country_txt**       | object           | Name of the country where the incident occurred.                                                                                                                            |
| **country**           | int64            | Country code where the incident occurred.                                                                                                                                   |
| **region_txt**        | object           | Name of the region where the incident occurred.                                                                                                                             |
| **region**            | int64            | Region code where the incident occurred.                                                                                                                                    |
| **city**              | object           | City where the incident occurred.                                                                                                                                           |
| **latitude**          | float64          | Geographic latitude of the incident.                                                                                                                                        |
| **longitude**         | float64          | Geographic longitude of the incident.                                                                                                                                       |
| **vicinity**          | int64            | Indicates if the incident occurred in the vicinity of a city or locality. Values: 1 for "Yes, nearby", 0 for "No, at the exact location", 9 for "Unknown".                  |
| **crit1**             | int64            | Criterion 1 for inclusion in the database, evaluating if the incident meets certain terrorism standards. Values: 1 for "Yes", 0 for "No".                                   |
| **crit2**             | int64            | Criterion 2 for inclusion in the database, evaluating if the incident meets certain terrorism standards. Values: 1 for "Yes", 0 for "No".                                   |
| **crit3**             | int64            | Criterion 3 for inclusion in the database, evaluating if the incident meets certain terrorism standards. Values: 1 for "Yes", 0 for "No".                                   |
| **doubtterr**         | float64          | Indicates if there are doubts about whether the incident is an act of terrorism. Values: 1 for "Yes", 0 for "No" (no doubt it is a terrorist act).                           |
| **multiple**          | float64          | Indicates if the incident is part of multiple related incidents. Values: 1 for "Yes", 0 for "No".                                                                            |
| **success**           | int64            | Indicates if the terrorist attack was successful. Values: 1 for "Yes", 0 for "No".                                                                                          |
| **suicide**           | int64            | Indicates if the attack was a suicide attack. Values: 1 for "Yes", 0 for "No".                                                                                              |
| **attacktype1_txt**   | object           | Textual description of the type of attack.                                                                                                                                  |
| **attacktype1**       | int64            | Code of the type of attack.                                                                                                                                                 |
| **targtype1_txt**     | object           | Textual description of the type of target.                                                                                                                                  |
| **targtype1**         | int64            | Code of the type of target.                                                                                                                                                 |
| **natlty1_txt**       | object           | Textual description of the nationality of the target.                                                                                                                       |
| **natlty1**           | float64          | Code of the nationality of the target.                                                                                                                                      |
| **gname**             | object           | Name of the group that carried out the attack.                                                                                                                              |
| **guncertain1**       | float64          | Indicates if the perpetrator group is suspected or unconfirmed. Values: 1 for "Yes", 0 for "No".                                                                             |
| **individual**        | int64            | Indicates if the perpetrators were individuals not affiliated with a group. Values: 1 for "Yes", 0 for "No".                                                                 |
| **nperps**            | float64          | Number of perpetrators involved in the incident.                                                                                                                            |
| **nperpcap**          | float64          | Number of captured perpetrators.                                                                                                                                            |
| **claimed**           | float64          | Indicates if someone claimed responsibility for the attack. Values: 1 for "Yes", 0 for "No".                                                                                |
| **weaptype1_txt**     | object           | Textual description of the type of weapon.                                                                                                                                  |
| **weaptype1**         | int64            | Code of the type of weapon.                                                                                                                                                 |
| **nkill**             | float64          | Number of people killed.                                                                                                                                                    |
| **nwound**            | float64          | Number of people wounded.                                                                                                                                                   |
| **property**          | int64            | Indicates if there was property damage. Values: 1 for "Yes", 0 for "No", 9 for "Unknown".                                                                                   |
| **ishostkid**         | float64          | Indicates if there was a hostage kidnapping. Values: 1 for "Yes", 0 for "No", 9 for "Unknown".                                                                              |
| **INT_ANY**           | int64            | Indicates international participation. Values: 1 for "Yes", 0 for "No", 9 for "Unknown".                                                                                    |
| **date**              | datetime64[ns]   | Date of the incident.                                                                                                                                                       |
| **date_country_actor**| object           | Unique identifier combining date, country, and actor information.                                                                                                           |

## API Information <img src="https://cdn-icons-png.flaticon.com/512/10169/10169724.png" alt="API" width="30px"/>

For this installment of the project, [we must also use an API](https://acleddata.com/) that must be merged with the main dataset using a ***merge***. After passing such data through cleansing and transformation processes, our dataset presents the following columns arranged for analysis and visualization of your data:

| Column Name | Type | Description |
| --- | --- | --- |
| event_id_cnty | string | A unique alphanumeric event identifier by number and country acronym. This identifier remains constant even when the event details are updated. |
| event_date | date | The date on which the event took place. Recorded as Year-Month-Day. |
| year | int | The year in which the event took place. |
| time_precision | int | A numeric code between 1 and 3 indicating the level of precision of the date recorded for the event. The higher the number, the lower the precision. |
| disorder_type | string | The disorder category an event belongs to. |
| event_type | string | The type of event; further specifies the nature of the event. |
| sub_event_type | string | A subcategory of the event type. |
| actor1 | string | One of two main actors involved in the event (does not necessarily indicate the aggressor). |
| assoc_actor_1 | string | Actor(s) involved in the event alongside ‘Actor 1’ or actor designations that further identify ‘Actor 1’ |
| inter1 | int | A numeric code between 0 and 8 indicating the type of ‘Actor 1’. |
| actor2 | string | One of two main actors involved in the event (does not necessarily indicate the target or victim). |
| assoc_actor_2 | string | Actor(s) involved in the event alongside ‘Actor 2’ or actor designation further identifying ‘Actor 2’. |
| inter2 | int | A numeric code between 0 to 8 indicating the type of ‘Actor 2’. |
| interaction | int | A two-digit numeric code (combination of ‘Inter 1’ and ‘Inter 2’) indicating the two actor types interacting in the event. |
| civilian_targeting | String | This column indicates whether the event involved civilian targeting. |
| iso | int | A unique three-digit numeric code assigned to each country or territory according to ISO 3166. |
| region | string | The region of the world where the event took place. |
| country | string | The country or territory in which the event took place. |
| admin1 | string | The largest sub-national administrative region in which the event took place. |
| admin2 | string | The second largest sub-national administrative region in which the event took place. |
| admin3 | string | The third largest sub-national administrative region in which the event took place. |
| location | string | The name of the location at which the event took place. |
| latitude | decimal | The latitude of the location in four decimal degrees notation (EPSG:3857). |
| longitude | decimal | The longitude of the location in four decimal degrees notation (EPSG:3857). |
| geo_precision | int | A numeric code between 1 and 3 indicating the level of certainty of the location recorded for the event. The higher the number, the lower the precision. |
| source | string | The sources used to record the event. Separated by a semicolon. |
| source_scale | string | An indication of the geographic closeness of the used sources to the event |
| notes | string | A short description of the event. |
| fatalities | int | The number of reported fatalities arising from an event. When there are conflicting reports, the most conservative estimate is recorded |
| tags | string | Additional structured information about the event. Separated by a semicolon. |
| timestamp | int/date | An automatically generated Unix timestamp that represents the exact date and time an event was last uploaded to the ACLED API. |
| population_1km | int | Estimated population in a 1km radius (only returned if population=full) |
| population_2km | int | Estimated population in a 2km radius (only returned if population=full) |
| population_5km | int | Estimated population in a 5km radius (only returned if population=full) |
| population_best | int | Best estimate of affected population (only returned if population=full OR population=TRUE) |

## Data flow <img src="https://cdn-icons-png.flaticon.com/512/1953/1953319.png" alt="Data flow" width="22px"/>

![Flujo de datos](https://github.com/user-attachments/assets/9e196f2a-b330-452a-be45-78c8410332e8)

## Run the project <img src="https://github.com/user-attachments/assets/99bffef1-2692-4cb8-ba13-d6c8c987c6dd" alt="Running code" width="30px"/>

### Clone the repository 🔧

Execute the following command to clone the repository:

```bash
  git clone https://github.com/JuanRuizIng/GlobalTerrorismAnalysis_ETL.git
```

---

### Download the dataset 📥

Given the large size of the file to be analyzed, we recommend downloading the dataset on your own at [this link](https://www.kaggle.com/datasets/START-UMD/gtd). Once downloaded, create a folder called data in the cloned repository: inside it save the CSV file.

#### Demonstration of the process

![CSV file](https://github.com/user-attachments/assets/f6da9726-8423-46c9-a146-cd2a1db33dc9)

---

### Enviromental variables 🌐

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

API_KEY = # ACLED API key
API_EMAIL = # Registered ACLED API email
 ```

#### Demonstration of the process

![ENV file](https://github.com/user-attachments/assets/ed5d86b4-aab7-4085-adb2-ff790ad2b35b)

---

### Installing the dependencies with *Poetry* 📦

> To install Poetry follow [this link](https://elcuaderno.notion.site/Poetry-8f7b23a0f9f340318bbba4ef36023d60?pvs=4).

Execute `poetry install` to install the dependencies. In some case of error with the *.lock* file, just execute `poetry lock` to fix it. Now you can execute the notebooks!

#### Demonstration of the process

![Poetry](https://github.com/user-attachments/assets/e68ff3ad-d3d7-4d4a-bd41-22550b1daa4b)

---

### Deploy the database in the cloud ☁️

To perform the Airflow tasks related to Data Extraction and Loading we recommend **making use of a cloud database service**. Here are some guidelines for deploying your database in the cloud:

* [Microsoft Azure - Guide](https://github.com/JuanRuizIng/GlobalTerrorismAnalysis_ETL/blob/main/docs/guides/azure_postgres.md)
* [Google Cloud Platform (GCP) - Guide](https://github.com/JuanRuizIng/GlobalTerrorismAnalysis_ETL/blob/main/docs/guides/gcp_postgres.md)

---

### Run the notebooks 📓

We execute the 3 notebooks following the next order. You can run these by just pressing the "Execute All" button:

   1. *001_rawDataLoad.ipynb*
   2. *002_GlobalTerrorismEDA.ipynb*
   3. *003_cleanDataLoad.ipynb*
   4. *004_api_analysis.ipynb*

![orden_ejecucion](https://github.com/user-attachments/assets/ed210736-f1ce-4ef3-a5b5-d8777202e132)

Remember to choose **the right Python kernel** at the time of running the notebook.

![py_kernel](https://github.com/user-attachments/assets/684d8050-2990-4825-838e-55d0c82f9d9d)

---

### 🚀 Running the Airflow pipeline

To run Apache Airflow you must first export the `AIRFLOW_HOME` environment variable. This environment variable determines the project directory where we will be working with Airflow.

```bash
export AIRFLOW_HOME="$(pwd)/airflow"
```

You can run Apache Airflow with the following command:

```bash
airflow standalone
```

Allow Apache Airflow to read the modules contained in `src` by giving the absolute path to that directory in the configuration variable `plugins_folder` at the `airflow.cfg` file. You may need to restart Apache Airflow in case you recieve some DAG Import Error.

![plugins_folder](https://github.com/user-attachments/assets/70437ba5-a810-47fa-9c2c-faf8988727b5)

#### Demonstration of the process

> [!IMPORTANT]
> You need to enter the address [http://localhost:8080](http://localhost:8080/) in order to run the Airflow GUI and run the DAG corresponding to the project (*gta_dag*).

![airflow](https://github.com/user-attachments/assets/b8bbb85c-c2da-4e57-9844-0fcfcc62db7a)

---

## Thank you! 💕🐍

Thanks for visiting our project. Any suggestion or contribution is always welcome, 👄.
