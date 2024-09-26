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

> [!WARNING]
> Apache Airflow only runs correctly in Linux environments. If you have Windows, we recommend using a virtual machine or WSL.

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

## Data flow <img src="https://cdn-icons-png.flaticon.com/512/1953/1953319.png" alt="Data flow" width="22px"/>

![Data flow](https://github.com/user-attachments/assets/44665b88-3789-4821-94cc-70fe05df9658)

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
 ```

#### Demonstration of the process

![ENV file](https://github.com/user-attachments/assets/ed5d86b4-aab7-4085-adb2-ff790ad2b35b)

---

### Virtual environment 🐍

To install the dependencies you need to first create a Python virtual environment. In order to create it run the following command:

```bash
python 3 -m venv venv
```

Once created, run this other command to be able to run the environment. It is important that you are inside the project directory:

```bash
source venv/bin/activate
```

#### Demonstration of the process

![venv](https://github.com/user-attachments/assets/42cfa6ca-ffac-4790-bd75-1fd172f69cdc)

---

### Install the dependencies 📦

Once you enter the virtual environment you can and execute `pip install -r requirements.txt` to install the dependencies. Now, you can execute both the notebooks and the Airflow pipeline.

#### Demonstration of the process

![pip install](https://github.com/user-attachments/assets/8c377a48-2164-4546-a12e-5765765fddab)

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
   4. NOTEBOOK-API

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

Allow Apache Airflow to read the modules contained in `src` by giving the absolute path to that directory in the configuration variable `plugins_folder` at the `airflow.cfg` file:

![plugins_folder](https://github.com/user-attachments/assets/70437ba5-a810-47fa-9c2c-faf8988727b5)

#### Demonstration of the process

> [!IMPORTANT]
> You need to enter the address [http://localhost:8080](http://localhost:8080/) in order to run the Airflow GUI and run the DAG corresponding to the project (*gta_dag*).

![airflow](https://github.com/user-attachments/assets/b8bbb85c-c2da-4e57-9844-0fcfcc62db7a)

---

## Thank you! 💕🐍

Thanks for visiting our project. Any suggestion or contribution is always welcome, 👄.
