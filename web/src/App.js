import "./App.css";
import config from "./config.json";
import Editor from "./components/Editor";
import Footer from "./components/Footer";
import Header from "./components/Header";
import MetricsGrid from "./components/MetricsGrid";
import { useCallback, useEffect, useState } from "react";

function App() {
  const [ isLoading, setIsLoading ] = useState(false);
  const [ metrics, setMetrics ] = useState(config.metrics);
  const [ percentiles, setPercentiles ] = useState([]);
  const [ project, setProject ] = useState("p1");
  const [ userStory, setUserStory ] = useState("");

  /*
    Loading project percentiles via api
  */
  const loadPercentiles = useCallback(async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/percentiles`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "project": project }),
      });
      const result = await response.json();
      setPercentiles(result);
    } catch (error) {
        console.log("Error fetching data:", error);
    }
  }, [project]);

  /*
    Metrics evaluation method connected with the api
  */
  const evalUserStory = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/metrics`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ "project": project, "user_story": userStory }),
        });
        const result = await response.json();
        setMetrics(result);
        setIsLoading(false);
    } catch (error) {
        console.log("Error fetching data:", error);
    }
  }, [project, userStory]);

  /*
    Set metrics to default when project domain changed (new percentiles are loaded)
  */
  useEffect(() => {
    loadPercentiles().then(
      () => setMetrics(config.metrics));
  }, [loadPercentiles])

  /*
    Reset metrics function is called when story text changed
  */
  function resetMetrics() {
    setMetrics(config.metrics);
  }

  return (
    <div className="app">
      <Header className="header"/>
      <Editor
        setProject={setProject}
        setUserStory={setUserStory}
        handleSubmit={evalUserStory}
        toggleSubmit={!userStory}
        isLoading={isLoading}
        resetMetrics={resetMetrics}
      />
      <MetricsGrid
        metrics={metrics}
        percentiles={percentiles}
      />
      <Footer/>
    </div>
  );
}

export default App;
