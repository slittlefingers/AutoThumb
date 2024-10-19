


const Checker = ({adbConnection,
    rootAuthority,
    adbErrorMessage,
    rootErrorMessage}) => {
    

    return (
        <div className="space-y-8 text-gray-600">
            <div className="flex items-center space-x-4">
                <div className="text-lg font-medium">Adb Connection</div>
                {adbConnection !== null ? (
                    <span className={adbConnection ? "text-green-500" : "text-red-500"}>
                        {adbConnection ? "✔" : "✘"}
                    </span>
                ) : (
                    <span>Loading...</span>
                )}
            </div>
            {!adbConnection && (
                <p className="text-sm text-red-500">
                    {adbErrorMessage}
                </p>
            )}
            <div className="flex items-center space-x-4">
                <div className="text-lg font-medium">Root Authority</div>
                {rootAuthority !== null ? (
                    <span className={rootAuthority ? "text-green-500" : "text-red-500"}>
                        {rootAuthority ? "✔" : "✘"}
                    </span>
                ) : (
                    <span>Loading...</span>
                )}
            </div>
            {!rootAuthority && (
                <p className="text-sm text-red-500">
                    {rootErrorMessage}
                </p>
            )}
        </div>
    );
}

export default Checker;
