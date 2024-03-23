import config from "../config.json";
import { useRef } from "react";
import { useTranslation } from "react-i18next";

// https://medium.com/@adrianhuber17/how-to-dockerize-a-simple-app-using-flask-react-postgresql-and-socket-io-987b1b04faf0

/*
  Editor component to handle story input option and project selection
*/
export default function Editor({ setProject, setUserStory, handleSubmit, toggleSubmit, isLoading, resetMetrics }) {
  const defaultText = "Please type in your user story ...";
  const submitRef = useRef(null);
  const [ t ] = useTranslation('common');

  /*
    Set input user story text
  */
  function handleTyping(event) {
    setUserStory(event.target.value);
    resetMetrics();
  }

  /*
    Set project of the user story
  */
  function handleSelection(event) {
    setProject(event.target.value);
  }

  /*
    Clear default text in user story input field, after user starts typing.
  */
  function toggleInput(event) {
    if (event.target.value === defaultText) {
        event.target.value = ""
        event.target.style.color = 'black'
        submitRef.disabled = false
    } else if (event.target.value === "") {
        event.target.value = defaultText
        event.target.style.color = 'gray'
        submitRef.disabled = true
    }
  }

  return (
    <div className={['editor', isLoading ? 'disabled' : ''].join(' ')}>
      <div className="user_story">
        <div className={isLoading ? 'loader' : ''}></div>
        <textarea
          className="text_area"
          name="text_area"
          defaultValue={defaultText}
          onChange={handleTyping}
          onFocus={toggleInput}
          onBlur={toggleInput}
        />
      </div>
      <div>
        {config.projects.map((project) => (
          <label key={project.key}>
            {t(`projects.${project.key}`)}
            <input
              defaultChecked={project.default === true}
              type="radio"
              id={project.key}
              name="project"
              value={project.key}
              onChange={handleSelection}
            />
          </label>
        ))}
        <button 
          name="submit" 
          ref={submitRef} 
          disabled={toggleSubmit}
          onClick={handleSubmit}
        >
          Submit
        </button>
      </div>
    </div>
  );
}