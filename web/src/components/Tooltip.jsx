import { useTranslation } from "react-i18next";

/*
  Tooltip component showing the percentiles of the project metrics
  to provide information to the user to give orientation during the interpretation
  of the current metric values
*/
export default function Tooltip({ metric, metricPercentiles }) {
    const [ t ] = useTranslation('common');

    return metricPercentiles ? (
        <span className="tooltip">
            <div className="desc hypenate">
                {t(`metrics.${metric.key}.desc`)}
            </div>
            <ul className="percentiles">
                <li>&ge;{ metricPercentiles._66.toFixed(2) } green</li>
                <li>&gt;{ metricPercentiles._33.toFixed(2) } yellow</li>
                <li>&le;{ metricPercentiles._33.toFixed(2) } red</li>
            </ul>
        </span>
        ) : (<></>);
}