import "./Calculator.css";






export default function Calculadora({ expressao, handleButtonClick, clearDisplay, setResultado, calculateResult }) {


    return (
        <div className="calculator-wrapper wrapper-style">

            <div className="calculator-inner-wrapper">
                <div className="calculator-display-container">
                    <input type="text" value={expressao} className="calculator-input" readOnly />
                </div>

                <div className="buttons-container">
                    <div className="buttons-grid">
                        <button onClick={clearDisplay} data-clear >Clear</button>
                        <button onClick={() => handleButtonClick("j")} data-number>j</button>
                        <button onClick={() => handleButtonClick("0")} data-number>0</button>
                        <button onClick={() => handleButtonClick("(")} data-operation>(</button>
                        <button onClick={() => handleButtonClick(")")} data-number>)</button>
                        <button onClick={() => handleButtonClick("1")} data-number>1</button>
                        <button onClick={() => handleButtonClick("2")} data-number>2</button>
                        <button onClick={() => handleButtonClick("3")} data-operation>3</button>
                        <button onClick={() => handleButtonClick("-")} data-number>-</button>
                        <button onClick={() => handleButtonClick("+")} data-number>+</button>
                        <button onClick={() => handleButtonClick("4")} data-number>4</button>
                        <button onClick={() => handleButtonClick("5")} data-operation>5</button>
                        <button onClick={() => handleButtonClick("6")} data-number>6</button>
                        <button onClick={() => handleButtonClick("*")} data-number>*</button>
                        <button onClick={() => handleButtonClick("/")} data-number>÷</button>
                        <button onClick={() => handleButtonClick("7")} data-operation>7</button>
                        <button onClick={() => handleButtonClick("8")} data-number>8</button>
                        <button onClick={() => handleButtonClick("9")} data-number>9</button>
                        <button onClick={calculateResult} data-equals class="span-two">=</button>
                    </div>
                </div>
            </div>

        </div>
    )
}