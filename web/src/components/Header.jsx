import config from "../config.json"

export default function Header() {
    return (
        <div className="header">{ config.name }: { config.desc }</div>
    );
}