import "./App.css";
import Header from "./components/Header.jsx";
import Predictor from "./components/Predictor.jsx";
import Stats from "./components/Stats.jsx";
import Footer from "./components/Footer.jsx";

function App() {
  return (
    <div className="app-shell">
      <Header />
      <main>
        <Predictor />
        <Stats />
      </main>
      <Footer />
    </div>
  );
}

export default App;
