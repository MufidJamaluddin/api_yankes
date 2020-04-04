from flask import Flask, render_template, request, jsonify, redirect, make_response
import click
from flask import Flask
from yankes_api import app, AppDatabase
from yankes_api.domain.faskes import JenisFaskes, Province, RumahSakit, Jenis_Ruang, Kelas_Ruang, Occupations


@click.command()
def db_migrate():
    """
    Create table
    """
    db = AppDatabase.create(app.config)
    db.create_tables([JenisFaskes, Province, RumahSakit, Jenis_Ruang, Kelas_Ruang, Occupations], safe=True)