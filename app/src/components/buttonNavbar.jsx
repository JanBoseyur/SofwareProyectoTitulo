
import "../styles/button.css";

function Button({ children, onClick, className = "", type = "button", icon: Icon}) {
    return (
    
        <button
            type = {type}
            className = {`button ${className}`}
            onClick = {onClick}
        >
            {Icon && <Icon className = "buttonIcon" />}
            {children}
        </button>

    );
}

export default Button;