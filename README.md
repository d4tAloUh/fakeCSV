# FakeCSV is an online service for generating CSV files with fake(dummy) data using Python and Django:

#### Deployed to [heroku](fake-csv-d4t-alouh.herokuapp.com/)

### Service has following features:
* Schema creation and updating (Name, Columns etc.)
* DataSet creation
* DataSet download in csv format

### Libraries/Frameworks/Services used:
* Django
* Celery
* Bootstrap
* Firebase (heroku does not allow usage of internal storage)
* WhiteNoise (serving static files without proxy for django)
* Faker (data generating)
* Redis

### Test user:
```bash
username: test
password: test123

```

### To run celery on windows:
```bash
celery -A planeks.celery worker -P solo --loglevel=DEBUG
```
