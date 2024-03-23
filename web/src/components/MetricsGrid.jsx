import Metric from "./Metric";

/*
  Metrics grid component to show the result of all metrics
*/
export default function MetricsGrid({ metrics, percentiles }) {
    /*
        Evaluation metric postion in grid layout. Mark each element whether 
        it's in three column grid layout on first, middle, or last postion
    */
    function evalGridPosition(index) {
        const width = 3;
        var row = Math.floor(index / width);
        var maxRows = Math.floor(metrics.length / width);
        var col = index % width;
        var gridPos = {
            colPos: "",
            rowPos: ""
        };
        
        if (col === 0) {
            gridPos.colPos = "col_first";
        } else if (col === 1) {
            gridPos.colPos = "col_middle";
        } else if (col === 2) {
            gridPos.colPos = "col_last";
        }

        if (row === 0) {
            gridPos.rowPos = "row_first"
        } else if (row === maxRows) {
            gridPos.rowPos = "row_last";
        } else {
            gridPos.rowPos = "row_middle";
        }

        return gridPos;
    }

    return (
        <div className="metrics_grid">
            {metrics.map((metric, index) => (
                <Metric 
                    key={metric.key}
                    position={evalGridPosition(index)}
                    metric={metric}
                    metricPercentiles={percentiles[metric.key]}
                />
            ))}
        </div>
    );
  }