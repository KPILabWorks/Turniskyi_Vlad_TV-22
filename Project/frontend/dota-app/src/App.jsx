import { useState } from 'react'
import Header from './components/Header';
import MainContent from './components/MainContent';
import './App.css'
import { ContentType } from './enums/ContentType.js';

function App() {
  const [type, setType] = useState(ContentType.META);

  return (
    <div className="min-h-screen p-8 flex flex-col w-screen">
      <Header type={type} setType={setType} />
      <MainContent type={type} />
    </div>
  )
}

export default App
