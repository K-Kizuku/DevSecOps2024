import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [vector, setVector] = useState<string>("");
  const [message, setMessage] = useState("");
  const [completeMessages, setCompleteMessages] = useState<string[]>([]);

  useEffect(() => {
    const eventSource = new EventSource(
      "http://localhost:8000/api/v1/chats/streaming"
    );

    eventSource.onmessage = (event) => {
      setVector(event.data);
      console.log(event.data);
      const char = event.data;
      // メッセージの終わりを示す特定の文字（例えば改行文字 '\n'）を検出
      if (char === "\n") {
        // 完全なメッセージとして配列に追加
        setCompleteMessages((prev) => [...prev, message]);
        // 次のメッセージのためにメッセージ状態をリセット
        setMessage("");
        console.log(char);
      } else {
        // メッセージに文字を追加
        setMessage((prev) => prev + char);
        console.log(char);
      }
    };

    return () => {
      eventSource.close();
    };
  }, [message]);

  return (
    <>
      <h1>AI Chat Bot</h1>
      <div>
        <h2>入力欄</h2>
        <input placeholder="ここに入力してください" />
        <button>送信</button>
      </div>
      <div>
        <h2>出力欄</h2>
        <p>ベクトル検索の結果</p>
        <div>{vector}</div>
        <p>LLMの回答</p>
        <ul>
          {completeMessages.map((msg, index) => (
            <li key={index}>{msg}</li>
          ))}
          {message}
        </ul>
      </div>
    </>
  );
}

export default App;
