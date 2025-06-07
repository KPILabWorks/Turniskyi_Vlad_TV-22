import { useState, useRef, useEffect } from 'react';
import { Heroes } from '../../enums/Heroes';

function HeroChoiceElement ({ selectedHero, onHeroSelect }) {
    const [isOpen, setIsOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [position, setPosition] = useState('bottom'); // 'bottom' или 'top'
    // const [hero, setHero] = useState('');
    const triggerRef = useRef(null);
    const dropdownRef = useRef(null);


    const handleClickOutside = (event) => {
    if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target)
    ) {
        setIsOpen(false);
    }
    };

    const openDropdown = () => {
        if (triggerRef.current) {
            const rect = triggerRef.current.getBoundingClientRect();
            const spaceBelow = window.innerHeight - rect.bottom;
            const spaceAbove = rect.top;

            console.log('spaceBelow:', spaceBelow, 'spaceAbove:', spaceAbove);

            if (spaceBelow < 200 && spaceAbove > spaceBelow) {
            setPosition('top');
            } else {
            setPosition('bottom');
            }
        }
        setIsOpen(!isOpen);
    };

    useEffect(() => {
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const items = Object.keys(Heroes);
    const filteredItems = items.filter((item) => item.toLowerCase().includes(searchTerm.toLowerCase()));

    // const handleChange = (e) => {
    //     setHero(e.target.value);
    //     console.log('Selected hero:', e.target.value);
    // };

    return(
      <div className="relative" ref={dropdownRef}>
        <div class="aspect-[16/9] w-full bg-gray-200 rounded-md">
            <img 
                src={Heroes[selectedHero]?.image ? ("/src/assets/heroes/" + Heroes[selectedHero]?.image) : ""}
                class="w-full h-full object-cover rounded-md"
                //onClick={toggleDropdown} 
                 onClick={openDropdown}
                ref={triggerRef}
            />
            </div>
                {/* Дропдаун-меню */}
                {isOpen && (
                <div
                className={`absolute ${
                position === 'top' ? 'bottom-full mb-2' : 'top-full mt-2'
                } right-0 w-56 max-h-64 overflow-y-auto rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 p-1 space-y-1 z-10`}
            >
                {/* Поисковое поле */}
                <input
                type="text"
                placeholder="Search items"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="block w-full px-4 py-2 text-gray-800 border rounded-md border-gray-300 focus:outline-none"
                />

                {/* Список пунктов */}
                {filteredItems.map((item) => (
                <a
                    key={item}
                    href="#"
                    className="block px-4 py-2 text-gray-700 hover:bg-gray-100 active:bg-blue-100 cursor-pointer rounded-md"
                    // onClick={() => setHero(item)} 
                    onClick={() => {
                        onHeroSelect(item); 
                        setIsOpen(false); 
                    }}
                >
                    {item}
                </a>
                ))}
                {/* <select
                    value={hero}
                    onChange={handleChange}
                    className="block w-full px-4 py-2 text-gray-700 border rounded-md"
                >
                    <option value="">Выберите героя</option>
                    {filteredItems.map((item) => (
                    <option key={item} value={item}>
                        {item}
                    </option>
                    ))}
                </select> */}

                {filteredItems.length === 0 && (
                <div className="px-4 py-2 text-gray-500 text-sm">No results</div>
                )}
            </div>
            )}
        </div>
    );
}

export default HeroChoiceElement