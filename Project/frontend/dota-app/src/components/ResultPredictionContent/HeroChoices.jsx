import HeroChoiceElement from "./HeroChoiceElement.jsx"
import { useState } from "react";

function HeroChoices ({selectedHeroes, setSelectedHeroes, otherHeroes, winProbability}) {
    // const [selectedHeroes, setSelectedHeroes] = useState(Array(5).fill(null));
    const handleHeroSelect = (index, heroName) => {
        if (otherHeroes.includes(heroName)) {
            alert("This hero is already chosen in the other list!");
            return;
        }
        if (selectedHeroes.includes(heroName)) {
            alert('This hero is already chosen!');
            return;
        }

        const newHeroes = [...selectedHeroes];
        newHeroes[index] = heroName;
        setSelectedHeroes(newHeroes);
    };
    return(
        <div className="bg-yellow-800 border-2 border-yellow-950 p-3 rounded-md">
            <p className={`font-semibold text-3xl pb-3 ${(winProbability > 0) && (winProbability >= 0.5 ? "text-green-500" : "text-red-500")}`}
            >{ winProbability < 0 ? "TEAM" : ((winProbability >= 0.5 ? "WiNNER - " : "LOSER - ") + (winProbability*100).toFixed(2) + "%" )}</p>
            <div class="grid grid-cols-5 gap-4">
               {selectedHeroes.map((hero, idx) => (
                    <HeroChoiceElement
                    key={idx}
                    selectedHero={hero}
                    onHeroSelect={(heroName) => handleHeroSelect(idx, heroName)}
                    />
                ))}

{/* 
                <div class="aspect-[16/9] w-full bg-gray-200">
                    <img class="w-full h-full object-cover" />
                </div> */}
            </div>
        </div>
    );
}
export default HeroChoices