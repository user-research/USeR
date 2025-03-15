from config.config_parser import config, load_config
import click
from flask.cli import FlaskGroup
from importer.p1_importer import P1Importer
from metrics.metrics import Metrics
import os
import pandas as pd
from stats.global_stats import GlobalStats
from stats.project_stats import ProjectStats

# https://github.com/shap/shap/issues/2909
# https://github.com/lmcinnes/umap/issues/1004
# TODO remove filter when code fix is applied to decorator
import warnings
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")

# https://stackoverflow.com/questions/25351968/how-to-display-full-non-truncated-dataframe-information-in-html-when-convertin
pd.set_option('display.max_colwidth', None)

cli = FlaskGroup()

@cli.command('train')
def train():
    """
    Train the model
    """
    projects = config['app']['projects'].split(r',')
    for project in projects:
        Metrics(project=project)

@cli.command('import')
@click.option("--env", is_flag=False)
def import_backlog(env:str):
    """
    Import the backlog
    """
    if env == 'TEST':
        os.environ['ENV'] = 'TEST'
        load_config()

    projects = config['app']['projects'].split(r',')
    for project in projects:
        if project.capitalize() + 'Importer' in globals():
            importer = globals()[project.capitalize() + 'Importer']()
            importer.import_backlog()

@cli.command('generate_predictions')
def generate_predictions():
    """
    Generate predictions
    """
    projects = config['app']['projects'].split(r',')
    for project in projects:
        pm = ProjectStats(project)
        pm.generate_predictions()

    gm = GlobalStats()
    gm.generate_predictions()

@cli.command('generate_percentiles')
def generate_percentiles():
    """
    Generate percentiles
    """
    projects = config['app']['projects'].split(r',')
    for project in projects:
        pm = ProjectStats(project)
        pm.generate_percentiles()

    gm = GlobalStats()
    gm.generate_percentiles()

if __name__ == "__main__":
    cli()
