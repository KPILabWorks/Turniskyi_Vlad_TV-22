import { useState, useEffect } from 'react'
import RankHeader from "./RankHeader.jsx"
import HeroChoices from "./HeroChoices.jsx"
import { Rank } from '../../enums/Rank.js';
import { Heroes } from '../../enums/Heroes';
import {Spinner} from "@heroui/spinner";

function ResultPredictionContent (){
    const [rank, setRank] = useState(Rank.ALL);
    const [heroesRadiant, setHeroesRadiant] = useState(Array(5).fill(null));
    const [heroesDire, setHeroesDire] = useState(Array(5).fill(null));
    const [radiantWin, setRadiantWin] = useState(-1);
    const [loading, setLoading] = useState(false);

    const isFull = heroesRadiant.every((h) => h !== null) && heroesDire.every((h) => h !== null) && rank !== Rank.ALL;

    const predict = async () => {
        if (!isFull) {
            alert("Select all heroes and specify the rank");
            return;
        }
        setLoading(true);
        try {
            const response = await fetch("http://localhost:8000/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    radiant: heroesRadiant.map(name => Heroes[name]?.id),
                    dire: heroesDire.map(name => Heroes[name]?.id),
                    rank: rank,
                }),
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }

            const result = await response.json();
            console.log("Prediction result:", result);

            setRadiantWin(result.radiant_win_probability);
            alert(`Radiant win probability: ${(result.radiant_win_probability * 100).toFixed(2)}%`);

        } catch (error) {
            console.error("Prediction failed:", error);
            alert("Failed to get prediction. See console for details.");
        } finally {
            setLoading(false); 
        }
    }


    return (
        <div className="w-full px-6">
            <RankHeader rank={rank} setRank={setRank}/>
            <div className='mb-8 mt-3 border mx-5 border-yellow-950'></div>
            <div class="h-[32rem] flex flex-col justify-between p-4 content-center">
                <HeroChoices selectedHeroes={heroesRadiant} setSelectedHeroes={setHeroesRadiant} otherHeroes={heroesDire} winProbability={radiantWin}/>
                <button
                    className={`px-4 py-2 my-4 w-fit rounded-lg shadow text-white mx-auto 
                        ${isFull ? 'bg-yellow-800 hover:bg-yellow-900 hover:cursor-pointer border-2 border-yellow-950 ' : 'bg-gray-500 cursor-not-allowed'}
                    `}
                    disabled={!isFull || loading}
                    onClick={predict}
                >{loading ? "loading..." : "Predict"}</button>
                <HeroChoices selectedHeroes={heroesDire} setSelectedHeroes={setHeroesDire} otherHeroes={heroesRadiant} winProbability={radiantWin == -1 ? radiantWin : (1 - radiantWin)}/>
            </div>
        </div>
    );
}
export default ResultPredictionContent