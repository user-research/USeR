from config.user.UserConfigParser import config
import click
from flask.cli import FlaskGroup
from importer.P1Importer import P1Importer
from itertools import islice
from metrics.Metrics import Metrics
from stats.ProjectStats import ProjectStats
from stats.GlobalStats import GlobalStats
import pandas as pd

# https://github.com/shap/shap/issues/2909
# https://github.com/lmcinnes/umap/issues/1004
# TODO remove filter when code fix is applied to decorator
import warnings
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")

# https://stackoverflow.com/questions/25351968/how-to-display-full-non-truncated-dataframe-information-in-html-when-convertin
pd.set_option('display.max_colwidth', None)

"""
import debugpy
debugpy.listen(("0.0.0.0", 5678))
print("Waiting for client to attach...")
debugpy.wait_for_client()
"""

# Default config values
project = config['app']['default_project']

cli = FlaskGroup()

@cli.command('train')
@click.argument('project')
def train(project):
    Metrics(project=project)

@cli.command('stop_words')
def stop_words():
    m = Metrics()
    cs = m.get_metric('customer_speak')
    stop_words = cs.stop_words
    print(stop_words)

@cli.command('list_modules')
def list_modules():
    help("sklearn")

@cli.command('import')
@click.argument('project')
def import_backlog(project):
    if project == 'p1':
        importer = P1Importer()
    importer.import_backlog()

@cli.command('generate_predictions')
def generate_predictions():
    projects = config['app']['projects'].split(r',')
    for project in projects:
        pm = ProjectStats(project)
        pm.generate_predictions()

    gm = GlobalStats()
    gm.generate_predictions()

@cli.command('generate_percentiles')
def generate_percentiles():
    projects = config['app']['projects'].split(r',')
    for project in projects:
        pm = ProjectStats(project)
        pm.generate_percentiles()

    gm = GlobalStats()
    gm.generate_percentiles()

def batched(iterable, chunk_size):
    iterator = iter(iterable)
    while chunk := tuple(islice(iterator, chunk_size)):
        yield chunk

@cli.command('predict_small')
def predict_small():

    projects = config['app']['projects'].split(r',')
    #projects = ['p1']
    for project in projects:
        # Add user story ids where we want to predict the quality
        usids = pd.read_csv(config['project']['usids_file'].format(project=project), encoding='utf-8')

        # Add the full backlog to query user stories
        backlog = pd.read_csv(config['project']['backlog_file'].format(project=project), encoding='utf-8')

        for _,usid in enumerate(usids['usid']):
            user_story = backlog.loc[backlog['usid'] == usid]
            if user_story.empty:
                continue

            user_story = user_story['text'].to_string(index = False)
            m = Metrics(project=project, user_story=user_story, usid=usid)
            s = m.get_metric('small')
            s.run()

@cli.command('debug')
def debug():
    # For cli debugging
    m = Metrics()
    cs = m.get_metric('customer_speak')

if __name__ == "__main__":
    cli()
