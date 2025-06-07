import { useState, useEffect } from 'react'
import RankHeader from "./RankHeader.jsx"
import HeroTable from "./HeroTable.jsx"
import { Rank } from '../../enums/Rank.js';
import { GameMode } from '../../enums/GameMode.js';


function MetaContent (){
const [rank, setRank] = useState(Rank.ALL);
const [gamemode, setGamemode] = useState(GameMode.ALL_PICK);
const [heroes, setHeroes] = useState([]);

    useEffect(() => {
        const fetchMeta = async () => {
            try {
            console.log(`http://127.0.0.1:8000/meta?gm=${gamemode}&rank=${rank}`);
            const response = await fetch(`http://127.0.0.1:8000/meta?gm=${gamemode}&rank=${rank}`);
            const data = await response.json();
            setHeroes(data);
            } catch (error) {
            console.error("Error loading meta data:", error);
            }
        };

        fetchMeta();
    }, [rank, gamemode]);

    return (
        <div className="w-full">
            <RankHeader rank={rank} setRank={setRank} gamemode={gamemode} setGamemode={setGamemode} />
            <div className='mb-10 mt-3 border mx-5 border-yellow-950'></div>
            <HeroTable heroes={heroes}/>
        </div>
    );
}

export default MetaContent;