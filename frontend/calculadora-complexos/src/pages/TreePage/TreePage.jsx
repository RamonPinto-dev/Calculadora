import "./TreePage.css";
import { useNavigate } from "react-router-dom";

export default function TreePage() {
    const navigate = useNavigate();

    return (
        <div className="tree-page-container">
            <h2>Árvore de Análise</h2>
            <p>Em construção...</p>
            <button className="back-btn" onClick={() => navigate('/')}>Voltar</button>
        </div>
    )
}