 import React from "react";
 import { Link } from "react-router-dom";

const Header = () => {
    return(
<nav className="w-full flex justify-between items-center text-lg py-4 bg-[#f8f8f6] px-6">
    <div className="flex items-center space-x-4">
        {/* <div className="cursor-pointer hover:text-gray-700 font-bold w-auto text-center" style={{ fontFamily: 'Lobster', fontSize: '1.5rem', letterSpacing: '0.1rem' }}>Auto</div> */}
        <div className="cursor-pointer flex justify-center items-center">
            <Link to="/">
                <img src="/logo.webp" 
                alt="logo"
                className="w-16 h-auto "
                />
            </Link>
        </div>
        <div className="cursor-pointer hover:text-gray-700 font-mono font-bold w-auto text-center" style={{ fontFamily: 'Lobster', fontSize: '1.5rem', letterSpacing: '0.1rem' }}>Thumb</div>
    </div>

    <div className="flex space-x-6  text-base font-medium" style={{paddingRight: '15rem'}}>
        <Link to="/" className="hover:text-gray-700 cursor-pointer" style={{paddingRight: '4rem'}}>Home</Link>
        <Link to="/setting" className="hover:text-gray-700 cursor-pointer" style={{paddingRight: '4rem'}}>Setting</Link>
        <Link to="/operation" className="hover:text-gray-700 cursor-pointer" style={{paddingRight: '4rem'}}>Operation</Link>
    
        <Link to="/analysis" className="hover:text-gray-700 cursor-pointer" style={{paddingRight: '4rem'}}>Analysis</Link>
    </div>
</nav>
    )
}

export default Header