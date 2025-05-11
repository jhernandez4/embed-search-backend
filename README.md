# Backend Set Up and Installation

## Prerequisites
* **Python 3.8+**
* **PostgreSQL 17.2+**


## Installation
**1. Clone the repository**
```bash
git clone https://github.com/jhernandez4/embed-search-backend.git
cd embed-search-backend 
```

**2. Create a PostgreSQL database** 
```sql
CREATE DATABASE embed_search;
```

**3. Create an `.env` file**
* In the root of your project directory, create a `.env` file with the following content
* Make sure that the name of the database created in the previous step 
matches the database name in the `.env` file

```bash
MYSQL_URI="postgresql://<username>:<password>@localhost/embed_search"
FRONTEND_ORIGIN="http://localhost:5173"
```

**4. Create a virtual environment**
```bash
python -m venv virtualEnv
```
**5. Activate the virtual environment**
* **Windows**
```bash
.\virtualEnv\Scripts\activate
```
* **MacOS/Linux**
```bash
source virtualEnv/bin/activate
```

**6. Install the dependencies**
```bash
pip install -r requirements.txt 
```

**7. Run the FastAPI development server**
```bash
fastapi dev .\main.py
```