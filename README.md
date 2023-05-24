# flask-planet.org

### Community Website for Flask

The flask-planet.org website is a community website for the Flask microframework. It aggregates news, articles and
resources for the Flask framework.

### Contributing

If you want to contribute to the website, clone this repository and create a new branch. Then add your changes, commit,
push and create a pull request.

### Contributing to the website content

For News / Articles see: [Artilce Repo](https://github.com/Flask-Planet/flask-planet.org-submitted-articles)

For Resources see: [Resources Repo](https://github.com/Flask-Planet/flask-planet.org-submitted-resources)

### Running the website locally

To run the website locally, you need to install the dependencies first:

```bash
$ python3 -m venv venv
```

```bash
$ source venv/bin/activate
```

```bash
(venv)$ pip install -r requirements.txt
```

Then you can run the website with:

```bash
(venv)$ flask run
```

### cli commands
```bash
# Reset the database, drops then creates all tables
(venv)$ flask reset-db
```

```bash
# Create a new user
(venv)$ flask create-user
```

```bash
# Create example data
(venv)$ flask example-data
```

### Live website is hosted in docker that is not automatically deployed.