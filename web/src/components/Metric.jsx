import { useTranslation } from "react-i18next";
import Tooltip from "./Tooltip";

/*
  Metric component to show the result of a specific metric
*/
export default function Metric({metric, position, metricPercentiles}) {
    var classStr = ['metric', position.colPos, position.rowPos, getBgColor()].join(' ');
    const [ t ] = useTranslation('common');
    
    /*
        Helper to retrieve the bg color based on the percentiles
    */
    function getBgColor() {
        if (metric.value === -1) {
            return 'gray'
        }
        if (metric.value >= metricPercentiles['_66']) {
            return 'green';
        }
        if (metric.value > metricPercentiles['_33']) {
            return 'yellow';
        }   
        if (metric.value <= metricPercentiles['_33']) {
            return 'red';
        }
        return ''
    }

    return (
        <div className={classStr}>
            <div className="name">
                {t(`metrics.${metric.key}.name`)}
            </div>
            <div className="info">
                &#9432;
            </div>
            <div className="value">
                {(metric.value !== -1) ? metric.value.toFixed(2) : ''}
            </div>
            <Tooltip metric={metric} metricPercentiles={metricPercentiles}/>
        </div>
    );
}