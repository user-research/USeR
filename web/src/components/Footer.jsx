import config from "../config.json";

export default function Footer() {
    return (
        <div className="footer">{ config.name } { config.version } - { config.contact }</div>
    );
}