import { useEffect, useState } from "react";

type HelloWorld = {
  id: string;
  content: string;
  created_time: string;
  updated_time: string;
};

function App() {
  const [content, setContent] = useState("");

  useEffect(() => {
    fetch("/hello-world")
      .then((response) => response.json())
      .then((helloWorld: HelloWorld) => setContent(helloWorld.content));
  }, []);

  return <h1>{content}</h1>;
}

export default App;
