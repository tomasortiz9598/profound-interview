import { useEffect, useState } from "react";

type HelloWorld = {
  id: string;
  content: string;
  created_time: string;
  updated_time: string;
};

function App() {
  const [content, setContent] = useState("");
  const [challengeStatus, setChallengeStatus] = useState("");

  useEffect(() => {
    fetch("/hello-world")
      .then((response) => response.json())
      .then((helloWorld: HelloWorld) => setContent(helloWorld.content));
  }, []);

  const startAccountChallenge = () => {
    setChallengeStatus("Starting...");
    fetch("/account-challenge", { method: "POST" })
      .then((response) => response.json())
      .then((body: { status: string }) =>
        setChallengeStatus(`Account challenge ${body.status}`)
      )
      .catch(() => setChallengeStatus("Account challenge failed"));
  };

  return (
    <div>
      <h1>{content}</h1>
      <button type="button" onClick={startAccountChallenge}>
        Run account challenge
      </button>
      {challengeStatus ? <p>{challengeStatus}</p> : null}
    </div>
  );
}

export default App;
