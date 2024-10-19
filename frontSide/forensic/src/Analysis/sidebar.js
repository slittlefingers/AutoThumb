import React from "react";



// Title component
const Title = ({ children }) => (
    <h3 className='pb-3 px-4 font-medium text-gray-800 md:px-8'>
        {children}
    </h3>
);

// Sections List
const SectionsList = ({ items, onOperationClick }) => (
    <div className='text-gray-600 px-4 md:px-8 '>
        <ul>
            {items?.map((item, idx) => (
                <li key={idx}>
                    <div
                        onClick={() => onOperationClick(item.operation_id)}
                        title={item.operation_description}
                        active='text-gray-900 border-indigo-600'
                        className='block w-full py-2 px-4 border-l hover:border-gray-500 hover:text-gray-900 duration-150'>
                        Operation_{item.operation_id}
                    </div>
                </li>
            ))}
        </ul>
    </div>
);


const Thumbcomp = ({ openModal, getkeywordmatch }) => {
    const handleClick = () => {
        openModal();  // 先调用第一个函数
        getkeywordmatch();  // 然后调用第二个函数
    };

    return (
        <div className="flex items-center justify-center relative w-full bg-[#f8f8f6]">
            <button
                onClick={handleClick}
                className="flex items-center justify-center px-10 py-2 text-sm text-white duration-100 bg-gray-500 rounded-lg shadow-md focus:shadow-none ring-offset-2 ring-indigo-600 focus:ring-2"
            >
                Thumbcomp
            </button>
        </div>
    );
};



const Sidebar = ({ Operation, onOperationClick, openModal, getkeywordmatch,get_all_experiment }) => {
    return (
        <>
            <nav
                className="fixed z-40 top-0 left-0 w-full h-full border-r bg-[#f8f8f6] space-y-8 overflow-auto sm:w-80">
                <div className="sticky top-0 space-y-8 bg-[#f8f8f6]">
                    <div className='h-20 flex items-center justify-center px-4 border-b bg-[#f8f8f6]'>
                        <a href='/' className='flex items-center justify-center'>
                            <img src="/logo.webp" width={140} className="w-1/4 max-w-[300px]" />
                        </a>
                    </div>
                    <div className='px-4 md:px-8'>
                        <Thumbcomp openModal={openModal} getkeywordmatch={getkeywordmatch} />
                    </div>
                </div>
                <div className='text-[0.9rem] space-y-6'>
                    {Object.keys(Operation).map((key) => (
                        <div key={key}>
                            <Title>{key.replace(/([A-Z])/g, ' $1').trim()}</Title>
                            <SectionsList items={Operation[key]} onOperationClick={onOperationClick} />
                        </div>
                    ))}
                </div>

                <div className="flex justify-center item-center p-4 fixed bottom-1 pl-20">
                    <button
                        onClick={get_all_experiment}
                        className="flex item-center justify-center bg-gray-500 text-white py-2 px-4 text-sm rounded-lg shadow hover:bg-blue-600 transition duration-150"
                    >
                        Get All Experiment
                    </button>
                </div>
            </nav>
        </>
    );
};

export default Sidebar;