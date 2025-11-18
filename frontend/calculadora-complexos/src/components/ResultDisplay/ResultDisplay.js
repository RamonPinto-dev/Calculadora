import "./ResultDisplay.css";
import { useNavigate } from "react-router-dom";





export default function ResultDisplay({ resultado }) {
    const navigate = useNavigate();

    return (
        <div className="result-container">
            <span>Notação LISP:</span>

            <div className="notation-lisp" role="region" aria-label="Notação LISP" tabIndex="0">
                <h3>{resultado}</h3>
            </div>

            <div className="buttons-result-container">
                <button type="button" onClick={() => { }}>Limpar</button>
                <button type="button" onClick={() => navigate('/tree')}>Gerar Árvore</button>
            </div>
        </div>
    );
}
