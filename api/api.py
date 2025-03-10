from config.config_parser import config
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from metrics.metrics import Metrics
import os
from stats.project_stats import ProjectStats

api = Flask(__name__)
CORS(api, origins=[os.getenv('REACT_APP_FRONTEND_URL')])

@api.route('/metrics', methods=['POST'])
def metrics():
    """
    Provides access to the metric calculation
    """
    metrics_list = []

    project = request.json['project']
    user_story = request.json['user_story']

    m = Metrics(project=project, user_story=user_story)

    # Calculate the format complete metric
    format_complete = m.get_metric('format_complete').run()
    metrics_list.append(
        {'key':'format_complete', 'value':format_complete}
    )

    # Calculate the flesch readability score
    readable = m.get_metric('readable').run()
    metrics_list.append(
        {'key':'readable', 'value':readable}
    )

    # Calculate customer_speak quality index
    customer_speak = m.get_metric('customer_speak').run()
    metrics_list.append(
        {'key':'customer_speak', 'value':customer_speak}
    )

    # Calculate the small quality index
    small = m.get_metric('small').run()
    metrics_list.append(
        {'key':'small', 'value':small}
    )

    # Calculate independent quality index
    independent = m.get_metric('independent').run()
    metrics_list.append(
        {'key':'independent', 'value':independent}
    )

    # Calculate the word ratio quality index
    word_sparse = m.get_metric('word_sparse').run()
    metrics_list.append(
        {'key':'word_sparse', 'value':word_sparse}
    )

    # Calculate the sentence ratio quality index
    sentence_sparse = m.get_metric('sentence_sparse').run()
    metrics_list.append(
        {'key':'sentence_sparse', 'value':sentence_sparse}
    )
    # Calculate the degree of easy words used
    easy_language = m.get_metric('easy_language').run()
    metrics_list.append(
        {'key':'easy_language', 'value':easy_language}
    )

    # JSONify response
    response = make_response(jsonify(metrics_list))

    return response

@api.route('/percentiles', methods=['POST'])
def percentiles():
    """
    Provide the user infos to each indicator based on the stats percentile calculation
    """
    project = request.json['project']
    ps = ProjectStats(project=project)

    app_metrics = config['app']['metrics'].split(r',')
    pts = {}

    for metric in app_metrics:
        pts[metric] = {
            '_33':ps.get_percentiles(name=metric)['_33'],
            '_66':ps.get_percentiles(name=metric)['_66']
        }

    # JSONify response
    response = make_response(jsonify(pts))

    return response
