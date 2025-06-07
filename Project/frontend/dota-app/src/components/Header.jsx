import { ContentType } from '../enums/ContentType.js';
function Header ({ type, setType }) {
    const classSelectedAnchor = " border-neutral-100 border-b text-neutral-200 hover:cursor-text ";
    const classUnselectedAnchor = " text-neutral-400 hover:text-neutral-200 hover:cursor-pointer ";

    return(
        <header className='w-[50%] mx-auto '>
            <nav className=" border-neutral-200 px-4 lg:px-6 py-2.5 border-b-2 pb-4">
                <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl ">
                    <ul className="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-8 lg:mt-0 mx-auto">
                        <li>
                            <a 
                                className={"text-3xl  mx-4" 
                                    + (type === ContentType.META ? classSelectedAnchor : classUnselectedAnchor)}
                                onClick={() => setType(ContentType.META)}
                                >
                                    Meta report
                            </a>
                        </li>
                        <li>
                            <a 
                                className={"text-3xl  mx-4" 
                                    + (type === ContentType.RESULT ? classSelectedAnchor : classUnselectedAnchor)}
                                onClick={() => setType(ContentType.RESULT)}
                                >Predict result
                            </a>
                        </li>
                        <li>
                            <a 
                                className={"text-3xl  mx-4" 
                                    + (type === ContentType.HERO ? classSelectedAnchor : classUnselectedAnchor)}
                                onClick={() => setType(ContentType.HERO)}
                                >Predict hero
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
        </header>
    );
}

export default Header