======================================================================
{{ cookiecutter.project_name }}: {{ cookiecutter.short_description }}
======================================================================

Building
=========

Install Visual Studio code and load this project.

On VSCode command prompt run following:

* Run Task > Build Project


Initializing Database
======================

You will need following databases created on your local PostgreSQL:

* {{ cookiecutter.project_name }}
{% if cookiecutter.project_type == "morpcc" %}
* {{ cookiecutter.project_name }}_warehouse
* {{ cookiecutter.project_name }}_cache
{% endif %}

On VSCode command prompt run following sequence:

* Run Task > Generate Migrations
* Run Task > Update Database

{% if cookiecutter.project_type == "morpcc" %}
* Run Task > MorpCC: Create Default Admin User (admin:admin)
{% endif %}

Starting Up
===========

* Run Task > Start Application

{% if cookiecutter.project_type == "morpcc" %}
Login as ``admin``, with password ``admin``
{% endif %}
